from db.src.models._Shared import db
from db.src.models.HistoryTypes import HistoryTypes

def create_tables():
    db.create_all()

def initialize_tables():
    # Populate the history types for price, num_reviews and review_ratio
    history_types = ["price", "num_reviews", "review_ratio"]
    for type in history_types:
        if len(HistoryTypes.query.filter_by(type=type).all()) ==0:
            price_hist = HistoryTypes(type=type)
            db.session.add(price_hist)
    db.session.commit()