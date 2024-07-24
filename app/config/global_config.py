from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Configuración de la aplicación
config={
  "env": os.getenv("FLASK_ENV", "development"),
  "port": int(os.getenv("PORT", 5000)),
  "secret_key": os.getenv("SECRET_KEY"),
  "access_token_expire_minutes": int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)),
  "db_user": os.getenv("DB_USER"),
  "db_password": os.getenv("DB_PASSWORD"),
  "db_host": os.getenv("DB_HOST"),
  "db_name": os.getenv("DB_NAME"),
  "db_port": int(os.getenv("DB_PORT")),
  "algorithm": os.getenv("ALGORITHM", "HS256"),
}
