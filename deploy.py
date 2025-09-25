#!/usr/bin/env python3
"""
RepoMaster Deployment Script

This script handles the complete deployment and setup of RepoMaster,
including dependency management, configuration validation, and environment setup.

Usage:
    python deploy.py                    # Full deployment
    python deploy.py --quick            # Quick setup (skip some checks)
    python deploy.py --validate-only    # Only validate current setup
    python deploy.py --fix-deps         # Fix dependency issues only
"""

import os
import sys
import subprocess
import shutil
import logging
import argparse
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import json
import time

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_banner():
    """Print deployment banner"""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    🚀 RepoMaster Deployment Script 🚀                       ║
║                                                                              ║
║              Automated setup and dependency management                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Colors.END}
"""
    print(banner)

def print_step(step_num: int, total_steps: int, description: str):
    """Print step progress"""
    print(f"\n{Colors.BLUE}[{step_num}/{total_steps}]{Colors.END} {Colors.BOLD}{description}{Colors.END}")

def print_success(message: str):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_warning(message: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def print_error(message: str):
    """Print error message"""
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_info(message: str):
    """Print info message"""
    print(f"{Colors.CYAN}ℹ️  {message}{Colors.END}")

class DeploymentManager:
    """Manages the complete deployment process"""
    
    def __init__(self, quick_mode: bool = False, validate_only: bool = False, fix_deps_only: bool = False):
        self.quick_mode = quick_mode
        self.validate_only = validate_only
        self.fix_deps_only = fix_deps_only
        self.project_root = Path(__file__).parent
        self.python_executable = sys.executable
        self.issues_found = []
        self.fixes_applied = []
        
    def run_command(self, command: List[str], capture_output: bool = True, check: bool = True) -> subprocess.CompletedProcess:
        """Run a command with proper error handling"""
        try:
            logger.debug(f"Running command: {' '.join(command)}")
            result = subprocess.run(
                command,
                capture_output=capture_output,
                text=True,
                check=check,
                cwd=self.project_root
            )
            return result
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {' '.join(command)}")
            logger.error(f"Error: {e.stderr if e.stderr else e.stdout}")
            raise
    
    def check_python_version(self) -> bool:
        """Check if Python version is compatible"""
        print_step(1, 8, "🐍 Checking Python Version")
        
        version = sys.version_info
        min_version = (3, 8)
        
        if version >= min_version:
            print_success(f"Python {version.major}.{version.minor}.{version.micro} is compatible")
            return True
        else:
            print_error(f"Python {version.major}.{version.minor}.{version.micro} is too old. Minimum required: {min_version[0]}.{min_version[1]}")
            self.issues_found.append(f"Python version {version.major}.{version.minor} < {min_version[0]}.{min_version[1]}")
            return False
    
    def check_virtual_environment(self) -> bool:
        """Check if running in virtual environment"""
        print_step(2, 8, "🏠 Checking Virtual Environment")
        
        in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
        
        if in_venv:
            print_success("Running in virtual environment")
            return True
        else:
            print_warning("Not running in virtual environment")
            print_info("Consider using: python -m venv venv && source venv/bin/activate")
            return True  # Not critical, just a warning
    
    def install_dependencies(self) -> bool:
        """Install and validate dependencies"""
        print_step(3, 8, "📦 Installing Dependencies")
        
        requirements_file = self.project_root / "requirements.txt"
        if not requirements_file.exists():
            print_error("requirements.txt not found")
            self.issues_found.append("Missing requirements.txt")
            return False
        
        try:
            # Upgrade pip first
            print_info("Upgrading pip...")
            self.run_command([self.python_executable, "-m", "pip", "install", "--upgrade", "pip"])
            
            # Install requirements
            print_info("Installing requirements...")
            result = self.run_command([
                self.python_executable, "-m", "pip", "install", "-r", str(requirements_file)
            ], capture_output=False)
            
            print_success("Dependencies installed successfully")
            self.fixes_applied.append("Installed dependencies")
            return True
            
        except subprocess.CalledProcessError as e:
            print_error("Failed to install dependencies")
            self.issues_found.append("Dependency installation failed")
            
            # Try to fix common PyMuPDF issues
            if "PyMuPDF" in str(e):
                print_info("Attempting to fix PyMuPDF installation...")
                try:
                    # Uninstall and reinstall PyMuPDF with specific version
                    self.run_command([self.python_executable, "-m", "pip", "uninstall", "PyMuPDF", "-y"])
                    self.run_command([self.python_executable, "-m", "pip", "install", "PyMuPDF==1.23.26"])
                    print_success("Fixed PyMuPDF installation")
                    self.fixes_applied.append("Fixed PyMuPDF version conflict")
                    return True
                except:
                    print_warning("Could not fix PyMuPDF. PDF features will be disabled.")
                    return True  # Continue without PDF support
            
            return False
    
    def validate_imports(self) -> bool:
        """Validate that critical imports work"""
        print_step(4, 8, "🔍 Validating Critical Imports")
        
        critical_imports = [
            ("streamlit", "Streamlit web framework"),
            ("pandas", "Data processing"),
            ("requests", "HTTP requests"),
            ("openai", "OpenAI API client"),
        ]
        
        optional_imports = [
            ("fitz", "PyMuPDF (PDF processing)"),
            ("PIL", "Pillow (Image processing)"),
        ]
        
        all_good = True
        
        # Test critical imports
        for module, description in critical_imports:
            try:
                __import__(module)
                print_success(f"{description} - OK")
            except ImportError as e:
                print_error(f"{description} - FAILED: {e}")
                self.issues_found.append(f"Missing critical import: {module}")
                all_good = False
        
        # Test optional imports
        for module, description in optional_imports:
            try:
                __import__(module)
                print_success(f"{description} - OK")
            except ImportError as e:
                print_warning(f"{description} - OPTIONAL: {e}")
        
        return all_good
    
    def validate_configuration(self) -> bool:
        """Validate configuration files"""
        print_step(5, 8, "⚙️  Validating Configuration")
        
        config_files = [
            ("configs/.env", "Environment configuration"),
            (".streamlit/config.toml", "Streamlit configuration"),
        ]
        
        all_good = True
        
        for file_path, description in config_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                print_success(f"{description} - Found")
                
                # Validate .env file
                if file_path.endswith('.env'):
                    self.validate_env_file(full_path)
                    
            else:
                print_warning(f"{description} - Missing")
                if file_path.endswith('.env'):
                    self.create_default_env()
        
        return all_good
    
    def validate_env_file(self, env_path: Path):
        """Validate environment file"""
        try:
            with open(env_path, 'r') as f:
                content = f.read()
                
            required_vars = ['OPENAI_API_KEY', 'OPENAI_MODEL', 'OPENAI_BASE_URL']
            missing_vars = []
            
            for var in required_vars:
                if f"{var}=" not in content:
                    missing_vars.append(var)
            
            if missing_vars:
                print_warning(f"Missing environment variables: {', '.join(missing_vars)}")
            else:
                print_success("Environment variables configured")
                
        except Exception as e:
            print_warning(f"Could not validate .env file: {e}")
    
    def create_default_env(self):
        """Create default .env file"""
        env_path = self.project_root / "configs" / ".env"
        env_example_path = self.project_root / "configs" / "env.example"
        
        if env_example_path.exists() and not env_path.exists():
            try:
                shutil.copy(env_example_path, env_path)
                print_success("Created .env from example")
                self.fixes_applied.append("Created default .env file")
            except Exception as e:
                print_warning(f"Could not create .env file: {e}")
    
    def check_ports(self) -> bool:
        """Check if required ports are available"""
        print_step(6, 8, "🔌 Checking Port Availability")
        
        import socket
        
        ports_to_check = [8501, 8502, 8503]  # Streamlit default ports
        available_ports = []
        
        for port in ports_to_check:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            
            if result != 0:  # Port is available
                available_ports.append(port)
                print_success(f"Port {port} is available")
            else:
                print_warning(f"Port {port} is in use")
        
        if available_ports:
            print_success(f"Available ports: {', '.join(map(str, available_ports))}")
            return True
        else:
            print_error("No available ports found")
            self.issues_found.append("No available ports for Streamlit")
            return False
    
    def test_basic_functionality(self) -> bool:
        """Test basic application functionality"""
        print_step(7, 8, "🧪 Testing Basic Functionality")
        
        try:
            # Test launcher import
            sys.path.insert(0, str(self.project_root))
            
            # Test configuration loading
            from configs.mode_config import ModeConfigManager
            config_manager = ModeConfigManager()
            print_success("Configuration manager loaded")
            
            # Test basic imports from src
            try:
                from src.frontend.terminal_show import print_repomaster_title
                print_success("Frontend modules loaded")
            except ImportError as e:
                print_warning(f"Some frontend modules failed: {e}")
            
            return True
            
        except Exception as e:
            print_error(f"Basic functionality test failed: {e}")
            self.issues_found.append(f"Basic functionality test failed: {e}")
            return False
    
    def generate_report(self) -> bool:
        """Generate deployment report"""
        print_step(8, 8, "📋 Generating Deployment Report")
        
        print(f"\n{Colors.BOLD}🎯 Deployment Summary{Colors.END}")
        print("=" * 50)
        
        if self.fixes_applied:
            print(f"\n{Colors.GREEN}✅ Fixes Applied:{Colors.END}")
            for fix in self.fixes_applied:
                print(f"  • {fix}")
        
        if self.issues_found:
            print(f"\n{Colors.YELLOW}⚠️  Issues Found:{Colors.END}")
            for issue in self.issues_found:
                print(f"  • {issue}")
        
        # Overall status
        critical_issues = [issue for issue in self.issues_found if any(word in issue.lower() for word in ['critical', 'failed', 'missing critical'])]
        
        if not critical_issues:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 Deployment Successful!{Colors.END}")
            print(f"\n{Colors.CYAN}🚀 Ready to launch RepoMaster:{Colors.END}")
            print(f"  • Frontend: python launcher.py --mode frontend")
            print(f"  • Backend:  python launcher.py --mode backend --backend-mode unified")
            print(f"  • Interactive: python start.py")
            return True
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}❌ Deployment has critical issues{Colors.END}")
            print(f"\n{Colors.YELLOW}Please fix the issues above before running RepoMaster{Colors.END}")
            return False
    
    def deploy(self) -> bool:
        """Run the complete deployment process"""
        print_banner()
        
        if self.validate_only:
            print_info("Running validation only...")
        elif self.fix_deps_only:
            print_info("Fixing dependencies only...")
            return self.install_dependencies()
        
        success = True
        
        # Run all deployment steps
        steps = [
            self.check_python_version,
            self.check_virtual_environment,
            self.install_dependencies,
            self.validate_imports,
            self.validate_configuration,
            self.check_ports,
            self.test_basic_functionality,
            self.generate_report
        ]
        
        if self.validate_only:
            # Skip installation steps for validation
            steps = [steps[0], steps[1], steps[3], steps[4], steps[5], steps[6], steps[7]]
        
        for step in steps:
            try:
                if not step():
                    success = False
                    if not self.quick_mode and step != self.generate_report:
                        # In non-quick mode, stop on first failure (except report)
                        break
            except KeyboardInterrupt:
                print_error("\nDeployment interrupted by user")
                return False
            except Exception as e:
                print_error(f"Unexpected error in deployment step: {e}")
                logger.exception("Deployment step failed")
                success = False
                if not self.quick_mode:
                    break
        
        return success

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="RepoMaster Deployment Script")
    parser.add_argument("--quick", action="store_true", help="Quick deployment (continue on errors)")
    parser.add_argument("--validate-only", action="store_true", help="Only validate current setup")
    parser.add_argument("--fix-deps", action="store_true", help="Fix dependency issues only")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    deployer = DeploymentManager(
        quick_mode=args.quick,
        validate_only=args.validate_only,
        fix_deps_only=args.fix_deps
    )
    
    try:
        success = deployer.deploy()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print_error("\nDeployment interrupted")
        sys.exit(1)
    except Exception as e:
        print_error(f"Deployment failed with unexpected error: {e}")
        logger.exception("Deployment failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
