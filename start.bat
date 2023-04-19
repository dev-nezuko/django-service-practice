@echo off

echo Setting up venv...
set VENV_DIR=".venv"
python -m venv %VENV_DIR%
call %VENV_DIR%\Scripts\activate

echo Installing requirements...
pip install --upgrade pip
pip install -r requirements.txt

echo Migrating...
python manage.py migrate --settings=config.settings.local
