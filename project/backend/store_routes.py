from flask import Blueprint, request, jsonify
import psycopg2.extras
from db import get_connection

store_bp = Blueprint('store_bp', __name__)

# GET /api/stores/mall/<mall_id>
@store_bp.route('/mall/<int:mall_id>', methods=['GET'])
def get_stores_by_mall(mall_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        sql = """
            SELECT s.*, c.name as category_name, c.icon as category_icon, f.floor_code, f.name as floor_name
            FROM Store s
            JOIN StoreCategory c ON s.category_id = c.id
            JOIN Floor f ON s.floor_id = f.id
            WHERE s.mall_id = %s
        """
        cursor.execute(sql, (mall_id,))
        stores = cursor.fetchall()
        return jsonify({"success": True, "data": [dict(s) for s in stores]})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# GET /api/stores/search?mall_id=&q=
@store_bp.route('/search', methods=['GET'])
def search_stores():
    mall_id = request.args.get('mall_id')
    query = request.args.get('q', '')
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        sql = """
            SELECT s.*, c.name as category_name, c.icon as category_icon, f.floor_code
            FROM Store s
            JOIN StoreCategory c ON s.category_id = c.id
            JOIN Floor f ON s.floor_id = f.id
            WHERE s.mall_id = %s AND (s.name ILIKE %s OR c.name ILIKE %s)
        """
        search_param = f"%{query}%"
        cursor.execute(sql, (mall_id, search_param, search_param))
        stores = cursor.fetchall()
        return jsonify({"success": True, "data": [dict(s) for s in stores]})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# GET /api/stores/<store_id>
@store_bp.route('/<int:store_id>', methods=['GET'])
def get_store_by_id(store_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        sql = """
            SELECT s.*, c.name as category_name, c.icon as category_icon, f.floor_code, f.name as floor_name
            FROM Store s
            JOIN StoreCategory c ON s.category_id = c.id
            JOIN Floor f ON s.floor_id = f.id
            WHERE s.id = %s
        """
        cursor.execute(sql, (store_id,))
        store = cursor.fetchone()
        if store:
            return jsonify({"success": True, "data": dict(store)})
        return jsonify({"success": False, "message": "Store not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()