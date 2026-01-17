"""
COMPREHENSIVE PYTHON PACKAGING, ENVIRONMENTS & CONTAINERS GUIDE
================================================================
This comprehensive guide covers:
1. Packaging: pip, pipx, pyproject.toml, Semantic Versioning
2. Environments: Virtual environments, dependency pinning, reproducible builds
3. Containers: Docker basics, why containers matter, Python pitfalls
"""

print("=" * 80)
print("PYTHON PACKAGING, ENVIRONMENTS & CONTAINERS")
print("=" * 80)

# ============================================================================
# PART 1: PACKAGING
# ============================================================================

print("\n" + "=" * 35)
print("PACKAGING")
print("=" * 35)

# ----------------------------------------------------------------------------
# 1.1 PIP (Python Package Installer)
# ----------------------------------------------------------------------------
print("\n" + "-" * 20)
print("PIP - PYTHON PACKAGE INSTALLER")
print("-" * 20)

"""
pip is the standard package manager for Python. It installs packages from:
- PyPI (Python Package Index)
- Version control systems (Git, Mercurial)
- Local directories
- Distribution archives
"""

class PIPSimulator:
    """Simulates pip commands and behavior"""
    
    @staticmethod
    def demonstrate_common_commands():
        """Show common pip commands"""
        commands = {
            "install": {
                "description": "Install a package",
                "examples": [
                    "pip install requests",  # Latest version
                    "pip install requests==2.28.1",  # Specific version
                    "pip install requests>=2.20,<3.0",  # Version range
                    "pip install -e .",  # Editable install (development)
                    "pip install -r requirements.txt",  # From requirements file
                    "pip install --user package_name",  # User install
                    "pip install --no-deps package_name",  # No dependencies
                ]
            },
            "uninstall": {
                "description": "Remove a package",
                "examples": [
                    "pip uninstall requests",
                    "pip uninstall -y package_name",  # Auto-confirm
                ]
            },
            "freeze": {
                "description": "Output installed packages in requirements format",
                "examples": [
                    "pip freeze",  # All packages
                    "pip freeze > requirements.txt",  # Save to file
                    "pip freeze --local",  # Only local packages (not system)
                ]
            },
            "list": {
                "description": "List installed packages",
                "examples": [
                    "pip list",  # All packages
                    "pip list --outdated",  # Show outdated packages
                    "pip list --not-required",  # Show not required by others
                    "pip list --format=json",  # JSON output
                ]
            },
            "show": {
                "description": "Show information about a package",
                "examples": [
                    "pip show requests",
                    "pip show -f requests",  # Show files location
                ]
            },
            "search": {
                "description": "Search PyPI for packages",
                "examples": [
                    "pip search 'web framework'",
                ]
            },
            "download": {
                "description": "Download packages without installing",
                "examples": [
                    "pip download requests",
                    "pip download -d ./downloads requests",  # Specific directory
                ]
            },
            "check": {
                "description": "Verify installed packages have compatible dependencies",
                "examples": [
                    "pip check",
                ]
            },
            "cache": {
                "description": "Manage pip cache",
                "examples": [
                    "pip cache list",  # List cache contents
                    "pip cache purge",  # Clear cache
                ]
            }
        }
        
        print("\nCommon pip commands and their usage:")
        for cmd, info in commands.items():
            print(f"\n  {cmd}: {info['description']}")
            for example in info['examples'][:2]:  # Show first 2 examples
                print(f"    $ {example}")
    
    @staticmethod
    def demonstrate_pip_config():
        """Show pip configuration options"""
        print("\n\nPip Configuration Options:")
        
        config_sources = {
            "1. Command Line": "--index-url, --trusted-host, --timeout",
            "2. Environment Variables": "PIP_INDEX_URL, PIP_TRUSTED_HOST",
            "3. User Config": "~/.config/pip/pip.conf (Linux/Mac) or ~/pip/pip.ini (Windows)",
            "4. Global Config": "/etc/pip.conf (Linux/Mac)",
            "5. Virtual Environment": "venv/pip.conf",
        }
        
        for source, example in config_sources.items():
            print(f"  {source}: {example}")
        
        print("\nExample pip.conf:")
        pip_conf_example = """
[global]
index-url = https://pypi.org/simple
trusted-host = pypi.org
               files.pythonhosted.org
timeout = 60

[install]
no-deps = yes

[freeze]
all = yes
        """.strip()
        print(pip_conf_example)


# Run pip demonstration
pip_sim = PIPSimulator()
pip_sim.demonstrate_common_commands()
pip_sim.demonstrate_pip_config()

# ----------------------------------------------------------------------------
# 1.2 PIPX (Python Package Installer for Applications)
# ----------------------------------------------------------------------------
print("\n\n" + "-" * 20)
print("PIPX - APPLICATION INSTALLER")
print("-" * 20)

"""
pipx installs Python applications in isolated environments while making 
their CLI tools globally available. Perfect for tools like black, poetry, etc.
"""

