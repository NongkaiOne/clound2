from flask import Blueprint, request, jsonify, current_app
import jwt
import bcrypt
from datetime import datetime, timedelta
from functools import wraps
from db import get_connection  # ตรวจสอบให้แน่ใจว่า import ฟังก์ชันเชื่อม DB ถูกต้อง

auth_bp = Blueprint('auth_bp', __name__)

# ==========================================
# 1. Decorator สำหรับตรวจสอบ Token และ Role
# ==========================================
def token_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None
            # เช็คว่ามี Authorization header ส่งมาไหม
            if 'Authorization' in request.headers:
                try:
                    token = request.headers['Authorization'].split(" ")[1] # แยกคำว่า Bearer ออก
                except IndexError:
                    return jsonify({'message': 'Bearer token malformed!'}), 401

            if not token:
                return jsonify({'message': 'Token is missing!'}), 401

            try:
                # ถอดรหัส Token
                data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
                current_user_role = data.get('role')
                
                # เช็คสิทธิ์ (Role)
                if current_user_role not in allowed_roles:
                    return jsonify({'message': 'You do not have permission to perform this action!'}), 403
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired!'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Invalid token!'}), 401

            return f(data, *args, **kwargs)
        return decorated_function
    return decorator

# ==========================================
# 2. Route สำหรับสมัครสมาชิก (Register)
# ==========================================
@auth_bp.route('/register', methods=['POST'])
def register_user():
    conn = None
    cursor = None
    try:
        data = request.get_json()
        if not data or not data.get('UserName') or not data.get('Password') or not data.get('Email') or not data.get('RoleID'):
            return jsonify({"status": "error", "message": "Missing required data"}), 400

        username = data.get('UserName')
        email = data.get('Email')
        password = data.get('Password').encode('utf-8')
        role_id = data.get('RoleID')

        # เข้ารหัสผ่านด้วย bcrypt
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        conn = get_connection()
        cursor = conn.cursor()
        
        sql = "INSERT INTO User (UserName, Email, PasswordHash, RoleID) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (username, email, hashed_password.decode('utf-8'), role_id))
        conn.commit()

        return jsonify({"status": "ok", "message": "User registered successfully"}), 201

    except Exception as e:
        print("ERROR REGISTER USER:", e)
        return jsonify({"status": "error", "message": "Internal server error"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# ==========================================
# 3. Route สำหรับเข้าสู่ระบบ (Login)
# ==========================================
@auth_bp.route('/login', methods=['POST'])
def login():
    conn = None
    cursor = None
    try:
        data = request.get_json()
        if not data or not data.get('UserName') or not data.get('Password'):
            return jsonify({"status": "error", "message": "Missing username or password"}), 400

        username = data.get('UserName')
        password = data.get('Password').encode('utf-8')

        conn = get_connection()
        cursor = conn.cursor(dictionary=True) # ให้คืนค่ามาเป็น Dictionary เหมือนโค้ดที่ 1

        sql = """
            SELECT u.UserID, u.UserName, u.PasswordHash, r.RoleName
            FROM User u
            JOIN Role r ON u.RoleID = r.RoleID
            WHERE u.UserName = %s
        """
        cursor.execute(sql, (username,))
        user = cursor.fetchone()

        # ตรวจสอบรหัสผ่านที่รับมา กับรหัสผ่านที่ Hash ไว้ในฐานข้อมูล
        if user and bcrypt.checkpw(password, user['PasswordHash'].encode('utf-8')):
            
            # สร้าง JWT Token
            token = jwt.encode({
                'user_id': user['UserID'],
                'role': user['RoleName'],
                'exp': datetime.utcnow() + timedelta(hours=24) # หมดอายุใน 24 ชั่วโมง
            }, current_app.config['SECRET_KEY'], algorithm='HS256')

            return jsonify({
                "status": "ok",
                "message": "Login successful",
                "token": token,
                "user": {
                    "UserID": user['UserID'],
                    "UserName": user['UserName'],
                    "Role": user['RoleName']
                }
            })
        else:
            return jsonify({"status": "error", "message": "Invalid username or password"}), 401

    except Exception as e:
        print("ERROR LOGIN:", e)
        return jsonify({"status": "error", "message": "Internal server error"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()