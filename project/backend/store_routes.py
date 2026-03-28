from flask import Blueprint, request, jsonify
from db import get_connection

store_bp = Blueprint('store_bp', __name__)


# =========================
# Helper: floor code
# =========================
def get_floor_code(name):
    if not name:
        return ""
    if "Lower" in name:
        return "LG"
    if "Ground" in name:
        return "G"
    return name.split()[-1]  # "Floor 1" → "1"


# =========================
# Helper: category icon (fallback)
# =========================
ICON_MAP = {
    "Food & Beverage": "🍔",
    "Clothing": "👕",
    "Electronics": "💻",
    "Beauty": "💄",
    "Sports": "⚽"
}


# =========================
# FORMATTER
# =========================
def format_store(s):
    return {
        "id": s.get("id"),
        "floor_id": s.get("floor_id"),
        "mall_id": s.get("mall_id"),
        "name": s.get("name"),
        "description": s.get("description", ""),
        "category_name": s.get("category_name"),
        "category_icon": s.get("category_icon") or ICON_MAP.get(s.get("category_name"), "🏬"),
        "floor_name": s.get("floor_name"),
        "floor_code": s.get("floor_code") or get_floor_code(s.get("floor_name")),
        "map_x": s.get("map_x"),
        "map_y": s.get("map_y")
    }


# =========================
# ROUTES
# =========================

# 📋 ดึงร้านค้าทั้งหมด (สำหรับ Admin)
@store_bp.route('/', methods=['GET'])
def get_all_stores():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    # Query ข้อมูลจากตาราง Store โดยตรงตามโครงสร้างใน sampleData.sql
    sql = "SELECT * FROM Store ORDER BY StoreID DESC"
    cursor.execute(sql)
    stores = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({
        "success": True,
        "data": stores
    })

# ➕ เพิ่มร้านค้าใหม่ (สำหรับ Admin)
@store_bp.route('/', methods=['POST'])
def create_store():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = """
            INSERT INTO Store (
                UserID, StoreName, StoreCategoryName, StoreCategoryID, 
                Description, Phone, OpeningHours, LogoURL, 
                MallID, FloorName, FloorID, PosX, PosY
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data.get('UserID'), data.get('StoreName'), data.get('StoreCategoryName'),
            data.get('StoreCategoryID'), data.get('Description'), data.get('Phone'),
            data.get('OpeningHours'), data.get('LogoURL'), data.get('MallID'),
            data.get('FloorName'), data.get('FloorID'), data.get('PosX'), data.get('PosY')
        )
        cursor.execute(sql, values)
        conn.commit()
        return jsonify({"success": True, "message": "Store created successfully"}), 201
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# 📝 แก้ไขข้อมูลร้านค้า (สำหรับ Admin)
@store_bp.route('/<int:store_id>', methods=['PUT'])
def update_store(store_id):
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = """
            UPDATE Store SET 
                StoreName=%s, StoreCategoryName=%s, StoreCategoryID=%s, 
                Description=%s, Phone=%s, OpeningHours=%s, LogoURL=%s, 
                FloorName=%s, PosX=%s, PosY=%s
            WHERE StoreID=%s
        """
        values = (
            data.get('StoreName'), data.get('StoreCategoryName'), data.get('StoreCategoryID'),
            data.get('Description'), data.get('Phone'), data.get('OpeningHours'), 
            data.get('LogoURL'), data.get('FloorName'), data.get('PosX'), 
            data.get('PosY'), store_id
        )
        cursor.execute(sql, values)
        conn.commit()
        return jsonify({"success": True, "message": "Store updated successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# 🗑️ ลบร้านค้า (สำหรับ Admin)
@store_bp.route('/<int:store_id>', methods=['DELETE'])
def delete_store(store_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Store WHERE StoreID = %s", (store_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"success": True, "message": "Store deleted successfully"})

# 🏬 ดึงร้านค้าทั้งหมดใน Mall
@store_bp.route('/mall/<int:mall_id>', methods=['GET'])
def get_stores_by_mall(mall_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    sql = """
        SELECT 
            s.StoreID AS id,
            s.FloorID AS floor_id,
            s.MallID AS mall_id,
            s.StoreName AS name,
            s.Description AS description,
            s.PosX AS map_x,
            s.PosY AS map_y,
            s.StoreCategoryName AS category_name,
            s.StoreCategoryIcon AS category_icon,
            f.FloorName AS floor_name,
            f.FloorCode AS floor_code
        FROM Store s
        JOIN Floor f ON s.FloorID = f.FloorID
        WHERE s.MallID = %s
        ORDER BY s.StoreName ASC
    """

    cursor.execute(sql, (mall_id,))
    stores = cursor.fetchall()

    cursor.close()
    conn.close()

    formatted = [format_store(s) for s in stores]

    return jsonify({
        "success": True,
        "data": formatted
    })


# 🔍 ค้นหาร้านค้าใน Mall
@store_bp.route('/search', methods=['GET'])
def search_stores():
    mall_id = request.args.get('mall_id')
    query = request.args.get('q', '').strip()

    if not mall_id:
        return jsonify({
            "success": False,
            "message": "mall_id is required"
        }), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    sql = """
        SELECT 
            s.StoreID AS id,
            s.FloorID AS floor_id,
            s.MallID AS mall_id,
            s.StoreName AS name,
            s.Description AS description,
            s.PosX AS map_x,
            s.PosY AS map_y,
            s.StoreCategoryName AS category_name,
            s.StoreCategoryIcon AS category_icon,
            f.FloorName AS floor_name,
            f.FloorCode AS floor_code
        FROM Store s
        JOIN Floor f ON s.FloorID = f.FloorID
        WHERE s.MallID = %s 
          AND (s.StoreName LIKE %s OR s.StoreCategoryName LIKE %s)
        ORDER BY s.StoreName ASC
    """

    search_param = f"%{query}%"
    cursor.execute(sql, (mall_id, search_param, search_param))

    stores = cursor.fetchall()

    cursor.close()
    conn.close()

    formatted = [format_store(s) for s in stores]

    return jsonify({
        "success": True,
        "data": formatted
    })


# 🔍 ดูรายละเอียดร้านค้าตาม ID
@store_bp.route('/<int:store_id>', methods=['GET'])
def get_store_by_id(store_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    sql = """
        SELECT 
            s.StoreID AS id,
            s.FloorID AS floor_id,
            s.MallID AS mall_id,
            s.StoreName AS name,
            s.Description AS description,
            s.PosX AS map_x,
            s.PosY AS map_y,
            s.StoreCategoryName AS category_name,
            s.StoreCategoryIcon AS category_icon,
            f.FloorName AS floor_name,
            f.FloorCode AS floor_code
        FROM Store s
        JOIN Floor f ON s.FloorID = f.FloorID
        WHERE s.StoreID = %s
    """

    cursor.execute(sql, (store_id,))
    store = cursor.fetchone()

    cursor.close()
    conn.close()

    if not store:
        return jsonify({
            "success": False,
            "message": "Store not found"
        }), 404

    return jsonify({
        "success": True,
        "data": format_store(store)
    })