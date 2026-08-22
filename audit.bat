@echo off
set REPO_DIR=%CD%
start "SECURE ENGINE - FORENSIC AUDIT" cmd /k "cd /d "C:\LOC MY FILE\Project Code\audit-code" && call venv\Scripts\activate.bat && python main.py "%REPO_DIR%""