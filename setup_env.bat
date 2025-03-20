@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing requirements...
pip install -r requirements.txt

echo Virtual environment setup complete!
echo To activate the environment later, run: venv\Scripts\activate.bat
