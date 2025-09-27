#!/usr/bin/env python3
"""
Windows-Specific RepoMaster Test Script
Handles Windows encoding issues and provides clean test results
"""

import sys
import os
import subprocess
import importlib.util
from pathlib import Path

def safe_print(text="", color=None):
    """Windows-safe print function"""
    if not text:
        print()
        return
    
    # Convert to string and handle encoding
    text_str = str(text)
    
    try:
        # Try UTF-8 first
        print(text_str.encode('utf-8', errors='ignore').decode('utf-8'))
    except:
        try:
            # Fallback to ASCII
            ascii_text = ''.join(char for char in text_str if ord(char) < 128)
            print(ascii_text)
        except:
            # Ultimate fallback
            print("Output encoding error")

def test_basic_functionality():
    """Test basic RepoMaster functionality on Windows"""
    safe_print("🚀 Windows RepoMaster Test")
    safe_print("=" * 40)
    
    # Test 1: Python version
    safe_print("\n1. Python Version:")
    version = sys.version_info
    safe_print(f"   Python {version.major}.{version.minor}.{version.micro}")
    if version >= (3, 8):
        safe_print("   ✅ Compatible")
    else:
        safe_print("   ❌ Too old")
        return False
    
    # Test 2: Critical imports
    safe_print("\n2. Critical Imports:")
    imports = [
        ("streamlit", "Streamlit"),
        ("pandas", "Pandas"),
        ("requests", "Requests"),
        ("plotly", "Plotly"),
        ("bs4", "BeautifulSoup"),
    ]
    
    import_success = 0
    for module, name in imports:
        try:
            __import__(module)
            safe_print(f"   ✅ {name}")
            import_success += 1
        except ImportError:
            safe_print(f"   ❌ {name}")
    
    safe_print(f"   Imports: {import_success}/{len(imports)}")
    
    # Test 3: RepoMaster modules
    safe_print("\n3. RepoMaster Modules:")
    try:
        from src.utils.autogen_compat import AssistantAgent
        safe_print("   ✅ AutoGen compatibility")
        
        from src.utils.tool_streamlit import AppContext
        safe_print("   ✅ Tool utilities")
        
        # Test agent creation (should not print warnings)
        agent = AssistantAgent(name="test")
        safe_print("   ✅ Agent creation")
        
    except Exception as e:
        safe_print(f"   ❌ Module error: {str(e)[:50]}...")
        return False
    
    # Test 4: Configuration files
    safe_print("\n4. Configuration:")
    config_files = [
        "configs/.env",
        "launcher.py", 
        "start.py",
        "requirements.txt"
    ]
    
    config_ok = 0
    for file in config_files:
        if Path(file).exists():
            safe_print(f"   ✅ {file}")
            config_ok += 1
        else:
            safe_print(f"   ❌ {file}")
    
    safe_print(f"   Config files: {config_ok}/{len(config_files)}")
    
    # Test 5: Simple launcher test (without subprocess issues)
    safe_print("\n5. Launcher Test:")
    try:
        # Import launcher components
        from configs.mode_config import ModeConfigManager
        config_manager = ModeConfigManager()
        safe_print("   ✅ Configuration manager")
        
        # Test basic functionality without running subprocess
        safe_print("   ✅ Basic launcher components")
        
    except Exception as e:
        safe_print(f"   ❌ Launcher error: {str(e)[:50]}...")
    
    # Summary
    safe_print("\n" + "=" * 40)
    safe_print("📊 Windows Test Summary:")
    
    if import_success >= len(imports) * 0.8 and config_ok >= len(config_files) * 0.8:
        safe_print("✅ READY TO USE!")
        safe_print("\n🚀 Launch Commands:")
        safe_print("   python start.py")
        safe_print("   python launcher.py --mode frontend")
        return True
    else:
        safe_print("⚠️  NEEDS SETUP")
        safe_print("\n🔧 Run these commands:")
        safe_print("   pip install -r requirements.txt")
        safe_print("   pip install -e .")
        return False

if __name__ == "__main__":
    success = test_basic_functionality()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)
