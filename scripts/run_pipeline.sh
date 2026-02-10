#!/bin/bash
set -e

echo "=== GAMETRACKER PIPELINE ==="

#Attente de la base de données
./scripts/wait-for-db.sh

#Initialisation de la base de données
echo "[AUTO] Initialisation des tables..."
mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" --skip-ssl "$DB_NAME" < scripts/init-db.sql

#Lancement de Python
echo "[AUTO] Lancement du traitement Python (ETL)..."
python3 -m src.main

echo "[AUTO] Création du rapport de synthèse..."
python3 -m src.report

