<<<<<<< HEAD
from flask import Blueprint, request, jsonify
import psycopg2.extras
=======
from flask import Blueprint, request

from api_utils import fail, ok
>>>>>>> origin/backend
from db import get_connection
from logger import log

mall_bp = Blueprint("mall_bp", __name__)

<<<<<<< HEAD
def format_mall(m):
    return {
        "id": m.get("mallid") or m.get("id"),
        "name": m.get("mallname") or m.get("name"),
        "location": m.get("location"),
        "store_count": m.get("store_count") or m.get("storecount", 0),
        "is_popular": m.get("ispopular") or m.get("is_popular", False)
    }

# GET /api/malls
@mall_bp.route('', methods=['GET'])
@mall_bp.route('/', methods=['GET'])
=======

def format_mall(row):
    return {
        "id": row["MallID"],
        "name": row["MallName"],
        "location": row["Location"],
        "image": row["MallImageURL"],
        "is_popular": bool(row.get("IsPopular", 0)),
        "store_count": int(row.get("store_count") or 0),
    }


BASE_SQL = """
    SELECT
        m.MallID,
        m.MallName,
        m.Location,
        m.IsPopular,
        m.MallImageURL,
        COUNT(s.StoreID) AS store_count
    FROM Mall m
    LEFT JOIN Store s ON s.MallID = m.MallID
"""


@mall_bp.route("/", methods=["GET"])
>>>>>>> origin/backend
def get_malls():
    conn = None
    cursor = None
    try:
<<<<<<< HEAD
        search = request.args.get('search', '')
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        if search:
            sql = "SELECT * FROM Mall WHERE MallName ILIKE %s OR Location ILIKE %s"
            cursor.execute(sql, (f"%{search}%", f"%{search}%"))
        else:
            cursor.execute("SELECT * FROM Mall")

        malls = cursor.fetchall()
        formatted = [format_mall(dict(m)) for m in malls]
        log.info(f"Fetched {len(formatted)} malls")
        return jsonify({"success": True, "data": formatted}), 200

    except Exception as e:
        log.error(f"ERROR GET MALLS: {e}")
        return jsonify({"success": False, "message": str(e)}), 500
=======
        search = (request.args.get("search") or "").strip()
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        if search:
            sql = BASE_SQL + " WHERE m.MallName LIKE %s OR m.Location LIKE %s GROUP BY m.MallID ORDER BY m.MallName ASC"
            like = f"%{search}%"
            cursor.execute(sql, (like, like))
        else:
            sql = BASE_SQL + " GROUP BY m.MallID ORDER BY m.MallName ASC"
            cursor.execute(sql)
        return ok([format_mall(row) for row in cursor.fetchall()])
    except Exception as e:
        log.error("ERROR GET MALLS: %s", e)
        return fail("An internal server error occurred", 500)
>>>>>>> origin/backend
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

<<<<<<< HEAD
# GET /api/malls/popular
@mall_bp.route('/popular', methods=['GET'])
=======

@mall_bp.route("/popular", methods=["GET"])
>>>>>>> origin/backend
def get_popular_malls():
    conn = None
    cursor = None
    try:
        conn = get_connection()
<<<<<<< HEAD
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT * FROM Mall WHERE IsPopular = TRUE")
        malls = cursor.fetchall()
        formatted = [format_mall(dict(m)) for m in malls]
        return jsonify({"success": True, "data": formatted}), 200

    except Exception as e:
        log.error(f"ERROR GET POPULAR MALLS: {e}")
        return jsonify({"success": False, "message": str(e)}), 500
=======
        cursor = conn.cursor(dictionary=True)
        cursor.execute(BASE_SQL + " WHERE m.IsPopular = 1 GROUP BY m.MallID ORDER BY m.MallName ASC")
        return ok([format_mall(row) for row in cursor.fetchall()])
    except Exception as e:
        log.error("ERROR GET POPULAR MALLS: %s", e)
        return fail("An internal server error occurred", 500)
>>>>>>> origin/backend
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

<<<<<<< HEAD
# GET /api/malls/recent
@mall_bp.route('/recent', methods=['GET'])
def get_recent_malls():
    return jsonify({"success": True, "data": []}), 200

# GET /api/malls/<id>
@mall_bp.route('/<int:mall_id>', methods=['GET'])
=======

@mall_bp.route("/recent/", methods=["GET"])
def get_recent_malls():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(BASE_SQL + " GROUP BY m.MallID ORDER BY m.MallID DESC LIMIT 3")
        return ok([format_mall(row) for row in cursor.fetchall()])
    except Exception as e:
        log.error("ERROR GET RECENT MALLS: %s", e)
        return fail("An internal server error occurred", 500)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@mall_bp.route("/<int:mall_id>", methods=["GET"])
>>>>>>> origin/backend
def get_mall_by_id(mall_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
<<<<<<< HEAD
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT * FROM Mall WHERE MallID = %s", (mall_id,))
        mall = cursor.fetchone()

        if not mall:
            return jsonify({"success": False, "message": "Mall not found"}), 404

        return jsonify({"success": True, "data": format_mall(dict(mall))}), 200

    except Exception as e:
        log.error(f"ERROR GET MALL BY ID {mall_id}: {e}")
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
=======
        cursor = conn.cursor(dictionary=True)
        cursor.execute(BASE_SQL + " WHERE m.MallID = %s GROUP BY m.MallID", (mall_id,))
        row = cursor.fetchone()
        if not row:
            return fail("Mall not found", 404)
        return ok(format_mall(row))
    except Exception as e:
        log.error("ERROR GET MALL BY ID: %s", e)
        return fail("An internal server error occurred", 500)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
>>>>>>> origin/backend
