from _Shared import db
from datetime import datetime
from HistoryTypes import HistoryTypes


class History(db.Model):
    __tablename__ = "history"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    add_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    type = db.relationship('HistoryTypes', uselist=False, back_populates="history")

    def __repr__(self):
        return '<History %r>' % self.id