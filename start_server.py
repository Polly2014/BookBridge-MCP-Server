#!/usr/bin/env python3
"""
Simple server startup script for BookBridge-MCP
"""

import sys
import subprocess
from pathlib import Path

def main():
    """Start the MCP server directly"""
    print("🚀 Starting BookBridge-MCP Server...")
    print("   The server will run in stdio mode (standard for MCP servers)")
    print("   Press Ctrl+C to stop the server")
    print("="*50)
    
    # Check if we're in Poetry environment
    try:
        result = subprocess.run([
            "poetry", "env", "info"
        ], capture_output=True, text=True, check=False)
        
        if result.returncode != 0:
            print("❌ Poetry environment not found")
            print("💡 Please run: poetry install")
            sys.exit(1)
            
    except FileNotFoundError:
        print("❌ Poetry not found. Please install Poetry first.")
        print("💡 Run: python setup_poetry.py")
        sys.exit(1)
    
    # Start the server
    try:
        subprocess.run(["poetry", "run", "python", "server.py"])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