class PIPXSimulator:
    """Simulates pipx commands and behavior"""
    
    @staticmethod
    def demonstrate_common_commands():
        """Show common pipx commands"""
        commands = {
            "install": {
                "description": "Install a Python application in isolated environment",
                "examples": [
                    "pipx install black",  # Install black formatter
                    "pipx install poetry",  # Install poetry package manager
                    "pipx install --python python3.9 package",  # Specific Python version
                    "pipx install --force package",  # Force reinstall
                ]
            },
            "inject": {
                "description": "Add packages to an existing pipx-managed environment",
                "examples": [
                    "pipx inject black click",  # Add click to black's environment
                ]
            },
            "upgrade": {
                "description": "Upgrade a package",
                "examples": [
                    "pipx upgrade black",
                    "pipx upgrade-all",  # Upgrade all packages
                ]
            },
            "uninstall": {
                "description": "Uninstall a package",
                "examples": [
                    "pipx uninstall black",
                ]
            },
            "list": {
                "description": "List installed applications",
                "examples": [
                    "pipx list",  # Show all installed apps
                    "pipx list --include-injected",  # Show injected packages too
                ]
            },
            "run": {
                "description": "Run an app in temporary, isolated environment",
                "examples": [
                    "pipx run black --check .",  # Run without installing
                    "pipx run --spec package_name command",  # Specific version
                ]
            },
            "reinstall": {
                "description": "Reinstall all packages",
                "examples": [
                    "pipx reinstall-all",  # Reinstall all packages
                ]
            }
        }
        
        print("\nCommon pipx commands:")
        for cmd, info in commands.items():
            print(f"\n  {cmd}: {info['description']}")
            for example in info['examples']:
                print(f"    $ {example}")
    
    @staticmethod
    def demonstrate_use_cases():
        """Show when to use pipx vs pip"""
        print("\n\nWhen to use pipx vs pip:")
        
        use_cases = {
            "pipx (Use for)": [
                "Command-line applications/tools (black, poetry, pytest, mypy)",
                "Tools you want globally available but isolated",
                "Avoiding dependency conflicts between tools",
                "Python applications with entry points",
            ],
            "pip (Use for)": [
                "Library dependencies for your projects",
                "Development dependencies",
                "Packages imported in Python code",
                "When working within a virtual environment",
            ]
        }
        
        for tool, cases in use_cases.items():
            print(f"\n  {tool}:")
            for case in cases:
                print(f"    • {case}")
        
        print("\nExample workflow:")
        print("  1. $ pipx install black          # Install black globally")
        print("  2. $ pipx install poetry         # Install poetry globally")
        print("  3. $ black .                     # Use black anywhere")
        print("  4. $ poetry new myproject        # Use poetry anywhere")


# Run pipx demonstration
pipx_sim = PIPXSimulator()
pipx_sim.demonstrate_common_commands()
pipx_sim.demonstrate_use_cases()

# ----------------------------------------------------------------------------
# 1.3 PYPROJECT.TOML (Modern Python Project Configuration)
# ----------------------------------------------------------------------------
print("\n\n" + "-" * 20)
print("PYPROJECT.TOML - MODERN CONFIG")
print("-" * 20)

"""
pyproject.toml is the modern standard for Python project configuration.
It replaces setup.py, setup.cfg, requirements.txt, and more.
"""

class PyProjectTOMLDemo:
    """Demonstrates pyproject.toml structure and features"""
    
    @staticmethod
    def show_complete_example():
        """Show a complete pyproject.toml example"""
        print("\nComplete pyproject.toml example:\n")
        
        example = """[build-system]
# Build system requirements (PEP 518)
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
# Project metadata (PEP 621)
name = "my-awesome-package"
version = "1.0.0"
description = "An awesome Python package"
readme = "README.md"
authors = [
    {name = "John Doe", email = "john@example.com"},
    {name = "Jane Smith", email = "jane@example.com"},
]
maintainers = [
    {name = "Maintainer Team", email = "maintainers@example.com"},
]
license = {text = "MIT"}
keywords = ["awesome", "python", "package"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]
urls = {Homepage = "https://github.com/user/my-awesome-package"}

# Dependencies
dependencies = [
    "requests>=2.25.0",
    "click>=8.0.0",
    "pydantic>=1.8.0",
]

# Optional dependencies (extras)
[project.optional-dependencies]
dev = [
    "pytest>=6.0",
    "black>=22.0",
    "mypy>=0.900",
    "flake8>=4.0",
]
docs = [
    "sphinx>=4.0",
    "sphinx-rtd-theme>=1.0",
]
gui = [
    "pyqt5>=5.15",
    "matplotlib>=3.5",
]

# Entry points (CLI commands, plugins, etc.)
[project.scripts]
mycli = "my_package.cli:main"

[project.gui-scripts]
myapp = "my_package.gui:main"

[project.entry-points."pytest11"]
myplugin = "my_package.plugin"

# URLs for dynamic version, etc.
[tool.setuptools.dynamic]
version = {attr = "my_package.__version__"}

# Package discovery
[tool.setuptools.packages.find]
where = ["src"]
include = ["my_package*"]
exclude = ["my_package.tests*"]

# Testing configuration
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra -q"
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"

# Code formatting (black)
[tool.black]
line-length = 88
target-version = ['py38', 'py39', 'py310', 'py311']
include = '\\.pyi?$'
extend-exclude = '''
/(
  \\.eggs
  | \\.git
  | \\.hg
  | \\.mypy_cache
  | \\.tox
  | \\.venv
  | _build
  | buck-out
  | build
  | dist
)/
'''

# Type checking (mypy)
[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

# Linting (flake8)
[tool.flake8]
max-line-length = 88
extend-ignore = ["E203", "W503"]
exclude = [".git", "__pycache__", "build", "dist", "*.egg-info"]

# Coverage
[tool.coverage.run]
source = ["my_package"]
omit = ["*/tests/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
]

# Documentation (Sphinx)
[tool.sphinx]
source_dir = "docs/source"
build_dir = "docs/build"
"""

        print(example)
    
    @staticmethod
    def demonstrate_section_explanations():
        """Explain key sections of pyproject.toml"""
        print("\n\nKey sections explained:")
        
        sections = {
            "[build-system]": {
                "purpose": "Declares build backend and requirements",
                "importance": "Required by PEP 518 for modern builds",
                "example": 'requires = ["setuptools>=61.0", "wheel"]'
            },
            "[project]": {
                "purpose": "Package metadata and dependencies (PEP 621)",
                "importance": "Replaces setup.py and setup.cfg",
                "includes": "name, version, dependencies, entry-points"
            },
            "[project.optional-dependencies]": {
                "purpose": "Define extra/optional dependencies",
                "usage": "Install with: pip install package[dev,docs]",
                "example": "dev = ['pytest', 'black']"
            },
            "[tool.*] sections": {
                "purpose": "Tool-specific configurations",
                "examples": "tool.black, tool.mypy, tool.pytest",
                "benefit": "Centralized configuration for all tools"
            }
        }
        
        for section, info in sections.items():
            print(f"\n  {section}:")
            for key, value in info.items():
                print(f"    {key}: {value}")


