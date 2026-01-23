"""
COMPREHENSIVE PYTHON MODULES AND PACKAGES DEMONSTRATION
This script demonstrates Python modules, packages, imports, and virtual environments.
"""

print("=" * 70)
print("PYTHON MODULES, PACKAGES, AND VIRTUAL ENVIRONMENTS")
print("=" * 70)

# ============================================================================
# SECTION 1: INTRODUCTION TO MODULES
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 1: INTRODUCTION TO MODULES")
print("=" * 60)

print("""
1.1 What are Modules?

A module in Python is simply a file containing Python definitions and statements.
Modules allow you to:
- Organize code logically
- Reuse code across multiple programs
- Avoid naming conflicts
- Make code more maintainable

Every Python file (.py) is a module that can be imported.
Modules can contain:
- Functions
- Classes
- Variables
- Executable code
""")

# Let's first create some example modules to demonstrate importing
print("\n1.2 Creating example module files for demonstration...")

# We'll create these modules in memory for demonstration
# In practice, these would be separate .py files

# Create module1.py content
module1_content = '''
"""
Module 1: A simple module with functions and variables.
"""

# Module-level variable
MODULE_NAME = "Module 1"

# Function definitions
def greet(name):
    """Return a greeting message."""
    return f"Hello, {name}! Welcome to {MODULE_NAME}."

def calculate_square(n):
    """Calculate the square of a number."""
    return n ** 2

# Class definition
class Calculator:
    """A simple calculator class."""
    
    def __init__(self):
        self.history = []
    
    def add(self, a, b):
        """Add two numbers."""
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def get_history(self):
        """Get calculation history."""
        return self.history.copy()

# Executable code that runs when module is executed directly
if __name__ == "__main__":
    print(f"This is {MODULE_NAME}")
    print(greet("Developer"))
'''

# Create module2.py content
module2_content = '''
"""
Module 2: Another module with different functionality.
"""

# This variable might conflict with module1
MODULE_NAME = "Module 2"

def multiply(a, b):
    """Multiply two numbers."""
    return a * b

def calculate_cube(n):
    """Calculate the cube of a number."""
    return n ** 3

# Special variable
__version__ = "1.0.0"
'''

# Create a simple package structure
package_structure = '''
# This would be a directory structure:
# mypackage/
# │
# ├── __init__.py          # Package initialization
# ├── math_utils.py        # Module 1 in package
# ├── string_utils.py      # Module 2 in package
# └── subpackage/
#     ├── __init__.py
#     └── advanced.py
'''

print("   Example module structure created for demonstration.")

# ============================================================================
# SECTION 2: IMPORT STYLES
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 2: IMPORT STYLES")
print("=" * 60)

print("2.1 Different Ways to Import:")

# Since we can't actually create separate files, we'll simulate importing
# by creating the modules in the current namespace
exec(module1_content)
exec(module2_content)

# ----------------------------------------------------------------------------
# BASIC IMPORT
# ----------------------------------------------------------------------------
print("\n2.2 Basic Import (import module):")
print("""
# Import the entire module
import math

# Use module.attribute syntax
result = math.sqrt(25)
""")

# Simulate importing math module
import math
print(f"   math.sqrt(25) = {math.sqrt(25)}")

# ----------------------------------------------------------------------------
# IMPORT WITH ALIAS
# ----------------------------------------------------------------------------
print("\n" + "2.3 Import with Alias (import module as alias):")
print("""
# Import with an alias (shorter or non-conflicting name)
import numpy as np
import pandas as pd
""")

import math as m
print(f"   m.pi = {m.pi}")

# ----------------------------------------------------------------------------
# IMPORT SPECIFIC ITEMS
# ----------------------------------------------------------------------------
print("\n" + "2.4 Import Specific Items (from module import item):")
print("""
# Import specific functions/variables
from math import sqrt, pi

# Use directly without module prefix
result = sqrt(16)
""")

from math import sqrt, pi
print(f"   sqrt(16) = {sqrt(16)}")
print(f"   pi = {pi}")

# ----------------------------------------------------------------------------
# IMPORT WITH ALIAS FOR SPECIFIC ITEMS
# ----------------------------------------------------------------------------
print("\n" + "2.5 Import Specific Items with Alias:")
print("""
# Import with alias for specific items
from math import sqrt as square_root
""")

from math import sqrt as square_root
print(f"   square_root(9) = {square_root(9)}")

