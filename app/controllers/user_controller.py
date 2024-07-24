from flask import abort
import models.user_model as user_model
import schemas.user_schema as user_schema
import config.db_config as db_config

db = db_config.db

# Controlador de usuario
def get_users():
  users = user_model.User.query.all()
  return user_schema.users_schema.dump(users)

def get_user(id: int):
  user = user_model.User.query.get(id)
  
  if not user:
    abort(404, description="User not found")

  return user_schema.user_schema.dump(user)

def create_user(data: dict):
  user = user_model.User.query.filter_by(username=data['username']).first()

  if user:
    abort(409, description="Username already exists")

  new_user = user_model.User(
    name=data['name'],
    username=data['username'],
    email=data['email'],
    password=data['password']
  )

  db.session.add(new_user)
  db.session.commit()

  return user_schema.user_schema.dump(new_user)

def update_user(id: int, data: dict):
  user_to_update = user_model.User.query.get(id)

  if not user_to_update:
    abort(404, description="User not found")

  user_to_update.name = data['name']
  user_to_update.username = data['username']
  user_to_update.email = data['email']
  user_to_update.password = data['password']

  db.session.commit()

  return user_schema.user_schema.dump(user_to_update)

def delete_user(id: int):
  user = user_model.User.query.get(id)

  if not user:
    abort(404, description="User not found")

  db.session.delete(user)
  db.session.commit()
  return {"message": "User deleted successfully"}
