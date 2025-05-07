import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from api.models import db
from api.routes import api  # Blueprint con las rutas de la API
from api.utils import APIException

# === Inicializa la app de Flask ===
app = Flask(__name__)
app.url_map.strict_slashes = False

# CORS permite solicitudes desde otros orígenes (frontend)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# === Configuración de la Base de Datos ===
db_url = os.getenv("DATABASE_URL")
if db_url:
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# === Configuración de JWT ===
# ¡Cambia esto en producción!
app.config["JWT_SECRET_KEY"] = "clave-super-secreta"

# === Inicialización de extensiones ===
db.init_app(app)
Migrate(app, db)
JWTManager(app)

# === Registro del blueprint con prefijo /api ===
app.register_blueprint(api, url_prefix="/api")

# === Manejo global de errores personalizados ===


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# === Ruta base para verificar el servidor ===


@app.route("/")
def index():
    return jsonify({"msg": "Servidor Flask activo 🔥"}), 200


# === Ejecutar el servidor ===
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 3001))
    app.run(host="0.0.0.0", port=PORT, debug=True)
