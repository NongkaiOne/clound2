from flask import Blueprint, jsonify
import psycopg2.extras
from db import get_connection

floor_bp = Blueprint('floor_bp', __name__)

# GET /api/floors/mall/<mall_id>
@floor_bp.route('/mall/<int:mall_id>', methods=['GET'])
def get_floors_by_mall(mall_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        sql = """
            SELECT f.*, (SELECT COUNT(*) FROM Store s WHERE s.floor_id = f.id) as store_count
            FROM Floor f
            WHERE f.mall_id = %s
            ORDER BY f.floor_order ASC
        """
        cursor.execute(sql, (mall_id,))
        floors = cursor.fetchall()
        return jsonify({"success": True, "data": [dict(f) for f in floors]})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# GET /api/floors/<floor_id>/stores
@floor_bp.route('/<int:floor_id>/stores', methods=['GET'])
def get_stores_by_floor(floor_id):
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
            WHERE s.floor_id = %s
        """
        cursor.execute(sql, (floor_id,))
        stores = cursor.fetchall()
        return jsonify({"success": True, "data": [dict(s) for s in stores]})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()