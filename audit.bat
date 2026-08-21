@echo off
set REPO_DIR=%CD%
cd /d "C:\LOC MY FILE\Project Code\audit-code"
call venv\Scripts\activate.bat
python main.py "%REPO_DIR%"