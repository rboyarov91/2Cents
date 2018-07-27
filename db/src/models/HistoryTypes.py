from _Shared import db

class HistoryTypes(db.Model):
    __tablename__ = "history_types"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    history = db.relationship("History", back_populates="type")

    def __repr__(self):
        return '<history_types %r>' % self.type