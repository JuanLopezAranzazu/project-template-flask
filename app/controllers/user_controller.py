from flask import abort
from argon2 import PasswordHasher
import models.user_model as user_model
import schemas.user_schema as user_schema
import config.db_config as db_config

db = db_config.db

# Para encriptar la contraseña
ph = PasswordHasher()

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

  # Encriptar la contraseña
  hashed_password = ph.hash(data['password'])

  new_user = user_model.User(
    name=data['name'],
    username=data['username'],
    email=data['email'],
    password=hashed_password
  )

  db.session.add(new_user)
  db.session.commit()

  return user_schema.user_schema.dump(new_user)

def update_user(id: int, data: dict):
  user_to_update = user_model.User.query.get(id)

  if not user_to_update:
    abort(404, description="User not found")

  # Encriptar la contraseña
  if 'password' in data:
    hashed_password = ph.hash(data['password'])
    user_to_update.password = hashed_password

  user_to_update.name = data['name']
  user_to_update.username = data['username']
  user_to_update.email = data['email']

  db.session.commit()

  return user_schema.user_schema.dump(user_to_update)

def delete_user(id: int):
  user = user_model.User.query.get(id)

  if not user:
    abort(404, description="User not found")

  db.session.delete(user)
  db.session.commit()
  return {"message": "User deleted successfully"}
