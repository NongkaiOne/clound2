<<<<<<< HEAD
from flask import Blueprint, jsonify
import psycopg2.extras
=======
from flask import Blueprint

from api_utils import fail, ok
>>>>>>> origin/backend
from db import get_connection
from logger import log

floor_bp = Blueprint("floor_bp", __name__)

<<<<<<< HEAD
# GET /api/floors/mall/<mall_id>
@floor_bp.route('/mall/<int:mall_id>', methods=['GET'])
=======

def format_floor(row):
    return {
        "id": row["FloorID"],
        "name": row["FloorName"],
        "mall_id": row["MallID"],
        "floor_code": row["FloorCode"],
        "floor_order": row["FloorOrder"],
        "store_count": int(row.get("store_count") or 0),
    }


def format_store(row):
    return {
        "id": row["StoreID"],
        "name": row["StoreName"],
        "mall_id": row["MallID"],
        "floor": row["FloorCode"],
        "floor_id": row["FloorID"],
        "position": {"x": float(row.get("PosX") or 0), "y": float(row.get("PosY") or 0)},
        "logo": row.get("LogoURL"),
        "category_name": row.get("StoreCategoryName"),
        "category": {
            "name": row.get("StoreCategoryName"),
            "icon": row.get("StoreCategoryIcon"),
        },
        "description": row.get("Description"),
        "phone": row.get("Phone"),
        "opening_hours": row.get("OpeningHours"),
    }


@floor_bp.route("/mall/<int:mall_id>", methods=["GET"])
>>>>>>> origin/backend
def get_floors_by_mall(mall_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
<<<<<<< HEAD
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
=======
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT
                f.FloorID,
                f.FloorName,
                f.MallID,
                f.FloorCode,
                f.FloorOrder,
                COUNT(s.StoreID) AS store_count
            FROM Floor f
            LEFT JOIN Store s ON s.FloorID = f.FloorID
            WHERE f.MallID = %s
            GROUP BY f.FloorID
            ORDER BY f.FloorOrder ASC
        """
        cursor.execute(sql, (mall_id,))
        return ok([format_floor(row) for row in cursor.fetchall()])
    except Exception as e:
        log.error("ERROR GET FLOORS BY MALL: %s", e)
        return fail("An internal server error occurred", 500)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@floor_bp.route("/<int:floor_id>/stores", methods=["GET"])
>>>>>>> origin/backend
def get_stores_by_floor(floor_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
<<<<<<< HEAD
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
=======
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT
                s.StoreID,
                s.StoreName,
                s.MallID,
                s.FloorID,
                f.FloorCode,
                s.PosX,
                s.PosY,
                s.LogoURL,
                s.StoreCategoryName,
                s.StoreCategoryIcon,
                s.Description,
                s.Phone,
                s.OpeningHours
            FROM Store s
            JOIN Floor f ON f.FloorID = s.FloorID
            WHERE s.FloorID = %s
            ORDER BY s.StoreName ASC
        """
        cursor.execute(sql, (floor_id,))
        return ok([format_store(row) for row in cursor.fetchall()])
    except Exception as e:
        log.error("ERROR GET STORES BY FLOOR: %s", e)
        return fail("An internal server error occurred", 500)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
>>>>>>> origin/backend