# ----------------------------------------------------------------------------
# IMPORT MULTIPLE ITEMS
# ----------------------------------------------------------------------------
print("\n" + "2.6 Import Multiple Items:")
print("""
# Import multiple items
from math import sqrt, pi, sin, cos
""")

from math import sqrt, pi, sin, cos
print(f"   sin(pi/2) = {sin(pi/2)}")

# ----------------------------------------------------------------------------
# IMPORT EVERYTHING (GENERALLY NOT RECOMMENDED)
# ----------------------------------------------------------------------------
print("\n" + "2.7 Import Everything (from module import *):")
print("""
# Import all names from module
from math import *

# Use functions directly
result = sqrt(25) + sin(pi/2)

WARNING: This can lead to namespace pollution and naming conflicts!
Use sparingly and only when you know what you're importing.
""")

# ----------------------------------------------------------------------------
# RELATIVE IMPORTS (FOR PACKAGES)
# ----------------------------------------------------------------------------
print("\n" + "2.8 Relative Imports (within packages):")
print("""
# Inside a package, you can use relative imports
# mypackage/string_utils.py:
from .math_utils import add_numbers    # Import from sibling module
from ..other_package import some_func  # Import from parent package
""")

# ============================================================================
# SECTION 3: NAMESPACES AND NAME CONFLICTS
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 3: NAMESPACES AND NAME CONFLICTS")
print("=" * 60)

print("""
3.1 Understanding Namespaces:

Each module has its own namespace. When you import a module, you're
accessing objects in that module's namespace.
""")

# Demonstrate namespaces
print("\n3.2 Module Namespaces in Action:")

# Import our simulated modules
print("   Importing our example modules...")

# Execute the modules to create their content in separate namespaces
# We'll use dictionaries to simulate separate module namespaces
namespace1 = {}
namespace2 = {}
exec(module1_content, namespace1)
exec(module2_content, namespace2)

print(f"   Module 1 namespace contains: {list(namespace1.keys())[:5]}...")
print(f"   Module 2 namespace contains: {list(namespace2.keys())[:5]}...")

# Show that MODULE_NAME exists in both but with different values
print(f"\n   Both modules have 'MODULE_NAME':")
print(f"   Module 1 MODULE_NAME: {namespace1['MODULE_NAME']}")
print(f"   Module 2 MODULE_NAME: {namespace2['MODULE_NAME']}")

# Demonstrate name conflicts
print("\n3.3 Name Conflict Example:")

def local_function():
    return "This is a local function"

# Simulate importing everything from a module (bad practice)
print("""
   # What happens with conflicting names:
   
   from module1 import *
   from module2 import *
   
   # Now we have two different MODULE_NAME variables!
   # The last import wins
""")

# Demonstrate with our simulated modules
from_module1 = {k: v for k, v in namespace1.items() if not k.startswith('__')}
from_module2 = {k: v for k, v in namespace2.items() if not k.startswith('__')}

# Simulate the namespace after imports
global_namespace = {}
global_namespace.update(from_module1)  # First import
global_namespace.update(from_module2)  # Second import overwrites

print(f"   After importing both modules, MODULE_NAME = '{global_namespace.get('MODULE_NAME')}'")

print("\n3.4 Avoiding Name Conflicts:")
print("""
Best practices to avoid name conflicts:

1. Use explicit imports with module prefix:
   import module1
   import module2
   
   print(module1.MODULE_NAME)
   print(module2.MODULE_NAME)

2. Use aliases:
   import module1 as m1
   import module2 as m2

3. Import only what you need:
   from module1 import MODULE_NAME as MODULE1_NAME
   from module2 import MODULE_NAME as MODULE2_NAME

4. Avoid 'from module import *'
""")

# ============================================================================
# SECTION 4: __name__ == "__main__" PATTERN
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 4: __name__ == '__main__' PATTERN")
print("=" * 60)

print("""
4.1 Understanding __name__:

Every Python module has a special attribute called __name__.
It tells us how the module is being used:

- If a module is being run directly: __name__ == "__main__"
- If a module is being imported: __name__ == module's filename

This allows us to write code that behaves differently when
run directly vs when imported as a module.
""")

print("\n4.2 Current Module's __name__:")
print(f"   In this script, __name__ = '{__name__}'")

# ----------------------------------------------------------------------------
# PRACTICAL EXAMPLE
# ----------------------------------------------------------------------------
print("\n4.3 Practical Example of __name__ == '__main__':")

