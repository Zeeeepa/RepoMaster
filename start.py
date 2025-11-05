#!/usr/bin/env python3
"""
RepoMaster Interactive Launcher

This script provides an interactive way to start RepoMaster with different modes.
It checks configuration, validates setup, and launches the selected mode.

Usage:
    python start.py
"""

import os
import sys
import subprocess
import signal
from pathlib import Path
from typing import Optional
import time

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

class RepoMasterLauncher:
    def __init__(self):
        self.root_dir = Path(__file__).parent.absolute()
        self.config_dir = self.root_dir / "configs"
        self.env_file = self.config_dir / ".env"
        self.launcher_script = self.root_dir / "launcher.py"
        self.process: Optional[subprocess.Popen] = None
        
    def print_banner(self):
        """Print the RepoMaster launcher banner"""
        banner = f"""
{Colors.HEADER}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  🚀 RepoMaster Interactive Launcher                                          ║
║                                                                              ║
║  Your AI-powered GitHub repository assistant                                 ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Colors.ENDC}
"""
        print(banner)
        
    def check_configuration(self) -> bool:
        """Check if RepoMaster is properly configured"""
        if not self.env_file.exists():
            print(f"{Colors.FAIL}❌ Configuration file not found: {self.env_file}{Colors.ENDC}")
            print(f"{Colors.WARNING}💡 Run 'python deploy.py' to set up RepoMaster{Colors.ENDC}")
            return False
            
        # Load environment variables
        try:
            from dotenv import load_dotenv
            load_dotenv(self.env_file, override=True)
            
            # Check required API key
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key or api_key == 'your_zai_api_key_here':
                print(f"{Colors.FAIL}❌ Z.ai API key not configured{Colors.ENDC}")
                print(f"{Colors.WARNING}💡 Run 'python deploy.py' to configure your API keys{Colors.ENDC}")
                return False
                
            print(f"{Colors.OKGREEN}✅ Configuration validated{Colors.ENDC}")
            return True
            
        except ImportError:
            print(f"{Colors.FAIL}❌ python-dotenv not installed{Colors.ENDC}")
            print(f"{Colors.WARNING}💡 Run 'python deploy.py' to install dependencies{Colors.ENDC}")
            return False
        except Exception as e:
            print(f"{Colors.FAIL}❌ Configuration error: {e}{Colors.ENDC}")
            return False
            
    def show_menu(self) -> str:
        """Show the interactive menu and get user choice"""
        print(f"\n{Colors.HEADER}🎯 Choose RepoMaster Mode{Colors.ENDC}")
        print("Select how you want to run RepoMaster:\n")
        
        options = [
            ("1", "🌐 Web Interface (Streamlit)", "Launch the web-based dashboard", "frontend"),
            ("2", "🤖 Unified AI Assistant", "Intelligent multi-agent orchestration", "unified"),
            ("3", "🔍 Deep Search Agent", "Specialized repository search and analysis", "deepsearch"),
            ("4", "💻 General Assistant", "Programming and development assistance", "general_assistant"),
            ("5", "📁 Repository Agent", "Repository exploration and understanding", "repository_agent"),
            ("6", "❓ Help", "Show detailed help information", "help"),
            ("7", "⚙️ Reconfigure", "Run deployment setup again", "deploy"),
            ("0", "🚪 Exit", "Exit the launcher", "exit"),
        ]
        
        for num, name, desc, _ in options:
            print(f"{Colors.OKBLUE}{num}. {name}{Colors.ENDC}")
            print(f"   {desc}\n")
            
        while True:
            choice = input(f"{Colors.OKCYAN}Enter your choice (0-7): {Colors.ENDC}").strip()
            if choice in [opt[0] for opt in options]:
                return next(opt[3] for opt in options if opt[0] == choice)
            print(f"{Colors.WARNING}⚠️ Invalid choice. Please enter a number from 0-7.{Colors.ENDC}")
            
    def launch_mode(self, mode: str) -> bool:
        """Launch RepoMaster in the specified mode"""
        if mode == "exit":
            print(f"{Colors.OKCYAN}👋 Goodbye!{Colors.ENDC}")
            return False
            
        if mode == "help":
            self.show_help()
            return True
            
        if mode == "deploy":
            self.run_deployment()
            return True
            
        # Build command based on mode
        if mode == "frontend":
            cmd = [sys.executable, str(self.launcher_script), "--mode", "frontend"]
            print(f"{Colors.OKGREEN}🌐 Starting Web Interface...{Colors.ENDC}")
            print(f"{Colors.OKCYAN}💡 Access the dashboard at: http://localhost:8501{Colors.ENDC}")
        else:
            cmd = [sys.executable, str(self.launcher_script), "--mode", "backend", "--backend-mode", mode]
            mode_names = {
                "unified": "Unified AI Assistant",
                "deepsearch": "Deep Search Agent",
                "general_assistant": "General Assistant",
                "repository_agent": "Repository Agent"
            }
            print(f"{Colors.OKGREEN}🤖 Starting {mode_names.get(mode, mode)}...{Colors.ENDC}")
            
        print(f"{Colors.WARNING}💡 Press Ctrl+C to stop the service{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Command: {' '.join(cmd)}{Colors.ENDC}\n")
        
        # Launch the process
        try:
            self.process = subprocess.Popen(cmd, cwd=self.root_dir)
            
            # Wait for the process to complete
            self.process.wait()
            
            if self.process.returncode == 0:
                print(f"\n{Colors.OKGREEN}✅ Service stopped normally{Colors.ENDC}")
            else:
                print(f"\n{Colors.WARNING}⚠️ Service stopped with code {self.process.returncode}{Colors.ENDC}")
                
        except KeyboardInterrupt:
            print(f"\n{Colors.WARNING}⚠️ Stopping service...{Colors.ENDC}")
            if self.process:
                self.process.terminate()
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.process.kill()
            print(f"{Colors.OKGREEN}✅ Service stopped{Colors.ENDC}")
        except Exception as e:
            print(f"\n{Colors.FAIL}❌ Error launching service: {e}{Colors.ENDC}")
            
        return True
        
    def show_help(self):
        """Show detailed help information"""
        help_text = f"""
{Colors.HEADER}📖 RepoMaster Help{Colors.ENDC}

{Colors.OKBLUE}🌐 Web Interface (Streamlit){Colors.ENDC}
   - Interactive web dashboard
   - Visual interface for all RepoMaster features
   - Best for beginners and visual users
   - Access at: http://localhost:8501

{Colors.OKBLUE}🤖 Unified AI Assistant{Colors.ENDC}
   - Intelligent multi-agent orchestration
   - Automatically routes tasks to appropriate agents
   - Recommended for most users
   - Command-line interface

{Colors.OKBLUE}🔍 Deep Search Agent{Colors.ENDC}
   - Specialized in repository search and analysis
   - Advanced code exploration capabilities
   - Best for research and discovery tasks

{Colors.OKBLUE}💻 General Assistant{Colors.ENDC}
   - Programming and development assistance
   - Code generation and debugging help
   - General-purpose AI assistant

{Colors.OKBLUE}📁 Repository Agent{Colors.ENDC}
   - Repository exploration and understanding
   - Codebase analysis and documentation
   - Best for understanding new codebases

{Colors.HEADER}🔧 Configuration{Colors.ENDC}
- Configuration file: {self.env_file}
- Required: Z.ai API key from https://z.ai/model-api
- Optional: SERPER_API_KEY, JINA_API_KEY for enhanced features

{Colors.HEADER}🚀 Quick Start{Colors.ENDC}
1. Run 'python deploy.py' to set up RepoMaster
2. Configure your Z.ai API key
3. Use 'python start.py' to launch interactively
4. Or use direct commands like 'python launcher.py --mode frontend'

{Colors.WARNING}💡 For more information, see README.md or USAGE.md{Colors.ENDC}
"""
        print(help_text)
        input(f"\n{Colors.OKCYAN}Press Enter to continue...{Colors.ENDC}")
        
    def run_deployment(self):
        """Run the deployment script"""
        deploy_script = self.root_dir / "deploy.py"
        if not deploy_script.exists():
            print(f"{Colors.FAIL}❌ deploy.py not found{Colors.ENDC}")
            return
            
        print(f"{Colors.OKCYAN}🚀 Running deployment setup...{Colors.ENDC}")
        try:
            subprocess.run([sys.executable, str(deploy_script)], cwd=self.root_dir)
        except KeyboardInterrupt:
            print(f"\n{Colors.WARNING}⚠️ Deployment cancelled{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.FAIL}❌ Deployment error: {e}{Colors.ENDC}")
            
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            print(f"\n{Colors.WARNING}⚠️ Received signal {signum}, shutting down...{Colors.ENDC}")
            if self.process:
                self.process.terminate()
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.process.kill()
            sys.exit(0)
            
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
    def run(self):
        """Main launcher loop"""
        self.setup_signal_handlers()
        self.print_banner()
        
        # Check configuration
        if not self.check_configuration():
            print(f"\n{Colors.WARNING}Would you like to run the deployment setup now? (y/n): {Colors.ENDC}", end="")
            if input().lower().strip() == 'y':
                self.run_deployment()
                # Re-check configuration after deployment
                if not self.check_configuration():
                    print(f"{Colors.FAIL}❌ Configuration still invalid. Exiting.{Colors.ENDC}")
                    return
            else:
                print(f"{Colors.FAIL}❌ Cannot proceed without proper configuration{Colors.ENDC}")
                return
                
        # Main menu loop
        while True:
            try:
                mode = self.show_menu()
                if not self.launch_mode(mode):
                    break
                    
                # Ask if user wants to continue
                if mode not in ["help", "deploy"]:
                    print(f"\n{Colors.OKCYAN}Would you like to launch another mode? (y/n): {Colors.ENDC}", end="")
                    if input().lower().strip() != 'y':
                        break
                        
            except KeyboardInterrupt:
                print(f"\n{Colors.WARNING}⚠️ Launcher interrupted{Colors.ENDC}")
                break
            except Exception as e:
                print(f"{Colors.FAIL}❌ Unexpected error: {e}{Colors.ENDC}")
                break

def main():
    """Main function"""
    launcher = RepoMasterLauncher()
    launcher.run()

if __name__ == "__main__":
    main()
