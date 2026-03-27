from flask import Blueprint, request, jsonify
from db import get_connection
from logger import log

mall_bp = Blueprint("mall_bp", __name__)


# =========================
# FORMATTER
# =========================
def format_mall(m):
    return {
        "id": m.get("MallID"),
        "name": m.get("MallName"),
        "location": m.get("Location"),
        "store_count": m.get("StoreCount", 0), # ดึงจากคอลัมน์ DB ตรงๆ เลย
        "is_popular": m.get("IsPopular", 0),
        "image": m.get("MallImageURL") # เผื่อ Front-end ต้องการใช้
    }


# =========================
# GET ALL MALLS
# =========================
@mall_bp.route('/', methods=['GET'])
def get_malls():
    conn = None
    cursor = None

    try:
        search = request.args.get('search', '').strip()

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """
            SELECT 
                MallID,
                MallName,
                Location,
                IsPopular,
                StoreCount,
                MallImageURL
            FROM Mall
        """

        if search:
            sql += " WHERE MallName LIKE %s OR Location LIKE %s"
            cursor.execute(sql, (f"%{search}%", f"%{search}%"))
        else:
            cursor.execute(sql)

        malls = cursor.fetchall()
        formatted = [format_mall(m) for m in malls]

        log.info(f"Fetched {len(formatted)} malls")

        return jsonify({
            "success": True,
            "data": formatted
        }), 200

    except Exception as e:
        log.error(f"ERROR GET MALLS: {e}")
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        if cursor: cursor.close()
        if conn: conn.close()


# =========================
# GET POPULAR
# =========================
@mall_bp.route('/popular', methods=['GET'])
def get_popular_malls():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                MallID,
                MallName,
                Location,
                IsPopular,
                StoreCount,
                MallImageURL
            FROM Mall
            WHERE IsPopular = 1
        """)

        malls = cursor.fetchall()
        formatted = [format_mall(m) for m in malls]

        return jsonify({
            "success": True,
            "data": formatted
        }), 200

    except Exception as e:
        log.error(f"ERROR GET POPULAR MALLS: {e}")
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        if cursor: cursor.close()
        if conn: conn.close()


# =========================
# GET BY ID
# =========================
@mall_bp.route('/<int:mall_id>', methods=['GET'])
def get_mall_by_id(mall_id):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                MallID,
                MallName,
                Location,
                IsPopular,
                StoreCount,
                MallImageURL
            FROM Mall
            WHERE MallID = %s
        """, (mall_id,))

        mall = cursor.fetchone()

        if not mall:
            return jsonify({
                "success": False,
                "message": "Mall not found"
            }), 404

        return jsonify({
            "success": True,
            "data": format_mall(mall)
        }), 200

    except Exception as e:
        log.error(f"ERROR GET MALL BY ID {mall_id}: {e}")
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        if cursor: cursor.close()
        if conn: conn.close()