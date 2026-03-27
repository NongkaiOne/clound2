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
        "floor_code": f.get("FloorCode"), # ดึงเพิ่มจาก Schema ใหม่
        "floor_order": f.get("FloorOrder"), # ดึงเพิ่มเผื่อ Front-end เอาไปจัดเรียง
        "store_count": f.get("StoreCount", 0) # อิงชื่อให้ตรงกับ DB ใหม่
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
            "name": s.get("StoreCategoryName"), # ดึงจาก Denormalized field ได้เลย
            "icon": s.get("StoreCategoryIcon")  # ดึงจาก Denormalized field ได้เลย
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

        # อัปเดต SQL ดึงคอลัมน์ให้ตรง Schema
        sql = """
            SELECT 
                FloorID,
                FloorName,
                FloorCode,
                FloorOrder,
                MallID,
                StoreCount
            FROM Floor
            WHERE MallID = %s
            ORDER BY FloorOrder ASC
        """

        cursor.execute(sql, (mall_id,))
        floors = cursor.fetchall()

        formatted = [format_floor(f) for f in floors]

        return jsonify({
            "success": True,
            "data": formatted
        }), 200

    except Exception as e:
        print(f"🔥 ERROR GET FLOORS: {e}") # เพิ่มบรรทัดนี้
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

        # เราเก็บ CategoryName กับ CategoryIcon ไว้ในตาราง Store 
        # ดังนั้นไม่ต้อง JOIN ตาราง StoreCategory แล้ว ทำให้โหลดเร็วขึ้นด้วย
        sql = """
            SELECT 
                StoreID,
                StoreName,
                FloorID,
                PosX,
                PosY,
                LogoURL,
                StoreCategoryName,
                StoreCategoryIcon
            FROM Store
            WHERE FloorID = %s
            ORDER BY StoreName ASC
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