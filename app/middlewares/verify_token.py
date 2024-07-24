from flask import request, jsonify
from functools import wraps
from jose import jwt
import config.global_config as global_config

config = global_config.config

# Middleware para verificar el token de acceso
def verify_access_token(f):
  @wraps(f)
  def decorator(*args, **kwargs):
    token = None
        
    if 'Authorization' in request.headers:
      token = request.headers['Authorization'].split()[1]

    if not token:
      return jsonify({'message': 'Token not found!'}), 401

    try:
      payload = jwt.decode(token, config["secret_key"], algorithms=config["algorithm"])
      user_id = payload['user_id']
      request.user_id = user_id # Agregar el id del usuario a la petición
    except:
      return jsonify({'message': 'Token disabled!'}), 401

    return f(*args, **kwargs)

  return decorator

