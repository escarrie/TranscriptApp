#!/bin/bash

# Vérifie si Python est installé
if ! command -v python3 &> /dev/null
then
    echo "Python n'est pas installé ou n'est pas dans le PATH."
    exit 1
fi

if [ -f env/bin/activate ]; then
    echo "L'environnement virtuel existe déjà."
else
    # Création d'un environnement virtuel nommé "env"
    echo "Création de l'environnement virtuel..."
    python3 -m venv env
fi

# Activation de l'environnement virtuel
echo "Activation de l'environnement virtuel..."
source env/bin/activate

# Installation des dépendances
if [ -f requirements_installed.txt ]; then
    echo "Les dépendances ont déjà été installées."
elif [ -f requirements.txt ]; then
    echo "Installation des packages depuis requirements.txt..."
    pip install -r requirements.txt
    echo "Les dépendances ont été installées avec succès." > requirements_installed.txt
else
    echo "Le fichier requirements.txt est introuvable. Aucune dépendance installée."
    exit 1
fi

python3 main.py