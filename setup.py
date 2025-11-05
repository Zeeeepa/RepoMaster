#!/usr/bin/env python3
"""
RepoMaster Setup Script
Enables pip install -e . for development installation
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "RepoMaster: AI-powered GitHub repository assistant"

# Read requirements from requirements-minimal.txt for Python 3.13 compatibility
def read_requirements():
    # Try minimal requirements first for Python 3.13 compatibility
    minimal_requirements_path = os.path.join(os.path.dirname(__file__), 'requirements-minimal.txt')
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    
    # Use minimal requirements if available
    target_file = minimal_requirements_path if os.path.exists(minimal_requirements_path) else requirements_path
    
    requirements = []
    if os.path.exists(target_file):
        with open(target_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if line and not line.startswith('#'):
                    # Handle version specifiers
                    if '~=' in line:
                        line = line.replace('~=', '>=')
                    requirements.append(line)
    return requirements

setup(
    name="repomaster",
    version="1.0.0",
    description="AI-powered GitHub repository assistant",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="RepoMaster Team",
    author_email="support@repomaster.ai",
    url="https://github.com/Zeeeepa/RepoMaster",
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Version Control :: Git",
    ],
    entry_points={
        'console_scripts': [
            'repomaster=launcher:main',
            'repomaster-start=start:main',
            'repomaster-deploy=deploy:main',
        ],
    },
    package_data={
        'repomaster': [
            'configs/*.py',
            'configs/*.example',
            'src/**/*.py',
            'docs/**/*',
            '.streamlit/*',
        ],
    },
    zip_safe=False,
)
