@echo off
cd /d "%~dp0"
echo ==========================================
echo CRIANDO VERSAO PARA DISTRIBUICAO
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
echo [1/4] Verificando dependencias...
"%VENV_PYTHON%" -m pip install pyinstaller Pillow requests

echo.
echo [2/4] Compilando executavel...
"%VENV_PYTHON%" -m PyInstaller --clean --noconfirm --onefile --windowed --name "MudaeOrganizador" organizador.py

echo.
echo [3/4] Preparando pasta para envio...
:: Cria uma pasta limpa para voce enviar
if exist "MudaOrganizador_DISTRIBUICAO" rmdir /s /q "MudaOrganizador_DISTRIBUICAO"
mkdir "MudaOrganizador_DISTRIBUICAO"

:: Copia o executavel
if exist "dist\MudaeOrganizador.exe" (
    copy "dist\MudaeOrganizador.exe" "MudaOrganizador_DISTRIBUICAO\" >nul
    
    :: Cria um dados.txt vazio para o amigo nao ficar perdido
    type nul > "MudaOrganizador_DISTRIBUICAO\dados.txt"
    
    echo.
    echo [4/4] Limpando bagunca...
    rmdir /s /q build
    rmdir /s /q dist
    del /q MudaeOrganizador.spec
    
    echo.
    echo [SUCESSO] Tudo pronto!
    echo.
    echo Envie APENAS a pasta "MudaOrganizador_DISTRIBUICAO" para seu amigo.
    echo (Ela contem o .exe e o dados.txt. Nao precisa da pasta .venv ou imagens)
) else (
    echo.
    echo [ERRO] Falha na criacao.
)
pause