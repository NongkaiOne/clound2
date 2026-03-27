from flask import Blueprint, jsonify
from db import get_connection

floor_bp = Blueprint('floor_bp', __name__)

# ==========================================
# FORMATTERS (แปลง DB → Frontend)
# ==========================================

def format_floor(f):
    return {
        "id": f.get("FloorID"),
        "name": f.get("FloorName"),
        "mall_id": f.get("MallID"),
        "map_image_url": f.get("MapImageURL"),
        "store_count": f.get("store_count", 0)
    }


def format_store(s):
    return {
        "id": s.get("StoreID"),
        "name": s.get("StoreName"),
        "floor_id": s.get("FloorID"),
        "position": {
            "x": s.get("PosX"),
            "y": s.get("PosY")
        },
        "logo": s.get("LogoURL"),
        "category": {
            "name": s.get("CategoryName"),
            "icon": s.get("CategoryIcon")
        }
    }


# ==========================================
# 1. GET FLOORS BY MALL
# GET /api/floors/mall/<mall_id>
# ==========================================

@floor_bp.route('/mall/<int:mall_id>', methods=['GET'])
def get_floors_by_mall(mall_id):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """
            SELECT 
                f.FloorID,
                f.FloorName,
                f.MallID,
                f.MapImageURL,
                (
                    SELECT COUNT(*) 
                    FROM Store s 
                    WHERE s.FloorID = f.FloorID
                ) AS store_count
            FROM Floor f
            WHERE f.MallID = %s
            ORDER BY f.FloorID ASC
        """

        cursor.execute(sql, (mall_id,))
        floors = cursor.fetchall()

        formatted = [format_floor(f) for f in floors]

        return jsonify({
            "success": True,
            "data": formatted
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        if cursor: cursor.close()
        if conn: conn.close()


# ==========================================
# 2. GET STORES BY FLOOR
# GET /api/floors/<floor_id>/stores
# ==========================================

@floor_bp.route('/<int:floor_id>/stores', methods=['GET'])
def get_stores_by_floor(floor_id):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """
            SELECT 
                s.StoreID,
                s.StoreName,
                s.FloorID,
                s.PosX,
                s.PosY,
                s.LogoURL,
                c.CategoryName,
                c.IconURL AS CategoryIcon
            FROM Store s
            JOIN StoreCategory c 
                ON s.StoreCategoryID = c.StoreCategoryID
            WHERE s.FloorID = %s
            ORDER BY s.StoreName ASC
        """

        cursor.execute(sql, (floor_id,))
        stores = cursor.fetchall()

        formatted = [format_store(s) for s in stores]

        return jsonify({
            "success": True,
            "data": formatted
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        if cursor: cursor.close()
        if conn: conn.close()