# Run pyproject.toml demonstration
pyproject_demo = PyProjectTOMLDemo()
pyproject_demo.show_complete_example()
pyproject_demo.demonstrate_section_explanations()

# ----------------------------------------------------------------------------
# 1.4 SEMANTIC VERSIONING (SemVer)
# ----------------------------------------------------------------------------
print("\n\n" + "-" * 20)
print("SEMANTIC VERSIONING")
print("-" * 20)

"""
Semantic Versioning (SemVer) is a versioning scheme: MAJOR.MINOR.PATCH
MAJOR: Incompatible API changes
MINOR: New functionality (backward compatible)
PATCH: Bug fixes (backward compatible)
"""

class SemanticVersioning:
    """Demonstrates Semantic Versioning principles"""
    
    @staticmethod
    def explain_version_scheme():
        """Explain the SemVer scheme"""
        print("\nSemantic Versioning Format: MAJOR.MINOR.PATCH")
        
        scheme = {
            "MAJOR version (X.0.0)": {
                "when": "Incompatible API changes",
                "examples": [
                    "Removing deprecated functions",
                    "Changing function signatures",
                    "Breaking changes to public API",
                    "Major architectural changes"
                ],
                "user_impact": "Users must update their code"
            },
            "MINOR version (0.Y.0)": {
                "when": "New functionality in backward-compatible manner",
                "examples": [
                    "Adding new functions/classes",
                    "Adding optional parameters",
                    "New features",
                    "Performance improvements"
                ],
                "user_impact": "Safe to upgrade, new features available"
            },
            "PATCH version (0.0.Z)": {
                "when": "Backward-compatible bug fixes",
                "examples": [
                    "Fixing bugs in existing functionality",
                    "Security patches",
                    "Documentation updates",
                    "Internal refactoring"
                ],
                "user_impact": "Safe to upgrade, recommended for all users"
            }
        }
        
        for version_type, info in scheme.items():
            print(f"\n  {version_type}:")
            print(f"    When to increment: {info['when']}")
            print(f"    Examples:")
            for example in info['examples'][:2]:
                print(f"      • {example}")
            print(f"    User impact: {info['user_impact']}")
    
    @staticmethod
    def demonstrate_version_constraints():
        """Show how to specify version constraints"""
        print("\n\nVersion Constraints in Python:")
        
        constraints = {
            "Exact version": "package==1.2.3",
            "Compatible release (~=)": "package~=1.2.3  # >=1.2.3,<1.3.0",
            "Version range": "package>=1.2.0,<2.0.0",
            "Minimum version": "package>=1.2.0",
            "Maximum version": "package<=2.0.0",
            "Wildcard": "package==1.2.*  # Any patch version of 1.2",
            "Not equal": "package!=1.2.3",
        }
        
        for description, example in constraints.items():
            print(f"  {description:25} → {example}")
    
    @staticmethod
    def show_real_world_examples():
        """Show real-world versioning examples"""
        print("\n\nReal-world versioning examples:")
        
        examples = [
            ("requests", "2.28.1", "Major=2, Minor=28, Patch=1"),
            ("django", "4.1.3", "Major=4, Minor=1, Patch=3"),
            ("numpy", "1.23.5", "Major=1, Minor=23, Patch=5"),
            ("pandas", "1.5.0", "Major=1, Minor=5, Patch=0"),
        ]
        
        for package, version, explanation in examples:
            print(f"  {package:10} {version:10} → {explanation}")
        
        print("\nVersion constraint examples in pyproject.toml:")
        constraint_examples = """
# Good practices:
dependencies = [
    "requests>=2.25.0,<3.0.0",    # Allow minor updates, block breaking changes
    "click~=8.0.0",              # Allow patch updates only
    "pytest>=7.0.0",             # Minimum version
]

# For libraries (more flexible):
dependencies = [
    "requests>=2.25.0",          # Allow future major versions (users decide)
]

# For applications (more strict):
dependencies = [
    "requests==2.28.1",          # Exact version for reproducibility
]
        """.strip()
        print(constraint_examples)


# Run semantic versioning demonstration
semver = SemanticVersioning()
semver.explain_version_scheme()
semver.demonstrate_version_constraints()
semver.show_real_world_examples()

# ============================================================================
# PART 2: ENVIRONMENTS
# ============================================================================

print("\n" + "=" * 35)
print("ENVIRONMENTS")
print("=" * 35)

# ----------------------------------------------------------------------------
# 2.1 VIRTUAL ENVIRONMENTS
# ----------------------------------------------------------------------------
print("\n" + "-" * 20)
print("VIRTUAL ENVIRONMENTS")
print("-" * 20)

"""
Virtual environments isolate Python installations and packages.
Each project gets its own environment with specific dependencies.
"""

