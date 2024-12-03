# Vérifie si Python est installé
try {
    python3 --version
} catch {
    Write-Host "Python n'est pas installé ou n'est pas dans le PATH."
    exit 1
}

# Création d'un environnement virtuel nommé "env"
Write-Host "Création de l'environnement virtuel..."
python3 -m venv env

if (Test-Path "env\Scripts\Activate.ps1") {
    Write-Host "L'environnement virtuel a été créé avec succès."
} else {
    # Activation de l'environnement virtuel
    Write-Host "Activation de l'environnement virtuel..."
    & "env\Scripts\Activate.ps1"
}

# Installation des dépendances
if (Test-Path "requirements_installed.txt") {
    Write-Host "Les dépendances ont déjà été installées."
} elseif (Test-Path "requirements.txt") {
    Write-Host "Installation des packages depuis requirements.txt..."
    & "env\Scripts\pip.exe" install -r requirements.txt
    "Les dépendances ont été installées avec succès." | Out-File -FilePath requirements_installed.txt
} else {
    Write-Host "Le fichier requirements.txt est introuvable. Aucune dépendance installée."
    exit 1
}

& "env\Scripts\Activate.ps1"
