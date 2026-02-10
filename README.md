# Projet ETL – Pipeline de Données - GameTracker

## Description
Ce projet met en œuvre un pipeline **ETL (Extract, Transform, Load)** permettant
d’extraire des données brutes, de les transformer afin d’améliorer leur qualité,
puis de les charger dans une base de données **MySQL**.
Le projet est entièrement conteneurisé avec **Docker** afin d’assurer la
reproductibilité, la portabilité et la facilité de déploiement.

---

## Prérequis techniques
- Docker
- Docker Compose
- Python 3
- MySQL
- Système compatible Linux, macOS ou Windows

---

## Instructions de lancement

### Démarrage des services
Lancer les conteneurs Docker à partir du fichier `docker-compose.yml` :
``bash
docker compose up -d


### Vérification de l’état des services
docker compose ps
Le service MySQL doit être en état healthy avant de continuer.

### Accès au conteneur applicatif
docker compose exec app bash

### Test du script d’attente de la base de données
/app/scripts/wait-for-db.sh

### Initialisation des tables MySQL
mysql -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" < /app/scripts/init.sql

### Test des modules ETL individuellement
python extract.py
python transform.py
python load.py
Chaque module doit être testé séparément avant de passer au suivant.

Structure du projet
projet-etl/
│
├── docker-compose.yml        # Orchestration des services Docker
├── Dockerfile                # Image de l’application Python
├── README.md                 # Documentation du projet
│
├── src/
│   ├── extract.py            # Module d’extraction des données
│   ├── transform.py          # Module de transformation et nettoyage
│   ├── load.py               # Module de chargement en base de données
│   └── config.py             # Configuration via variables d’environnement
│
├── scripts/
│   ├── wait-for-db.sh        # Script d’attente de disponibilité MySQL
│   └── init.sql              # Script SQL d’initialisation des tables
│
├── data/
│   └── raw/                  # Données brutes
│
├── output/
│   └── processed/            # Données transformées
│
└── volumes/
    └── mysql_data/           # Volume Docker pour MySQL


Problèmes de qualité des données traités
Le module Transform permet de corriger plusieurs problèmes de qualité des
données, notamment :
    - Présence de valeurs manquantes
    - Doublons dans les données
    - Types de données incorrects
    - Formats incohérents (dates, chaînes de caractères)
    - Nettoyage des espaces et normalisation des valeurs

Ces traitements garantissent des données cohérentes et exploitables avant leur
chargement dans la base de données.

Nathan PUAUD
Projet réalisé dans le cadre du BUT Science des Données – Automatisation et Tests.