class VirtualEnvironments:
    """Demonstrates virtual environment usage"""
    
    @staticmethod
    def demonstrate_creation_methods():
        """Show different ways to create virtual environments"""
        print("\nCreating Virtual Environments:")
        
        methods = {
            "venv (Standard Library)": {
                "command": "python -m venv venv",
                "activation_linux": "source venv/bin/activate",
                "activation_windows": "venv\\Scripts\\activate",
                "deactivation": "deactivate",
                "when_to_use": "Standard method, Python 3.3+"
            },
            "virtualenv (Third-party)": {
                "command": "virtualenv venv",
                "activation": "Same as venv",
                "features": "Faster, more features than venv",
                "when_to_use": "Need extra features or Python 2"
            },
            "conda (Anaconda/Miniconda)": {
                "command": "conda create -n myenv python=3.9",
                "activation": "conda activate myenv",
                "features": "Cross-platform, non-Python packages too",
                "when_to_use": "Data science, mixed language projects"
            },
            "pipenv": {
                "command": "pipenv install",
                "activation": "pipenv shell",
                "features": "Combines pip + virtualenv + dependency management",
                "when_to_use": "Simple dependency management"
            },
            "poetry": {
                "command": "poetry install",
                "activation": "poetry shell",
                "features": "Modern dependency and package management",
                "when_to_use": "Package development with pyproject.toml"
            }
        }
        
        for tool, info in methods.items():
            print(f"\n  {tool}:")
            for key, value in info.items():
                print(f"    {key}: {value}")
    
    @staticmethod
    def show_workflow_example():
        """Show complete virtual environment workflow"""
        print("\n\nComplete Virtual Environment Workflow:")
        
        workflow = """
# 1. Create project directory
mkdir myproject
cd myproject

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Linux/Mac:
source venv/bin/activate
# Windows:
# venv\\Scripts\\activate

# 4. Verify Python path
which python  # Should point to venv/bin/python
python --version

# 5. Upgrade pip in the virtual environment
pip install --upgrade pip

# 6. Install project dependencies
pip install requests pandas numpy

# 7. Freeze dependencies
pip freeze > requirements.txt

# 8. Work on your project
# ... write code ...

# 9. Deactivate when done
deactivate

# 10. Reactivate next time
source venv/bin/activate
        """.strip()
        
        print(workflow)
    
    @staticmethod
    def demonstrate_venv_structure():
        """Show virtual environment directory structure"""
        print("\n\nVirtual Environment Structure:")
        
        structure = """
venv/
├── bin/                    # Scripts directory (Linux/Mac)
│   ├── python             # Python interpreter
│   ├── python3            # Python 3 interpreter
│   ├── pip                # Package installer
│   ├── activate           # Activation script
│   └── ...                # Other installed command-line tools
├── Scripts/               # Scripts directory (Windows)
│   ├── python.exe
│   ├── pip.exe
│   ├── activate.bat
│   └── ...
├── lib/                   # Installed packages
│   └── python3.9/
│       └── site-packages/
│           ├── requests/
│           ├── numpy/
│           └── ...
├── include/               # C headers
├── pyvenv.cfg            # Configuration file
└── ...
        """.strip()
        
        print(structure)


# Run virtual environment demonstration
venv_demo = VirtualEnvironments()
venv_demo.demonstrate_creation_methods()
venv_demo.show_workflow_example()
venv_demo.demonstrate_venv_structure()

# ----------------------------------------------------------------------------
# 2.2 DEPENDENCY PINNING
# ----------------------------------------------------------------------------
print("\n\n" + "-" * 20)
print("DEPENDENCY PINNING")
print("-" * 20)

"""
Dependency pinning ensures reproducible installations by specifying exact versions.
"""

class DependencyPinning:
    """Demonstrates dependency pinning strategies"""
    
    @staticmethod
    def demonstrate_pinning_levels():
        """Show different levels of dependency pinning"""
        print("\nDependency Pinning Strategies:")
        
        strategies = {
            "No Pinning (Dangerous)": {
                "example": "requests",
                "risk": "Breaking changes, non-reproducible builds",
                "use_case": "Library development only"
            },
            "Major Version Pinning": {
                "example": "requests>=2.0.0,<3.0.0",
                "risk": "Minor updates might introduce bugs",
                "use_case": "Libraries, allow minor updates"
            },
            "Minor Version Pinning": {
                "example": "requests>=2.28.0,<2.29.0",
                "risk": "Miss security patches in newer minor versions",
                "use_case": "Applications, balance stability and updates"
            },
            "Exact Pinning": {
                "example": "requests==2.28.1",
                "risk": "Miss all updates including security",
                "use_case": "Production applications, maximum stability"
            },
            "Hash Pinning": {
                "example": "requests==2.28.1 --hash=sha256:abc123...",
                "risk": "Very strict, requires hash updates",
                "use_case": "High security requirements, reproducible builds"
            }
        }
        
        for strategy, info in strategies.items():
            print(f"\n  {strategy}:")
            print(f"    Example: {info['example']}")
            print(f"    Risk: {info['risk']}")
            print(f"    Use case: {info['use_case']}")
    
    @staticmethod
    def demonstrate_requirements_files():
        """Show different requirements file formats"""
        print("\n\nRequirements File Formats:")
        
        print("\n1. requirements.txt (Basic):")
        basic_req = """
# Exact versions for production
requests==2.28.1
pandas==1.5.0
numpy==1.23.5

# With hashes for security
django==4.1.3 \
    --hash=sha256:abc123... \
    --hash=sha256:def456...
        """.strip()
        print(basic_req)
        
        print("\n\n2. requirements-dev.txt (Development):")
        dev_req = """
-r requirements.txt  # Include production dependencies

# Development tools
pytest==7.2.0
black==22.12.0
flake8==6.0.0
mypy==0.991
        """.strip()
        print(dev_req)
        
        print("\n\n3. Constraints File (requirements.in + pip-compile):")
        print("requirements.in (human-written):")
        requirements_in = """
requests>=2.25.0
pandas>=1.5.0
numpy>=1.23.0
        """.strip()
        print(requirements_in)
        
        print("\nrequirements.txt (generated by pip-compile):")
        requirements_txt = """
#
# This file is autogenerated by pip-compile with python 3.9
# To update, run:
#
#    pip-compile requirements.in
#
click==8.1.3
    # via requests
numpy==1.23.5
pandas==1.5.0
    # via
    #   -r requirements.in
    #   (other dependencies)
python-dateutil==2.8.2
    # via pandas
pytz==2022.7
    # via pandas
requests==2.28.1
    # via -r requirements.in
urllib3==1.26.13
    # via requests
        """.strip()
        print(requirements_txt)


