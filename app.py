#!flask/bin/python
from flask import Flask, jsonify, abort, make_response
from db.src.models._Shared import db
import db.src.init_db as init_db
from db.src.models.Product import Product
import os
from db.src.models.HistoryTypes import HistoryTypes
from db.src.models.History import History
import api.src.AmazonSearchUtils as AmazonSearchUtils

def configure_app():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



app = Flask(__name__)
configure_app()
db.init_app(app)
db.app = app
#app.before_first_request(init_db.initialize_database)
init_db.initialize_database()
import api.src.routes.product as product_api

def get_route_files():
    routes_dir = "api/src/routes/"
    routes_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), routes_dir)
    return [p.split(".")[0] for p in os.listdir(routes_path) if p.split(".")[-1] == "py" and p[0] != "_"]


def import_from(module, name):
    module = __import__(module, fromlist=[name])
    return getattr(module, name)

blueprints = [import_from("api.src.routes.{}".format(route), "{}_bp".format(route)) for route in get_route_files()]

for bp in blueprints:
    app.register_blueprint(bp, url_prefix='/api')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
#
# @app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
# def get_task(task_id):
#     task = [task for task in tasks if task['id'] == task_id]
#     if len(task) == 0:
#         abort(404)
#     return jsonify({'task': task[0]})

if __name__ == '__main__':
    #app.run()
    init_db.initialize_database(drop_first=True)
    init_db.populate_test_data()
    print Product.query.all()
    #print HistoryTypes.query.all()

    app.run()
