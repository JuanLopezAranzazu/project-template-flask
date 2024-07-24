from flask import abort

# Función para validar la unicidad de un username
def validate_username_uniqueness(model, data):
  if 'username' in data:
    element = model.query.filter_by(username=data['username']).first()
    if element:
      abort(409, description="Username already exists")

