#!/usr/bin/env python3
"""
Poetry Setup Script for BookBridge-MCP
Automates Poetry installation and project setup
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description=None):
    """Run a command and handle errors"""
    if description:
        print(f"🔄 {description}...")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        if result.stdout.strip():
            print(result.stdout.strip())
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False


def check_poetry():
    """Check if Poetry is installed"""
    try:
        result = subprocess.run(
            ["poetry", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ Poetry is already installed: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def install_poetry():
    """Install Poetry using the official installer"""
    print("📦 Installing Poetry...")
    
    # Try to install Poetry using pip first (simpler)
    if run_command("pip install poetry", "Installing Poetry via pip"):
        return True
    
    # If pip installation fails, try the official installer
    print("Trying official Poetry installer...")
    if sys.platform.startswith('win'):
        # Windows
        command = '(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -'
        shell_cmd = ["powershell", "-Command", command]
    else:
        # Unix-like systems
        shell_cmd = ["curl", "-sSL", "https://install.python-poetry.org", "|", "python3", "-"]
    
    try:
        subprocess.run(shell_cmd, check=True)
        print("✅ Poetry installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install Poetry. Please install manually:")
        print("   Visit: https://python-poetry.org/docs/#installation")
        return False


def setup_poetry_project():
    """Set up the Poetry project"""
    print("🏗️ Setting up Poetry project...")
    
    # Initialize poetry if pyproject.toml doesn't exist
    if not Path("pyproject.toml").exists():
        print("❌ pyproject.toml not found. Please run this script from the project root.")
        return False
    
    # Install dependencies
    if not run_command("poetry install", "Installing project dependencies"):
        return False
    
    # Install development dependencies
    if not run_command("poetry install --with dev", "Installing development dependencies"):
        return False
    
    # Install client dependencies (optional)
    if not run_command("poetry install --with client", "Installing client dependencies"):
        print("⚠️ Client dependencies installation failed (this is optional)")
    
    print("✅ Project setup complete!")
    return True


def setup_pre_commit():
    """Set up pre-commit hooks"""
    print("🪝 Setting up pre-commit hooks...")
    
    if not run_command("poetry run pre-commit install", "Installing pre-commit hooks"):
        print("⚠️ Pre-commit setup failed (optional feature)")
        return False
    
    print("✅ Pre-commit hooks installed!")
    return True


def display_next_steps():
    """Display next steps for the user"""
    print("\n" + "="*60)
    print("🎉 BookBridge-MCP Poetry setup complete!")
    print("="*60)
    print("\n📋 Next steps:")
    print("1. Activate the Poetry environment:")
    print("   poetry shell")
    print("\n2. Start the MCP server:")
    print("   poetry run python start.py")
    print("   # or using the script:")
    print("   poetry run bookbridge-server")
    print("\n3. Run tests:")
    print("   poetry run pytest")
    print("\n4. Run the client example:")
    print("   poetry run python examples/client_example.py")
    print("\n5. Format code:")
    print("   poetry run black .")
    print("   poetry run isort .")
    print("\n6. Type checking:")
    print("   poetry run mypy src/")
    print("\n📁 Project structure:")
    print("   • src/          - Source code")
    print("   • examples/     - Client examples")
    print("   • tests/        - Test files")
    print("   • pyproject.toml - Poetry configuration")
    print("\n🔧 Useful Poetry commands:")
    print("   • poetry add <package>     - Add new dependency")
    print("   • poetry remove <package>  - Remove dependency")
    print("   • poetry show             - List installed packages")
    print("   • poetry env info         - Show environment info")
    print("   • poetry build            - Build the package")


def main():
    """Main setup function"""
    print("🚀 BookBridge-MCP Poetry Setup")
    print("="*40)
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    print(f"📂 Working directory: {script_dir}")
    
    # Check if Poetry is installed
    if not check_poetry():
        print("📦 Poetry not found. Installing Poetry...")
        if not install_poetry():
            sys.exit(1)
    
    # Set up the project
    if not setup_poetry_project():
        sys.exit(1)
    
    # Set up pre-commit (optional)
    setup_pre_commit()
    
    # Display next steps
    display_next_steps()


if __name__ == "__main__":
    main()
