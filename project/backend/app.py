from flask import Flask
from auth_routes import auth_bp
from map_routes import map_bp
from store_routes import store_bp
from product_routes import product_bp
from favorite_routes import favorite_bp
from upload_routes import upload_bp

app = Flask(__name__)

app.register_blueprint(auth_bp)
app.register_blueprint(map_bp)
app.register_blueprint(store_bp)
app.register_blueprint(product_bp)
app.register_blueprint(favorite_bp)
app.register_blueprint(upload_bp)

if __name__ == "__main__":
    app.run(debug=True)