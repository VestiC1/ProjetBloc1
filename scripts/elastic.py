from elasticsearch import Elasticsearch
from config import elasticsearch_config
from pprint import pprint
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def elastic_health():
    try:
        es = Elasticsearch(
            [elasticsearch_config["url"]],
            basic_auth=(elasticsearch_config["username"], elasticsearch_config["password"]),
            verify_certs=elasticsearch_config["verify_certs"],
            ssl_show_warn=False # Désactive les avertissements SSL
        )
        health = es.cluster.health()
        print(f"Connected! Cluster status: {health['status']}")
    except Exception as e:
        print(f"Connection failed: {e}")

es = Elasticsearch(
    [elasticsearch_config["url"]],
    basic_auth=(elasticsearch_config["username"], elasticsearch_config["password"]),
    verify_certs=elasticsearch_config["verify_certs"],
    ssl_show_warn=False # Désactive les avertissements SSL
)

# Définir le mappage de l'index
index_mapping = {
    "mappings": {
        "properties": {
            "title": {"type": "text"},
            "summary": {"type": "text"},
            "storyline": {"type": "text"},
            "keywords": {"type": "keyword"},
        }
    }
}


def create_index(index_name, mapping):
    """Créer l'index"""
    try:
        if not es.indices.exists(index=index_name):
            es.indices.create(index=index_name, body=mapping)
            print(f"Index '{index_name}' created successfully.")
        else:
            print(f"Index '{index_name}' already exists.")
    except Exception as e:
        print(f"Error creating index: {e}")

# Vérifier si l'index existe
def check_index_exists(index_name):
    try:
        exists = es.indices.exists(index=index_name)
        if exists:
            print(f"Index '{index_name}' exists.")
        else:
            print(f"Index '{index_name}' does not exist.")
    except Exception as e:
        print(f"Error checking index: {e}")

# Obtenir des infos sur l'index
def get_index_info(index_name):
    try:
        info = es.indices.get(index=index_name)
        print(f"Info for index '{index_name}':")
        pprint(json.loads(str(info).replace("'", '"')))
    except Exception as e:
        print(f"Error getting index info: {e}")

def delete_index(index_name):
    try:
        if es.indices.exists(index=index_name):
            es.indices.delete(index=index_name)
            print(f"Index '{index_name}' and all its documents have been deleted.")
        else:
            print(f"Index '{index_name}' does not exist.")
    except Exception as e:
        print(f"Error deleting index: {e}")

# Création d'un Document
def create_document(index_name, _id, document, verbose=True):
    try:
        response = es.index(index=index_name, id=_id, document=document)
        if verbose :
            print(f"Document created: {response['_id']}")
        return response
    except Exception as e:
        print(f"Error creating document: {e}")
        return None

# Suppression d'un Document
def delete_document(index_name, document_id):
    try:
        response = es.delete(index=index_name, id=document_id)
        print(f"Document deleted: {response['_id']}")
        return response
    except Exception as e:
        print(f"Error deleting document: {e}")
        return None

# Affichage d'un Document
def get_document(index_name, document_id):
    try:
        response = es.get(index=index_name, id=document_id)
        print(f"Document retrieved: {response['_source']}")
        return response
    except Exception as e:
        print(f"Error retrieving document: {e}")
        return None

# Lister les Documents d'un Index
def list_documents(index_name):
    try:
        response = es.search(index=index_name, query={"match_all": {}}, size=500)
        print(f"Documents in index '{index_name}':")
        for i, hit in enumerate(response['hits']['hits']):
            print(i, hit['_id'],hit['_source'])
            print()
        return response
    except Exception as e:
        print(f"Error listing documents: {e}")
        return None
    
def count_documents(index_name):
    try:
        # Utiliser l'API de comptage pour obtenir le nombre de documents dans l'index
        count = es.count(index=index_name)['count']
        print(f"Number of documents in index '{index_name}': {count}")
        return count
    except Exception as e:
        print(f"Error counting documents: {e}")
        return None



if __name__ == "__main__":
    #create_index("games", index_mapping)
    #check_index_exists("games")
    #get_index_info("games")
    #delete_index("games")
    #count_documents("games")

    # Exemple de document
    game_document = {
        "title": "cuicui",
        "summary": "Un jeu d'aventure passionnant.",
        "storyline": "Un héros part à l'aventure pour sauver le monde.",
        "keywords": ["aventure", "action", "héros"]
    }

    # Créer un document
    #create_document("games", 1, game_document)

    # Lister les documents
    #list_documents("games")

    # Récupérer un document
    #get_document("games", 1)

    # Supprimer un document
    #delete_document("games", 1)

    # Status
    #elastic_health()