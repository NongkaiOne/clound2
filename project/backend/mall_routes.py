from flask import Blueprint, request, jsonify
import psycopg2.extras
from db import get_connection
from logger import log

mall_bp = Blueprint("mall_bp", __name__)

def format_mall(m):
    return {
        "id": m.get("mallid") or m.get("id"),
        "name": m.get("mallname") or m.get("name"),
        "location": m.get("location"),
        "store_count": m.get("store_count") or m.get("storecount", 0),
        "is_popular": m.get("ispopular") or m.get("is_popular", False)
    }

# GET /api/malls
@mall_bp.route('', methods=['GET'])
@mall_bp.route('/', methods=['GET'])
def get_malls():
    conn = None
    cursor = None
    try:
        search = request.args.get('search', '')
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        if search:
            sql = "SELECT * FROM Mall WHERE MallName ILIKE %s OR Location ILIKE %s"
            cursor.execute(sql, (f"%{search}%", f"%{search}%"))
        else:
            cursor.execute("SELECT * FROM Mall")

        malls = cursor.fetchall()
        formatted = [format_mall(dict(m)) for m in malls]
        log.info(f"Fetched {len(formatted)} malls")
        return jsonify({"success": True, "data": formatted}), 200

    except Exception as e:
        log.error(f"ERROR GET MALLS: {e}")
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# GET /api/malls/popular
@mall_bp.route('/popular', methods=['GET'])
def get_popular_malls():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT * FROM Mall WHERE IsPopular = TRUE")
        malls = cursor.fetchall()
        formatted = [format_mall(dict(m)) for m in malls]
        return jsonify({"success": True, "data": formatted}), 200

    except Exception as e:
        log.error(f"ERROR GET POPULAR MALLS: {e}")
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# GET /api/malls/recent
@mall_bp.route('/recent', methods=['GET'])
def get_recent_malls():
    return jsonify({"success": True, "data": []}), 200

# GET /api/malls/<id>
@mall_bp.route('/<int:mall_id>', methods=['GET'])
def get_mall_by_id(mall_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT * FROM Mall WHERE MallID = %s", (mall_id,))
        mall = cursor.fetchone()

        if not mall:
            return jsonify({"success": False, "message": "Mall not found"}), 404

        return jsonify({"success": True, "data": format_mall(dict(mall))}), 200

    except Exception as e:
        log.error(f"ERROR GET MALL BY ID {mall_id}: {e}")
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()