# Run dependency pinning demonstration
pinning_demo = DependencyPinning()
pinning_demo.demonstrate_pinning_levels()
pinning_demo.demonstrate_requirements_files()

# ----------------------------------------------------------------------------
# 2.3 REPRODUCIBLE BUILDS
# ----------------------------------------------------------------------------
print("\n\n" + "-" * 20)
print("REPRODUCIBLE BUILDS")
print("-" * 20)

"""
Reproducible builds ensure the same dependencies are installed everywhere.
"""

class ReproducibleBuilds:
    """Demonstrates reproducible build techniques"""
    
    @staticmethod
    def demonstrate_tools_and_techniques():
        """Show tools for reproducible builds"""
        print("\nTools for Reproducible Builds:")
        
        tools = {
            "pip-tools": {
                "purpose": "Compile requirements from .in files",
                "commands": [
                    "pip install pip-tools",
                    "pip-compile requirements.in",
                    "pip-compile requirements-dev.in",
                    "pip-sync requirements.txt requirements-dev.txt"
                ],
                "benefit": "Deterministic dependency resolution"
            },
            "poetry": {
                "purpose": "Modern dependency management",
                "commands": [
                    "poetry install",  # Install with lock file
                    "poetry update",   # Update dependencies
                    "poetry lock",     # Generate/update lock file
                    "poetry export --without-hashes > requirements.txt"
                ],
                "benefit": "pyproject.toml + poetry.lock for consistency"
            },
            "pipenv": {
                "purpose": "Pip + virtualenv management",
                "commands": [
                    "pipenv install",  # Install from Pipfile
                    "pipenv install --dev",  # Install dev dependencies
                    "pipenv lock",     # Generate Pipfile.lock
                    "pipenv sync"      # Install exactly from lock file
                ],
                "benefit": "Simple, integrated solution"
            },
            "conda-lock": {
                "purpose": "Lock files for conda",
                "commands": [
                    "conda-lock -f environment.yml",
                    "conda-lock install --name myenv conda-lock.yml"
                ],
                "benefit": "Reproducible conda environments"
            },
            "docker": {
                "purpose": "Containerization",
                "commands": [
                    "docker build -t myapp .",
                    "docker run myapp"
                ],
                "benefit": "Complete environment isolation"
            }
        }
        
        for tool, info in tools.items():
            print(f"\n  {tool}:")
            print(f"    Purpose: {info['purpose']}")
            print(f"    Commands:")
            for cmd in info['commands'][:2]:
                print(f"      $ {cmd}")
            print(f"    Benefit: {info['benefit']}")
    
    @staticmethod
    def show_poetry_lock_example():
        """Show poetry.lock file structure"""
        print("\n\nPoetry Lock File Example (poetry.lock):")
        
        # Simplified lock file example
        lock_example = """
# This file is automatically generated by Poetry and should not be changed manually.

[[package]]
name = "requests"
version = "2.28.1"
description = "Python HTTP for Humans."
category = "main"
optional = false
python-versions = ">=3.7"
files = [
    {file = "requests-2.28.1-py3-none-any.whl", hash = "sha256:8fefa2a1a1365bf6c4aede6f8c5c2dacf9dc2c768c528e4d05445a2c0d3dc3d9"},
    {file = "requests-2.28.1.tar.gz", hash = "sha256:8fefa2a1a1365bf6c4aede6f8c5c2dacf9dc2c768c528e4d05445a2c0d3dc3d9"},
]

[package.dependencies]
certifi = ">=2017.4.17"
charset-normalizer = ">=2,<3"
idna = ">=2.5,<4"
urllib3 = ">=1.21.1,<1.27"

[[package]]
name = "urllib3"
version = "1.26.13"
description = "HTTP library with thread-safe connection pooling, file post, and more."
category = "main"
optional = false
python-versions = ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*"
files = [
    {file = "urllib3-1.26.13-py2.py3-none-any.whl", hash = "sha256:47cc0d1f6c6d7f9c8a6d0f5d8c9c6c4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1"},
    {file = "urllib3-1.26.13.tar.gz", hash = "sha256:47cc0d1f6c6d7f9c8a6d0f5d8c9c6c4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1"},
]

[metadata]
lock-version = "2.0"
python-versions = "^3.8"
content-hash = "abc123def456ghi789"
        """.strip()
        
        print(lock_example)
    
    @staticmethod
    def demonstrate_best_practices():
        """Show best practices for reproducible builds"""
        print("\n\nBest Practices for Reproducible Builds:")
        
        practices = [
            "1. Always use lock files (poetry.lock, Pipfile.lock, requirements.txt with exact versions)",
            "2. Pin all dependencies, including transitive dependencies",
            "3. Use hash checking where security is critical",
            "4. Separate development and production dependencies",
            "5. Document the Python version explicitly",
            "6. Use Docker for ultimate reproducibility",
            "7. Keep build environment consistent (CI/CD matches production)",
            "8. Regularly update dependencies in controlled manner",
            "9. Use dependency vulnerability scanners",
            "10. Test with dependency updates before deploying"
        ]
        
        for practice in practices:
            print(f"  {practice}")


