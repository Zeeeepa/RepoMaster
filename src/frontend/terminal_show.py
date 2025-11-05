#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import the comprehensive encoding solution
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# Import and configure encoding
try:
    from src.utils.encoding_config import safe_print, configure_console_encoding, is_utf8_available
    # Configure console encoding at module import
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


def print_repomaster_title():

    repomaster_logo = r"""
 ██████╗ ███████╗██████╗  ██████╗ ███╗   ███╗ █████╗ ███████╗████████╗███████╗██████╗ 
 ██╔══██╗██╔════╝██╔══██╗██╔═══██╗████╗ ████║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗
 ██████╔╝█████╗  ██████╔╝██║   ██║██╔████╔██║███████║███████╗   ██║   █████╗  ██████╔╝
 ██╔══██╗██╔══╝  ██╔═══╝ ██║   ██║██║╚██╔╝██║██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗
 ██║  ██║███████╗██║     ╚██████╔╝██║ ╚═╝ ██║██║  ██║███████║   ██║   ███████╗██║  ██║
 ╚═╝  ╚═╝╚══════╝╚═╝      ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝"""
    
    subtitle = "🚀 Autonomous Exploration & Understanding of GitHub Repositories for Complex Task Solving"
    
    safe_print("\n\n======================================================================\n")
    safe_print(repomaster_logo)
    safe_print("\n" + subtitle)
    safe_print("\n======================================================================\n")


def print_progressive_startup_panel(env_status, api_status, config):
    """Print a progressive startup panel with status updates"""
    import time
    
    safe_print("\n🔄 Initializing...\n")
    
    print_optimized_startup_sequence(env_status, api_status, config)
    
    # Progress bar
    safe_print("\n[████████████████████████████████████████] 100%\n")
    
    print_repomaster_title()


def print_optimized_startup_sequence(env_status, api_status, config):
    """Print optimized startup sequence with proper status indicators"""
    import time
    
    # Step 1: Environment Setup
    if env_status.get('env_loaded', False):
        step1_msg = "[1/4] 📁 Environment Setup... ✅ Loaded from " + str(env_status.get('env_path', 'config'))
        safe_print("\033[32m" + step1_msg + "\033[0m")
    else:
        step1_msg = "[1/4] 📁 Environment Setup... ❌ Failed to load .env"
        safe_print("\033[31m" + step1_msg + "\033[0m")
    
    time.sleep(0.3)
    
    # Step 2: API Configuration
    if api_status.get('configured', False):
        provider = api_status.get('provider', 'Unknown')
        model = api_status.get('model', 'Unknown')
        step2_msg = f"[2/4] 🔑 API Configuration... ✅ {provider} {model}"
        safe_print("\033[32m" + step2_msg + "\033[0m")
    else:
        step2_msg = "[2/4] 🔑 API Configuration... ❌ Not configured"
        safe_print("\033[31m" + step2_msg + "\033[0m")
    
    time.sleep(0.3)
    
    # Step 3: Service Configuration
    mode = getattr(config, 'mode', 'Unknown')
    work_dir = str(getattr(config, 'work_dir', 'Unknown'))
    if hasattr(config, 'streamlit_port'):
        service_info = f"Web Interface, Work: ...{work_dir[-20:]}" if len(work_dir) > 20 else f"Web Interface, Work: {work_dir}"
    else:
        backend_mode = getattr(config, 'backend_mode', 'Unknown')
        service_info = f"{backend_mode.title()} Assistant, Work: ...{work_dir[-20:]}" if len(work_dir) > 20 else f"{backend_mode.title()} Assistant, Work: {work_dir}"
    
    step3_msg = f"[3/4] ⚙️  Service Configuration... ✅ {service_info}"
    safe_print("\033[32m" + step3_msg + "\033[0m")
    
    time.sleep(0.3)
    
    # Step 4: Service Launch
    step4_msg = "[4/4] 🚀 Service Launch... ✅ Ready!"
    safe_print("\033[32m" + step4_msg + "\033[0m")
    
    time.sleep(0.5)


def print_quick_start_guide():
    """Print the quick start guide"""
    guide = """
╔═══════════════════════════════════ Quick Start ═══════════════════════════════════╗
║                                                                                    ║
║  🖥️  Frontend Mode (Web Interface):                                               ║
║      python launcher.py --mode frontend --streamlit-port 8501                     ║
║      Access: http://localhost:8501                                                ║
║                                                                                    ║
║  🤖 Backend Mode (Unified AI Assistant) ⭐ Recommended:                          ║
║      python launcher.py --mode backend --backend-mode unified                     ║
║                                                                                    ║
║  📝 Shell Script Shortcuts:                                                       ║
║      bash run.sh frontend           # Launch web interface                        ║
║      bash run.sh backend unified    # Run unified assistant                       ║
║                                                                                    ║
╚════════════════════════════════════════════════════════════════════════════════════╝"""
    
    safe_print(guide)


