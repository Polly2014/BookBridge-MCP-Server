@echo off
REM BookBridge-MCP Development Commands for Windows
REM Requires Poetry to be installed

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="setup" goto setup
if "%1"=="install" goto install
if "%1"=="dev-install" goto dev-install
if "%1"=="test" goto test
if "%1"=="test-coverage" goto test-coverage
if "%1"=="lint" goto lint
if "%1"=="format" goto format
if "%1"=="format-check" goto format-check
if "%1"=="type-check" goto type-check
if "%1"=="pre-commit" goto pre-commit
if "%1"=="clean" goto clean
if "%1"=="build" goto build
if "%1"=="run" goto run
if "%1"=="server" goto server
if "%1"=="client-example" goto client-example
if "%1"=="shell" goto shell
if "%1"=="env-info" goto env-info
if "%1"=="show-deps" goto show-deps
if "%1"=="update-deps" goto update-deps
if "%1"=="install-git-hooks" goto install-git-hooks
if "%1"=="check" goto check
if "%1"=="ci" goto ci
if "%1"=="dev-setup" goto dev-setup
if "%1"=="quick-test" goto quick-test

goto help

:help
echo BookBridge-MCP Development Commands
echo ==================================
echo.
echo setup           - Set up the project with Poetry
echo install         - Install dependencies
echo dev-install     - Install with development dependencies
echo test            - Run tests
echo test-coverage   - Run tests with coverage report
echo lint            - Run linting (flake8)
echo format          - Format code (black + isort)
echo format-check    - Check code formatting without making changes
echo type-check      - Run type checking (mypy)
echo pre-commit      - Run pre-commit hooks on all files
echo clean           - Clean up temporary files and caches
echo build           - Build the package
echo run             - Start the MCP server
echo server          - Start the MCP server (alias for run)
echo client-example  - Run the client example
echo shell           - Activate Poetry shell
echo env-info        - Show environment information
echo show-deps       - Show installed dependencies
echo update-deps     - Update dependencies
echo install-git-hooks - Install git hooks
echo check           - Run all checks (format, lint, type-check, test)
echo ci              - Run CI pipeline
echo dev-setup       - Complete development setup
echo quick-test      - Quick test without coverage
goto end

:setup
python setup_poetry.py
goto end

:install
poetry install
goto end

:dev-install
poetry install --with dev --with client
goto end

:test
poetry run pytest -v
goto end

:test-coverage
poetry run pytest --cov=src --cov-report=html --cov-report=term
goto end

:lint
poetry run flake8 src/ tests/ examples/
goto end

:format
poetry run black .
poetry run isort .
goto end

:format-check
poetry run black --check .
poetry run isort --check-only .
goto end

:type-check
poetry run mypy src/
goto end

:pre-commit
poetry run pre-commit run --all-files
goto end

:clean
echo Cleaning up temporary files...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
for /r . %%f in (*.pyc) do @if exist "%%f" del /q "%%f"
if exist ".coverage" del /q ".coverage"
if exist "htmlcov" rd /s /q "htmlcov"
if exist ".pytest_cache" rd /s /q ".pytest_cache"
if exist ".mypy_cache" rd /s /q ".mypy_cache"
echo Cleanup complete!
goto end

:build
poetry build
goto end

:run
poetry run python start.py
goto end

:server
poetry run python start.py
goto end

:client-example
poetry run python examples/client_example.py
goto end

:shell
poetry shell
goto end

:env-info
poetry env info
goto end

:show-deps
poetry show
goto end

:update-deps
poetry update
goto end

:install-git-hooks
poetry run pre-commit install
goto end

:check
call :format-check
call :lint
call :type-check
call :test
goto end

:ci
call :format-check
call :lint  
call :type-check
call :test-coverage
goto end

:dev-setup
call :dev-install
call :install-git-hooks
echo.
echo ✅ Development environment ready!
echo Next steps:
echo   1. Run 'make.bat run' to start the server
echo   2. Run 'make.bat client-example' to test the client
echo   3. Run 'make.bat test' to run tests
goto end

:quick-test
poetry run pytest tests/ -x -v
goto end

:end