# Run reproducible builds demonstration
reproducible_demo = ReproducibleBuilds()
reproducible_demo.demonstrate_tools_and_techniques()
reproducible_demo.show_poetry_lock_example()
reproducible_demo.demonstrate_best_practices()

# ============================================================================
# PART 3: CONTAINERS (CONCEPTUAL)
# ============================================================================

print("\n" + "=" * 35)
print("CONTAINERS")
print("=" * 35)

# ----------------------------------------------------------------------------
# 3.1 DOCKER BASICS
# ----------------------------------------------------------------------------
print("\n" + "-" * 20)
print("DOCKER BASICS")
print("-" * 20)

"""
Docker containers package applications with all dependencies.
Containers are lightweight, portable, and consistent across environments.
"""

class DockerBasics:
    """Demonstrates Docker concepts and usage for Python"""
    
    @staticmethod
    def explain_key_concepts():
        """Explain Docker key concepts"""
        print("\nDocker Key Concepts:")
        
        concepts = {
            "Container": "A running instance of a Docker image (like an object from a class)",
            "Image": "A read-only template with instructions for creating a container",
            "Dockerfile": "A text file with instructions to build a Docker image",
            "Docker Hub": "A registry of Docker images (like GitHub for Docker)",
            "Volume": "Persistent storage for containers",
            "Network": "Isolated network for containers to communicate",
            "Compose": "Tool for defining and running multi-container applications",
            "Registry": "A storage and distribution system for Docker images"
        }
        
        for concept, definition in concepts.items():
            print(f"  {concept:20} → {definition}")
    
    @staticmethod
    def show_python_dockerfile_examples():
        """Show different Dockerfile examples for Python"""
        print("\n\nPython Dockerfile Examples:")
        
        print("\n1. Basic Python Dockerfile:")
        basic_dockerfile = """
# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Copy requirements first (caching optimization)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "app.py"]
        """.strip()
        print(basic_dockerfile)
        
        print("\n\n2. Multi-stage Build (Production Optimized):")
        multi_stage_dockerfile = """
# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim AS runtime

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create non-root user
RUN useradd -m -u 1000 appuser
USER appuser

WORKDIR /app

# Copy application
COPY --chown=appuser:appuser . .

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi:app"]
        """.strip()
        print(multi_stage_dockerfile)
        
        print("\n\n3. Development Dockerfile:")
        dev_dockerfile = """
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements-dev.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-dev.txt

# Copy application code
COPY . .

# Mount volume for live reload
VOLUME ["/app"]

# Command for development
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
        """.strip()
        print(dev_dockerfile)
    
    @staticmethod
    def demonstrate_docker_commands():
        """Show common Docker commands"""
        print("\n\nCommon Docker Commands:")
        
        commands = {
            "Build": {
                "docker build -t myapp:latest .": "Build image from Dockerfile",
                "docker build -f Dockerfile.dev -t myapp:dev .": "Build with specific Dockerfile",
            },
            "Run": {
                "docker run myapp:latest": "Run container from image",
                "docker run -p 8000:8000 myapp": "Map port 8000",
                "docker run -v $(pwd):/app myapp": "Mount current directory",
                "docker run -e VAR=value myapp": "Set environment variable",
                "docker run -d myapp": "Run in detached mode",
            },
            "Management": {
                "docker ps": "List running containers",
                "docker ps -a": "List all containers",
                "docker images": "List images",
                "docker stop container_id": "Stop container",
                "docker rm container_id": "Remove container",
                "docker rmi image_id": "Remove image",
            },
            "Logs & Inspection": {
                "docker logs container_id": "View container logs",
                "docker exec -it container_id bash": "Enter running container",
                "docker inspect container_id": "Inspect container details",
            },
            "Compose": {
                "docker-compose up": "Start services",
                "docker-compose up -d": "Start in background",
                "docker-compose down": "Stop services",
                "docker-compose logs": "View logs",
            }
        }
        
        for category, cmds in commands.items():
            print(f"\n  {category}:")
            for cmd, desc in cmds.items():
                print(f"    $ {cmd:45} # {desc}")


# Run Docker basics demonstration
docker_demo = DockerBasics()
docker_demo.explain_key_concepts()
docker_demo.show_python_dockerfile_examples()
docker_demo.demonstrate_docker_commands()

# ----------------------------------------------------------------------------
# 3.2 WHY CONTAINERS MATTER
# ----------------------------------------------------------------------------
print("\n\n" + "-" * 20)
print("WHY CONTAINERS MATTER")
print("-" * 20)

