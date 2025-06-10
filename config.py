import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Accéder aux variables d'environnement
db_config = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'name': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

mongo_config = {
    'host': os.getenv('MONGO_HOST'),
    'port': os.getenv('MONGO_PORT'),
    'dbname': os.getenv('MONGO_DBNAME'),
    'user': os.getenv('MONGO_USER'),
    'password': os.getenv('MONGO_PASSWORD')
}

print("PostgreSQL Configuration:", db_config)
print("MongoDB Configuration:", mongo_config)
