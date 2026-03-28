from flask import Blueprint, jsonify
import psycopg2.extras
from db import get_connection

product_bp = Blueprint('product_bp', __name__)

# GET /api/products/store/<store_id>
@product_bp.route('/store/<int:store_id>', methods=['GET'])
def get_products_by_store(store_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT * FROM Product WHERE store_id = %s", (store_id,))
        products = cursor.fetchall()
        return jsonify({"success": True, "data": [dict(p) for p in products]})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# GET /api/products/<product_id>
@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT * FROM Product WHERE id = %s", (product_id,))
        product = cursor.fetchone()
        if product:
            return jsonify({"success": True, "data": dict(product)})
        return jsonify({"success": False, "message": "Product not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()