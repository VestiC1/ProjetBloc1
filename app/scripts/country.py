import csv
import sys
from typing import List
from .crud import db_connect, db_close, add_country 

# Augmente la limite de taille des champs CSV pour "Geo Shape"
csv.field_size_limit(sys.maxsize)


def extract_data(row: List):
    """ Extraire les informations pertinentes de la ligne """
    
    # Vérifie que chaque ligne contient exactement 11 éléments
    assert len(row) == 11
    
    # Extrait et assigne les données pertinentes à partir de la ligne actuelle du CSV
    id_  = row[3]
    name = row[7]
    lat  = None
    long = None
    
    # Les territoires d'outre-mer autonomes ne disposent pas de coordonnées GPS
    # Vérifie si le champ des coordonnées GPS (index 10) n'est pas vide
    if len(row[10]) :
        # Si des coordonnées sont présentes, les diviser en latitude et longitude
        lat, long = row[10].split(', ')
    
    # Applique les contraintes de non-nullité SQL
    assert id_  is not None
    assert name is not None

    return id_, name, lat, long

def insert_country(conn, row:List):
    """ Insère les informations sur un pays dans la table Country """

    id_, name, lat, long = extract_data(row=row)
    print(f"Inserting id : {id_}, name : {name}, lat : {lat}, long = {long}")
    add_country(conn=conn, id=id_, name=name, lat=lat, long=long)

def inject_csv(conn, file : str ):
    """ Charger les informations pertinentes dans la base de données SQL """
    with open(file, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=';', quoting=csv.QUOTE_NONE)
        for i, row in enumerate(reader):
            if i == 0 : continue
            insert_country(conn=conn, row=row)

def main():
    file = "donnees/countries-codes.csv"
    
    conn = db_connect()
    inject_csv(conn = conn, file=file)
    db_close(conn)


if __name__ == "__main__": main()
