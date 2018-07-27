from db.src.models._Shared import db
from db.src.models.HistoryTypes import HistoryTypes
import api.src.AmazonSearchUtils as AmazonSearchUtils
from db.src.models.Product import Product
from db.src.models.History import History

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

def initialize_database(drop_first=False):
    if drop_first:
        db.drop_all()
    create_tables()
    initialize_tables()

def populate_test_data():
    phrase = "timex watch men"
    for p in AmazonSearchUtils.get_search_page_results(phrase, use_cached=True):
        try:
            product = Product(product_id=p.id, name=p.name, link=p.link)
            # Add price history
            history = History(value=p.price)
            history.type = HistoryTypes.query.filter_by(type="price").first()
            product.history.append(history)
            # Add review number history
            history = History(value=p.current_num_reviews)
            history.type = HistoryTypes.query.filter_by(type="num_reviews").first()
            product.history.append(history)
            # Add review ratio history
            history = History(value=p.current_review_ratio)
            history.type = HistoryTypes.query.filter_by(type="review_ratio").first()
            product.history.append(history)
            db.session.add(product)
            db.session.commit()
        except Exception as e:
            # print "Broke on this product"
            # print e
            # print p
            db.session.rollback()

