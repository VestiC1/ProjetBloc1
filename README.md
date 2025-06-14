# ProjetBloc1
Projet de certification pour ma formation de développeur en IA Bloc 1

# Creation de l'environnement virtuel sous Linux

## Création environnement virtuel
```bash
python3 -m venv .venv
```
## Activation de l'environnement virtuel
```bash
source .venv/bin/activate
```
## Installation librairies listées dans 'requirements.txt'
```bash
pip install -r requirements.txt
```

# Creation de l'environnement Virtuel sous windows

## Création de l'environnement virtuel
```bash
python -m venv .venv
```
## Activation de l'environnement virtuel
```bash
.venv\Scripts\activate.bat
```
## Installation des librairies listées dans 'requirements.txt'
```bash
pip install -r requirements.txt
```

# Creation des BDD :

## Configuration des BDD dans docker-compose.yml

## Démarrer les conteneurs :
```bash
docker compose up -d
```

## Vérifier les conteneurs :
```bash
docker ps
```

## Accéder aux bases de données :

### PostgreSQL :
```bash
docker exec -it pgvector psql -U postgres
```
### PostgreSQL :
```bash
docker exec -it mongodb mongosh -u admin -p admin00
```