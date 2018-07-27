from _Shared import db
from History import History

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(12), unique=True, nullable=False)
    link = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), unique=True, nullable=False)
    history = db.relationship("History")

    def __repr__(self):
        return '<product %r>' % self.product_id

    def get_current_price(self):
        history = History.query.filter(History.type.has(type="price")).filter_by(product_id=self.id).order_by(History.add_date).first()
        if history is not None:
            return history.value
        else:
            return None

    def get_current_number_of_reviews(self):
        history = History.query.filter(History.type.has(type="num_reviews")).filter_by(product_id=self.id).order_by(History.add_date).first()
        if history is not None:
            return int(history.value)
        else:
            return None

    def get_current_review_ratio(self):
        history = History.query.filter(History.type.has(type="review_ratio")).filter_by(product_id=self.id).order_by(History.add_date).first()
        if history is not None:
            return history.value
        else:
            return None


    def __str__(self):
        return "Item: {}\nLink: {}\nID: {}".format(self.name, self.link, self.product_id)