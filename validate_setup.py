#!/usr/bin/env python3
"""
RepoMaster Setup Validation Script

This script performs comprehensive validation of the RepoMaster setup,
checking dependencies, configuration, and system readiness.

Usage:
    python validate_setup.py           # Full validation
    python validate_setup.py --quick   # Quick validation (skip some tests)
    python validate_setup.py --fix     # Attempt to fix issues automatically
"""

import os
import sys
import subprocess
import importlib
import socket
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import argparse

class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

class ValidationResult:
    """Represents the result of a validation check"""
    def __init__(self, name: str, passed: bool, message: str, fix_command: Optional[str] = None):
        self.name = name
        self.passed = passed
        self.message = message
        self.fix_command = fix_command

class SetupValidator:
    """Validates RepoMaster setup and configuration"""
    
    def __init__(self, quick_mode: bool = False, auto_fix: bool = False):
        self.quick_mode = quick_mode
        self.auto_fix = auto_fix
        self.project_root = Path(__file__).parent
        self.results: List[ValidationResult] = []
    
    def print_header(self):
        """Print validation header"""
        print(f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    🔍 RepoMaster Setup Validation 🔍                        ║
║                                                                              ║
║                  Comprehensive system readiness check                        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Colors.END}
""")
    
    def add_result(self, name: str, passed: bool, message: str, fix_command: Optional[str] = None):
        """Add a validation result"""
        result = ValidationResult(name, passed, message, fix_command)
        self.results.append(result)
        
        if passed:
            print(f"{Colors.GREEN}✅ {name}: {message}{Colors.END}")
        else:
            print(f"{Colors.RED}❌ {name}: {message}{Colors.END}")
            if fix_command and self.auto_fix:
                print(f"{Colors.YELLOW}   🔧 Attempting fix: {fix_command}{Colors.END}")
                self.run_fix_command(fix_command)
    
    def run_fix_command(self, command: str):
        """Run a fix command"""
        try:
            subprocess.run(command, shell=True, check=True, cwd=self.project_root)
            print(f"{Colors.GREEN}   ✅ Fix applied successfully{Colors.END}")
        except subprocess.CalledProcessError as e:
            print(f"{Colors.RED}   ❌ Fix failed: {e}{Colors.END}")
    
    def validate_python_version(self):
        """Validate Python version"""
        version = sys.version_info
        min_version = (3, 8)
        
        if version >= min_version:
            self.add_result(
                "Python Version",
                True,
                f"Python {version.major}.{version.minor}.{version.micro} (>= {min_version[0]}.{min_version[1]})"
            )
        else:
            self.add_result(
                "Python Version",
                False,
                f"Python {version.major}.{version.minor}.{version.micro} (requires >= {min_version[0]}.{min_version[1]})",
                "Please upgrade Python to version 3.8 or higher"
            )
    
    def validate_virtual_environment(self):
        """Check if running in virtual environment"""
        in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
        
        if in_venv:
            self.add_result("Virtual Environment", True, "Running in virtual environment")
        else:
            self.add_result(
                "Virtual Environment",
                False,
                "Not running in virtual environment (recommended)",
                "python -m venv venv && source venv/bin/activate"
            )
    
    def validate_dependencies(self):
        """Validate critical dependencies"""
        critical_deps = {
            'streamlit': 'Web framework',
            'pandas': 'Data processing',
            'requests': 'HTTP requests',
            'openai': 'OpenAI API client',
            'tiktoken': 'Token counting',
            'python-dotenv': 'Environment variables'
        }
        
        optional_deps = {
            'fitz': 'PyMuPDF (PDF processing)',
            'PIL': 'Pillow (Image processing)',
            'plotly': 'Data visualization',
            'beautifulsoup4': 'HTML parsing'
        }
        
        # Check critical dependencies
        missing_critical = []
        for dep, description in critical_deps.items():
            try:
                importlib.import_module(dep)
                self.add_result(f"Dependency: {dep}", True, f"{description} - Available")
            except ImportError:
                missing_critical.append(dep)
                self.add_result(
                    f"Dependency: {dep}",
                    False,
                    f"{description} - Missing",
                    f"pip install {dep}"
                )
        
        # Check optional dependencies
        for dep, description in optional_deps.items():
            try:
                importlib.import_module(dep)
                self.add_result(f"Optional: {dep}", True, f"{description} - Available")
            except ImportError:
                self.add_result(f"Optional: {dep}", False, f"{description} - Missing (optional)")
        
        # Overall dependency status
        if not missing_critical:
            self.add_result("Critical Dependencies", True, "All critical dependencies available")
        else:
            self.add_result(
                "Critical Dependencies",
                False,
                f"Missing: {', '.join(missing_critical)}",
                f"pip install {' '.join(missing_critical)}"
            )
    
    def validate_configuration_files(self):
        """Validate configuration files"""
        config_files = [
            ("requirements.txt", "Python dependencies"),
            ("launcher.py", "Main launcher script"),
            ("configs/mode_config.py", "Mode configuration"),
            (".streamlit/config.toml", "Streamlit configuration"),
        ]
        
        for file_path, description in config_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                self.add_result(f"Config: {file_path}", True, f"{description} - Found")
            else:
                self.add_result(f"Config: {file_path}", False, f"{description} - Missing")
    
    def validate_environment_file(self):
        """Validate environment configuration"""
        env_file = self.project_root / "configs" / ".env"
        env_example = self.project_root / "configs" / "env.example"
        
        if env_file.exists():
            self.add_result("Environment File", True, ".env file exists")
            
            # Check for required variables
            try:
                with open(env_file, 'r') as f:
                    content = f.read()
                
                required_vars = ['OPENAI_API_KEY', 'OPENAI_MODEL', 'OPENAI_BASE_URL']
                missing_vars = []
                
                for var in required_vars:
                    if f"{var}=" not in content:
                        missing_vars.append(var)
                
                if not missing_vars:
                    self.add_result("Environment Variables", True, "Required variables configured")
                else:
                    self.add_result(
                        "Environment Variables",
                        False,
                        f"Missing: {', '.join(missing_vars)}"
                    )
            except Exception as e:
                self.add_result("Environment Variables", False, f"Error reading .env: {e}")
        
        elif env_example.exists():
            self.add_result(
                "Environment File",
                False,
                ".env missing but example found",
                f"cp {env_example} {env_file}"
            )
        else:
            self.add_result("Environment File", False, ".env and example missing")
    
    def validate_ports(self):
        """Check port availability"""
        ports_to_check = [8501, 8502, 8503]
        available_ports = []
        
        for port in ports_to_check:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            
            if result != 0:  # Port is available
                available_ports.append(port)
        
        if available_ports:
            self.add_result(
                "Port Availability",
                True,
                f"Available ports: {', '.join(map(str, available_ports))}"
            )
        else:
            self.add_result(
                "Port Availability",
                False,
                "No available ports found (8501-8503)"
            )
    
    def validate_file_permissions(self):
        """Check file permissions"""
        files_to_check = [
            "launcher.py",
            "deploy.py",
            "start.py",
            "validate_setup.py"
        ]
        
        permission_issues = []
        
        for file_name in files_to_check:
            file_path = self.project_root / file_name
            if file_path.exists():
                if not os.access(file_path, os.R_OK):
                    permission_issues.append(f"{file_name} (not readable)")
                elif file_name.endswith('.py') and not os.access(file_path, os.X_OK):
                    permission_issues.append(f"{file_name} (not executable)")
        
        if not permission_issues:
            self.add_result("File Permissions", True, "All files have correct permissions")
        else:
            self.add_result(
                "File Permissions",
                False,
                f"Issues: {', '.join(permission_issues)}",
                f"chmod +x {' '.join(files_to_check)}"
            )
    
    def validate_import_paths(self):
        """Test critical import paths"""
        if self.quick_mode:
            return
        
        import_tests = [
            ("configs.mode_config", "Configuration module"),
            ("src.frontend.terminal_show", "Frontend display module"),
        ]
        
        # Add project root to path temporarily
        sys.path.insert(0, str(self.project_root))
        
        try:
            for module_path, description in import_tests:
                try:
                    importlib.import_module(module_path)
                    self.add_result(f"Import: {module_path}", True, f"{description} - OK")
                except ImportError as e:
                    self.add_result(f"Import: {module_path}", False, f"{description} - Failed: {e}")
        finally:
            # Remove from path
            if str(self.project_root) in sys.path:
                sys.path.remove(str(self.project_root))
    
    def validate_launcher_functionality(self):
        """Test launcher basic functionality"""
        if self.quick_mode:
            return
        
        try:
            # Test launcher help command
            result = subprocess.run(
                [sys.executable, "launcher.py", "--help"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                self.add_result("Launcher Help", True, "Help command works")
            else:
                self.add_result("Launcher Help", False, f"Help command failed: {result.stderr}")
        
        except subprocess.TimeoutExpired:
            self.add_result("Launcher Help", False, "Help command timed out")
        except Exception as e:
            self.add_result("Launcher Help", False, f"Help command error: {e}")
    
    def generate_report(self):
        """Generate validation report"""
        print(f"\n{Colors.BOLD}📋 Validation Report{Colors.END}")
        print("=" * 60)
        
        passed_count = sum(1 for r in self.results if r.passed)
        total_count = len(self.results)
        
        print(f"\n{Colors.CYAN}Summary:{Colors.END}")
        print(f"  Total checks: {total_count}")
        print(f"  Passed: {Colors.GREEN}{passed_count}{Colors.END}")
        print(f"  Failed: {Colors.RED}{total_count - passed_count}{Colors.END}")
        
        # Show failed checks
        failed_results = [r for r in self.results if not r.passed]
        if failed_results:
            print(f"\n{Colors.RED}Failed Checks:{Colors.END}")
            for result in failed_results:
                print(f"  ❌ {result.name}: {result.message}")
                if result.fix_command:
                    print(f"     💡 Fix: {result.fix_command}")
        
        # Overall status
        success_rate = (passed_count / total_count) * 100 if total_count > 0 else 0
        
        if success_rate >= 90:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 Setup is ready! ({success_rate:.1f}%){Colors.END}")
            print(f"{Colors.CYAN}You can start RepoMaster with:{Colors.END}")
            print(f"  • python start.py")
            print(f"  • python launcher.py --mode frontend")
            return True
        elif success_rate >= 70:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  Setup mostly ready ({success_rate:.1f}%){Colors.END}")
            print(f"{Colors.CYAN}Consider fixing the issues above for optimal performance{Colors.END}")
            return True
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}❌ Setup needs attention ({success_rate:.1f}%){Colors.END}")
            print(f"{Colors.CYAN}Please fix the critical issues before running RepoMaster{Colors.END}")
            print(f"{Colors.CYAN}Run: python deploy.py{Colors.END}")
            return False
    
    def run_validation(self) -> bool:
        """Run complete validation"""
        self.print_header()
        
        print(f"{Colors.CYAN}Running validation checks...{Colors.END}\n")
        
        # Run all validation checks
        self.validate_python_version()
        self.validate_virtual_environment()
        self.validate_dependencies()
        self.validate_configuration_files()
        self.validate_environment_file()
        self.validate_ports()
        self.validate_file_permissions()
        self.validate_import_paths()
        self.validate_launcher_functionality()
        
        # Generate report
        return self.generate_report()

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="RepoMaster Setup Validation")
    parser.add_argument("--quick", action="store_true", help="Quick validation (skip some tests)")
    parser.add_argument("--fix", action="store_true", help="Attempt to fix issues automatically")
    
    args = parser.parse_args()
    
    validator = SetupValidator(quick_mode=args.quick, auto_fix=args.fix)
    
    try:
        success = validator.run_validation()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Validation interrupted{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Validation failed: {e}{Colors.END}")
        sys.exit(1)

if __name__ == "__main__":
    main()
