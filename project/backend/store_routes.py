from flask import Blueprint, request, jsonify
from db import get_connection  # เปลี่ยนมาใช้ get_connection เพื่อให้เป็นมาตรฐานเดียวกัน
from middleware_auth import require_role

store_bp = Blueprint("store", __name__)

# ==========================================
# 1. Get All Stores (ดึงข้อมูลร้านค้าทั้งหมด)
# API Endpoint: GET /api/store/
# ==========================================
@store_bp.route("/", methods=["GET"])
def get_stores():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # ใช้ Schema ฐานข้อมูลที่ละเอียดขึ้นจากโค้ดที่ 2
        sql = """
        SELECT StoreID, UserID, StoreName, StoreCategoryID,
               Phone, LogoURL, FloorID, PosX, PosY
        FROM Store
        """
        cursor.execute(sql)
        stores = cursor.fetchall()

        return jsonify({
            "status": "ok",
            "stores": stores
        }), 200

    except Exception as e:
        print("ERROR GET STORES:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# ==========================================
# 2. Create Store (สร้างร้านค้าใหม่)
# API Endpoint: POST /api/store/
# ==========================================
@store_bp.route("/", methods=["POST"])
@require_role("Admin")  # ใช้ Middleware เดิมของคุณได้เลย
def create_store():
    conn = None
    cursor = None
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No JSON received"}), 400

        # รับค่าตาม Schema ใหม่
        userID = data.get("UserID")
        storeName = data.get("StoreName")
        categoryID = data.get("StoreCategoryID")
        phone = data.get("Phone")
        logo = data.get("LogoURL")
        floorID = data.get("FloorID")
        posX = data.get("PosX")
        posY = data.get("PosY")

        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        INSERT INTO Store
        (UserID, StoreName, StoreCategoryID, Phone, LogoURL, FloorID, PosX, PosY)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(sql, (
            userID, storeName, categoryID, phone, logo, floorID, posX, posY
        ))
        
        conn.commit()

        return jsonify({
            "status": "ok", 
            "message": "Store created successfully"
        }), 201

    except Exception as e:
        print("ERROR CREATE STORE:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# ==========================================
# 3. Delete Store (ลบร้านค้า)
# API Endpoint: DELETE /api/store/<store_id>
# ==========================================
@store_bp.route("/<int:store_id>", methods=["DELETE"])
@require_role("Admin")
def delete_store(store_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # อิงตามชื่อ Column DB ใหม่ (StoreID)
        cursor.execute("DELETE FROM Store WHERE StoreID=%s", (store_id,))
        conn.commit()

        # เช็คว่าลบสำเร็จจริงๆ หรือไม่ (มีข้อมูลถูกลบไปไหม)
        if cursor.rowcount == 0:
            return jsonify({"status": "error", "message": "Store not found"}), 404

        return jsonify({
            "status": "ok", 
            "message": "Store deleted successfully"
        }), 200

    except Exception as e:
        print("ERROR DELETE STORE:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        if cursor: cursor.close()
        if conn: conn.close()