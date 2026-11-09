@echo off
setlocal EnableExtensions

rem Inicia o aplicativo desktop que fica nesta mesma pasta.
set "SCRIPT=%~dp0reclass_desktop.py"
set "VENV1=%~dp0python_api\.venv\Scripts\python.exe"
set "VENV2=%~dp0.venv\Scripts\python.exe"
set "PYTHON_EXE="
set "USE_PY_LAUNCHER=0"

if not exist "%SCRIPT%" (
    echo ERRO: Nao encontrei o arquivo:
    echo "%SCRIPT%"
    echo Coloque este arquivo BAT na mesma pasta de reclass_desktop.py.
    pause
    exit /b 1
)

rem Tenta primeiro os ambientes virtuais do projeto, se tiverem as dependencias.
if exist "%VENV1%" (
    "%VENV1%" -c "import PyQt6, pymysql" >nul 2>&1
    if not errorlevel 1 set "PYTHON_EXE=%VENV1%"
)

if not defined PYTHON_EXE if exist "%VENV2%" (
    "%VENV2%" -c "import PyQt6, pymysql" >nul 2>&1
    if not errorlevel 1 set "PYTHON_EXE=%VENV2%"
)

rem Caso nao encontre um ambiente virtual compativel, tenta o Python Launcher.
if not defined PYTHON_EXE (
    where py >nul 2>&1
    if not errorlevel 1 (
        py -3 -c "import PyQt6, pymysql" >nul 2>&1
        if not errorlevel 1 set "USE_PY_LAUNCHER=1"
    )
)

rem Ultima tentativa: comando python no PATH.
if not defined PYTHON_EXE if "%USE_PY_LAUNCHER%"=="0" (
    where python >nul 2>&1
    if not errorlevel 1 (
        python -c "import PyQt6, pymysql" >nul 2>&1
        if not errorlevel 1 set "PYTHON_EXE=python"
    )
)

if defined PYTHON_EXE (
    "%PYTHON_EXE%" "%SCRIPT%"
) else if "%USE_PY_LAUNCHER%"=="1" (
    py -3 "%SCRIPT%"
) else (
    echo ERRO: Nao encontrei um Python com PyQt6 e pymysql instalados.
    echo Instale as dependencias no mesmo Python usado para executar o Reclass Desktop.
    echo Exemplo: py -3 -m pip install PyQt6 PyMySQL
    pause
    exit /b 1
)

if errorlevel 1 (
    echo O Reclass Desktop foi encerrado com erro.
    pause
)
endlocal
