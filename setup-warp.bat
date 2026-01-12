@echo off
REM Sarva - Warp Integration Setup Script (Windows)

echo Setting up Warp CLI for Sarva...
echo ====================================
echo.

REM Check if in project root
if not exist "package.json" (
    echo Error: Not in Sarva project root directory
    echo Please run this script from the Sarva project root
    exit /b 1
)

echo Step 1: Creating directory structure...
if not exist ".warp" mkdir .warp
if not exist "docs\guides" mkdir docs\guides
if not exist "docs\runbooks" mkdir docs\runbooks
echo Done
echo.

echo Step 2: Moving Warp configuration files...
if exist "warp-workflows.yaml" move warp-workflows.yaml .warp\workflows.yaml
if exist "warp-aliases.sh" move warp-aliases.sh .warp\aliases.sh
if exist "warp-ai-workflows.md" move warp-ai-workflows.md .warp\ai-workflows.md
if exist "WARP-QUICKSTART.md" move WARP-QUICKSTART.md docs\guides\WARP-QUICKSTART.md
if exist "warp-deployment-runbook.md" move warp-deployment-runbook.md docs\runbooks\deployment.md
echo Done
echo.

echo Step 3: Setup complete!
echo.
echo Created structure:
echo   sarva/
echo   ├── .warp/
echo   │   ├── workflows.yaml
echo   │   ├── aliases.sh
echo   │   └── ai-workflows.md
echo   └── docs/
echo       ├── guides/
echo       │   └── WARP-QUICKSTART.md
echo       └── runbooks/
echo           └── deployment.md
echo.
echo Next steps:
echo   1. Open Warp terminal
echo   2. Press Cmd+Shift+R to access workflows
echo   3. Read: docs\guides\WARP-QUICKSTART.md
echo.
pause