# Create a reusable module with test code
example_module_code = '''
"""
example_calculator.py - A reusable calculator module.
"""

def add(a, b):
    """Add two numbers."""
    return a + b

def subtract(a, b):
    """Subtract b from a."""
    return a - b

def multiply(a, b):
    """Multiply two numbers."""
    return a * b

def divide(a, b):
    """Divide a by b."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# Test functions that should only run when module is executed directly
def run_tests():
    """Run tests for calculator functions."""
    print("Running tests...")
    assert add(2, 3) == 5
    assert subtract(5, 2) == 3
    assert multiply(3, 4) == 12
    assert divide(10, 2) == 5
    print("All tests passed!")

# This code only runs when the module is executed directly
if __name__ == "__main__":
    print(f"Running {__name__} directly")
    run_tests()
    
    # Also provide a simple interactive interface
    print("\nInteractive mode:")
    try:
        a = float(input("Enter first number: "))
        b = float(input("Enter second number: "))
        print(f"{a} + {b} = {add(a, b)}")
        print(f"{a} - {b} = {subtract(a, b)}")
        print(f"{a} * {b} = {multiply(a, b)}")
        if b != 0:
            print(f"{a} / {b} = {divide(a, b)}")
        else:
            print("Cannot divide by zero")
    except ValueError:
        print("Please enter valid numbers")
'''

print("""
   Example module structure:
   
   example_calculator.py:
   
   # ... function definitions ...
   
   def run_tests():
       # Test code here
       pass
   
   if __name__ == "__main__":
       # This runs only when file is executed directly
       run_tests()
       # Could also have CLI interface here
""")

# Execute the example to show the pattern
example_namespace = {}
exec(example_module_code, example_namespace)

print("\n   When imported, __name__ != '__main__', so tests don't run automatically.")
print("   When run directly, __name__ == '__main__', so tests execute.")

# Demonstrate importing vs running
print("\n4.4 Simulating Different Execution Modes:")

# Simulate what happens when module is imported
print("\n   Simulation: Module is imported")
print("   (Only function definitions are available, tests don't run)")

# Access functions from the "imported" module
print(f"   example_namespace['add'](5, 3) = {example_namespace['add'](5, 3)}")

# Simulate what happens when module is run directly
print("\n   Simulation: Module is run directly")
print("   (Tests would run, interactive mode would start)")

# To demonstrate, we could manually trigger the __main__ block
if False:  # Change to True to see it in action
    print("\n   Manually triggering __main__ block:")
    if '__main__' in example_namespace:
        # In real module execution, Python would run this automatically
        pass

print("\n4.5 Common Use Cases for __name__ == '__main__':")
print("""
1. UNIT TESTS: Run tests when module is executed directly
2. DEMO/EXAMPLES: Provide example usage
3. COMMAND-LINE INTERFACE: Create CLI tools
4. SCRIPT FUNCTIONALITY: Make file both importable and executable
5. CONFIGURATION: Different behavior for script vs module mode
""")

# ============================================================================
# SECTION 5: PYTHON PATH BASICS
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 5: PYTHON PATH BASICS")
print("=" * 60)

print("""
5.1 What is Python Path?

Python Path (PYTHONPATH) is a list of directories that Python searches
when looking for modules to import. When you import a module, Python:

1. Checks built-in modules
2. Searches directories in sys.path
3. Searches directories in PYTHONPATH environment variable
""")

# ----------------------------------------------------------------------------
# DEMONSTRATING PYTHON PATH
# ----------------------------------------------------------------------------
print("\n5.2 Viewing and Modifying sys.path:")

import sys

print("   Current sys.path (where Python looks for modules):")
for i, path in enumerate(sys.path[:10]):  # Show first 10
    print(f"   [{i}] {path}")

if len(sys.path) > 10:
    print(f"   ... and {len(sys.path) - 10} more directories")

print("\n   Important directories in sys.path:")
print("   1. Current directory (empty string or '.') - where script runs")
print("   2. Python's standard library paths")
print("   3. Site-packages directory (for pip-installed packages)")
print("   4. Directories in PYTHONPATH environment variable")

# ----------------------------------------------------------------------------
# ADDING TO PYTHON PATH
# ----------------------------------------------------------------------------
print("\n5.3 Adding Directories to Python Path:")

