#!/usr/bin/env python3
"""
RepoMaster Interactive Deployment Script

This script provides an interactive setup and deployment experience for RepoMaster.
It guides users through:
1. Environment setup and dependency installation
2. API key configuration (Z.ai, SERPER, JINA)
3. Configuration validation
4. Service deployment options

Usage:
    python deploy.py
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import json

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class RepoMasterDeployer:
    def __init__(self):
        self.root_dir = Path(__file__).parent.absolute()
        self.config_dir = self.root_dir / "configs"
        self.env_file = self.config_dir / ".env"
        self.env_example = self.config_dir / "env.example"
        self.requirements_file = self.root_dir / "requirements.txt"
        
    def print_banner(self):
        """Print the RepoMaster deployment banner"""
        banner = f"""
{Colors.HEADER}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  🚀 RepoMaster Interactive Deployment & Setup                               ║
║                                                                              ║
║  Transform GitHub repositories into your personal AI toolbox                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Colors.ENDC}
"""
        print(banner)
        
    def print_step(self, step: int, total: int, title: str, status: str = ""):
        """Print a deployment step with status"""
        status_icon = {
            "running": "⏳",
            "success": "✅",
            "error": "❌",
            "warning": "⚠️"
        }.get(status, "📋")
        
        print(f"{Colors.OKBLUE}[{step}/{total}] {status_icon} {title}{Colors.ENDC} {status}")
        
    def check_python_version(self) -> bool:
        """Check if Python version is compatible"""
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print(f"{Colors.FAIL}❌ Python 3.8+ required. Current version: {version.major}.{version.minor}{Colors.ENDC}")
            return False
        print(f"{Colors.OKGREEN}✅ Python {version.major}.{version.minor}.{version.micro} - Compatible{Colors.ENDC}")
        return True
        
    def check_dependencies(self) -> Tuple[bool, List[str]]:
        """Check if required dependencies are installed"""
        missing_deps = []
        required_packages = [
            'streamlit', 'pandas', 'requests', 'python-dotenv', 
            'beautifulsoup4', 'pillow', 'openai', 'plotly', 'gradio'
        ]
        
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
            except ImportError:
                missing_deps.append(package)
                
        return len(missing_deps) == 0, missing_deps
        
    def install_dependencies(self) -> bool:
        """Install Python dependencies"""
        try:
            print(f"{Colors.OKCYAN}📦 Installing Python dependencies...{Colors.ENDC}")
            
            # Install core packages first
            core_packages = [
                'streamlit', 'pandas', 'requests', 'python-dotenv', 
                'beautifulsoup4', 'pillow', 'openai', 'plotly', 'tqdm', 
                'joblib', 'networkx', 'humanize', 'gradio'
            ]
            
            cmd = [sys.executable, '-m', 'pip', 'install'] + core_packages
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"{Colors.WARNING}⚠️ Some packages failed to install. Trying additional packages...{Colors.ENDC}")
                
            # Try additional packages
            additional_packages = ['streamlit_extras', 'genson', 'grep_ast']
            for package in additional_packages:
                try:
                    subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                                 capture_output=True, check=True)
                except subprocess.CalledProcessError:
                    print(f"{Colors.WARNING}⚠️ Optional package {package} failed to install (skipping){Colors.ENDC}")
                    
            print(f"{Colors.OKGREEN}✅ Core dependencies installed successfully{Colors.ENDC}")
            return True
            
        except Exception as e:
            print(f"{Colors.FAIL}❌ Failed to install dependencies: {e}{Colors.ENDC}")
            return False
            
    def setup_environment_file(self) -> bool:
        """Setup the .env configuration file"""
        if not self.env_example.exists():
            print(f"{Colors.FAIL}❌ env.example file not found{Colors.ENDC}")
            return False
            
        # Copy example to .env if it doesn't exist
        if not self.env_file.exists():
            shutil.copy(self.env_example, self.env_file)
            print(f"{Colors.OKGREEN}✅ Created .env file from template{Colors.ENDC}")
        else:
            print(f"{Colors.OKGREEN}✅ .env file already exists{Colors.ENDC}")
            
        return True
        
    def get_user_input(self, prompt: str, default: str = "", required: bool = True) -> str:
        """Get user input with optional default value"""
        if default:
            full_prompt = f"{prompt} [{default}]: "
        else:
            full_prompt = f"{prompt}: "
            
        while True:
            value = input(full_prompt).strip()
            if not value and default:
                return default
            if not value and required:
                print(f"{Colors.WARNING}⚠️ This field is required{Colors.ENDC}")
                continue
            return value
            
    def configure_api_keys(self) -> bool:
        """Interactive API key configuration"""
        print(f"\n{Colors.HEADER}🔑 API Key Configuration{Colors.ENDC}")
        print("Configure your API keys for RepoMaster functionality:\n")
        
        # Read current .env file
        env_vars = {}
        if self.env_file.exists():
            with open(self.env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        env_vars[key] = value
                        
        # Z.ai API Key (Required)
        print(f"{Colors.OKBLUE}1. Z.ai API Key (Required){Colors.ENDC}")
        print("   Get your API key from: https://z.ai/model-api")
        current_key = env_vars.get('OPENAI_API_KEY', 'your_zai_api_key_here')
        if current_key == 'your_zai_api_key_here':
            current_key = ""
            
        zai_key = self.get_user_input("   Enter your Z.ai API key", current_key, required=True)
        env_vars['OPENAI_API_KEY'] = zai_key
        
        # SERPER API Key (Optional)
        print(f"\n{Colors.OKBLUE}2. SERPER API Key (Optional - for enhanced search){Colors.ENDC}")
        print("   Get your API key from: https://serper.dev/login")
        current_serper = env_vars.get('SERPER_API_KEY', 'your_serper_api_key_here_optional')
        if current_serper == 'your_serper_api_key_here_optional':
            current_serper = ""
            
        serper_key = self.get_user_input("   Enter your SERPER API key (or press Enter to skip)", 
                                       current_serper, required=False)
        if serper_key:
            env_vars['SERPER_API_KEY'] = serper_key
            
        # JINA API Key (Optional)
        print(f"\n{Colors.OKBLUE}3. JINA API Key (Optional - for document processing){Colors.ENDC}")
        print("   Get your API key from: https://jina.ai/")
        current_jina = env_vars.get('JINA_API_KEY', 'your_jina_api_key_here_optional')
        if current_jina == 'your_jina_api_key_here_optional':
            current_jina = ""
            
        jina_key = self.get_user_input("   Enter your JINA API key (or press Enter to skip)", 
                                     current_jina, required=False)
        if jina_key:
            env_vars['JINA_API_KEY'] = jina_key
            
        # Write updated .env file
        self.write_env_file(env_vars)
        print(f"{Colors.OKGREEN}✅ API keys configured successfully{Colors.ENDC}")
        return True
        
    def write_env_file(self, env_vars: Dict[str, str]):
        """Write environment variables to .env file"""
        # Read the template to preserve structure and comments
        template_lines = []
        if self.env_example.exists():
            with open(self.env_example, 'r') as f:
                template_lines = f.readlines()
                
        # Update the template with new values
        updated_lines = []
        for line in template_lines:
            if '=' in line and not line.strip().startswith('#'):
                key = line.split('=')[0]
                if key in env_vars:
                    updated_lines.append(f"{key}={env_vars[key]}\n")
                else:
                    updated_lines.append(line)
            else:
                updated_lines.append(line)
                
        # Write to .env file
        with open(self.env_file, 'w') as f:
            f.writelines(updated_lines)
            
    def validate_configuration(self) -> bool:
        """Validate the configuration"""
        try:
            # Load environment variables
            from dotenv import load_dotenv
            load_dotenv(self.env_file, override=True)
            
            # Check required API key
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key or api_key == 'your_zai_api_key_here':
                print(f"{Colors.FAIL}❌ Z.ai API key not configured{Colors.ENDC}")
                return False
                
            print(f"{Colors.OKGREEN}✅ Configuration validated successfully{Colors.ENDC}")
            return True
            
        except Exception as e:
            print(f"{Colors.FAIL}❌ Configuration validation failed: {e}{Colors.ENDC}")
            return False
            
    def show_deployment_options(self):
        """Show deployment options to the user"""
        print(f"\n{Colors.HEADER}🚀 Deployment Options{Colors.ENDC}")
        print("Choose how you want to run RepoMaster:\n")
        
        options = [
            ("1", "Web Interface (Streamlit)", "python launcher.py --mode frontend"),
            ("2", "CLI - Unified Assistant", "python launcher.py --mode backend --backend-mode unified"),
            ("3", "CLI - Deep Search Agent", "python launcher.py --mode backend --backend-mode deepsearch"),
            ("4", "CLI - General Assistant", "python launcher.py --mode backend --backend-mode general_assistant"),
            ("5", "CLI - Repository Agent", "python launcher.py --mode backend --backend-mode repository_agent"),
        ]
        
        for num, name, cmd in options:
            print(f"{Colors.OKBLUE}{num}. {name}{Colors.ENDC}")
            print(f"   Command: {Colors.OKCYAN}{cmd}{Colors.ENDC}\n")
            
        print(f"{Colors.WARNING}💡 You can also use the start.py script for interactive launching{Colors.ENDC}")
        
    def run_deployment(self):
        """Run the complete deployment process"""
        self.print_banner()
        
        # Step 1: Check Python version
        self.print_step(1, 6, "Checking Python version", "running")
        if not self.check_python_version():
            return False
        self.print_step(1, 6, "Python version check", "success")
        
        # Step 2: Check/Install dependencies
        self.print_step(2, 6, "Checking dependencies", "running")
        deps_ok, missing = self.check_dependencies()
        if not deps_ok:
            print(f"{Colors.WARNING}⚠️ Missing dependencies: {', '.join(missing)}{Colors.ENDC}")
            if input(f"{Colors.OKCYAN}Install missing dependencies? (y/n): {Colors.ENDC}").lower() == 'y':
                if not self.install_dependencies():
                    self.print_step(2, 6, "Dependency installation", "error")
                    return False
            else:
                self.print_step(2, 6, "Dependencies", "warning")
        self.print_step(2, 6, "Dependencies", "success")
        
        # Step 3: Setup environment file
        self.print_step(3, 6, "Setting up environment file", "running")
        if not self.setup_environment_file():
            self.print_step(3, 6, "Environment setup", "error")
            return False
        self.print_step(3, 6, "Environment setup", "success")
        
        # Step 4: Configure API keys
        self.print_step(4, 6, "Configuring API keys", "running")
        if not self.configure_api_keys():
            self.print_step(4, 6, "API configuration", "error")
            return False
        self.print_step(4, 6, "API configuration", "success")
        
        # Step 5: Validate configuration
        self.print_step(5, 6, "Validating configuration", "running")
        if not self.validate_configuration():
            self.print_step(5, 6, "Configuration validation", "error")
            return False
        self.print_step(5, 6, "Configuration validation", "success")
        
        # Step 6: Show deployment options
        self.print_step(6, 6, "Deployment ready", "success")
        self.show_deployment_options()
        
        print(f"\n{Colors.OKGREEN}🎉 RepoMaster deployment completed successfully!{Colors.ENDC}")
        print(f"{Colors.OKCYAN}You can now run RepoMaster using the commands shown above.{Colors.ENDC}")
        print(f"{Colors.OKCYAN}For interactive launching, use: python start.py{Colors.ENDC}")
        
        return True

def main():
    """Main deployment function"""
    deployer = RepoMasterDeployer()
    
    try:
        success = deployer.run_deployment()
        if not success:
            print(f"\n{Colors.FAIL}❌ Deployment failed. Please check the errors above.{Colors.ENDC}")
            sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}⚠️ Deployment cancelled by user{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.FAIL}❌ Unexpected error during deployment: {e}{Colors.ENDC}")
        sys.exit(1)

if __name__ == "__main__":
    main()
