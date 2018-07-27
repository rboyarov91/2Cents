from flask import Blueprint, jsonify
from db.src.models.Product import Product

product_bp = Blueprint("product", __name__)

@product_bp.route('product/<product_id>', methods=['GET'])
def get_product_info(product_id):
    product = Product.query.filter_by(product_id=product_id).first()
    if product is None:
        return jsonify(
            {
              "Found": "None"
            }
        )
    else:
        return jsonify({
            "name": product.name,
            "url": product.link,
            "price": product.get_current_price(),
            "num_reviews": product.get_current_number_of_reviews(),
            "review_ratio": product.get_current_review_ratio()

        })

