# 🚀 RepoMaster Deployment Guide

This guide provides comprehensive instructions for deploying RepoMaster with Z.ai API integration.

## 📋 Prerequisites

- **Python 3.8+** (Python 3.13.7 tested and working)
- **Z.ai API Key** (required) - Get from [z.ai/model-api](https://z.ai/model-api)
- **SERPER API Key** (optional) - For enhanced search functionality
- **JINA API Key** (optional) - For document processing

## 🎯 Quick Start (Interactive Setup)

### Option 1: Interactive Deployment (Recommended)

```bash
# Clone the repository
git clone https://github.com/QuantaAlpha/RepoMaster.git
cd RepoMaster

# Run interactive deployment
python deploy.py
```

The interactive deployment will:
1. ✅ Check Python version compatibility
2. 📦 Install required dependencies
3. ⚙️ Set up configuration files
4. 🔑 Guide you through API key configuration
5. ✅ Validate your setup
6. 🚀 Show deployment options

### Option 2: Interactive Launcher

After deployment, use the interactive launcher:

```bash
python start.py
```

This provides a menu-driven interface to:
- 🌐 Launch Web Interface (Streamlit)
- 🤖 Start Unified AI Assistant
- 🔍 Run Deep Search Agent
- 💻 Access General Assistant
- 📁 Use Repository Agent

## 🔧 Manual Setup

If you prefer manual setup:

### 1. Install Dependencies

```bash
pip install streamlit pandas requests python-dotenv beautifulsoup4 pillow openai plotly tqdm joblib networkx humanize gradio
```

Optional packages:
```bash
pip install streamlit_extras genson grep_ast
```

### 2. Configure Environment

```bash
# Copy configuration template
cp configs/env.example configs/.env

# Edit with your API keys
nano configs/.env  # or use your preferred editor
```

### 3. Configure Z.ai API

Edit `configs/.env` and set:

```bash
# Z.ai Configuration (OpenAI-compatible)
OPENAI_API_KEY=your_zai_api_key_here
OPENAI_MODEL=glm-4.5
OPENAI_BASE_URL=https://api.z.ai/api/paas/v4/

# Optional: Enhanced functionality
SERPER_API_KEY=your_serper_api_key_here_optional
JINA_API_KEY=your_jina_api_key_here_optional
```

## 🚀 Deployment Options

### Web Interface (Recommended for Beginners)

```bash
python launcher.py --mode frontend
```

- Access at: http://localhost:8501
- Interactive web dashboard
- Visual interface for all features

### Command Line Interface

#### Unified Assistant (Recommended)
```bash
python launcher.py --mode backend --backend-mode unified
```
- Intelligent multi-agent orchestration
- Automatically routes tasks to appropriate agents

#### Specialized Agents
```bash
# Deep Search Agent
python launcher.py --mode backend --backend-mode deepsearch

# General Programming Assistant
python launcher.py --mode backend --backend-mode general_assistant

# Repository Exploration Agent
python launcher.py --mode backend --backend-mode repository_agent
```

## 🔑 API Key Setup

### Z.ai API Key (Required)

1. Visit [z.ai/model-api](https://z.ai/model-api)
2. Sign up or log in
3. Create an API key
4. Add to your `.env` file as `OPENAI_API_KEY`

### SERPER API Key (Optional)

1. Visit [serper.dev/login](https://serper.dev/login)
2. Sign up and get your API key
3. Add to your `.env` file as `SERPER_API_KEY`

### JINA API Key (Optional)

1. Visit [jina.ai](https://jina.ai/)
2. Sign up and get your API key
3. Add to your `.env` file as `JINA_API_KEY`

## 🐛 Troubleshooting

### Common Issues

#### 1. Missing Dependencies
```bash
# If you see import errors, install missing packages
pip install --upgrade pip
pip install -r requirements.txt
```

#### 2. Python Version Issues
```bash
# Check Python version
python --version

# RepoMaster requires Python 3.8+
# If you have an older version, upgrade Python
```

#### 3. API Key Issues
```bash
# Verify your .env file exists and has the correct format
cat configs/.env

# Make sure OPENAI_API_KEY is set to your actual Z.ai API key
# Not the placeholder "your_zai_api_key_here"
```

#### 4. Port Already in Use (Web Interface)
```bash
# If port 8501 is busy, specify a different port
python launcher.py --mode frontend --streamlit-port 8502
```

### Validation Commands

```bash
# Test configuration
python launcher.py --help

# Check if all dependencies are installed
python -c "import streamlit, pandas, requests, openai; print('All core dependencies installed')"

# Validate environment file
python -c "from dotenv import load_dotenv; import os; load_dotenv('configs/.env'); print('API Key configured:', bool(os.getenv('OPENAI_API_KEY')))"
```

## 🔄 Updating RepoMaster

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Re-run deployment if needed
python deploy.py
```

## 📊 System Requirements

### Minimum Requirements
- **OS**: Windows 10, macOS 10.15, or Linux
- **Python**: 3.8+
- **RAM**: 4GB
- **Storage**: 2GB free space
- **Network**: Internet connection for API calls

### Recommended Requirements
- **Python**: 3.10+
- **RAM**: 8GB+
- **Storage**: 5GB free space
- **Network**: Stable broadband connection

## 🌐 Network Configuration

### Firewall Settings
- **Web Interface**: Allow inbound connections on port 8501 (or your chosen port)
- **API Access**: Allow outbound HTTPS connections to:
  - `api.z.ai` (Z.ai API)
  - `serper.dev` (SERPER API, if used)
  - `jina.ai` (JINA API, if used)

### Proxy Configuration
If you're behind a corporate proxy, set environment variables:
```bash
export HTTP_PROXY=http://your-proxy:port
export HTTPS_PROXY=https://your-proxy:port
```

## 🔒 Security Considerations

1. **API Keys**: Never commit API keys to version control
2. **Environment File**: Keep `configs/.env` secure and private
3. **Network**: Use HTTPS for all API communications
4. **Access**: Restrict web interface access if deployed on a server

## 📈 Performance Optimization

### For Better Performance
1. **Use SSD storage** for faster file operations
2. **Increase RAM** for handling larger repositories
3. **Use stable internet** for reliable API calls
4. **Close unnecessary applications** to free up resources

### Monitoring
- Monitor API usage to stay within rate limits
- Check system resources during heavy operations
- Use the web interface for resource-intensive tasks

## 🆘 Getting Help

1. **Check this guide** for common solutions
2. **Review logs** in the terminal output
3. **Validate configuration** using the commands above
4. **Check API status** at the provider websites
5. **Create an issue** on GitHub with detailed error information

## 📝 Configuration Reference

### Complete .env Example
```bash
# ==============================================================================
# RepoMaster Environment Configuration
# ==============================================================================

# Default API Provider Configuration
DEFAULT_API_PROVIDER=openai

# Search Engine APIs (Optional - for enhanced functionality)
SERPER_API_KEY=your_serper_api_key_here_optional
JINA_API_KEY=your_jina_api_key_here_optional

# Z.ai Configuration (OpenAI-compatible)
OPENAI_API_KEY=your_zai_api_key_here
OPENAI_MODEL=glm-4.5
OPENAI_BASE_URL=https://api.z.ai/api/paas/v4/

# Alternative AI Providers (Optional)
# ANTHROPIC_API_KEY=your_claude_key
# DEEPSEEK_API_KEY=your_deepseek_key
# GEMINI_API_KEY=your_gemini_key
```

---

🎉 **Congratulations!** You've successfully deployed RepoMaster with Z.ai integration. Start exploring GitHub repositories with AI-powered assistance!
