#!/usr/bin/env python3
"""
Environment Test for BookBridge-MCP
Validates Poetry environment and dependency installations
"""

def test_basic():
    """Basic test that always passes"""
    assert 1 + 1 == 2
    print("✅ Basic test passed")

def test_poetry_environment():
    """Test Poetry environment and dependencies"""
    import sys
    print(f"🐍 Python version: {sys.version}")
    
    # Test core dependencies
    dependencies = [
        ("docx", "python-docx"),
        ("markdown", "markdown"),
        ("bs4", "beautifulsoup4"),
        ("openai", "openai"),
        ("fastmcp", "fastmcp")
    ]
    
    for module_name, package_name in dependencies:
        try:
            __import__(module_name)
            print(f"✅ {package_name} imported successfully")
        except ImportError as e:
            print(f"❌ {package_name} import failed: {e}")
            return False
    
    print("🎉 All dependencies are properly installed!")
    return True

def test_project_structure():
    """Test project structure"""
    from pathlib import Path
    
    required_files = [
        "pyproject.toml",
        "poetry.lock", 
        "server.py",
        "start.py",
        "src/__init__.py",
        "tests/conftest.py"
    ]
    
    project_root = Path(__file__).parent
    
    for file_path in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            return False
    
    print("🏗️ Project structure is valid!")
    return True

if __name__ == "__main__":
    print("🔍 BookBridge-MCP Environment Test")
    print("=" * 50)
    
    test_basic()
    test_poetry_environment()
    test_project_structure()
    
    print("=" * 50)
    print("✅ Environment test completed!")
