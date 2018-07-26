from _Shared import db
from History import History

class Product(db.Model):
    id = db.Column(db.String(12), primary_key=True)
    link = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), unique=True, nullable=False)
    history = db.relationship("History")

    def __repr__(self):
        return '<product %r>' % self.id