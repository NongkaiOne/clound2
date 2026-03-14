from flask import Blueprint, request, jsonify
from db import connect_db
from middleware_auth import require_role

product_bp = Blueprint("product", __name__)

@product_bp.route("/products", methods=["GET"])
def get_products():

    db = connect_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM products")

    return jsonify(cursor.fetchall())


@product_bp.route("/products", methods=["POST"])
@require_role("StoreOwner")
def add_product():

    data = request.json

    db = connect_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO products(name,price,store_id) VALUES(%s,%s,%s)",
        (data["name"], data["price"], data["store_id"])
    )

    db.commit()

    return jsonify({"message": "product added"})


@product_bp.route("/products/<int:id>", methods=["DELETE"])
@require_role("StoreOwner")
def delete_product(id):

    db = connect_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM products WHERE id=%s", (id,))
    db.commit()

    return jsonify({"message": "product deleted"})