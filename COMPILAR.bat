@echo off
cd /d "%~dp0"
echo ==========================================
echo FORCANDO O AMBIENTE VIRTUAL
echo ==========================================

:: Definir caminho absoluto para o Python do projeto
set "PROJ_DIR=%~dp0"
set "VENV_PYTHON=%PROJ_DIR%.venv\Scripts\python.exe"

:: Verificar se o Python existe na pasta .venv
if not exist "%VENV_PYTHON%" (
    echo [ERRO] Nao encontrei o Python na pasta .venv!
    echo Caminho procurado: "%VENV_PYTHON%"
    echo.
    echo Certifique-se de que a pasta .venv esta no mesmo local deste arquivo.
    pause
    exit /b
)

echo [INFO] Python encontrado: "%VENV_PYTHON%"
echo.
echo [1/3] Instalando PyInstaller...
"%VENV_PYTHON%" -m pip install pyinstaller

echo.
echo [2/3] Compilando executavel...
"%VENV_PYTHON%" -m PyInstaller --clean --noconfirm --onefile --windowed --name "MudaeOrganizador" organizador.py

echo.
echo [3/3] Limpando arquivos temporarios...
if exist "dist\MudaeOrganizador.exe" (
    move /Y "dist\MudaeOrganizador.exe" "MudaeOrganizador.exe" >nul
    rmdir /s /q build
    rmdir /s /q dist
    del /q MudaeOrganizador.spec
    echo.
    echo [SUCESSO] Executavel criado com sucesso!
) else (
    echo.
    echo [ERRO] Falha na criacao.
)
pause