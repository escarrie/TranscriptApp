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

# Vérification des arguments
if [ "$#" -lt 3 ]; then
    echo "Usage: ./start.sh <file_path> <output_file> <model> [--with-time] [--with-speaker] [--remove-original-file]"
    exit 1
fi

file_path=$1
output_file=$2
model=$3
shift 3

# Vérification de l'existence du fichier
if [ ! -f "$file_path" ]; then
    echo "Le fichier $file_path n'existe pas."
    exit 1
fi

# Vérification des options supplémentaires
with_time=false
with_speaker=false
remove_original_file=false

for arg in "$@"; do
    case $arg in
        --with-time)
            with_time=true
            ;;
        --with-speaker)
            with_speaker=true
            ;;
        --remove-original-file)
            remove_original_file=true
            ;;
    esac
done

# Construction de la commande Python avec les options
cmd="python3 main.py \"$file_path\" \"$output_file\" \"$model\""

if $with_time && $with_speaker && $remove_original_file; then
    cmd="$cmd --with-time --with-speaker --remove-original-file"
elif $with_time && $with_speaker; then
    cmd="$cmd --with-time --with-speaker"
elif $with_time && $remove_original_file; then
    cmd="$cmd -with-time --remove-original-file"
elif $with_speaker && $remove_original_file; then
    cmd="$cmd --with-speaker --remove-original-file"
elif $with_time; then
    cmd="$cmd --with-time"
elif $with_speaker; then
    cmd="$cmd --with-speaker"
elif $remove_original_file; then
    cmd="$cmd --remove-original-file"
fi

# Exécution de la commande
eval $cmd
