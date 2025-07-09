# Projet VestimLib

Projet de certification pour ma formation de développeur en IA Bloc 1.

## Environnement Virtuel

### Sous Linux

#### Création de l'environnement virtuel
```bash
python3 -m venv .venv
```

#### Activation de l'environnement virtuel
```bash
source .venv/bin/activate
```

#### Installation des librairies
```bash
pip install -r requirements.txt
```

### Sous Windows

#### Création de l'environnement virtuel
```bash
python -m venv .venv
```

#### Activation de l'environnement virtuel
```bash
.venv\Scripts\activate.bat
```

#### Installation des librairies
```bash
pip install -r requirements.txt
```

## Configuration et Gestion des Bases de Données

### Configuration avec Docker Compose

Le fichier `docker-compose.yml` est utilisé pour configurer et lancer les services PostgreSQL et Elasticsearch.

#### Elasticsearch
Créer manuellement le dossier `elk_data` pour le volume.

#### Démarrer les conteneurs
```bash
docker compose up -d
```

#### Vérifier les conteneurs
```bash
docker ps
```

### Accès aux Bases de Données

#### PostgreSQL et Elasticsearch
```bash
lazydocker
```

## Lancement de l'API avec FAST API
Une fois dans le dossier App :
```bash
python3 main.py
```

## Extraction des Données

Ce projet utilise plusieurs sources de données, notamment une API externe, un fichier CSV et une bases de données relationnelle et non relationnelle. Voici comment les données sont extraites et traitées :

- **Sélection** : Les données sont sélectionnées en utilisant des requêtes SQL pour PostgreSQL et des requêtes spécifiques pour Elasticsearch.
- **Filtrage** : Les données sont filtrées pour ne récupérer que les informations pertinentes pour le projet.
- **Jointure** : Les jointures SQL sont utilisées pour combiner les données de différentes tables dans PostgreSQL.
- **Optimisations** : Les requêtes sont optimisées pour améliorer les performances, notamment en utilisant des index et en limitant les résultats avec la pagination.

## Agrégation des Données

Les données issues de différentes sources sont agrégées pour créer un jeu de données unique et cohérent. Voici les étapes principales :

- **Dépendances** : Les scripts Python utilisent des bibliothèques comme SQLAlchemy et Elasticsearch pour interagir avec les bases de données.
- **Nettoyage** : Les données sont nettoyées pour supprimer les entrées corrompues et gérer les valeurs manquantes.
- **Homogénéisation** : Les formats des données sont homogénéisés pour assurer la cohérence et la compatibilité.

## Création de la Base de Données

La base de données est créée en utilisant PostgreSQL pour les données relationnelles et Elasticsearch pour les données non structurées.

### PostgreSQL

- **Image Docker** : `pgvector/pg17`
- **Configuration** : La base de données PostgreSQL est configurée avec un mot de passe défini dans les variables d'environnement et est exposée sur le port `5432`.
- **Volumes** : Les données sont persistées dans un volume Docker pour assurer la durabilité des données.

### Elasticsearch

- **Image Docker** : `elasticsearch:9.0.2`
- **Configuration** : Elasticsearch est configuré en tant que nœud unique avec des paramètres de mémoire définis pour optimiser les performances. Il est exposé sur le port `9200`.
- **Volumes** : Les données Elasticsearch sont également persistées dans un volume Docker.

### Scripts d'Automatisation

Les scripts Python sont utilisés pour automatiser la création et le remplissage des bases de données. Ces scripts utilisent SQLAlchemy pour interagir avec PostgreSQL et la bibliothèque Elasticsearch pour interagir avec Elasticsearch.

- **Exécution des Scripts** : Les scripts peuvent être exécutés en utilisant des commandes spécifiques pour initialiser et remplir les bases de données. Un script principal est en cours de développement pour automatiser l'ensemble du processus.

### Conformité RGPD

Les données sont traitées en conformité avec le RGPD pour assurer la protection des informations personnelles. Les scripts et les configurations de la base de données sont conçus pour respecter les réglementations en vigueur.

## API

L'API est développée en utilisant FastAPI et est documentée avec le Swagger.

- **Points de Terminaison** : L'API offre plusieurs points de terminaison pour accéder aux données des jeux vidéo.
- **Règles d'Authentification** : Les points de terminaison sont sécurisés avec une authentification JWT.

Pour plus de détails, consultez les docstrings dans le code source et la documentation Swagger de l'API.