class ContainerBenefits:
    """Explains why containers are important"""
    
    @staticmethod
    def demonstrate_benefits():
        """Show benefits of using containers"""
        print("\nBenefits of Using Containers:")
        
        benefits = {
            "Consistency": {
                "description": "Same environment everywhere (dev, test, prod)",
                "example": "No more 'works on my machine' problems",
                "impact": "Reduced deployment failures"
            },
            "Isolation": {
                "description": "Applications run in isolated environments",
                "example": "Different Python versions per app on same server",
                "impact": "No dependency conflicts"
            },
            "Portability": {
                "description": "Run anywhere Docker is installed",
                "example": "Local machine → Cloud → On-premises",
                "impact": "Vendor lock-in avoidance"
            },
            "Scalability": {
                "description": "Easy to scale horizontally",
                "example": "Kubernetes can manage thousands of containers",
                "impact": "Handles traffic spikes gracefully"
            },
            "Resource Efficiency": {
                "description": "Lightweight compared to VMs",
                "example": "Multiple containers on single OS kernel",
                "impact": "Better server utilization"
            },
            "Version Control": {
                "description": "Images are versioned and immutable",
                "example": "Rollback to previous image if issues",
                "impact": "Reliable deployments"
            },
            "CI/CD Integration": {
                "description": "Seamless integration with pipelines",
                "example": "Build once, deploy anywhere",
                "impact": "Faster delivery"
            },
            "Security": {
                "description": "Isolation provides security boundaries",
                "example": "Container escape requires kernel exploit",
                "impact": "Better security posture"
            }
        }
        
        for benefit, info in benefits.items():
            print(f"\n  {benefit}:")
            print(f"    Description: {info['description']}")
            print(f"    Example: {info['example']}")
            print(f"    Impact: {info['impact']}")
    
    @staticmethod
    def show_before_after_scenario():
        """Show before/after container adoption"""
        print("\n\nBefore Containers (Traditional Deployment):")
        before = """
1. Developer writes code on Mac with Python 3.9
2. Tests pass locally
3. Code pushed to Git
4. CI server (Ubuntu) tries to build
5. Fails because system Python is 3.8
6. Sysadmin manually installs Python 3.9
7. Build passes, but needs libxml2
8. More manual installation...
9. Finally deploys to production (CentOS)
10. Production has different glibc version
11. Application crashes
        """.strip()
        print(before)
        
        print("\n\nAfter Containers (Containerized Deployment):")
        after = """
1. Developer writes code with Dockerfile
2. Tests in container locally
3. Code pushed to Git
4. CI server builds Docker image
5. Same image tested in CI
6. Image pushed to registry
7. Production pulls same image
8. Runs exactly as tested
9. No environment issues
        """.strip()
        print(after)
    
    @staticmethod
    def demonstrate_use_cases():
        """Show when to use containers"""
        print("\n\nWhen to Use Containers:")
        
        use_cases = [
            ("Microservices", "Each service in its own container"),
            ("CI/CD Pipelines", "Consistent build/test environments"),
            ("Multi-tenant Applications", "Isolate customer data/processing"),
            ("Legacy Application Modernization", "Containerize old apps"),
            ("Development Environments", "Quick onboarding, no setup"),
            ("Batch Processing", "Run jobs in isolated containers"),
            ("Testing", "Test different configurations easily"),
            ("Hybrid Cloud", "Consistent deployment across clouds")
        ]
        
        for use_case, description in use_cases:
            print(f"  • {use_case:30} → {description}")


# Run container benefits demonstration
container_benefits = ContainerBenefits()
container_benefits.demonstrate_benefits()
container_benefits.show_before_after_scenario()
container_benefits.demonstrate_use_cases()

# ----------------------------------------------------------------------------
# 3.3 PYTHON IN CONTAINERS PITFALLS
# ----------------------------------------------------------------------------
print("\n\n" + "-" * 20)
print("PYTHON IN CONTAINERS: PITFALLS")
print("-" * 20)

class PythonContainerPitfalls:
    """Demonstrates common Python container pitfalls and solutions"""
    
    @staticmethod
    def demonstrate_common_pitfalls():
        """Show common Python container pitfalls"""
        print("\nCommon Python Container Pitfalls:")
        
        pitfalls = {
            "1. Not Using Python Optimized Base Images": {
                "problem": "Using python:latest instead of python:slim or python:alpine",
                "example": "python:latest is ~1GB, python:slim is ~100MB",
                "solution": "Use python:3.11-slim or python:3.11-alpine",
                "explanation": "Smaller images = faster builds, deployments, and reduced attack surface"
            },
            "2. Running as Root": {
                "problem": "Containers run as root by default",
                "risk": "Container escape could give root on host",
                "solution": "Create non-root user in Dockerfile",
                "example": """
RUN useradd -m -u 1000 appuser
USER appuser
                """.strip()
            },
            "3. Not Setting PYTHONUNBUFFERED": {
                "problem": "Python output is buffered in containers",
                "symptom": "No logs visible until buffer fills",
                "solution": "ENV PYTHONUNBUFFERED=1",
                "explanation": "Ensures logs are visible immediately in container logs"
            },
            "4. Installing System Dependencies Improperly": {
                "problem": "Not cleaning apt cache after install",
                "issue": "Image size bloated with unnecessary files",
                "solution": "Combine RUN commands and clean cache",
                "example": """
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
                """.strip()
            },
            "5. Copying Entire Directory Early": {
                "problem": "COPY . . before RUN pip install",
                "issue": "Cache invalidation on every code change",
                "solution": "Copy requirements first, then code",
                "example": """
COPY requirements.txt .        # Layer 1: Dependencies
RUN pip install -r requirements.txt
COPY . .                      # Layer 2: Application code
                """.strip()
            },
            "6. Not Using Multi-stage Builds": {
                "problem": "Build tools and source code in final image",
                "issue": "Large images, security risks from build tools",
                "solution": "Use multi-stage builds",
                "benefit": "Final image contains only runtime dependencies"
            },
            "7. Hardcoding Configuration": {
                "problem": "Configuration values in Dockerfile",
                "issue": "Need to rebuild for different environments",
                "solution": "Use environment variables or config files",
                "example": "Use -e DATABASE_URL=... when running container"
            },
            "8. Not Setting Resource Limits": {
                "problem": "Containers can consume all host resources",
                "risk": "Denial of service, noisy neighbor",
                "solution": "Set memory and CPU limits",
                "example": "docker run --memory=512m --cpus=1.0 myapp"
            },
            "9. Storing Data in Containers": {
                "problem": "Data lost when container stops",
                "issue": "Containers are ephemeral",
                "solution": "Use volumes or bind mounts",
                "example": "docker run -v mydata:/data myapp"
            },
            "10. Not Handling Signals Properly": {
                "problem": "Python doesn't handle SIGTERM by default",
                "issue": "Graceful shutdown not possible",
                "solution": "Use exec form of CMD and handle signals",
                "example": "CMD ['python', 'app.py'] instead of CMD python app.py"
            }
        }
        
        for pitfall_num, info in pitfalls.items():
            print(f"\n  {pitfall_num}: {list(info.keys())[0]}")
            for key, value in info.items():
                if key != pitfall_num:
                    print(f"    {key.capitalize()}: {value}")
    
    @staticmethod
    def show_best_practices_dockerfile():
        """Show a Dockerfile with all best practices"""
        print("\n\nPython Dockerfile with Best Practices:")
        
        best_practices_dockerfile = """
# Stage 1: Builder
FROM python:3.11-slim AS builder

# Set build-time arguments
ARG DEBIAN_FRONTEND=noninteractive

# Install system dependencies and clean up in single RUN
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim AS runtime

# Install runtime system dependencies only
RUN apt-get update && apt-get install -y \
    libpq5 \
    # Add other runtime deps here \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup -u 1000 appuser
USER appuser

# Set Python environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

# Set working directory
WORKDIR /app

# Copy application code (as non-root user)
COPY --chown=appuser:appgroup . .

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=2)" \
    || exit 1

# Expose port
EXPOSE 8000

# Use exec form for proper signal handling
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "app.main:app"]
        """.strip()
        
        print(best_practices_dockerfile)
    
    @staticmethod
    def demonstrate_docker_compose_example():
        """Show a Docker Compose example"""
        print("\n\nDocker Compose Example (docker-compose.yml):")
        
        docker_compose_example = """
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - REDIS_URL=redis://redis:6379/0
      - DEBUG=${DEBUG:-false}
    env_file:
      - .env
    volumes:
      - ./app:/app  # For development hot-reload
      - static_volume:/app/static
    depends_on:
      - db
      - redis
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=mydb
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data

  celery:
    build: .
    command: celery -A app.tasks worker --loglevel=info
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
  redis_data:
  static_volume:
        """.strip()
        
        print(docker_compose_example)


