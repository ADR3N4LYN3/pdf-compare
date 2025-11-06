# Guide de tests - pdf-compare

Toutes les commandes nécessaires pour tester l'application pdf-compare.

---

## 🚀 Tests rapides automatisés

### Windows

```powershell
# Activer le venv
.\venv\Scripts\activate

# Lancer la suite de tests
.\test_suite.bat
```

### Linux / macOS

```bash
# Activer le venv
source venv/bin/activate

# Créer les PDFs de test
python create_test_pdfs.py

# Lancer les tests manuellement (voir ci-dessous)
```

---

## 📋 Tests manuels - Commandes détaillées

### Préparation

```powershell
# Activer le venv
.\venv\Scripts\activate

# Créer les PDFs de test
python create_test_pdfs.py

# Créer le dossier de sortie
mkdir test_output
```

---

## Test 1️⃣ : Vérification de l'installation

```powershell
# Vérifier la version
pdf-compare --version

# Afficher l'aide
pdf-compare --help
```

**Résultat attendu :**
```
pdf-compare, version 1.0.0
```

---

## Test 2️⃣ : PDFs identiques

```powershell
# Comparaison simple
pdf-compare test_pdf1.pdf test_pdf1_copy.pdf
```

**Résultat attendu :**
- Message : `[OK] PDFs are IDENTICAL`
- Similarité : `100.00%`
- Code de sortie : `0`

**Vérifier le code de sortie :**
```powershell
pdf-compare test_pdf1.pdf test_pdf1_copy.pdf
echo $LASTEXITCODE  # PowerShell
# ou
echo %ERRORLEVEL%   # CMD
```

---

## Test 3️⃣ : PDFs différents

```powershell
# Comparaison simple
pdf-compare test_pdf1.pdf test_pdf2.pdf
```

**Résultat attendu :**
- Message : `[WARNING] PDFs are DIFFERENT`
- Similarité : environ `99%`
- Pages différentes : `1`
- Code de sortie : `1`

---

## Test 4️⃣ : Mode verbeux

```powershell
# Afficher les statistiques détaillées
pdf-compare test_pdf1.pdf test_pdf2.pdf --verbose
```

**Résultat attendu :**
```
Detailed Per-Page Statistics:
  Page 1:
    Similarity: 98.23%
    Different Pixels: 111,945 / 6,311,250
    Difference Regions: 12
```

---

## Test 5️⃣ : Rapport PDF avec différences

```powershell
# Générer un PDF annoté
pdf-compare test_pdf1.pdf test_pdf2.pdf --output-diff test_output\diff.pdf

# Ouvrir le PDF généré
start test_output\diff.pdf
```

**Résultat attendu :**
- Fichier créé : `test_output\diff.pdf`
- Contenu : Page de résumé + pages annotées avec différences en rouge

---

## Test 6️⃣ : Rapport JSON

```powershell
# Générer les statistiques JSON
pdf-compare test_pdf1.pdf test_pdf2.pdf --output-json test_output\stats.json

# Afficher le contenu
cat test_output\stats.json
# ou
type test_output\stats.json
```

**Résultat attendu :**
- Fichier JSON valide
- Contient : `overall_similarity`, `page_stats`, `difference_regions`

---

## Test 7️⃣ : Rapport HTML

```powershell
# Générer un rapport HTML interactif
pdf-compare test_pdf1.pdf test_pdf2.pdf --output-html test_output\report.html

# Ouvrir dans le navigateur
start test_output\report.html
```

**Résultat attendu :**
- Page HTML responsive
- Graphiques et statistiques colorés
- Images des différences intégrées

---

## Test 8️⃣ : Export des images

```powershell
# Exporter les images de différences
pdf-compare test_pdf1.pdf test_pdf2.pdf --output-images test_output\images

# Lister les images
dir test_output\images
```

**Résultat attendu :**
- Dossier créé : `test_output\images`
- Fichiers : `diff_page_001.png`, `diff_page_002.png`

---

## Test 9️⃣ : Résumé texte

```powershell
# Générer un résumé texte
pdf-compare test_pdf1.pdf test_pdf2.pdf --output-text test_output\summary.txt

# Afficher le contenu
cat test_output\summary.txt
# ou
type test_output\summary.txt
```

**Résultat attendu :**
- Fichier texte avec statistiques formatées
- Facile à lire en console

---

## Test 🔟 : Toutes les sorties en une fois

```powershell
pdf-compare test_pdf1.pdf test_pdf2.pdf \
  --output-diff test_output\complete_diff.pdf \
  --output-json test_output\complete_stats.json \
  --output-html test_output\complete_report.html \
  --output-images test_output\complete_images \
  --output-text test_output\complete_summary.txt \
  --verbose
```

**Résultat attendu :**
- 5 sorties générées
- Message de confirmation pour chaque fichier

---

## Test 1️⃣1️⃣ : DPI personnalisé

```powershell
# Haute résolution (meilleure qualité, plus lent)
pdf-compare test_pdf1.pdf test_pdf2.pdf --dpi 300 --output-diff test_output\high_res.pdf

# Basse résolution (rapide)
pdf-compare test_pdf1.pdf test_pdf2.pdf --dpi 72 --output-diff test_output\low_res.pdf
```

**Résultat attendu :**
- DPI 300 : Fichier plus gros, meilleure qualité
- DPI 72 : Fichier plus petit, traitement rapide

---

## Test 1️⃣2️⃣ : Seuil de tolérance

```powershell
# Comparaison stricte (défaut)
pdf-compare test_pdf1.pdf test_pdf2.pdf --threshold 0

# Ignorer petites différences
pdf-compare test_pdf1.pdf test_pdf2.pdf --threshold 10

# Tolérance élevée
pdf-compare test_pdf1.pdf test_pdf2.pdf --threshold 50
```

