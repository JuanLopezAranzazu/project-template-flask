import models.user_model as user_model
import schemas.user_schema as user_schema
import utils.generate_controller as generate_controller
import utils.helpers as helpers

def get_users():
  return generate_controller.get_elements(user_model.User, user_schema.users_schema)

def get_user(id: int):
  return generate_controller.get_element(user_model.User, user_schema.user_schema, id)

def create_user(data: dict):
  return generate_controller.create_element(
    user_model.User,
    user_schema.user_schema,
    data,
    [helpers.validate_username_uniqueness] # Funciones de validación
  )

def update_user(id: int, data: dict):
  return generate_controller.update_element(
    user_model.User,
    user_schema.user_schema,
    id,
    data,
    [helpers.validate_username_uniqueness] # Funciones de validación
  )

def delete_user(id: int):
  return generate_controller.delete_element(user_model.User, id)