print("""
Ways to add directories to Python's search path:

1. Environment variable (persistent):
   export PYTHONPATH="/my/modules:$PYTHONPATH"  # Linux/Mac
   set PYTHONPATH=C:\\my\\modules;%PYTHONPATH%    # Windows

2. Modify sys.path at runtime (temporary):
   import sys
   sys.path.insert(0, "/path/to/my/modules")
   
3. Using .pth files in site-packages
4. Through IDE/editor settings
""")

# Demonstrate adding a path
original_path_length = len(sys.path)
new_path = "/tmp/my_python_modules"

print(f"\n   Before adding: sys.path has {original_path_length} entries")

# Add a new path (temporarily for this script)
sys.path.insert(0, new_path)
print(f"   After adding '{new_path}': sys.path has {len(sys.path)} entries")
print(f"   New first entry: {sys.path[0]}")

# Remove it to avoid side effects
sys.path.pop(0)

# ----------------------------------------------------------------------------
# HOW IMPORT WORKS STEP BY STEP
# ----------------------------------------------------------------------------
print("\n5.4 How Import Works Step by Step:")

print("""
When Python executes 'import mymodule':

1. Check if module is already loaded (sys.modules cache)
2. If not cached, search for module in this order:
   a. Built-in modules
   b. Current directory
   c. Directories in sys.path
   d. Directories in PYTHONPATH
3. If found:
   a. Create a new module object
   b. Execute the module's code in the module's namespace
   c. Add module to sys.modules cache
   d. Create a name in current namespace pointing to module
4. If not found: raise ModuleNotFoundError
""")

# ============================================================================
# SECTION 6: PACKAGES
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 6: PACKAGES")
print("=" * 60)

print("""
6.1 What are Packages?

Packages are a way of organizing related modules into a directory hierarchy.
A package is essentially a directory containing:

1. Python modules (.py files)
2. A special __init__.py file (can be empty)
3. Can contain sub-packages (subdirectories with their own __init__.py)

This creates a namespace hierarchy: package.module.function
""")

# ----------------------------------------------------------------------------
# PACKAGE STRUCTURE EXAMPLE
# ----------------------------------------------------------------------------
print("\n6.2 Example Package Structure:")

package_structure_detailed = """
myproject/
│
├── README.md
├── setup.py
├── requirements.txt
│
└── mypackage/                    # Main package directory
    ├── __init__.py              # Package initialization
    ├── utils.py                 # Utility functions
    ├── math_operations.py       # Math-related functions
    ├── data_processing.py       # Data processing functions
    │
    ├── models/                  # Sub-package
    │   ├── __init__.py
    │   ├── linear_model.py
    │   └── neural_network.py
    │
    └── visualization/           # Another sub-package
        ├── __init__.py
        ├── plots.py
        └── charts.py
"""

print(package_structure_detailed)

# ----------------------------------------------------------------------------
# __init__.py FILES
# ----------------------------------------------------------------------------
print("\n6.3 The __init__.py File:")

print("""
The __init__.py file makes a directory a Python package.
It can be empty or can contain:

1. Package initialization code
2. Convenience imports to expose submodules
3. Package-level variables and constants
4. Version information
5. Any code that should run when package is imported

Python 3.3+ supports "namespace packages" without __init__.py,
but explicit packages with __init__.py are still recommended.
""")

print("\n6.4 Example __init__.py files:")

init_example1 = """
# mypackage/__init__.py - Simple version

__version__ = "1.0.0"
__author__ = "Your Name"

# Convenience imports
from .utils import helper_function
from .math_operations import add, multiply

# Package initialization
print(f"Initializing mypackage version {__version__}")
"""

init_example2 = """
# mypackage/models/__init__.py - More complex example

# Control what gets imported with 'from models import *'
__all__ = ['LinearModel', 'NeuralNetwork']

# Import model classes
from .linear_model import LinearModel
from .neural_network import NeuralNetwork

# Package metadata
MODEL_TYPES = ['linear', 'neural']
"""

print("   Example 1 - Simple package __init__.py:")
print(init_example1[:200] + "...")

print("\n   Example 2 - Subpackage __init__.py with __all__:")
print(init_example2[:200] + "...")

# ----------------------------------------------------------------------------
# IMPORTING FROM PACKAGES
# ----------------------------------------------------------------------------
print("\n6.5 Importing from Packages:")

