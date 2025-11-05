#!/usr/bin/env python3
"""
Test RepoMaster Installation
Quick test to verify that the installation is working correctly
"""

import sys
import os
import subprocess
from pathlib import Path

def test_imports():
    """Test critical imports"""
    print("🧪 Testing critical imports...")
    
    try:
        # Test basic imports
        import pandas
        print("✅ pandas imported successfully")
        
        import streamlit
        print("✅ streamlit imported successfully")
        
        import requests
        print("✅ requests imported successfully")
        
        # Test PyMuPDF import (this was the problematic one)
        try:
            import fitz  # PyMuPDF
            print("✅ PyMuPDF (fitz) imported successfully")
        except ImportError as e:
            print(f"❌ PyMuPDF import failed: {e}")
            return False
            
        # Test autogen import
        try:
            import autogen
            print("✅ autogen imported successfully")
        except ImportError as e:
            print(f"⚠️  autogen import failed: {e}")
            # Not critical, continue
            
        return True
        
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False

def test_package_installation():
    """Test if the package is properly installed"""
    print("\n📦 Testing package installation...")
    
    try:
        # Check if we can import from src
        sys.path.insert(0, str(Path(__file__).parent))
        
        # Test if we can import launcher
        import launcher
        print("✅ launcher module imported successfully")
        
        # Test if we can import start
        import start
        print("✅ start module imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Package import test failed: {e}")
        return False

def test_console_commands():
    """Test if console commands are available"""
    print("\n🖥️  Testing console commands...")
    
    try:
        # Test if repomaster command is available
        result = subprocess.run(['repomaster', '--help'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ repomaster command available")
        else:
            print("⚠️  repomaster command not available (pip install -e . needed)")
            
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("⚠️  repomaster command not available (pip install -e . needed)")
    
    return True

def test_configuration():
    """Test configuration files"""
    print("\n⚙️  Testing configuration...")
    
    config_dir = Path(__file__).parent / "configs"
    env_file = config_dir / ".env"
    
    if env_file.exists():
        print("✅ .env configuration file found")
        return True
    else:
        print("⚠️  .env configuration file not found")
        print("   Run: python deploy.py to set up configuration")
        return False

def main():
    """Run all tests"""
    print("🚀 RepoMaster Installation Test")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Package Installation Test", test_package_installation),
        ("Console Commands Test", test_console_commands),
        ("Configuration Test", test_configuration),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 All tests passed! RepoMaster is ready to use.")
        print("\n🚀 Quick start:")
        print("  python start.py")
        return True
    else:
        print("\n⚠️  Some tests failed. Consider running:")
        print("  python deploy.py")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
