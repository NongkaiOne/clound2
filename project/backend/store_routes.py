from flask import Blueprint, request
import psycopg2.extras
from api_utils import fail, ok
from auth_routes import token_required
from db import get_connection
from logger import log

store_bp = Blueprint("store_bp", __name__)

# -------------------
# Format functions
# -------------------
def format_store(row):
    return {
        "id": row["StoreID"],
        "name": row["StoreName"],
        "mall_id": row["MallID"],
        "floor": row.get("FloorCode"),
        "floor_id": row["FloorID"],
        "floor_code": row.get("FloorCode"),
        "map_x": float(row.get("PosX") or 0),
        "map_y": float(row.get("PosY") or 0),
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
        "owner_user_id": row.get("UserID"),
        "floor_name": row.get("FloorName"),
        "mall_name": row.get("MallName"),
        "store_category_id": row.get("StoreCategoryID"),
    }

def format_store_map(row):
    return {
        "id": row["StoreID"],
        "name": row["StoreName"],
        "mall_id": row["MallID"],
        "floor_id": row["FloorID"],
        "floor_code": row.get("FloorCode"),
        "map_x": float(row.get("PosX") or 0),
        "map_y": float(row.get("PosY") or 0),
        "position": {"x": float(row.get("PosX") or 0), "y": float(row.get("PosY") or 0)},
    }

# -------------------
# Base query
# -------------------
def base_store_query(where_clause="", order_clause="ORDER BY s.StoreName ASC"):
    return f"""
        SELECT
            s.StoreID,
            s.UserID,
            s.StoreName,
            s.StoreCategoryName,
            s.StoreCategoryIcon,
            s.StoreCategoryID,
            s.Description,
            s.Phone,
            s.OpeningHours,
            s.LogoURL,
            s.MallID,
            m.MallName,
            s.FloorID,
            f.FloorName,
            f.FloorCode,
            s.PosX,
            s.PosY
        FROM Store s
        JOIN Floor f ON f.FloorID = s.FloorID
        JOIN Mall m ON m.MallID = s.MallID
        {where_clause}
        {order_clause}
    """

# -------------------
# Endpoints
# -------------------
@store_bp.route("/", methods=["GET"])
def get_all_stores():
    conn = cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(base_store_query())
        stores = cursor.fetchall()
        return ok([format_store(row) for row in stores])
    except Exception as e:
        log.error("ERROR GET ALL STORES: %s", e)
        return fail("An internal server error occurred", 500)
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


@store_bp.route("/mall/<int:mall_id>", methods=["GET"])
def get_stores_by_mall(mall_id):
    conn = cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(base_store_query("WHERE s.MallID = %s"), (mall_id,))
        stores = cursor.fetchall()
        return ok([format_store(row) for row in stores])
    except Exception as e:
        log.error("ERROR GET STORES BY MALL: %s", e)
        return fail("An internal server error occurred", 500)
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


@store_bp.route("/search", methods=["GET"])
def search_stores():
    conn = cursor = None
    try:
        mall_id = request.args.get("mall_id", type=int)
        q = (request.args.get("q") or "").strip()

        conn = get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        conditions = []
        params = []
        if mall_id:
            conditions.append("s.MallID = %s")
            params.append(mall_id)
        if q:
            conditions.append("(s.StoreName ILIKE %s OR s.StoreCategoryName ILIKE %s)")
            like = f"%{q}%"
            params.extend([like, like])
        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        cursor.execute(base_store_query(where), tuple(params))
        stores = cursor.fetchall()
        return ok([format_store(row) for row in stores])
    except Exception as e:
        log.error("ERROR SEARCH STORES: %s", e)
        return fail("An internal server error occurred", 500)
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


@store_bp.route("/<int:store_id>", methods=["GET"])
def get_store_by_id(store_id):
    conn = cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(base_store_query("WHERE s.StoreID = %s", order_clause=""), (store_id,))
        row = cursor.fetchone()
        if not row:
            return fail("Store not found", 404)
        return ok(format_store(row))
    except Exception as e:
        log.error("ERROR GET STORE BY ID: %s", e)
        return fail("An internal server error occurred", 500)
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


# -------------------
# Map view
# -------------------
@store_bp.route("/map", methods=["GET"])
def get_map_stores():
    conn = cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(
            'SELECT "StoreID", "StoreName", "PosX", "PosY", "FloorID", "FloorCode" FROM "Store" ORDER BY "StoreName" ASC'
        )
        stores = cursor.fetchall()
        return ok([format_store_map(row) for row in stores])
    except Exception as e:
        log.error("ERROR GET MAP STORES: %s", e)
        return fail("An internal server error occurred", 500)
    finally:
        if cursor: cursor.close()
        if conn: conn.close()