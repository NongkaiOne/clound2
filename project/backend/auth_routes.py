from datetime import datetime, timedelta, timezone
from functools import wraps
<<<<<<< HEAD
import psycopg2.extras
=======

import bcrypt
import jwt
from flask import Blueprint, current_app, request

from api_utils import fail, ok
>>>>>>> origin/backend
from db import get_connection
from logger import log

auth_bp = Blueprint("auth_bp", __name__)

<<<<<<< HEAD
# ==========================================
# 1. Decorator for Token and Role Verification
# ==========================================
def token_required(allowed_roles):
=======
ROLE_NAMES = {
    "admin": "Admin",
    "storeowner": "StoreOwner",
    "seller": "StoreOwner",
    "customer": "Customer",
    "user": "Customer",
}


def normalize_role(role_name):
    if not role_name:
        return role_name
    return ROLE_NAMES.get(str(role_name).strip().lower(), role_name)


def fetch_user_by_email(cursor, email):
    sql = """
        SELECT
            u.UserID AS id,
            u.UserName AS username,
            u.Email AS email,
            u.PasswordHash AS password_hash,
            r.RoleName AS role_name,
            s.StoreID AS store_id,
            s.StoreName AS store_name
        FROM `User` u
        JOIN Role r ON u.RoleID = r.RoleID
        LEFT JOIN Store s ON s.UserID = u.UserID
        WHERE u.Email = %s
        LIMIT 1
    """
    cursor.execute(sql, (email,))
    user = cursor.fetchone()
    if user:
        user["role_name"] = normalize_role(user.get("role_name"))
    return user


def fetch_user_by_id(cursor, user_id):
    sql = """
        SELECT
            u.UserID AS id,
            u.UserName AS username,
            u.Email AS email,
            r.RoleName AS role,
            s.StoreID AS store_id,
            s.StoreName AS store_name
        FROM `User` u
        JOIN Role r ON u.RoleID = r.RoleID
        LEFT JOIN Store s ON s.UserID = u.UserID
        WHERE u.UserID = %s
        LIMIT 1
    """
    cursor.execute(sql, (user_id,))
    user = cursor.fetchone()
    if user:
        user["role"] = normalize_role(user.get("role"))
    return user


def build_user_payload(user):
    payload = {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "role": normalize_role(user.get("role") or user.get("role_name")),
    }
    if user.get("store_id"):
        payload["store_id"] = user["store_id"]
    if user.get("store_name"):
        payload["store_name"] = user["store_name"]
    return payload


def token_required(allowed_roles=None):
    allowed_roles = allowed_roles or []

>>>>>>> origin/backend
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            auth_header = request.headers.get("Authorization", "")
            if not auth_header.startswith("Bearer "):
                return fail("Authorization header is missing or malformed", 401)

            token = auth_header.split(" ", 1)[1].strip()
            if not token:
                return fail("Token is missing", 401)

            try:
<<<<<<< HEAD
                data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
                current_user_role = data.get('role')

                if current_user_role not in allowed_roles:
                    return jsonify({'message': f'Access denied. Requires one of these roles: {", ".join(allowed_roles)}'}), 403

                return f(data, *args, **kwargs)

=======
                decoded = jwt.decode(
                    token,
                    current_app.config["SECRET_KEY"],
                    algorithms=["HS256"],
                )
                decoded["role"] = normalize_role(decoded.get("role"))
>>>>>>> origin/backend
            except jwt.ExpiredSignatureError:
                return fail("Token has expired", 401)
            except jwt.InvalidTokenError:
                return fail("Invalid token", 401)

            if allowed_roles and decoded.get("role") not in allowed_roles:
                return fail("Access denied", 403)

            return f(decoded, *args, **kwargs)

        return wrapped

    return decorator

<<<<<<< HEAD
# ==========================================
# 2. Register
# ==========================================
@auth_bp.route('/register', methods=['POST'])
=======

@auth_bp.route("/register", methods=["POST"])
>>>>>>> origin/backend
def register_user():
    conn = None
    cursor = None
    try:
<<<<<<< HEAD
        data = request.get_json()
        if not data or not data.get('username') or not data.get('password') or not data.get('email'):
            return jsonify({"status": "error", "message": "Username, Email, and Password are required"}), 400

        username = data.get('username')
        email = data.get('email')
        password = data.get('password').encode('utf-8')
        role_id = 3

        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        conn = get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cursor.execute('SELECT id FROM "User" WHERE username = %s OR email = %s', (username, email))
=======
        data = request.get_json(silent=True) or {}
        username = (data.get("username") or "").strip()
        email = (data.get("email") or "").strip().lower()
        password = data.get("password") or ""

        if not username or not email or not password:
            return fail("Username, email, and password are required", 400)

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT UserID FROM `User` WHERE UserName = %s OR Email = %s LIMIT 1",
            (username, email),
        )
