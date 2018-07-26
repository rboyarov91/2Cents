from app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<ID %r>' % self.id