**Résultat attendu :**
- Threshold 0 : Détecte toutes les différences
- Threshold plus élevé : Moins de différences détectées

---

## Test 1️⃣3️⃣ : Mode silencieux

```powershell
# Seulement le code de sortie
pdf-compare test_pdf1.pdf test_pdf2.pdf --quiet
echo $LASTEXITCODE
```

**Résultat attendu :**
- Aucune sortie console
- Seulement code de sortie (0 ou 1)

---

## Test 1️⃣4️⃣ : Sans barre de progression

```powershell
# Désactiver la barre de progression
pdf-compare test_pdf1.pdf test_pdf2.pdf --no-progress
```

**Résultat attendu :**
- Pas de barre de progression animée
- Utile pour les logs

---

## Test 1️⃣5️⃣ : Tests unitaires

```powershell
# Installer pytest si nécessaire
pip install pytest

# Lancer tous les tests
pytest

# Tests avec verbosité
pytest -v

# Tests avec couverture
pip install pytest-cov
pytest --cov=pdf_compare --cov-report=html
```

**Résultat attendu :**
```
===== 18 passed, 5 warnings in 0.20s =====
```

---

## Test 1️⃣6️⃣ : Fichiers inexistants

```powershell
# Tester avec fichier inexistant
pdf-compare inexistant1.pdf inexistant2.pdf
```

**Résultat attendu :**
- Message d'erreur clair
- Code de sortie : `2`

---

## Test 1️⃣7️⃣ : PDFs avec différents nombres de pages

Créer un script `create_multipage.py` :

```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# PDF avec 3 pages
c = canvas.Canvas("test_3pages.pdf", pagesize=letter)
for i in range(3):
    c.drawString(100, 700, f"Page {i+1}")
    c.showPage()
c.save()

# PDF avec 5 pages
c = canvas.Canvas("test_5pages.pdf", pagesize=letter)
for i in range(5):
    c.drawString(100, 700, f"Page {i+1}")
    c.showPage()
c.save()
```

Puis tester :

```powershell
python create_multipage.py
pdf-compare test_3pages.pdf test_5pages.pdf --verbose
```

**Résultat attendu :**
- Compare les 3 premières pages
- Signale que test_5pages.pdf a 2 pages supplémentaires

---

## 🔄 Tests en boucle / Batch

### PowerShell - Comparer plusieurs fichiers

```powershell
$reference = "test_pdf1.pdf"
$files = @("test_pdf2.pdf", "test_pdf1_copy.pdf")

foreach ($file in $files) {
    Write-Host "`n=== Comparing $file ===" -ForegroundColor Cyan
    pdf-compare $reference $file --output-json "test_output\$($file -replace '\.pdf$', '.json')"
}
```

### CMD - Comparer tous les PDFs d'un dossier

```batch
for %%f in (*.pdf) do (
    if not "%%f"=="reference.pdf" (
        pdf-compare reference.pdf "%%f" --output-json "results\%%~nf.json"
    )
)
```

---

## 📊 Vérification des résultats

### Vérifier les fichiers générés

```powershell
# Lister tous les fichiers de sortie
dir test_output

# Taille des fichiers
dir test_output | Format-Table Name, Length

# Compter les fichiers
(Get-ChildItem test_output).Count
```

### Valider le JSON

```powershell
# Avec Python
python -c "import json; print(json.load(open('test_output/stats.json')))"

# Avec PowerShell
Get-Content test_output\stats.json | ConvertFrom-Json
```

---

## 🧹 Nettoyage après tests

```powershell
# Supprimer les fichiers de test
Remove-Item test_*.pdf
Remove-Item -Recurse test_output

# Ou avec CMD
del test_*.pdf
rmdir /s /q test_output
```

---

## ⚡ Commandes rapides à copier-coller

### Test complet rapide

```powershell
# Tout en une commande
.\venv\Scripts\activate && python create_test_pdfs.py && pdf-compare test_pdf1.pdf test_pdf2.pdf --output-html test_output\report.html --verbose && start test_output\report.html
```

### Comparaison + ouverture des résultats

```powershell
pdf-compare test_pdf1.pdf test_pdf2.pdf --output-diff out.pdf --output-html out.html && start out.pdf && start out.html
```

---

## 📝 Résumé des codes de sortie

| Code | Signification | Action |
|------|---------------|--------|
| `0` | PDFs identiques | Tout va bien |
| `1` | PDFs différents | Différences détectées (normal) |
| `2` | Erreur | Vérifier les fichiers/paramètres |

---

## 🐛 Debug

### Mode verbeux + sans barre de progression

```powershell
pdf-compare test_pdf1.pdf test_pdf2.pdf --verbose --no-progress 2>&1 | Tee-Object debug.log
```

### Exécuter avec Python directement

```powershell
python -m pdf_compare.cli test_pdf1.pdf test_pdf2.pdf --verbose
```

---

## ✅ Checklist de tests

- [ ] Installation vérifiée (`pdf-compare --version`)
- [ ] PDFs de test créés
- [ ] Comparaison PDFs identiques (exit code 0)
- [ ] Comparaison PDFs différents (exit code 1)
- [ ] Rapport PDF généré et consultable
- [ ] Rapport JSON valide
- [ ] Rapport HTML fonctionnel
- [ ] Export images réussi
- [ ] Mode verbeux affiche les détails
- [ ] Tests unitaires passent (18/18)

---

**Tous les tests passent ? L'application est prête ! 🎉**
