from flask import Blueprint, jsonify, request
from db import connect_db

mall_bp = Blueprint("mall", __name__)

#ดึงข้อมูลห้างสรรพสินค้าทั้งหมด
@mall_bp.route('/', methods=['GET'])
def get_malls():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM malls")
        malls = cursor.fetchall()
        return jsonify({"success": True, "data": malls}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

#ดึงข้อมูลห้างสรรพสินค้าตาม ID
@mall_bp.route('/<int:mall_id>', methods=['GET'])
def get_mall_by_id(mall_id):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM malls WHERE id = %s", (mall_id,))
        mall = cursor.fetchone()
        if mall:
            return jsonify({"success": True, "data": mall}), 200
        return jsonify({"success": False, "message": "Mall not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()