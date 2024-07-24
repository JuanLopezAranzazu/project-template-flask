from flask import Blueprint, jsonify, request
from argon2 import PasswordHasher
import models.user_model as user_model
import schemas.user_schema as user_schema
import utils.generate_token as generate_token
import config.db_config as db_config
# middlewares
import middlewares.verify_token as verify_token

db = db_config.db
create_access_token = generate_token.create_access_token
verify_access_token = verify_token.verify_access_token

# Crear un Blueprint para las rutas de usuarios
NAME = "auth"

auth_bp = Blueprint(NAME, __name__)
prefix = f"/{NAME}"
# Para encriptar la contraseña
ph = PasswordHasher()

@auth_bp.route(f'{prefix}/login', methods=['POST'])
def login():
  data = request.get_json()

  user = user_model.User.query.filter_by(username=data['username']).first()

  if not user:
    return jsonify({'message': 'User not found'}), 404

  if not ph.verify(user.password, data["password"]):
    return jsonify({'message': 'Invalid credentials'}), 401
  
  access_token = create_access_token(data={"user_id": user.id})

  return jsonify({"access_token": access_token})

@auth_bp.route(f'{prefix}/register', methods=['POST'])
def register():
  data = request.get_json()

  user = user_model.User.query.filter_by(username=data['username']).first()

  if user:
    return jsonify({'message': 'Username already exists'}), 400

  new_user = user_model.User(**data)
  new_user.password = ph.hash(data['password'])


  db.session.add(new_user)
  db.session.commit()

  return jsonify(user_schema.user_schema.dump(new_user)), 201

@auth_bp.route(f'{prefix}/me', methods=['GET'])
@verify_access_token
def me():
  user_id = request.user_id # obtenemos el id del usuario desde el token
  user = user_model.User.query.get(user_id)

  if not user:
    return jsonify({'message': 'User not found'}), 404

  return jsonify(user_schema.user_schema.dump(user))
