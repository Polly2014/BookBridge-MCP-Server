#!/usr/bin/env python3
"""
Quick setup and start script for BookBridge-MCP
"""

import subprocess
import sys
import os
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 10):
        print("❌ Python 3.10 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")


def check_poetry_environment():
    """Check if Poetry environment is set up"""
    print("\n📦 Checking Poetry environment...")
    
    # Check if we're in a Poetry environment
    try:
        result = subprocess.run([
            "poetry", "env", "info"
        ], capture_output=True, text=True, check=True)
        print("✅ Poetry environment is active")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Poetry environment not found")
        print("💡 Please run: poetry install")
        print("   Or use: python setup_poetry.py")
        sys.exit(1)


def verify_dependencies():
    """Verify that dependencies are installed"""
    print("\n🔍 Verifying dependencies...")
    
    try:
        # Test basic imports in the current Poetry environment
        import fastmcp
        import docx 
        import markdown
        print("✅ Core dependencies available")
    except ImportError as e:
        print(f"❌ Dependencies not installed properly: {e}")
        print("💡 Run: poetry install")
        sys.exit(1)


def setup_directories():
    """Create necessary directories"""
    print("\n📂 Setting up directories...")
    
    dirs = [
        "input_documents",
        "output_documents", 
        "temp_documents"
    ]
    
    for dir_name in dirs:
        dir_path = Path(dir_name)
        dir_path.mkdir(exist_ok=True)
        print(f"✅ Created/verified {dir_name}")


def create_sample_config():
    """Create sample configuration if not exists"""
    config_path = Path("config.env")
    
    if not config_path.exists():
        print("\n⚙️ Creating sample configuration...")
        sample_config = """# Environment Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1

# Document Processing Settings
INPUT_DIR=./input_documents
OUTPUT_DIR=./output_documents
TEMP_DIR=./temp_documents

# Translation Settings
SOURCE_LANGUAGE=chinese
TARGET_LANGUAGE=english
TRANSLATION_MODEL=gpt-4o-mini

# MCP Server Settings
SERVER_NAME=BookBridge-MCP
SERVER_VERSION=1.0.0
"""
        
        with open(config_path, 'w') as f:
            f.write(sample_config)
        
        print("✅ Sample configuration created")
        print("⚠️  Please edit config.env and set your OpenAI API key")
    else:
        print("✅ Configuration file exists")


def run_tests():
    """Run component tests"""
    print("\n🧪 Running component tests...")
    try:
        subprocess.check_call(["poetry", "run", "python", "test_simple.py"])
        print("✅ All tests passed!")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Some tests failed: {e}")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)
    except FileNotFoundError:
        print("❌ test_simple.py not found, skipping tests")


def start_server():
    """Start the MCP server"""
    print("\n🚀 Starting BookBridge-MCP Server...")
    print("   The server will run in stdio mode (standard for MCP servers)")
    print("   Press Ctrl+C to stop the server")
    print("   Use examples/client_example.py to test the server")
    print("\n" + "="*50)
    
    try:
        subprocess.run(["poetry", "run", "python", "server.py"])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")
    except FileNotFoundError:
        print("❌ Poetry not found. Please install Poetry first.")
        print("💡 Run: python setup_poetry.py")
        sys.exit(1)


def main():
    """Main setup and start function"""
    print("🌉 BookBridge-MCP Setup & Start")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Check Poetry environment
    check_poetry_environment()
    
    # Verify dependencies
    verify_dependencies()
    
    # Setup directories
    setup_directories()
    
    # Create sample config
    create_sample_config()
    
    # Ask user what to do next
    print("\n" + "=" * 50)
    print("Setup completed! What would you like to do?")
    print("1. Run component tests")
    print("2. Start the MCP server")
    print("3. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            run_tests()
            break
        elif choice == "2":
            start_server()
            break
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
