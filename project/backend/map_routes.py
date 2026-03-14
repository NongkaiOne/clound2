from flask import Blueprint, jsonify
from db import connect_db

map_bp = Blueprint("map", __name__)

@map_bp.route("/map/stores", methods=["GET"])
def get_map_stores():

    db = connect_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT id,name,x,y FROM stores")

    stores = cursor.fetchall()

    return jsonify(stores)