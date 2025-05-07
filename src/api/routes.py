from flask import Blueprint, request, jsonify
from api.models import db, User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api = Blueprint('api', __name__)  # Creamos un blueprint llamado 'api'


@api.route('/hello', methods=['GET'])
def hello():
    return jsonify({"msg": "Servidor Flask activo 🚀"}), 200


# ===========================
# /signup - Registro de usuario
# ===========================


@api.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email y contraseña requeridos"}), 400

    existing_user = User.query.filter_by(
        email=email).first()  # corregido first()
    if existing_user:
        return jsonify({"error": "El usuario ya existe"}), 409

    new_user = User(email=email, password=password, is_active=True)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "Usuario registrado exitosamente"}), 201

# ===========================
# /login - Inicio de sesión
# ===========================


@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email, password=password).first()
    if not user:
        return jsonify({"error": "Email o contraseña inválidos"}), 401

    access_token = create_access_token(identity=user.id)  # corregido
    return jsonify({"token": access_token}), 200

# ===========================
# /private - Ruta protegida
# ===========================


@api.route('/private', methods=['GET'])
@jwt_required()  # Requiere token
def private():
    user_id = get_jwt_identity()  # corregido
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify({"msg": f"Hola {user.email}, esta es una ruta privada"}), 200
