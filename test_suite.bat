@echo off
REM ========================================
REM Suite de tests complete pour pdf-compare
REM ========================================

echo.
echo ========================================
echo Suite de tests pdf-compare
echo ========================================
echo.

REM Verifier que pdf-compare est installe
where pdf-compare >nul 2>&1
if errorlevel 1 (
    echo ERREUR: pdf-compare n'est pas installe
    echo Veuillez executer install.bat d'abord
    pause
    exit /b 1
)

REM Creer le dossier de sortie pour les tests
if not exist "test_output" mkdir test_output

echo.
echo [1/8] Creation des PDFs de test...
python create_test_pdfs.py
if errorlevel 1 (
    echo ERREUR: Echec de creation des PDFs de test
    pause
    exit /b 1
)

echo.
echo [2/8] Test 1: Comparaison de PDFs identiques
echo ========================================
pdf-compare test_pdf1.pdf test_pdf1_copy.pdf
set TEST1_RESULT=%ERRORLEVEL%
echo Code de sortie: %TEST1_RESULT%
if %TEST1_RESULT% equ 0 (
    echo [OK] PDFs detectes comme identiques
) else (
    echo [ERREUR] PDFs identiques non detectes
)

echo.
echo [3/8] Test 2: Comparaison de PDFs differents
echo ========================================
pdf-compare test_pdf1.pdf test_pdf2.pdf
set TEST2_RESULT=%ERRORLEVEL%
echo Code de sortie: %TEST2_RESULT%
if %TEST2_RESULT% equ 1 (
    echo [OK] Differences detectees
) else (
    echo [ERREUR] Differences non detectees
)

echo.
echo [4/8] Test 3: Mode verbeux avec statistiques
echo ========================================
pdf-compare test_pdf1.pdf test_pdf2.pdf --verbose

echo.
echo [5/8] Test 4: Generation de rapport PDF
echo ========================================
pdf-compare test_pdf1.pdf test_pdf2.pdf --output-diff test_output\diff_report.pdf
if exist "test_output\diff_report.pdf" (
    echo [OK] Rapport PDF genere
) else (
    echo [ERREUR] Rapport PDF non genere
)

echo.
echo [6/8] Test 5: Generation de rapport JSON
echo ========================================
pdf-compare test_pdf1.pdf test_pdf2.pdf --output-json test_output\stats.json
if exist "test_output\stats.json" (
    echo [OK] Rapport JSON genere
    echo Contenu du JSON:
    type test_output\stats.json
) else (
    echo [ERREUR] Rapport JSON non genere
)

echo.
echo [7/8] Test 6: Generation de rapport HTML
echo ========================================
pdf-compare test_pdf1.pdf test_pdf2.pdf --output-html test_output\report.html
if exist "test_output\report.html" (
    echo [OK] Rapport HTML genere
    echo Pour visualiser: start test_output\report.html
) else (
    echo [ERREUR] Rapport HTML non genere
)

echo.
echo [8/8] Test 7: Generation de toutes les sorties
echo ========================================
pdf-compare test_pdf1.pdf test_pdf2.pdf ^
  --output-diff test_output\complete_diff.pdf ^
  --output-json test_output\complete_stats.json ^
  --output-html test_output\complete_report.html ^
  --output-images test_output\images ^
  --output-text test_output\summary.txt ^
  --verbose

echo.
echo ========================================
echo Resume des tests
echo ========================================
echo.

if exist "test_output\diff_report.pdf" echo [OK] Rapport PDF
if exist "test_output\stats.json" echo [OK] Rapport JSON
if exist "test_output\report.html" echo [OK] Rapport HTML
if exist "test_output\complete_diff.pdf" echo [OK] Rapport PDF complet
if exist "test_output\complete_stats.json" echo [OK] Stats JSON completes
if exist "test_output\complete_report.html" echo [OK] Rapport HTML complet
if exist "test_output\images" echo [OK] Images de differences
if exist "test_output\summary.txt" echo [OK] Resume texte

echo.
echo Fichiers generes dans: test_output\
echo.

REM Lister tous les fichiers crees
echo Fichiers de sortie:
dir /B test_output

echo.
echo ========================================
echo Tests termines !
echo ========================================
echo.
echo Pour visualiser les rapports:
echo   - PDF: test_output\complete_diff.pdf
echo   - HTML: test_output\complete_report.html
echo   - JSON: test_output\complete_stats.json
echo   - Texte: test_output\summary.txt
echo.
pause
