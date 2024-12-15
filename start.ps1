#!/usr/bin/env pwsh

# Vérifie si Python est installé
if (-not (Get-Command python3 -ErrorAction SilentlyContinue)) {
    Write-Host "Python n'est pas installé ou n'est pas dans le PATH."
    exit 1
}

if (Test-Path env/bin/Activate) {
    Write-Host "L'environnement virtuel existe déjà."
} else {
    # Création d'un environnement virtuel nommé "env"
    Write-Host "Création de l'environnement virtuel..."
    python3 -m venv env
}

# Activation de l'environnement virtuel
Write-Host "Activation de l'environnement virtuel..."
& env/bin/Activate

# Installation des dépendances
if (Test-Path requirements_installed.txt) {
    Write-Host "Les dépendances ont déjà été installées."
} elseif (Test-Path requirements.txt) {
    Write-Host "Installation des packages depuis requirements.txt..."
    pip install -r requirements.txt
    "Les dépendances ont été installées avec succès." | Out-File -FilePath requirements_installed.txt
} else {
    Write-Host "Le fichier requirements.txt est introuvable. Aucune dépendance installée."
    exit 1
}

# Vérification des arguments
if ($args.Count -lt 3) {
    Write-Host "Usage: ./start.ps1 <file_path> <output_file> <model> [--with-time] [--with-speaker] [--remove-original-file]"
    exit 1
}

$file_path = $args[0]
$output_file = $args[1]
$model = $args[2]
$args = $args[3..$args.Length]

# Vérification de l'existence du fichier
if (-not (Test-Path $file_path)) {
    Write-Host "Le fichier $file_path n'existe pas."
    exit 1
}

# Vérification des options supplémentaires
$with_time = $false
$with_speaker = $false
$remove_original_file = $false
$interface = $false

foreach ($arg in $args) {
    switch ($arg) {
        "--with-time" { $with_time = $true }
        "--with-speaker" { $with_speaker = $true }
        "--remove-original-file" { $remove_original_file = $true }
        "--interface" { $interface = $true }
        default { $interface = $true }
    }
}

# Construction de la commande Python avec les options
$cmd = "python3 main.py `"$file_path`" `"$output_file`" `"$model`""

if ($with_time -and $with_speaker -and $remove_original_file) {
    $cmd += " --with-time --with-speaker --remove-original-file"
} elseif ($with_time -and $with_speaker) {
    $cmd += " --with-time --with-speaker"
} elseif ($with_time -and $remove_original_file) {
    $cmd += " --with-time --remove-original-file"
} elseif ($with_speaker -and $remove_original_file) {
    $cmd += " --with-speaker --remove-original-file"
} elseif ($with_time) {
    $cmd += " --with-time"
} elseif ($with_speaker) {
    $cmd += " --with-speaker"
} elseif ($remove_original_file) {
    $cmd += " --remove-original-file"
}

# Exécution de la commande
Invoke-Expression $cmd
