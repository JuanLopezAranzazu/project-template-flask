from datetime import datetime
import config.db_config as db_config

db = db_config.db

# Definir el modelo de usuario
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(80), nullable=False)
  username = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(120), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)

  def __init__(self, name, username, email, password):
    self.name = name
    self.username = username
    self.email = email
    self.password = password

