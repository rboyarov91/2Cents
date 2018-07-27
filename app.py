#!flask/bin/python
from flask import Flask, jsonify, abort, make_response
from db.src.models._Shared import db
import db.src.init_db as init_db
from db.src.models.Product import Product
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
import api.src.routes.Product as product_api




# tasks = [
#     {
#         'id': 1,
#         'title': u'Buy groceries',
#         'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
#         'done': False
#     },
#     {
#         'id': 2,
#         'title': u'Learn Python',
#         'description': u'Need to find a good Python tutorial on the web',
#         'done': False
#     }
# ]
#
# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not found'}), 404)
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
    #app.run()
