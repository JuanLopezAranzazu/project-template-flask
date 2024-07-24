from flask import request, jsonify
from functools import wraps
from marshmallow import ValidationError

# Función para validar el request
def validate_request(schema):
  def decorator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
      try:
        data = request.get_json() # Obtener los datos del request
        schema().load(data)
      except ValidationError as err:
        return jsonify(err.messages), 400
      return f(*args, **kwargs)
    
    return decorated_function
  
  return decorator

