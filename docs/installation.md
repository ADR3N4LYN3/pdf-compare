# Guide d'installation - pdf-compare

Guide complet pour installer pdf-compare sur un nouveau poste Windows.

## Prérequis

- **Python 3.8 ou supérieur** (recommandé : Python 3.11+)
- **pip** (installé avec Python)
- **Git** (optionnel, pour cloner le repo)

### Vérifier Python

```powershell
# Vérifier si Python est installé
py --version
# ou
python --version

# Vérifier pip
py -m pip --version
```

Si Python n'est pas installé : [Télécharger Python](https://www.python.org/downloads/)

---

## Méthode 1 : Installation automatique (Recommandé)

### Étape 1 : Récupérer le code

**Option A : Avec Git**
```powershell
git clone https://github.com/ADR3N4LYN3/pdf-compare.git
cd pdf-compare
```

**Option B : Sans Git (ZIP)**
1. Télécharger le ZIP du projet
2. Extraire dans un dossier (ex: `C:\pdf-compare`)
3. Ouvrir PowerShell dans ce dossier

### Étape 2 : Installation automatique

```powershell
# Double-cliquer sur install.bat
# OU lancer dans PowerShell :
.\install.bat
```

L'installation fait automatiquement :
- ✅ Vérifie Python
- ✅ Met à jour pip
- ✅ Installe les dépendances
- ✅ Installe pdf-compare globalement

### Étape 3 : Vérifier l'installation

```powershell
# Vérifier la version
pdf-compare --version

# Afficher l'aide
pdf-compare --help
```

✅ **Installation terminée ! La commande fonctionne partout (PowerShell, CMD, etc.)**

---

## Méthode 2 : Installation manuelle

```powershell
cd pdf-compare

# Installer directement
pip install -r requirements.txt
pip install -e .

# Vérifier
pdf-compare --version
```

---


---

## Résolution des problèmes

### Erreur : "Python n'est pas reconnu"

```powershell
# Ajouter Python au PATH ou utiliser :
py -m pip install -r requirements.txt
```

### Erreur : "Module not found: numpy"

```powershell
pip install numpy
```

### Erreur : Caractères bizarres dans la sortie

```powershell
# Windows PowerShell - définir l'encodage UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

### Problème : Erreur de politique d'exécution PowerShell

```powershell
# Si vous avez une erreur lors de l'exécution de scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Mise à jour de l'application

```powershell
# Récupérer les dernières modifications (avec Git)
cd pdf-compare
git pull

# Réinstaller les dépendances si nécessaire
pip install -r requirements.txt --upgrade

# Réinstaller l'application
pip install -e .
```

---

## Désinstallation

```powershell
# Désinstaller le package Python
pip uninstall pdf-compare

# Nettoyer le cache pip (optionnel)
pip cache purge

# Supprimer le dossier du projet (optionnel)
```

---

## Installation sur d'autres systèmes

### Linux / macOS

```bash
# Créer venv
python3 -m venv venv

# Activer venv
source venv/bin/activate

# Installer
pip install -r requirements.txt
pip install -e .

# Vérifier
pdf-compare --version
```

---

## Variables d'environnement (optionnel)

Pour faciliter l'utilisation, vous pouvez ajouter Python Scripts au PATH :

```powershell
# Temporaire (pour la session actuelle)
$env:PATH += ";C:\chemin\vers\Python\Scripts"

# Permanent (via interface Windows)
# Panneau de configuration > Système > Paramètres système avancés > Variables d'environnement
```

**Note :** install.bat installe pdf-compare globalement, accessible depuis n'importe quel terminal.

---

## Support

En cas de problème :
1. Vérifier les prérequis (Python 3.8+)
2. Vérifier que pdf-compare est bien installé : `pdf-compare --version`
3. Consulter les logs d'erreur
4. Ouvrir une issue sur [GitHub](https://github.com/ADR3N4LYN3/pdf-compare/issues)