print("""
Different ways to import from packages:

1. Import entire package:
   import mypackage
   # Use: mypackage.utils.helper_function()

2. Import specific module from package:
   from mypackage import utils
   # Use: utils.helper_function()

3. Import from module in package:
   from mypackage.utils import helper_function
   # Use: helper_function()

4. Import from subpackage:
   from mypackage.models.linear_model import LinearModel
   
5. Relative imports (inside package):
   # In mypackage/utils.py:
   from . import math_operations  # Import sibling
   from ..other_package import x  # Import from parent
   from .models import LinearModel  # Import from subpackage
""")

# ============================================================================
# SECTION 7: VIRTUAL ENVIRONMENTS (venv)
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 7: VIRTUAL ENVIRONMENTS (venv)")
print("=" * 60)

print("""
7.1 Why Virtual Environments?

Virtual environments solve the "dependency hell" problem:
- Different projects need different package versions
- System-wide Python packages can conflict
- Reproducibility across different machines
- Isolation from system Python

A virtual environment is an isolated Python environment with:
- Its own Python interpreter
- Its own package directory
- Its own installed packages
- Isolated from system packages
""")

# ----------------------------------------------------------------------------
# CREATING VIRTUAL ENVIRONMENTS
# ----------------------------------------------------------------------------
print("\n7.2 Creating Virtual Environments:")

print("""
Using venv (built into Python 3.3+):

1. Create a virtual environment:
   python -m venv myenv

2. This creates a 'myenv' directory with:
   myenv/
   ├── bin/           # Scripts (Linux/Mac)
   ├── Scripts/       # Scripts (Windows)
   ├── lib/           # Python packages
   └── pyvenv.cfg    # Configuration

3. Activate the environment:
   Linux/Mac: source myenv/bin/activate
   Windows: myenv\\Scripts\\activate.bat
   
4. Deactivate when done:
   deactivate
""")

# ----------------------------------------------------------------------------
# ALTERNATIVES TO VENV
# ----------------------------------------------------------------------------
print("\n7.3 Alternatives to venv:")

print("""
1. virtualenv: Older tool, similar to venv but works with Python 2
2. conda: Package manager that also handles environments
3. pipenv: Combines pip and virtualenv with better dependency management
4. poetry: Modern dependency management and packaging tool
5. pyenv: For managing multiple Python versions (not exactly virtualenv)
""")

# ----------------------------------------------------------------------------
# PRACTICAL VENV EXAMPLE
# ----------------------------------------------------------------------------
print("\n7.4 Practical Virtual Environment Example:")

print("""
Project workflow with virtual environment:

1. Create project directory:
   mkdir myproject && cd myproject

2. Create virtual environment:
   python -m venv venv

3. Activate virtual environment:
   # Linux/Mac:
   source venv/bin/activate
   
   # Windows:
   venv\\Scripts\\activate

4. Install project dependencies:
   pip install requests numpy pandas

5. Freeze dependencies to requirements.txt:
   pip freeze > requirements.txt

6. Work on project...

7. Deactivate when done:
   deactivate

8. On another machine, recreate environment:
   python -m venv venv
   source venv/bin/activate  # or activate on Windows
   pip install -r requirements.txt
""")

# ----------------------------------------------------------------------------
# DEMONSTRATING VENV CONCEPTS
# ----------------------------------------------------------------------------
print("\n7.5 Demonstrating Virtual Environment Concepts:")

import os
import subprocess
import sys

print("   Current Python interpreter:")
print(f"   Executable: {sys.executable}")
print(f"   Version: {sys.version}")
print(f"   Prefix: {sys.prefix}")

print("\n   How to check if you're in a virtual environment:")
print("   1. Check sys.prefix != sys.base_prefix")
print(f"      In virtual env? {sys.prefix != sys.base_prefix}")
print("   2. Check for VIRTUAL_ENV environment variable")
print(f"      VIRTUAL_ENV env var: {os.environ.get('VIRTUAL_ENV', 'Not set')}")

print("\n   Package installation locations:")
print(f"   Site-packages: {sys.path[-1]}")

# ============================================================================
# SECTION 8: CREATING AND USING YOUR OWN MODULES/PACKAGES
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 8: CREATING AND USING YOUR OWN MODULES/PACKAGES")
print("=" * 60)

# ----------------------------------------------------------------------------
# CREATING A SIMPLE MODULE
# ----------------------------------------------------------------------------
print("\n8.1 Creating a Simple Module:")

