@echo off
REM ========================================
REM Installation automatique de pdf-compare
REM ========================================

echo.
echo ========================================
echo   Installation de pdf-compare v1.0.0
echo ========================================
echo.

REM Verifier Python
python --version >nul 2>&1
if errorlevel 1 (
    py --version >nul 2>&1
    if errorlevel 1 (
        echo [ERREUR] Python n'est pas installe ou pas dans le PATH
        echo.
        echo Veuillez installer Python 3.8 ou superieur depuis :
        echo https://www.python.org/downloads/
        echo.
        pause
        exit /b 1
    )
    set PYTHON_CMD=py
) else (
    set PYTHON_CMD=python
)

echo [1/3] Python detecte
%PYTHON_CMD% --version
echo.

REM Mettre a jour pip
echo [2/3] Mise a jour de pip...
%PYTHON_CMD% -m pip install --upgrade pip --quiet
echo [OK] pip mis a jour
echo.

REM Installer les dependances et pdf-compare
echo [3/3] Installation de pdf-compare et dependances...
echo Cela peut prendre quelques minutes...
echo.
%PYTHON_CMD% -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERREUR] Echec de l'installation des dependances
    pause
    exit /b 1
)
echo.
%PYTHON_CMD% -m pip install -e .
if errorlevel 1 (
    echo [ERREUR] Echec de l'installation de pdf-compare
    pause
    exit /b 1
)
echo.
echo [OK] Installation terminee
echo.

REM Verifier l'installation
echo Verification de l'installation...
pdf-compare --version
if errorlevel 1 (
    echo.
    echo [ATTENTION] pdf-compare n'est pas accessible directement
    echo Utilisez : python -m pdf_compare.cli au lieu de pdf-compare
    echo.
    echo OU redemarrez votre terminal pour actualiser le PATH
    echo.
) else (
    echo [OK] pdf-compare est pret a l'emploi
    echo.
)

echo ========================================
echo   Installation terminee avec succes !
echo ========================================
echo.
echo Utilisation :
echo   pdf-compare fichier1.pdf fichier2.pdf
echo.
echo Si la commande pdf-compare ne fonctionne pas :
echo   python -m pdf_compare.cli fichier1.pdf fichier2.pdf
echo.
echo Pour tester l'installation :
echo   python create_test_pdfs.py
echo   test_suite.bat
echo.
echo Documentation disponible :
echo   - README.md - Documentation complete
echo   - docs\installation.md - Guide d'installation
echo   - docs\examples.md - Exemples d'utilisation
echo   - docs\testing.md - Guide de tests
echo.
echo La commande pdf-compare est maintenant disponible
echo dans PowerShell, CMD et tous les terminaux !
echo.
pause