# Run Python container pitfalls demonstration
pitfalls_demo = PythonContainerPitfalls()
pitfalls_demo.demonstrate_common_pitfalls()
pitfalls_demo.show_best_practices_dockerfile()
pitfalls_demo.demonstrate_docker_compose_example()

# ============================================================================
# SUMMARY & INTEGRATION
# ============================================================================

print("\n" + "=" * 80)
print("INTEGRATED WORKFLOW EXAMPLE")
print("=" * 80)

class IntegratedWorkflow:
    """Shows complete integrated workflow using all concepts"""
    
    @staticmethod
    def demonstrate_complete_workflow():
        """Show complete workflow from development to deployment"""
        print("\nComplete Development-to-Deployment Workflow:\n")
        
        workflow = """
1. PROJECT SETUP
   $ mkdir myproject && cd myproject
   $ python -m venv venv
   $ source venv/bin/activate
   $ pip install --upgrade pip

2. PACKAGE MANAGEMENT WITH POETRY
   $ pip install poetry
   $ poetry init  # Creates pyproject.toml
   $ poetry add requests pandas numpy
   $ poetry add --dev pytest black mypy
   $ poetry install  # Creates poetry.lock

3. DEVELOPMENT
   $ poetry shell  # Activate virtual environment
   $ code .        # Open in VS Code
   # Write code following Semantic Versioning
   # Tests run in consistent environment

4. DOCKERIZE APPLICATION
   # Create Dockerfile with best practices
   # Create docker-compose.yml for multi-service setup
   $ docker build -t myapp:latest .
   $ docker-compose up -d

5. CI/CD PIPELINE
   # .github/workflows/ci.yml runs:
   # - Build Docker image
   # - Run tests in container
   # - Push to registry on main branch
   # - Deploy to production

6. PRODUCTION DEPLOYMENT
   $ docker pull myapp:latest
   $ docker run -d \
     --name myapp \
     --memory=512m \
     --cpus=1.0 \
     -p 8000:8000 \
     -e DATABASE_URL=... \
     myapp:latest

7. MONITORING & MAINTENANCE
   # Use docker logs, docker stats
   # Update dependencies with poetry update
   # Rebuild and redeploy with new version
        """.strip()
        
        print(workflow)


# Run integrated workflow demonstration
workflow_demo = IntegratedWorkflow()
workflow_demo.demonstrate_complete_workflow()

print("\n" + "=" * 80)
print("KEY TAKEAWAYS")
print("=" * 80)

takeaways = """
PACKAGING:
----------
• Use pip for libraries, pipx for applications
• pyproject.toml is the modern standard (replaces setup.py, requirements.txt)
• Follow Semantic Versioning: MAJOR.MINOR.PATCH
• Version constraints: == (exact), ~= (compatible), >= (minimum)

ENVIRONMENTS:
-------------
• Always use virtual environments (venv, poetry, pipenv)
• Pin dependencies for reproducibility
• Use lock files (poetry.lock, Pipfile.lock)
• Separate dev and production dependencies

CONTAINERS:
-----------
• Docker provides consistent environments
• Use multi-stage builds for smaller images
• Never run as root in containers
• Set resource limits and health checks
• Handle Python-specific issues (PYTHONUNBUFFERED, signal handling)

BEST PRACTICES SUMMARY:
-----------------------
1. Start with poetry and pyproject.toml
2. Use virtual environments always
3. Pin dependencies with lock files
4. Use Docker for deployment consistency
5. Follow Semantic Versioning
6. Write comprehensive Dockerfiles
7. Use Docker Compose for development
8. Implement health checks
9. Set resource limits
10. Monitor and update regularly
"""

print(takeaways)

print("\n" + "=" * 80)
print("DEMONSTRATION COMPLETE")
print("=" * 80)