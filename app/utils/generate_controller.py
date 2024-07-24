from flask import abort
import config.db_config as db_config

db = db_config.db

# Controlador general para realizar operaciones CRUD

"""
  Función para obtener todos los elementos de un modelo
  model: Modelo de la base de datos
  schema: Esquema de serialización
"""
def get_elements(model, schema):
  elements = model.query.all()
  return schema.dump(elements)

"""
  Función para obtener un elemento de un modelo
  model: Modelo de la base de datos
  schema: Esquema de serialización
  id: ID del elemento a obtener
"""
def get_element(model, schema, id: int):
  element = model.query.get(id)

  if not element:
    abort(404, description=f"{model.__name__} not found")

  return schema.dump(element)

"""
  Función para crear un elemento en la base de datos
  model: Modelo de la base de datos
  schema: Esquema de serialización
  data: Datos a insertar
  validation_functions: Funciones de validación a ejecutar
"""
def create_element(model, schema, data: dict, validation_functions=[]):
  # Ejecutar todas las funciones de validación pasadas

  print(validation_functions,data)
  for validate in validation_functions:
    validate(model, data)

  new_element = model(**data)

  db.session.add(new_element)
  db.session.commit()

  return schema.dump(new_element)

"""
  Función para actualizar un elemento en la base de datos
  model: Modelo de la base de datos
  schema: Esquema de serialización
  id: ID del elemento a actualizar
  data: Datos a actualizar
  validation_functions: Funciones de validación a ejecutar
"""
def update_element(model, schema, id: int, data: dict, validation_functions=[]):
  element_to_update = model.query.get(id)

  if not element_to_update:
    abort(404, description=f"{model.__name__} not found")

  # Ejecutar todas las funciones de validación pasadas
  for validate in validation_functions:
    validate(model, data)

  for key, value in data.items():
    setattr(element_to_update, key, value)

  db.session.commit()

  return schema.dump(element_to_update)

"""
  Función para eliminar un elemento de la base de datos
  model: Modelo de la base de datos
  id: ID del elemento a eliminar
"""
def delete_element(model, id: int):
  element = model.query.get(id)

  if not element:
    abort(404, description=f"{model.__name__} not found")

  db.session.delete(element)
  db.session.commit()

