@echo off
setlocal

REM ===== 現在のbatファイルの場所を取得 =====
set BASE_DIR=%~dp0
cd /d %BASE_DIR%\..

REM ===== 仮想環境パス =====
set VENV_DIR=venv
set PYTHON_SCRIPT=src\main.py

REM ===== 仮想環境存在チェック =====
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo [ERROR] 仮想環境が見つかりません。
    echo %VENV_DIR%\Scripts\activate.bat が存在しません。
    pause
    exit /b 1
)

REM ===== Pythonファイル存在チェック =====
if not exist "%PYTHON_SCRIPT%" (
    echo [ERROR] 実行対象のPythonファイルが見つかりません。
    echo %PYTHON_SCRIPT%
    pause
    exit /b 1
)

echo ==========================
echo 仮想環境を有効化します
echo ==========================

call %VENV_DIR%\Scripts\activate.bat

echo ==========================
echo Pythonスクリプト実行開始
echo ==========================

python %PYTHON_SCRIPT%
set EXIT_CODE=%ERRORLEVEL%

echo ==========================
echo 仮想環境を終了します
echo ==========================

call deactivate

REM ===== エラーチェック =====
if %EXIT_CODE% neq 0 (
    echo.
    echo [ERROR] Python実行中にエラーが発生しました。
    echo 終了コード: %EXIT_CODE%
    pause
    exit /b %EXIT_CODE%
)

echo.
echo 正常終了しました。
pause
exit /b 0
