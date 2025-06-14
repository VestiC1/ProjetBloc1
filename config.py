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

# Configuration de l'API IGDB
igdb_config = {
    'client_id': os.getenv('IGDB_CLIENT_ID'),
    'client_secret': os.getenv('IGDB_CLIENT_SECRET')
}