from flask import Flask, jsonify
from db import get_connection

app = Flask(__name__)

@app.route("/")
def hello():
    return "hello world"

@app.route("/testdb")
def testdb():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    return "Database Connected"

@app.route("/stores")
def get_stores():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT StoreID, StoreName, Phone, LogoURL FROM Store")
        stores = cursor.fetchall()

        return jsonify({"status": "ok", "stores": stores})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)