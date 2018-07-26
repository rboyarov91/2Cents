#!flask/bin/python
from flask import Flask, jsonify, abort, make_response
from db.src.models._Shared import db
from db.src.models.Product import Product
from db.src.models.History import History
from db.src.models.HistoryTypes import HistoryTypes
import db.src.init_db as init_db

def configure_app():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app = Flask(__name__)
configure_app()
db.init_app(app)
db.app = app



tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

if __name__ == '__main__':
    #app.run(debug=True)
    # Reset DB

    #print HistoryTypes.query.all()
    #print HistoryTypes.query.filter_by(type='price').all()
    init_db.create_tables()
    init_db.initialize_tables()
    print HistoryTypes.query.all()
    # db.create_all()
    #
    # product = Product(id="001", link="Link001", name="Name001")
    # price_hist = HistoryTypes(id="001", type="price")
    # history = History(value=123)
    # history.type = price_hist
    # product.history.append(history)
    #
    #
    # db.session.add(product)
    # db.session.commit()
    #print HistoryTypes.query.all()
    #db.session.commit()
    #product = Product(id="12BB23", link="http://amazon.com", name="Test Product")
    #db.session.add(product)
    #db.session.commit()
    #print Product.query.all()