>>>>>>> origin/backend
        if cursor.fetchone():
            return fail("Username or email already exists", 409)

        cursor.execute(
<<<<<<< HEAD
            'INSERT INTO "User" (username, email, password_hash, role_id) VALUES (%s, %s, %s, %s)',
            (username, email, hashed_password.decode('utf-8'), role_id)
        )
        conn.commit()

        log.info(f"New user registered: {username}")
        return jsonify({"success": True, "message": "User registered successfully as Customer"}), 201

=======
            "SELECT RoleID FROM Role WHERE LOWER(RoleName) IN ('customer', 'user') ORDER BY RoleID LIMIT 1"
        )
        role_row = cursor.fetchone()
        if not role_row:
            return fail("Customer role is missing in database", 500)

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        cursor.execute(
            "INSERT INTO `User` (UserName, Email, PasswordHash, RoleID) VALUES (%s, %s, %s, %s)",
            (username, email, hashed_password, role_row["RoleID"]),
        )
        conn.commit()
        log.info("Registered user %s", email)
        return ok(message="User registered successfully", status=201)
>>>>>>> origin/backend
    except Exception as e:
        log.error("ERROR REGISTER USER: %s", e)
        return fail("An internal server error occurred", 500)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

<<<<<<< HEAD
# ==========================================
# 3. Login
# ==========================================
@auth_bp.route('/login', methods=['POST'])
=======

@auth_bp.route("/login", methods=["POST"])
>>>>>>> origin/backend
def login():
    conn = None
    cursor = None
    try:
<<<<<<< HEAD
        data = request.get_json()
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({"status": "error", "message": "Missing email or password"}), 400
=======
        data = request.get_json(silent=True) or {}
        email = (data.get("email") or "").strip().lower()
        password = data.get("password") or ""
>>>>>>> origin/backend

        if not email or not password:
            return fail("Email and password are required", 400)

        conn = get_connection()
<<<<<<< HEAD
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        sql = """
            SELECT u.id, u.username, u.email, u.password_hash, u.store_id, r.role_name
            FROM "User" u
            JOIN Role r ON u.role_id = r.role_id
            WHERE u.email = %s
        """
        cursor.execute(sql, (email,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password, user['password_hash'].encode('utf-8')):
            payload = {
                'user_id': user['id'],
                'role': user['role_name'],
                'exp': datetime.utcnow() + timedelta(hours=24)
            }
            if user['role_name'] == 'StoreOwner' and user['store_id']:
                payload['store_id'] = user['store_id']

            token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

            user_response = {
                "id": user['id'],
                "username": user['username'],
                "email": user['email'],
                "role": user['role_name']
            }
            if user['role_name'] == 'StoreOwner':
                user_response['store_id'] = user['store_id']

            log.info(f"User '{user['username']}' logged in as '{user['role_name']}'.")
            return jsonify({
                "success": True,
                "message": "Login successful",
                "token": token,
                "user": user_response
            })
        else:
            log.warning(f"Login failed for: {email}")
            return jsonify({"success": False, "message": "Invalid email or password"}), 401
=======
        cursor = conn.cursor(dictionary=True)
        user = fetch_user_by_email(cursor, email)

        if not user or not bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
            return fail("Invalid email or password", 401)

        payload = {
            "user_id": user["id"],
            "role": user["role_name"],
            "exp": datetime.now(timezone.utc) + timedelta(hours=24),
        }
        if user.get("store_id"):
            payload["store_id"] = user["store_id"]
>>>>>>> origin/backend

        token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")
        return ok(build_user_payload(user), message="Login successful", token=token)
    except Exception as e:
        log.error("ERROR LOGIN: %s", e)
        return fail("An internal server error occurred", 500)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

<<<<<<< HEAD
# ==========================================
# 4. Profile
# ==========================================
@auth_bp.route('/profile', methods=['GET'])
@token_required(allowed_roles=['Admin', 'StoreOwner', 'Customer'])
=======

@auth_bp.route("/profile", methods=["GET"])
@token_required(["Admin", "StoreOwner", "Customer"])
>>>>>>> origin/backend
def get_profile(current_user):
    conn = None
    cursor = None
    try:
        conn = get_connection()
<<<<<<< HEAD
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        sql = """
            SELECT u.id, u.username, u.email, r.role_name as role, u.store_id
            FROM "User" u
            JOIN Role r ON u.role_id = r.role_id
            WHERE u.id = %s
        """
        cursor.execute(sql, (user_id,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404

        return jsonify({"success": True, "user": dict(user)})

=======
        cursor = conn.cursor(dictionary=True)
        user = fetch_user_by_id(cursor, current_user["user_id"])
        if not user:
            return fail("User not found", 404)
        return ok(build_user_payload(user), user=build_user_payload(user))
>>>>>>> origin/backend
    except Exception as e:
        log.error("ERROR PROFILE: %s", e)
        return fail("An internal server error occurred", 500)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
