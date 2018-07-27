from flask import Blueprint, jsonify
from db.src.models.Product import Product

product_bp = Blueprint("product", __name__)

@product_bp.route('tasks/<product_id>', methods=['GET'])
def get_product_info(product_id):
    products = Product.query.filter_by(product_id=product_id).first()
    if products is None:
        return jsonify


get_product_info("123AB")

