#!/usr/bin/env python3
"""
RepoMaster Interactive Startup Script

This script provides an interactive interface for starting RepoMaster
with proper service orchestration, health monitoring, and error handling.

Usage:
    python start.py                    # Interactive mode selection
    python start.py --mode frontend    # Direct frontend launch
    python start.py --mode backend     # Direct backend launch
    python start.py --health-check     # Check system health only
"""

import os
import sys
import subprocess
import signal
import time
import threading
import argparse
import socket
from pathlib import Path
from typing import Optional, Dict, List
import json

# Configure console encoding for Windows compatibility
try:
    from src.utils.encoding_config import safe_print, configure_console_encoding, is_utf8_available
    # Configure console encoding at startup
    configure_console_encoding()
except ImportError:
    # Fallback safe_print if encoding_config is not available
    def safe_print(text):
        """Fallback safe_print with basic ASCII conversion"""
        if not text:
            print()
            return
        try:
            print(text)
        except UnicodeEncodeError:
            # Ultimate fallback: strip all non-ASCII characters
            ascii_only = ''.join(char for char in text if ord(char) < 128)
            print(ascii_only)

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
    """Print startup banner"""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    🚀 RepoMaster Interactive Launcher 🚀                    ║
║                                                                              ║
║                   Your AI-powered GitHub repository assistant                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Colors.END}
"""
    safe_print(banner)

def print_success(message: str):
    """Print success message"""
    safe_print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_warning(message: str):
    """Print warning message"""
    safe_print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def print_error(message: str):
    """Print error message"""
    safe_print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_info(message: str):
    """Print info message"""
    safe_print(f"{Colors.CYAN}ℹ️  {message}{Colors.END}")

class ServiceManager:
    """Manages RepoMaster services with health monitoring"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.python_executable = sys.executable
        self.running_processes = {}
        self.shutdown_requested = False
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print_info("\nShutdown requested...")
        self.shutdown_requested = True
        self.stop_all_services()
        sys.exit(0)
    
    def find_available_port(self, start_port: int = 8501, max_attempts: int = 10) -> Optional[int]:
        """Find an available port starting from start_port"""
        for port in range(start_port, start_port + max_attempts):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            
            if result != 0:  # Port is available
                return port
        
        return None
    
    def check_system_health(self) -> Dict[str, bool]:
        """Check system health and dependencies"""
        health_status = {
            'python_version': False,
            'dependencies': False,
            'configuration': False,
            'ports': False
        }
        
        # Check Python version
        version = sys.version_info
        if version >= (3, 8):
            health_status['python_version'] = True
            print_success(f"Python {version.major}.{version.minor}.{version.micro}")
        else:
            print_error(f"Python {version.major}.{version.minor}.{version.micro} (requires >= 3.8)")
        
        # Check critical dependencies
        critical_deps = ['streamlit', 'pandas', 'requests', 'openai']
        missing_deps = []
        
        for dep in critical_deps:
            try:
                __import__(dep)
            except ImportError:
                missing_deps.append(dep)
        
        if not missing_deps:
            health_status['dependencies'] = True
            print_success("All critical dependencies available")
        else:
            print_error(f"Missing dependencies: {', '.join(missing_deps)}")
        
        # Check configuration
        env_file = self.project_root / "configs" / ".env"
        if env_file.exists():
            health_status['configuration'] = True
            print_success("Configuration file found")
        else:
            print_warning("Configuration file missing")
        
        # Check port availability
        available_port = self.find_available_port()
        if available_port:
            health_status['ports'] = True
            print_success(f"Port {available_port} available")
        else:
            print_error("No available ports found")
        
        return health_status
    
    def run_health_check(self) -> bool:
        """Run comprehensive health check"""
        safe_print(f"\n{Colors.BOLD}🏥 System Health Check{Colors.END}")
        safe_print("=" * 40)
        
        health_status = self.check_system_health()
        
        all_healthy = all(health_status.values())
        
        if all_healthy:
            safe_print(f"\n{Colors.GREEN}{Colors.BOLD}✅ System is healthy and ready!{Colors.END}")
        else:
            safe_print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  Some issues detected{Colors.END}")
            print_info("Run 'python deploy.py' to fix issues")
        
        return all_healthy
    
    def start_frontend(self, port: Optional[int] = None) -> bool:
        """Start the frontend service"""
        if not port:
            port = self.find_available_port()
            if not port:
                print_error("No available ports for frontend")
                return False
        
        print_info(f"Starting frontend on port {port}...")
        
        try:
            cmd = [
                self.python_executable, "launcher.py",
                "--mode", "frontend",
                "--streamlit-port", str(port)
            ]
            
            process = subprocess.Popen(
                cmd,
                cwd=self.project_root,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='ignore'  # Ignore encoding errors on Windows
            )
            
            self.running_processes['frontend'] = {
                'process': process,
                'port': port,
                'start_time': time.time()
            }
            
            # Wait a moment and check if process started successfully
            time.sleep(2)
            if process.poll() is None:
                print_success(f"Frontend started successfully")
                print_info(f"Access at: http://localhost:{port}")
                return True
            else:
                stdout, stderr = process.communicate()
                print_error(f"Frontend failed to start: {stderr}")
                return False
                
        except Exception as e:
            print_error(f"Failed to start frontend: {e}")
            return False
    
    def start_backend(self, mode: str = "unified") -> bool:
        """Start the backend service"""
        print_info(f"Starting backend in {mode} mode...")
        
        try:
            cmd = [
                self.python_executable, "launcher.py",
                "--mode", "backend",
                "--backend-mode", mode
            ]
            
            process = subprocess.Popen(
                cmd,
                cwd=self.project_root,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='ignore'  # Ignore encoding errors on Windows
            )
            
            self.running_processes['backend'] = {
                'process': process,
                'mode': mode,
                'start_time': time.time()
            }
            
            # Wait a moment and check if process started successfully
            time.sleep(2)
            if process.poll() is None:
                print_success(f"Backend started in {mode} mode")
                return True
            else:
                stdout, stderr = process.communicate()
                print_error(f"Backend failed to start: {stderr}")
                return False
                
        except Exception as e:
            print_error(f"Failed to start backend: {e}")
            return False
    
    def monitor_services(self):
        """Monitor running services"""
        while not self.shutdown_requested:
            for service_name, service_info in list(self.running_processes.items()):
                process = service_info['process']
                
                if process.poll() is not None:
                    # Process has terminated
                    print_warning(f"{service_name} service has stopped")
                    del self.running_processes[service_name]
            
            time.sleep(5)  # Check every 5 seconds
    
    def stop_all_services(self):
        """Stop all running services"""
        for service_name, service_info in self.running_processes.items():
            process = service_info['process']
            print_info(f"Stopping {service_name}...")
            
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print_warning(f"Force killing {service_name}")
                process.kill()
            except Exception as e:
                print_error(f"Error stopping {service_name}: {e}")
        
        self.running_processes.clear()
    
    def show_interactive_menu(self):
        """Show interactive mode selection menu"""
        safe_print(f"\n{Colors.BOLD}🎯 Choose RepoMaster Mode{Colors.END}")
        safe_print("Select how you want to run RepoMaster:")
        safe_print("")
        safe_print(f"{Colors.CYAN}0.{Colors.END} 🏥 Health Check")
        safe_print(f"   Check system health and dependencies")
        safe_print("")
        safe_print(f"{Colors.CYAN}1.{Colors.END} 🌐 Web Interface (Streamlit)")
        safe_print(f"   Launch the web-based dashboard")
        safe_print("")
        safe_print(f"{Colors.CYAN}2.{Colors.END} 🤖 Unified AI Assistant")
        safe_print(f"   Intelligent multi-agent orchestration")
        safe_print("")
        safe_print(f"{Colors.CYAN}3.{Colors.END} 🔍 Deep Search Agent")
        safe_print(f"   Specialized repository search and analysis")
        safe_print("")
        safe_print(f"{Colors.CYAN}4.{Colors.END} 💻 General Assistant")
        safe_print(f"   Programming and development assistance")
        safe_print("")
        safe_print(f"{Colors.CYAN}5.{Colors.END} 📁 Repository Agent")
        safe_print(f"   Repository exploration and understanding")
        safe_print("")
        safe_print(f"{Colors.CYAN}6.{Colors.END} ❓ Help")
        safe_print(f"   Show detailed help information")
        safe_print("")
        safe_print(f"{Colors.CYAN}7.{Colors.END} ⚙️  Reconfigure")
        safe_print(f"   Run deployment setup again")
        safe_print("")
        safe_print(f"{Colors.CYAN}8.{Colors.END} 🚪 Exit")
        safe_print(f"   Exit the launcher")
        safe_print("")
    
    def handle_user_choice(self, choice: str) -> bool:
        """Handle user menu choice"""
        choice = choice.strip()
        
        if choice == '0':
            return self.run_health_check()
        
        elif choice == '1':
            safe_print(f"\n{Colors.BLUE}🌐 Starting Web Interface...{Colors.END}")
            if self.start_frontend():
                print_info("Press Ctrl+C to stop the service")
                try:
                    # Start monitoring in background
                    monitor_thread = threading.Thread(target=self.monitor_services, daemon=True)
                    monitor_thread.start()
                    
                    # Keep main thread alive
                    while not self.shutdown_requested and self.running_processes:
                        time.sleep(1)
                except KeyboardInterrupt:
                    pass
                finally:
                    self.stop_all_services()
            else:
                # Fallback: Direct launch without subprocess
                print_info("Trying direct launch...")
                try:
                    import os
                    os.system(f"{self.python_executable} launcher.py --mode frontend")
                except Exception as e:
                    print_error(f"Direct launch failed: {e}")
                    print_info("Try running manually: python launcher.py --mode frontend")
            return True
        
        elif choice == '2':
            safe_print(f"\n{Colors.BLUE}🤖 Starting Unified AI Assistant...{Colors.END}")
            return self.start_backend("unified")
        
        elif choice == '3':
            safe_print(f"\n{Colors.BLUE}🔍 Starting Deep Search Agent...{Colors.END}")
            return self.start_backend("deepsearch")
        
        elif choice == '4':
            safe_print(f"\n{Colors.BLUE}💻 Starting General Assistant...{Colors.END}")
            return self.start_backend("general_assistant")
        
        elif choice == '5':
            safe_print(f"\n{Colors.BLUE}📁 Starting Repository Agent...{Colors.END}")
            return self.start_backend("repository_agent")
        
        elif choice == '6':
            self.show_help()
            return True
        
        elif choice == '7':
            safe_print(f"\n{Colors.BLUE}⚙️  Running deployment setup...{Colors.END}")
            try:
                subprocess.run([self.python_executable, "deploy.py"], cwd=self.project_root)
            except Exception as e:
                print_error(f"Deployment failed: {e}")
            return True
        
        elif choice == '8':
            print_info("Goodbye! 👋")
            return False
        
        else:
            print_error("Invalid choice. Please select 0-8.")
            return True
    
    def show_help(self):
        """Show detailed help information"""
        help_text = f"""
{Colors.BOLD}📖 RepoMaster Help{Colors.END}

{Colors.CYAN}Web Interface:{Colors.END}
  • Interactive dashboard for repository exploration
  • Visual file browser and code analysis
  • Multi-agent chat interface
  • Real-time progress tracking

{Colors.CYAN}Unified AI Assistant:{Colors.END}
  • Automatic agent orchestration
  • Intelligent task routing
  • Multi-modal capabilities
  • Best for complex tasks

{Colors.CYAN}Specialized Agents:{Colors.END}
  • Deep Search: Advanced code search and analysis
  • General Assistant: Programming help and code generation
  • Repository Agent: Repository structure understanding

{Colors.CYAN}Commands:{Colors.END}
  • python start.py --mode frontend    # Direct frontend launch
  • python start.py --mode backend     # Direct backend launch
  • python start.py --health-check     # System health check
  • python deploy.py                   # Fix deployment issues

{Colors.CYAN}Troubleshooting:{Colors.END}
  • Run health check first (option 0)
  • Use deployment script to fix issues (option 7)
  • Check logs in the logs/ directory
  • Ensure all dependencies are installed

{Colors.CYAN}Configuration:{Colors.END}
  • Edit configs/.env for API settings
  • Modify .streamlit/config.toml for UI settings
  • Check configs/mode_config.py for advanced options
"""
        safe_print(help_text)
    
    def run_interactive(self):
        """Run interactive mode"""
        print_banner()
        
        # Quick health check
        print_info("Running quick health check...")
        health_status = self.check_system_health()
        
        if not all(health_status.values()):
            print_warning("Some issues detected. Consider running deployment setup.")
            safe_print("")
        
        while True:
            try:
                self.show_interactive_menu()
                choice = input(f"\n{Colors.BOLD}Enter your choice (0-8): {Colors.END}")
                
                if not self.handle_user_choice(choice):
                    break
                    
                if choice not in ['1', '8']:  # Don't pause for frontend or exit
                    input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
                
            except KeyboardInterrupt:
                print_info("\nGoodbye! 👋")
                break
            except Exception as e:
                print_error(f"Unexpected error: {e}")
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="RepoMaster Interactive Startup Script")
    parser.add_argument("--mode", choices=["frontend", "backend"], help="Direct mode launch")
    parser.add_argument("--backend-mode", default="unified", help="Backend mode (unified, deepsearch, etc.)")
    parser.add_argument("--port", type=int, help="Port for frontend (default: auto-detect)")
    parser.add_argument("--health-check", action="store_true", help="Run health check only")
    
    args = parser.parse_args()
    
    service_manager = ServiceManager()
    
    try:
        if args.health_check:
            success = service_manager.run_health_check()
            sys.exit(0 if success else 1)
        
        elif args.mode == "frontend":
            print_banner()
            if service_manager.start_frontend(args.port):
                print_info("Press Ctrl+C to stop the service")
                try:
                    # Start monitoring
                    monitor_thread = threading.Thread(target=service_manager.monitor_services, daemon=True)
                    monitor_thread.start()
                    
                    while not service_manager.shutdown_requested and service_manager.running_processes:
                        time.sleep(1)
                except KeyboardInterrupt:
                    pass
                finally:
                    service_manager.stop_all_services()
        
        elif args.mode == "backend":
            print_banner()
            service_manager.start_backend(args.backend_mode)
        
        else:
            # Interactive mode
            service_manager.run_interactive()
    
    except KeyboardInterrupt:
        print_info("\nShutdown requested")
    except Exception as e:
        print_error(f"Startup failed: {e}")
        sys.exit(1)
    finally:
        service_manager.stop_all_services()

if __name__ == "__main__":
    main()