def print_health_check_results(results):
    """Print health check results with proper formatting"""
    safe_print("\n" + "="*50)
    safe_print("🏥 SYSTEM HEALTH CHECK RESULTS")
    safe_print("="*50)
    
    for category, status in results.items():
        if status.get('status') == 'ok':
            safe_print(f"✅ {category}: {status.get('message', 'OK')}")
        elif status.get('status') == 'warning':
            safe_print(f"⚠️  {category}: {status.get('message', 'Warning')}")
        else:
            safe_print(f"❌ {category}: {status.get('message', 'Error')}")
    
    safe_print("="*50)


def print_deployment_summary(fixes_applied, success=True):
    """Print deployment summary"""
    safe_print("\n🎯 Deployment Summary")
    safe_print("="*50)
    
    if fixes_applied:
        safe_print("\n✅ Fixes Applied:")
        for fix in fixes_applied:
            safe_print(f"  • {fix}")
    
    if success:
        safe_print("\n🎉 Deployment Successful!")
        safe_print("\n🚀 Ready to launch RepoMaster:")
        safe_print("  • Frontend: python launcher.py --mode frontend")
        safe_print("  • Backend:  python launcher.py --mode backend --backend-mode unified")
        safe_print("  • Interactive: python start.py")
    else:
        safe_print("\n❌ Deployment Failed!")
        safe_print("Please check the error messages above and try again.")


def print_mode_selection_menu():
    """Print the mode selection menu"""
    safe_print("\n🎯 Choose RepoMaster Mode")
    safe_print("Select how you want to run RepoMaster:\n")
    
    options = [
        ("0.", "🏥 Health Check", "Check system health and dependencies"),
        ("1.", "🌐 Web Interface (Streamlit)", "Launch the web-based dashboard"),
        ("2.", "🤖 Unified AI Assistant", "Intelligent multi-agent orchestration"),
        ("3.", "🔍 Deep Search Agent", "Specialized repository search and analysis"),
        ("4.", "💻 General Assistant", "Programming and development assistance"),
        ("5.", "📁 Repository Agent", "Repository exploration and understanding"),
        ("6.", "❓ Help", "Show detailed help information"),
        ("7.", "⚙️  Reconfigure", "Run deployment setup again"),
        ("8.", "🚪 Exit", "Exit the launcher")
    ]
    
    for num, title, desc in options:
        safe_print(f"\033[96m{num}\033[0m {title}")
        safe_print(f"   {desc}\n")


def print_status_message(message, status_type="info"):
    """Print a status message with appropriate formatting"""
    colors = {
        "info": "\033[96m",      # Cyan
        "success": "\033[92m",   # Green
        "warning": "\033[93m",   # Yellow
        "error": "\033[91m",     # Red
        "reset": "\033[0m"       # Reset
    }
    
    color = colors.get(status_type, colors["info"])
    safe_print(f"{color}{message}{colors['reset']}")


def print_error_message(error_msg):
    """Print an error message with proper formatting"""
    safe_print(f"\033[91m❌ {error_msg}\033[0m")


def print_success_message(success_msg):
    """Print a success message with proper formatting"""
    safe_print(f"\033[92m✅ {success_msg}\033[0m")


def print_info_message(info_msg):
    """Print an info message with proper formatting"""
    safe_print(f"\033[96mℹ️  {info_msg}\033[0m")


def print_warning_message(warning_msg):
    """Print a warning message with proper formatting"""
    safe_print(f"\033[93m⚠️  {warning_msg}\033[0m")


def print_separator(char="=", length=50):
    """Print a separator line"""
    safe_print(char * length)


def print_header(title, char="=", length=50):
    """Print a header with title"""
    safe_print(char * length)
    safe_print(f" {title} ")
    safe_print(char * length)


def print_footer():
    """Print a footer message"""
    safe_print("\n" + "="*50)
    safe_print("Thank you for using RepoMaster! 🚀")
    safe_print("="*50)

# Additional functions needed by launcher.py
def print_repomaster_cli():
    """Print CLI banner"""
    print_repomaster_title()

def print_startup_banner():
    """Print startup banner"""
    print_repomaster_title()

def print_environment_status(status):
    """Print environment status"""
    safe_print(f"Environment Status: {'✅' if status else '❌'}")

def print_api_config_status(status):
    """Print API configuration status"""
    safe_print(f"API Configuration: {'✅' if status else '❌'}")

def print_launch_config(config):
    """Print launch configuration"""
    safe_print(f"Launch Configuration: {config}")

def print_service_starting():
    """Print service starting message"""
    safe_print("🚀 Starting service...")

def print_unified_mode_welcome():
    """Print unified mode welcome message"""
    safe_print("🤖 Unified AI Assistant Mode")

def print_mode_welcome(mode):
    """Print mode welcome message"""
    safe_print(f"🎯 {mode} Mode")