# Create a simple module file
geometry_module = '''
"""
geometry.py - A module for geometric calculations.
"""

import math

__version__ = "1.0.0"

def circle_area(radius):
    """Calculate area of a circle."""
    if radius < 0:
        raise ValueError("Radius cannot be negative")
    return math.pi * radius ** 2

def rectangle_area(length, width):
    """Calculate area of a rectangle."""
    if length < 0 or width < 0:
        raise ValueError("Dimensions cannot be negative")
    return length * width

def triangle_area(base, height):
    """Calculate area of a triangle."""
    if base < 0 or height < 0:
        raise ValueError("Dimensions cannot be negative")
    return 0.5 * base * height

# Optional: Demo code that runs when module is executed directly
if __name__ == "__main__":
    print(f"Geometry Module v{__version__}")
    print("Testing functions:")
    print(f"  Circle area (r=5): {circle_area(5):.2f}")
    print(f"  Rectangle area (5x3): {rectangle_area(5, 3)}")
    print(f"  Triangle area (base=6, height=4): {triangle_area(6, 4)}")
'''

print("   geometry.py module code:")
print(geometry_module[:300] + "...")

# ----------------------------------------------------------------------------
# CREATING A PACKAGE
# ----------------------------------------------------------------------------
print("\n8.2 Creating a Package:")

# Show what the package directory structure would look like
print("""
   Creating a 'shapes' package:
   
   shapes/
   ├── __init__.py
   ├── two_dimensional.py
   ├── three_dimensional.py
   └── constants.py
""")

# Show __init__.py for the shapes package
shapes_init = '''
"""
shapes package - Geometric shape calculations.
"""

__version__ = "1.0.0"
__author__ = "Geometry Team"

# Import commonly used functions for convenience
from .two_dimensional import circle_area, rectangle_area
from .three_dimensional import sphere_volume, cube_volume
from .constants import PI, GOLDEN_RATIO

# Control what gets imported with 'from shapes import *'
__all__ = [
    'circle_area',
    'rectangle_area', 
    'sphere_volume',
    'cube_volume',
    'PI',
    'GOLDEN_RATIO'
]

print(f"Shapes package v{__version__} loaded")
'''

print("\n   shapes/__init__.py:")
print(shapes_init[:200] + "...")

# ----------------------------------------------------------------------------
# USING YOUR MODULES AND PACKAGES
# ----------------------------------------------------------------------------
print("\n8.3 Using Your Modules and Packages:")

print("""
Assuming your project structure:

my_project/
├── main.py
├── geometry.py          # Single module
└── shapes/             # Package
    ├── __init__.py
    ├── two_dimensional.py
    └── three_dimensional.py
""")

print("""
In main.py, you can import and use them:

# Import single module
import geometry
print(geometry.circle_area(5))

# Import from package
from shapes import circle_area, sphere_volume
print(circle_area(3))
print(sphere_volume(2))

# Or import entire package
import shapes
print(shapes.PI)
""")

# ----------------------------------------------------------------------------
# DISTRIBUTING YOUR PACKAGES
# ----------------------------------------------------------------------------
print("\n8.4 Distributing Your Packages:")

print("""
To share your package with others:

1. Create setup.py or pyproject.toml
2. Add README.md and LICENSE
3. Build distribution files:
   python -m pip install --upgrade build
   python -m build
   
4. Upload to PyPI:
   python -m pip install --upgrade twine
   python -m twine upload dist/*
   
5. Others can install with:
   pip install your-package-name
""")

# Show a simple setup.py example
setup_py_example = '''
from setuptools import setup, find_packages

setup(
    name="shapes",
    version="1.0.0",
    author="Your Name",
    description="A package for geometric calculations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/shapes",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
'''

print("\n   Example setup.py:")
print(setup_py_example[:300] + "...")

# ============================================================================
# SECTION 9: BEST PRACTICES
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 9: BEST PRACTICES")
print("=" * 60)

