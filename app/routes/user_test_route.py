from flask import Blueprint, request, jsonify
import controllers.user_test_controller as user_test_controller
import middlewares.validator_handler as validator_handler
import schemas.user_schema as user_schema

validate_request = validator_handler.validate_request

# Crear un Blueprint para las rutas de usuarios
NAME = "user_test"

user_bp = Blueprint(NAME, __name__)
prefix = f"/{NAME}"

@user_bp.route(prefix, methods=["GET"])
def get_users():
  return jsonify(user_test_controller.get_users())

@user_bp.route(f"{prefix}/<int:id>", methods=["GET"])
def get_user(id: int):
  return jsonify(user_test_controller.get_user(id))

@user_bp.route(prefix, methods=["POST"])
@validate_request(user_schema.UserSchema)
def create_user():
  data = request.get_json()
  user = user_test_controller.create_user(data)
  return jsonify(user), 201

@user_bp.route(f"{prefix}/<int:id>", methods=["PUT"])
@validate_request(user_schema.UserSchema)
def update_user(id: int):
  data = request.get_json()
  user = user_test_controller.update_user(id, data)
  return jsonify(user)

@user_bp.route(f"{prefix}/<int:id>", methods=["DELETE"])
def delete_user(id: int):
  return jsonify(user_test_controller.delete_user(id))

