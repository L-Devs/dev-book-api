@echo off
echo Installing dependencies...
if exist %~dp0\env\ (
  cd /d %cd%\env\scripts  
  activate & pip install -r %~dp0\requirements.txt 
  deactivate 
  echo Successfully installed all the dependencies, you may now use Run Server.bat
  pause
) else (
  python -m venv .\env
  cd /d %cd%\env\scripts  
  activate & pip install -r %~dp0\requirements.txt 
  deactivate 
  echo Successfully installed all the dependencies, you may now use Run Server.bat
  pause
)
