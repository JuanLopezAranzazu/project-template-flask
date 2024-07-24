from flask import Flask, jsonify, request
import services.service as service
import config.global_config as global_config
import config.db_config as db_config
# Importar modelos y esquemas
import models.user_model
import schemas.user_schema

config = global_config.config
db = db_config.db
ma = db_config.ma

# Crear la aplicación
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{config['db_user']}:{config['db_password']}@{config['db_host']}:{config['db_port']}/{config['db_name']}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializar la base de datos
db.init_app(app)
ma.init_app(app)

# Crear la base de datos
with app.app_context():
  db.create_all()

# Ruta principal
@app.route('/')
def home():
  return "Hello, World!"

@app.route('/data/<string:name>', methods=['GET'])
def get_data(name: str):
  return jsonify({"message": service.get_message(name)})


# Definiendo las rutas de la API
import routes.user_route as user_route
import routes.user_test_route as user_test_route

app.register_blueprint(user_route.user_bp)
app.register_blueprint(user_test_route.user_bp)

# Manejador de error para "Not Found"
@app.errorhandler(404)
def not_found(error):
  return jsonify({'error': 'Resource not found', 'message': str(error)}), 404

# Manejador de error para "Bad Request"
@app.errorhandler(400)
def bad_request(error):
  return jsonify({'error': 'Bad Request', 'message': str(error)}), 400

# Manejador de error para 409
@app.errorhandler(409)
def conflict(error):
  return jsonify({'error': 'Conflict', 'message': str(error)}), 409

# Manejador de error genérico para cualquier otro error
@app.errorhandler(Exception)
def handle_exception(error):
  return jsonify({'error': 'An unexpected error occurred', 'message': str(error)}), 500

if __name__ == '__main__':
  # Ejecutar la aplicación
  app.run(debug=True, port=config['port'])
