from datetime import datetime, timedelta
from jose import jwt
import config.global_config as global_config

config = global_config.config

# Función para generar un token de acceso
def create_access_token(data):
  to_encode = data.copy()

  expire = datetime.utcnow() + timedelta(minutes=config["access_token_expire_minutes"])
  to_encode.update({"exp": expire})

  encoded_jwt = jwt.encode(to_encode, config["secret_key"], algorithm=config["algorithm"])

  return encoded_jwt