print("""
9.1 Module and Package Best Practices:

1. USE DESCRIPTIVE NAMES:
   - Module names: lowercase_with_underscores.py
   - Package names: lowercase_without_underscores
   - Avoid names that conflict with standard library

2. ORGANIZE LOGICALLY:
   - Group related functionality in modules
   - Use packages for larger projects
   - Keep modules focused and cohesive

3. DOCUMENT YOUR MODULES:
   - Add docstring at top of each module
   - Document public functions and classes
   - Include examples where helpful

4. USE __init__.py WISELY:
   - Keep it simple
   - Use for package initialization
   - Control what's exported with __all__

5. HANDLE IMPORTS PROPERLY:
   - Import at top of file (PEP 8)
   - Group imports: standard library, third-party, local
   - Avoid circular imports
   - Prefer explicit imports over 'from module import *'

6. USE __name__ == "__main__" FOR TESTING:
   - Make modules both importable and executable
   - Include tests or demos in main block

7. MANAGE DEPENDENCIES:
   - Use virtual environments
   - Document dependencies in requirements.txt
   - Pin versions for reproducibility

8. VERSION YOUR PACKAGES:
   - Use semantic versioning (MAJOR.MINOR.PATCH)
   - Include __version__ in __init__.py

9. FOLLOW PEP 8:
   - Consistent formatting
   - Meaningful variable names
   - Proper documentation

10. TEST YOUR MODULES:
    - Write unit tests
    - Test both imported and direct execution
    - Consider using pytest or unittest
""")

# ----------------------------------------------------------------------------
# COMMON PITFALLS TO AVOID
# ----------------------------------------------------------------------------
print("\n9.2 Common Pitfalls to Avoid:")

print("""
1. CIRCULAR IMPORTS:
   Module A imports Module B, and Module B imports Module A
   Solution: Restructure or use local imports

2. MODIFYING sys.path HAPHAZARDLY:
   Can lead to hard-to-debug import issues
   Solution: Use proper package structure or setup.py

3. NAME SHADOWING:
   Importing common names that shadow built-ins
   Solution: Use descriptive names, avoid 'from module import *'

4. FORGETTING __init__.py:
   Directory won't be recognized as package
   Solution: Always include __init__.py (even if empty)

5. RELATIVE IMPORTS IN SCRIPTS:
   Relative imports don't work in scripts run as main
   Solution: Use absolute imports or -m flag

6. NOT USING VIRTUAL ENVIRONMENTS:
   Package conflicts and version issues
   Solution: Always use virtual environments for projects
""")

# ----------------------------------------------------------------------------
# PRACTICAL WORKFLOW EXAMPLE
# ----------------------------------------------------------------------------
print("\n9.3 Practical Development Workflow:")

print("""
Example workflow for a new project:

1. Create project directory:
   mkdir my_project && cd my_project

2. Initialize git repository:
   git init

3. Create virtual environment:
   python -m venv venv

4. Activate virtual environment:
   source venv/bin/activate  # or venv\\Scripts\\activate on Windows

5. Create project structure:
   my_project/
   ├── README.md
   ├── requirements.txt
   ├── setup.py
   ├── tests/
   │   └── test_module.py
   └── mypackage/
       ├── __init__.py
       ├── module1.py
       └── module2.py

6. Develop your modules and packages

7. Write tests and run them:
   python -m pytest tests/

8. Install in development mode:
   pip install -e .

9. Freeze dependencies:
   pip freeze > requirements.txt

10. Commit changes to git
""")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

print("""
KEY CONCEPTS COVERED:

1. MODULES:
   - Every .py file is a module
   - Contain functions, classes, variables
   - Import using various styles

2. __name__ == "__main__":
   - Determines if module is run directly or imported
   - Allows modules to be both importable and executable
   - Used for tests, demos, and CLIs

3. PACKAGES:
   - Directories containing modules and __init__.py
   - Organize related functionality
   - Create namespace hierarchies

4. PYTHON PATH:
   - List of directories Python searches for modules
   - sys.path contains current search paths
   - Can be modified programmatically or via environment variables

5. VIRTUAL ENVIRONMENTS:
   - Isolated Python environments
   - Prevent package conflicts
   - Essential for project dependency management
   - Created with python -m venv

6. IMPORT STYLES:
   - import module
   - import module as alias
   - from module import item
   - from module import item as alias
   - Avoid: from module import * (except in specific cases)

7. BEST PRACTICES:
   - Use descriptive names
   - Organize code logically
   - Document thoroughly
   - Use virtual environments
   - Test your modules
   - Follow PEP 8 guidelines

REMEMBER:
- Modules and packages help organize and reuse code
- Virtual environments keep projects isolated and reproducible
- Proper import practices prevent naming conflicts
- The __name__ pattern makes modules more versatile
- Good structure makes code more maintainable and shareable
""")

print("\n" + "=" * 70)
print("END OF MODULES AND PACKAGES DEMONSTRATION")
print("=" * 70)