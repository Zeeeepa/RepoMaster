# RepoMaster User Guide

This comprehensive guide provides everything you need to use RepoMaster effectively, from basic configuration to advanced usage patterns.

## 📋 Table of Contents

- [🚀 Getting Started](#-getting-started)
- [🧠 Intelligent Task Processing Engine](#-intelligent-task-processing-engine)
- [💻 Usage Modes](#-usage-modes)
- [🔧 Advanced Usage](#-advanced-usage)
- [📝 Use Cases](#-use-cases)
- [📖 Running Tests](#-running-tests)

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Git
- Internet connection for repository cloning

### Installation
```bash
git clone https://github.com/QuantaAlpha/RepoMaster.git
cd RepoMaster
pip install -r requirements.txt
```

### Basic Configuration

Copy the example configuration file and customize it with your API keys:

```bash
cp configs/env.example configs/.env
# Edit the configuration file with your API keys
nano configs/.env  # or use your preferred editor
```

**Configuration Template** (from `configs/env.example`):
```bash
# Set the default API provider (openai, claude, deepseek, azure_openai)
DEFAULT_API_PROVIDER=openai

# OpenAI Configuration
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-5

# Claude Configuration  
ANTHROPIC_API_KEY=your_claude_key
ANTHROPIC_MODEL=claude-4-sonnet

# DeepSeek Configuration
DEEPSEEK_API_KEY=your_deepseek_key
DEEPSEEK_MODEL=deepseek-v3

# Google Gemini Configuration
GEMINI_API_KEY=your_gemini_key
GEMINI_MODEL=gemini-2.5-pro

# Web Search APIs (Required for deep search functionality)
SERPER_API_KEY=your_serper_key          # For Google search results - Get API key at: https://serper.dev/login
JINA_API_KEY=your_jina_key              # For web content extraction - Get API key at: https://jina.ai/
```

#### ZAI (OpenAI-compatible) quick setup
Option A: use dedicated provider
```bash
DEFAULT_API_PROVIDER=zai
ZAI_API_KEY=your_zai_key
ZAI_MODEL=glm-4.5             # adjust to your proxy’s model id
ZAI_BASE_URL=https://<your-z-proxy>/v1
# Or select at runtime:
python launcher.py --mode backend --backend-mode unified --api-type zai
```
Option B: reuse OpenAI path (no code changes)
```bash
OPENAI_API_KEY=your_zai_key
OPENAI_MODEL=glm-4.5
OPENAI_BASE_URL=https://<your-z-proxy>/v1
```


💡 **Note**: The `configs/env.example` file contains the complete configuration template with all available options and detailed comments.

---

## 🧠 Multi-Agent Intelligence System

<div align="center">

### 🤖 One Interface, All GitHub Resources

> **Simply describe your task in natural language.** RepoMaster automatically finds the right GitHub tools and makes them work together to solve your task.

```bash
python launcher.py --mode backend --backend-mode unified
```

</div>

### 🎯 Intelligent Multi-Agent Orchestration

RepoMaster features a sophisticated **Multi-Agent System** where specialized AI agents work in harmony to deliver optimal solutions. Our intelligent dispatcher automatically routes tasks to the most suitable agent combination:

<div align="center">

| 🔍 **Deep Search Agent** | 💻 **Programming Assistant Agent** | 🏗️ **Repository Exploration Agent** |
|:---:|:---:|:---:|
| **Advanced Search & Web Analysis** | **Code Generation & Programming** | **Repository Understanding & Task Execution** |
| • Advanced web research & data retrieval | • Intelligent code generation | • Autonomous code exploration |
| • Information synthesis & analysis | • Algorithm implementation | • Complex task orchestration |
| • Query optimization | • Debug & code optimization | • Multi-repo coordination |

</div>

#### 🚀 How Multi-Agent System Works

```
👤 User Task Input
     ↓
🧠 AI Intelligent Dispatcher
     ↓
🔀 Task Analysis & Agent Selection
     ↓
┌─────────────────┬─────────────────┬─────────────────┐
│🔍 Deep Search &  │💻 Programming    │🏗️ Repository     │
│ Web Research     │ Assistant        │ Exploration     │
│                 │                 │                 │
│ • Web search     │ • Code generation│ • Repo analysis  │
│ • Data synthesis │ • Algorithm impl │ • Task execution │
│ • Context build  │ • Debug support  │ • Multi-repo ops │
└─────────────────┴─────────────────┴─────────────────┘
     ↓
🎯 Intelligent Result Orchestration
     ↓
✅ Perfect Solution Delivered
```

> **✨ Key Innovation:** No manual agent selection required - our AI dispatcher intelligently combines agents based on task complexity and requirements, ensuring optimal performance for every request.

---

## 💻 Multi-Agent Access Interfaces

### 🤖 Unified Multi-Agent Interface (Recommended)

The primary way to use RepoMaster - one command, all GitHub resources at your service:

```bash
python launcher.py --mode backend --backend-mode unified
```

**Why Unified Multi-Agent Interface?**
- 🧠 **AI-Powered Task Analysis**: Automatically understands your intent
- 🤝 **Intelligent Agent Collaboration**: Seamlessly coordinates multiple agents as needed
- 🎯 **Context-Aware Routing**: Dynamically selects optimal agent combinations
- ⚡ **Zero Configuration**: No manual agent selection required

### 🌐 Web Interface (Visual Multi-Agent Dashboard)

Launch the interactive web interface for visual multi-agent interaction:

```bash
python launcher.py --mode frontend
# Access: http://localhost:8501

# Configure file upload size limit (default: 200MB)
python launcher.py --mode frontend --max-upload-size 500  # Set to 500MB
```

**Multi-Agent Dashboard Features**:
- 🌐 Interactive multi-agent chat interface
- 📁 File upload and management across agents (configurable size limit)
- 👥 Multi-user session support
- 📊 Real-time agent collaboration visualization

### 🔧 Direct Agent Access (Advanced)

For developers who want direct access to individual agents:

<details>
<summary><strong>Individual Agent Interfaces (Click to expand)</strong></summary>

```bash
# Direct access to Deep Search Agent
python launcher.py --mode backend --backend-mode deepsearch

# Direct access to Programming Assistant Agent
python launcher.py --mode backend --backend-mode general_assistant

# Direct access to Repository Exploration Agent
python launcher.py --mode backend --backend-mode repository_agent
```

> 💡 **Note**: These direct agent interfaces are primarily for development, testing, and specialized workflows. For optimal performance and seamless agent collaboration, the unified multi-agent interface is recommended for production use.

</details>

### Shell Script Shortcuts

```bash
# Frontend
bash run.sh frontend

# Backend modes
bash run.sh backend unified
bash run.sh backend deepsearch  
bash run.sh backend general_assistant
bash run.sh backend repository_agent
```

---

## 🔧 Advanced Usage

### Command Line Configuration Options

RepoMaster supports various configuration options to customize your experience:

```bash
# Frontend configuration options
python launcher.py --mode frontend \
  --streamlit-port 8502 \              # Custom port (default: 8501)
  --streamlit-host 0.0.0.0 \           # Custom host (default: localhost)
  --max-upload-size 1000 \             # File upload limit in MB (default: 200)
  --log-level DEBUG                    # Logging level (default: INFO)

# Backend configuration options  
python launcher.py --mode backend --backend-mode unified \
  --api-type openai \                  # API provider (default: basic)
  --temperature 0.1 \                  # Model temperature (default: 0.1)
  --work-dir /custom/path \            # Working directory (default: coding)
  --timeout 300 \                      # Request timeout in seconds (default: 120)
  --max-tokens 8000                    # Maximum token count (default: 4000)
```

**File Upload Size Configuration**:
- Default limit: 200MB
- Range: 1MB - 2000MB (2GB)
- Affects web interface file uploads
- Example: `--max-upload-size 500` sets limit to 500MB

### Basic Programming Interface

```python
from core.agent_scheduler import RepoMasterAgent

# Simple task execution
task = "Transform this portrait into Van Gogh style using content.jpg and style.jpg"
result = repo_master.solve_task_with_repo(task)
```

For detailed programming examples, see our [Documentation](../docs/).

---

## 📝 Use Cases

### 🤖 AI/ML Tasks
**"Train an image classifier on CIFAR-10 dataset using transfer learning"**
>- Automatically finds relevant ML repositories and frameworks
>- Sets up complete training pipeline with best practices
>- Handles data loading, model configuration, and training execution

### 📄 Data Processing  
**"Extract tables from PDF reports and convert to structured CSV format"**
>- Discovers PDF processing libraries and tools
>- Implements extraction pipeline with error handling
>- Outputs clean, structured data in the desired format

### 🌐 Web Development
**"Create a REST API for user authentication with JWT tokens"**
>- Searches for authentication frameworks and security libraries
>- Generates production-ready API with proper security practices
>- Includes documentation and testing examples

### 👁️ Computer Vision
**"Detect and count objects in surveillance video footage"**
>- Finds state-of-the-art object detection models
>- Implements video processing pipeline with optimization
>- Provides detailed analysis results and visualizations

---

## 📖 Running Tests

```bash
# Run configuration tests
python test_config.py

# Run full test suite
pytest tests/

# Run specific benchmark
python -m core.git_task --config configs/gittaskbench.yaml
```

---

## 🤝 Contributing

### Development Environment Setup

```bash
git clone https://github.com/QuantaAlpha/RepoMaster.git
cd RepoMaster
pip install -e ".[dev]"
pre-commit install
```

### Contribution Types

- 🐛 Bug fixes
- ✨ New feature development
- 📚 Documentation improvements
- 🧪 Test case additions
- 🔧 Tools and utilities

---

## 📞 Support

- 📧 **Email**: quantaalpha.ai@gmail.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/QuantaAlpha/RepoMaster/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/QuantaAlpha/RepoMaster/discussions)

---

*Last updated: December 2024*
