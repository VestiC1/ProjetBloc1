import csv
import sys
from typing import List
from .crud import db_connect, db_close, add_country 

csv.field_size_limit(sys.maxsize)


def extract_data(row: List):
    """ Extract relevant informations from row"""
    
    # Make sure we get a 11 items list
    assert len(row) == 11
    
    # Pick up the relevant data
    id_  = row[3]
    name = row[7]
    lat  = None
    long = None
    
    # For Autonomous overseas teritorries 
    # no GPS coordinates are provided
    if len(row[10]) :
        lat, long = row[10].split(', ')
    
    # Enforces SQL non-nullity constraints
    assert id_  is not None
    assert name is not None

    return id_, name, lat, long

def insert_country(conn, row:List):
    """ Insert coountry information into the Country table. """

    id_, name, lat, long = extract_data(row=row)
    print(f"Inserting id : {id_}, name : {name}, lat : {lat}, long = {long}")
    add_country(conn=conn, id=id_, name=name, lat=lat, long=long)

def inject_csv(conn, file : str ):
    """ Load relevant information into SQL db. """
    with open(file, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=';', quoting=csv.QUOTE_NONE)
        for i, row in enumerate(reader):        # Skip header
            if i == 0 : continue
            insert_country(conn=conn, row=row)

def main():
    file = "donnees/countries-codes.csv"
    
    conn = db_connect()
    inject_csv(conn = conn, file=file)
    db_close(conn)


if __name__ == "__main__": main()
