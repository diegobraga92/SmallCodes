"""
COMPREHENSIVE PYTHON PACKAGING & DISTRIBUTION DEMONSTRATION

This module illustrates best practices for Python packaging including:
1. setup.py vs pyproject.toml (modern approach)
2. Building packages (wheel, sdist)
3. Publishing to PyPI
4. Versioning strategies
5. Dependency management
6. Package metadata and configuration

We'll create a real-world package called "data-validator" that validates
various data formats with a clean, extensible architecture.
"""

# Note: This is the main package code. The packaging configuration files
# (setup.py, pyproject.toml, setup.cfg) will be shown as separate examples below.

import json
import re
import csv
import datetime
import decimal
import pathlib
import hashlib
import mimetypes
from abc import ABC, abstractmethod
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
    Callable,
    TypeVar,
    Generic,
    ClassVar,
    get_type_hints,
)
from enum import Enum, auto
from dataclasses import dataclass, field, asdict
from pathlib import Path
import yaml  # Will be a dependency
import tomli  # For TOML parsing (Python 3.11+ has tomllib)

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False


# ============================================================================
# PACKAGE METADATA AND VERSIONING
# ============================================================================

# This should be the ONLY place where version is defined in the code
# It will be imported by __init__.py and read by setup.py/pyproject.toml
__version__ = "1.0.0a1"  # Following semantic versioning: MAJOR.MINOR.PATCH[.devN][+local]
__author__ = "Data Validation Team"
__email__ = "team@datavalidation.example.com"
__license__ = "MIT"
__copyright__ = f"Copyright 2024-{datetime.datetime.now().year}"


# ============================================================================
# CUSTOM EXCEPTIONS
# ============================================================================

class ValidationError(Exception):
    """Base exception for all validation errors."""
    
    def __init__(self, message: str, field: Optional[str] = None):
        self.message = message
        self.field = field
        super().__init__(f"Field '{field}': {message}" if field else message)


class SchemaError(Exception):
    """Raised when a schema definition is invalid."""
    pass


class ConfigurationError(Exception):
    """Raised when package configuration is invalid."""
    pass


# ============================================================================
# ENUMS AND CONSTANTS
# ============================================================================

class ValidationSeverity(Enum):
    """Severity levels for validation issues."""
    INFO = auto()      # Informational, not a problem
    WARNING = auto()   # Potential issue, but data is valid
    ERROR = auto()     # Data is invalid
    
    @classmethod
    def from_string(cls, severity_str: str) -> "ValidationSeverity":
        """Convert string to ValidationSeverity."""
        try:
            return cls[severity_str.upper()]
        except KeyError:
            raise ValueError(f"Invalid severity: {severity_str}")


class DataFormat(Enum):
    """Supported data formats."""
    JSON = "json"
    YAML = "yaml"
    TOML = "toml"
    CSV = "csv"
    XML = "xml"  # Not implemented in this example
    EXCEL = "excel"  # Requires pandas
    
    @property
    def extensions(self) -> List[str]:
        """Get file extensions for this format."""
        return {
            DataFormat.JSON: [".json", ".jsonl"],
            DataFormat.YAML: [".yaml", ".yml"],
            DataFormat.TOML: [".toml"],
            DataFormat.CSV: [".csv", ".tsv"],
            DataFormat.XML: [".xml"],
            DataFormat.EXCEL: [".xlsx", ".xls", ".ods"],
        }[self]
    
    @classmethod
    def from_extension(cls, extension: str) -> Optional["DataFormat"]:
        """Determine format from file extension."""
        extension = extension.lower()
        for format_ in cls:
            if extension in format_.extensions:
                return format_
        return None


# ============================================================================
# DATA CLASSES FOR VALIDATION RESULTS
# ============================================================================

@dataclass
class ValidationIssue:
    """Represents a single validation issue."""
    
    severity: ValidationSeverity
    message: str
    field: Optional[str] = None
    value: Optional[Any] = None
    rule: Optional[str] = None
    line: Optional[int] = None
    column: Optional[int] = None
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        data = asdict(self)
        data["severity"] = self.severity.name
        data["timestamp"] = self.timestamp.isoformat()
        return data


@dataclass
class ValidationResult:
    """Container for validation results."""
    
    is_valid: bool
    issues: List[ValidationIssue] = field(default_factory=list)
    validated_count: int = 0
    processing_time: float = 0.0
    data_hash: Optional[str] = None
    schema_version: Optional[str] = None
    
    @property
    def error_count(self) -> int:
        """Count of ERROR severity issues."""
        return sum(1 for issue in self.issues if issue.severity == ValidationSeverity.ERROR)
    
    @property
    def warning_count(self) -> int:
        """Count of WARNING severity issues."""
        return sum(1 for issue in self.issues if issue.severity == ValidationSeverity.WARNING)
    
    @property
    def info_count(self) -> int:
        """Count of INFO severity issues."""
        return sum(1 for issue in self.issues if issue.severity == ValidationSeverity.INFO)
    
    def add_issue(
        self,
        severity: ValidationSeverity,
        message: str,
        **kwargs: Any,
    ) -> None:
        """Add a validation issue."""
        self.issues.append(ValidationIssue(severity=severity, message=message, **kwargs))
        if severity == ValidationSeverity.ERROR:
            self.is_valid = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "is_valid": self.is_valid,
            "issues": [issue.to_dict() for issue in self.issues],
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "info_count": self.info_count,
            "validated_count": self.validated_count,
            "processing_time": self.processing_time,
            "data_hash": self.data_hash,
            "schema_version": self.schema_version,
        }
    
    def to_json(self, indent: Optional[int] = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, default=str)
    
    def summary(self) -> str:
        """Get a human-readable summary."""
        return (
            f"Validation {'PASSED' if self.is_valid else 'FAILED'} - "
            f"Errors: {self.error_count}, "
            f"Warnings: {self.warning_count}, "
            f"Info: {self.info_count}, "
            f"Processed: {self.validated_count} items"
        )


# ============================================================================
# VALIDATION RULES BASE CLASSES
# ============================================================================

class ValidationRule(ABC):
    """Base class for all validation rules."""
    
    def __init__(self, field: Optional[str] = None, severity: ValidationSeverity = ValidationSeverity.ERROR):
        self.field = field
        self.severity = severity
        self.name = self.__class__.__name__
    
    @abstractmethod
    def validate(self, value: Any) -> Optional[str]:
        """Validate a value. Return error message or None if valid."""
        pass
    
    def __call__(self, value: Any) -> Optional[str]:
        """Make rule callable."""
        return self.validate(value)


class CompositeRule(ValidationRule):
    """Rule that combines multiple rules."""
    
    def __init__(self, rules: List[ValidationRule], **kwargs):
        super().__init__(**kwargs)
        self.rules = rules
    
    def validate(self, value: Any) -> Optional[str]:
        """Validate with all rules, return first error."""
        for rule in self.rules:
            error = rule.validate(value)
            if error:
                return error
        return None


# ============================================================================
# BUILT-IN VALIDATION RULES
# ============================================================================

class RequiredRule(ValidationRule):
    """Check if value is not None or empty."""
    
    def validate(self, value: Any) -> Optional[str]:
        if value is None:
            return "Value is required"
        if isinstance(value, str) and not value.strip():
            return "Value cannot be empty"
        if isinstance(value, (list, dict, set)) and not value:
            return "Value cannot be empty"
        return None


class TypeRule(ValidationRule):
    """Check if value is of specific type."""
    
    def __init__(self, expected_type: Union[type, Tuple[type, ...]], **kwargs):
        super().__init__(**kwargs)
        self.expected_type = expected_type
    
    def validate(self, value: Any) -> Optional[str]:
        if value is None:
            return None  # Let RequiredRule handle this
        if not isinstance(value, self.expected_type):
            return f"Expected type {self.expected_type}, got {type(value)}"
        return None


class RangeRule(ValidationRule):
    """Check if numeric value is within range."""
    
    def __init__(self, min_val: Optional[float] = None, max_val: Optional[float] = None, **kwargs):
        super().__init__(**kwargs)
        self.min_val = min_val
        self.max_val = max_val
    
    def validate(self, value: Any) -> Optional[str]:
        if value is None:
            return None
        
        try:
            num = float(value)
        except (ValueError, TypeError):
            return f"Value must be numeric, got {type(value)}"
        
        errors = []
        if self.min_val is not None and num < self.min_val:
            errors.append(f"Value must be >= {self.min_val}")
        if self.max_val is not None and num > self.max_val:
            errors.append(f"Value must be <= {self.max_val}")
        
        return ", ".join(errors) if errors else None


class RegexRule(ValidationRule):
    """Check if string matches regular expression."""
    
    def __init__(self, pattern: str, **kwargs):
        super().__init__(**kwargs)
        self.pattern = pattern
        self.regex = re.compile(pattern)
    
    def validate(self, value: Any) -> Optional[str]:
        if value is None:
            return None
        if not isinstance(value, str):
            return f"Value must be string, got {type(value)}"
        if not self.regex.match(value):
            return f"Value must match pattern: {self.pattern}"
        return None


class EmailRule(RegexRule):
    """Check if string is a valid email address."""
    
    def __init__(self, **kwargs):
        # Simplified email regex for demonstration
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        super().__init__(pattern, **kwargs)


class LengthRule(ValidationRule):
    """Check length of string, list, or dict."""
    
    def __init__(
        self,
        min_len: Optional[int] = None,
        max_len: Optional[int] = None,
        exact_len: Optional[int] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.min_len = min_len
        self.max_len = max_len
        self.exact_len = exact_len
    
    def validate(self, value: Any) -> Optional[str]:
        if value is None:
            return None
        
        try:
            length = len(value)
        except TypeError:
            return f"Value must have length, got {type(value)}"
        
        errors = []
        if self.exact_len is not None and length != self.exact_len:
            errors.append(f"Length must be exactly {self.exact_len}")
        else:
            if self.min_len is not None and length < self.min_len:
                errors.append(f"Length must be >= {self.min_len}")
            if self.max_len is not None and length > self.max_len:
                errors.append(f"Length must be <= {self.max_len}")
        
        return ", ".join(errors) if errors else None


class EnumRule(ValidationRule):
    """Check if value is in allowed set."""
    
    def __init__(self, allowed_values: List[Any], **kwargs):
        super().__init__(**kwargs)
        self.allowed_values = allowed_values
    
    def validate(self, value: Any) -> Optional[str]:
        if value is None:
            return None
        if value not in self.allowed_values:
            return f"Value must be one of: {self.allowed_values}"
        return None


# ============================================================================
# SCHEMA DEFINITION
# ============================================================================

@dataclass
class FieldSchema:
    """Schema definition for a single field."""
    
    name: str
    type: Union[type, Tuple[type, ...]]
    required: bool = True
    rules: List[ValidationRule] = field(default_factory=list)
    default: Optional[Any] = None
    description: Optional[str] = None
    alias: Optional[str] = None  # For mapping different field names
    
    def __post_init__(self):
        """Add type rule automatically."""
        type_rule = TypeRule(self.type, field=self.name)
        if type_rule not in self.rules:
            self.rules.insert(0, type_rule)
        
        if self.required:
            required_rule = RequiredRule(field=self.name)
            if required_rule not in self.rules:
                self.rules.insert(0, required_rule)


@dataclass
class Schema:
    """Complete schema for data validation."""
    
    name: str
    fields: Dict[str, FieldSchema]
    version: str = "1.0.0"
    description: Optional[str] = None
    strict: bool = True  # Reject unknown fields
    
    def __post_init__(self):
        """Validate schema definition."""
        if not self.fields:
            raise SchemaError("Schema must have at least one field")
        
        for field_name, field_schema in self.fields.items():
            if field_name != field_schema.name:
                raise SchemaError(
                    f"Field name mismatch: dict key '{field_name}' "
                    f"vs field name '{field_schema.name}'"
                )
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate data against this schema."""
        result = ValidationResult(is_valid=True)
        start_time = datetime.datetime.now()
        
        try:
            # Track which schema fields we've validated
            validated_fields = set()
            
            # Check all data fields
            for field_name, value in data.items():
                # Find matching field schema
                field_schema = None
                
                # First try direct match
                if field_name in self.fields:
                    field_schema = self.fields[field_name]
                
                # Then try alias match
                if not field_schema:
                    for schema_field in self.fields.values():
                        if schema_field.alias == field_name:
                            field_schema = schema_field
                            break
                
                if field_schema:
                    # Validate known field
                    self._validate_field(field_schema, value, result)
                    validated_fields.add(field_schema.name)
                elif self.strict:
                    # Unknown field in strict mode
                    result.add_issue(
                        ValidationSeverity.ERROR,
                        f"Unknown field",
                        field=field_name,
                        value=value,
                    )
            
            # Check for missing required fields
            for field_name, field_schema in self.fields.items():
                if field_schema.required and field_name not in validated_fields:
                    # Check if it might be under an alias
                    if not field_schema.alias or field_schema.alias not in data:
                        result.add_issue(
                            ValidationSeverity.ERROR,
                            "Required field missing",
                            field=field_name,
                        )
            
            result.validated_count = len(data)
            
        except Exception as e:
            result.add_issue(
                ValidationSeverity.ERROR,
                f"Validation error: {str(e)}",
            )
        
        end_time = datetime.datetime.now()
        result.processing_time = (end_time - start_time).total_seconds()
        
        return result
    
    def _validate_field(
        self,
        field_schema: FieldSchema,
        value: Any,
        result: ValidationResult,
    ) -> None:
        """Validate a single field."""
        for rule in field_schema.rules:
            error = rule.validate(value)
            if error:
                result.add_issue(
                    rule.severity,
                    error,
                    field=field_schema.name,
                    value=value,
                    rule=rule.name,
                )


# ============================================================================
# SCHEMA REGISTRY (SINGLETON PATTERN)
# ============================================================================

class SchemaRegistry:
    """Registry for managing schemas across the application."""
    
    _instance: ClassVar[Optional["SchemaRegistry"]] = None
    _schemas: Dict[str, Schema]
    
    def __new__(cls) -> "SchemaRegistry":
        """Singleton pattern implementation."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._schemas = {}
        return cls._instance
    
    def register(self, schema: Schema) -> None:
        """Register a schema."""
        if schema.name in self._schemas:
            raise ValueError(f"Schema '{schema.name}' already registered")
        self._schemas[schema.name] = schema
    
    def get(self, name: str) -> Optional[Schema]:
        """Get a schema by name."""
        return self._schemas.get(name)
    
    def list(self) -> List[str]:
        """List all registered schema names."""
        return list(self._schemas.keys())
    
    def clear(self) -> None:
        """Clear all registered schemas."""
        self._schemas.clear()


# ============================================================================
# DATA VALIDATOR CLASS
# ============================================================================

class DataValidator:
    """Main validator class supporting multiple formats."""
    
    def __init__(self):
        self.schema_registry = SchemaRegistry()
        self._load_builtin_schemas()
    
    def _load_builtin_schemas(self) -> None:
        """Load built-in schemas."""
        # User schema example
        user_schema = Schema(
            name="user",
            description="User profile schema",
            fields={
                "id": FieldSchema(
                    name="id",
                    type=str,
                    rules=[RegexRule(r"^[A-Za-z0-9_-]+$")],
                    description="Unique user identifier",
                ),
                "email": FieldSchema(
                    name="email",
                    type=str,
                    rules=[EmailRule()],
                    description="User email address",
                ),
                "name": FieldSchema(
                    name="name",
                    type=str,
                    rules=[LengthRule(min_len=1, max_len=100)],
                    description="Full name",
                ),
                "age": FieldSchema(
                    name="age",
                    type=int,
                    required=False,
                    rules=[RangeRule(min_val=0, max_val=150)],
                    description="Age in years",
                ),
                "is_active": FieldSchema(
                    name="is_active",
                    type=bool,
                    required=False,
                    default=True,
                    description="Account active status",
                ),
            },
        )
        self.schema_registry.register(user_schema)
    
    def validate(
        self,
        data: Union[Dict[str, Any], List[Dict[str, Any]]],
        schema_name: Optional[str] = None,
        schema: Optional[Schema] = None,
    ) -> ValidationResult:
        """Validate data against a schema.
        
        Args:
            data: Data to validate (single dict or list of dicts)
            schema_name: Name of registered schema
            schema: Direct schema object (overrides schema_name)
            
        Returns:
            ValidationResult object
        """
        # Get schema
        if schema is None:
            if schema_name is None:
                raise ValueError("Either schema_name or schema must be provided")
            schema = self.schema_registry.get(schema_name)
            if schema is None:
                raise ValueError(f"Schema '{schema_name}' not found")
        
        # Handle single item or list
        if isinstance(data, dict):
            return schema.validate(data)
        elif isinstance(data, list):
            result = ValidationResult(is_valid=True)
            for i, item in enumerate(data):
                item_result = schema.validate(item)
                # Add index to field names for clarity
                for issue in item_result.issues:
                    if issue.field:
                        issue.field = f"[{i}].{issue.field}"
                result.issues.extend(item_result.issues)
                if not item_result.is_valid:
                    result.is_valid = False
                result.validated_count += item_result.validated_count
            return result
        else:
            raise TypeError(f"Data must be dict or list, got {type(data)}")
    
    def validate_file(
        self,
        filepath: Union[str, Path],
        schema_name: str,
        format: Optional[DataFormat] = None,
    ) -> ValidationResult:
        """Validate data from a file."""
        filepath = Path(filepath)
        
        # Determine format
        if format is None:
            ext = filepath.suffix.lower()
            format = DataFormat.from_extension(ext)
            if format is None:
                return ValidationResult(
                    is_valid=False,
                    issues=[ValidationIssue(
                        severity=ValidationSeverity.ERROR,
                        message=f"Unsupported file format: {ext}",
                    )],
                )
        
        # Read and validate
        try:
            data = self._read_file(filepath, format)
            return self.validate(data, schema_name)
        except Exception as e:
            return ValidationResult(
                is_valid=False,
                issues=[ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    message=f"Failed to read file: {str(e)}",
                )],
            )
    
    def _read_file(self, filepath: Path, format: DataFormat) -> Union[Dict, List]:
        """Read data from file based on format."""
        if format == DataFormat.JSON:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        elif format == DataFormat.YAML:
            with open(filepath, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        elif format == DataFormat.TOML:
            with open(filepath, 'rb') as f:
                return tomli.load(f)
        elif format == DataFormat.CSV:
            data = []
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
            return data
        elif format == DataFormat.EXCEL:
            if not PANDAS_AVAILABLE:
                raise ImportError("pandas is required for Excel support")
            df = pd.read_excel(filepath)
            return df.to_dict('records')
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def create_schema_from_data(
        self,
        data: Union[Dict, List[Dict]],
        name: str,
        **kwargs,
    ) -> Schema:
        """Infer schema from sample data."""
        if isinstance(data, dict):
            sample = data
        elif isinstance(data, list) and data:
            sample = data[0]
        else:
            raise ValueError("Cannot infer schema from empty data")
        
        fields = {}
        for field_name, value in sample.items():
            # Infer type
            if isinstance(value, (int, float)):
                field_type = (int, float)
            elif isinstance(value, bool):
                field_type = bool
            elif isinstance(value, (list, tuple)):
                field_type = list
            elif isinstance(value, dict):
                field_type = dict
            else:
                field_type = str
            
            fields[field_name] = FieldSchema(
                name=field_name,
                type=field_type,
                required=False,  # Be conservative
                description=f"Inferred from sample data",
            )
        
        return Schema(name=name, fields=fields, **kwargs)


# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

def main_cli() -> None:
    """Command-line interface for the data validator."""
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(
        description="Data Validator - Validate data files against schemas",
        epilog="Example: python -m data_validator validate data.json --schema user",
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate a file")
    validate_parser.add_argument("file", help="File to validate")
    validate_parser.add_argument("--schema", required=True, help="Schema name")
    validate_parser.add_argument("--format", help="File format (auto-detected)")
    validate_parser.add_argument("--output", help="Output file for results")
    validate_parser.add_argument("--quiet", action="store_true", help="Minimal output")
    
    # Schemas command
    schemas_parser = subparsers.add_parser("schemas", help="List available schemas")
    
    # Create schema command
    create_parser = subparsers.add_parser("create-schema", help="Create schema from data")
    create_parser.add_argument("file", help="Sample data file")
    create_parser.add_argument("--name", required=True, help="Schema name")
    create_parser.add_argument("--output", help="Output file for schema")
    
    args = parser.parse_args()
    
    validator = DataValidator()
    
    if args.command == "validate":
        # Determine format
        format_enum = None
        if args.format:
            try:
                format_enum = DataFormat[args.format.upper()]
            except KeyError:
                print(f"Error: Unknown format '{args.format}'", file=sys.stderr)
                sys.exit(1)
        
        # Validate
        result = validator.validate_file(args.file, args.schema, format_enum)
        
        # Output results
        if args.quiet:
            sys.exit(0 if result.is_valid else 1)
        else:
            print(result.summary())
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(result.to_dict(), f, indent=2, default=str)
                print(f"Results saved to {args.output}")
            sys.exit(0 if result.is_valid else 1)
    
    elif args.command == "schemas":
        schemas = validator.schema_registry.list()
        if schemas:
            print("Available schemas:")
            for schema_name in schemas:
                schema = validator.schema_registry.get(schema_name)
                print(f"  - {schema_name}: {schema.description or 'No description'}")
        else:
            print("No schemas registered")
    
    elif args.command == "create-schema":
        # Read file
        filepath = Path(args.file)
        ext = filepath.suffix.lower()
        format_enum = DataFormat.from_extension(ext)
        
        if format_enum is None:
            print(f"Error: Unsupported file format: {ext}", file=sys.stderr)
            sys.exit(1)
        
        try:
            data = validator._read_file(filepath, format_enum)
            schema = validator.create_schema_from_data(data, args.name)
            
            # Output schema
            schema_dict = {
                "name": schema.name,
                "version": schema.version,
                "description": schema.description,
                "strict": schema.strict,
                "fields": {
                    name: {
                        "name": fs.name,
                        "type": str(fs.type),
                        "required": fs.required,
                        "default": fs.default,
                        "description": fs.description,
                        "alias": fs.alias,
                    }
                    for name, fs in schema.fields.items()
                },
            }
            
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(schema_dict, f, indent=2)
                print(f"Schema saved to {args.output}")
            else:
                print(json.dumps(schema_dict, indent=2))
        
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    
    else:
        parser.print_help()
        sys.exit(1)


# ============================================================================
# PACKAGE INITIALIZATION
# ============================================================================

def get_version() -> str:
    """Get the package version."""
    return __version__


def get_validator() -> DataValidator:
    """Get a configured DataValidator instance."""
    return DataValidator()


# Export public API
__all__ = [
    # Core classes
    "DataValidator",
    "ValidationResult",
    "ValidationIssue",
    "ValidationSeverity",
    
    # Schemas
    "Schema",
    "FieldSchema",
    "SchemaRegistry",
    
    # Rules
    "ValidationRule",
    "RequiredRule",
    "TypeRule",
    "RangeRule",
    "RegexRule",
    "EmailRule",
    "LengthRule",
    "EnumRule",
    "CompositeRule",
    
    # Exceptions
    "ValidationError",
    "SchemaError",
    
    # Utilities
    "get_version",
    "get_validator",
    "DataFormat",
    
    # CLI
    "main_cli",
]


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Demonstrate package functionality
    print(f"Data Validator v{get_version()}")
    print("=" * 50)
    
    # Example usage
    validator = DataValidator()
    
    # Sample data
    user_data = {
        "id": "user_123",
        "email": "user@example.com",
        "name": "John Doe",
        "age": 30,
        "is_active": True,
    }
    
    # Validate
    result = validator.validate(user_data, "user")
    
    print(f"Validation: {result.summary()}")
    
    # Show details if there are issues
    if not result.is_valid or result.warning_count > 0:
        for issue in result.issues:
            print(f"  {issue.severity.name}: {issue.message}")
    
    print(f"\nAvailable schemas: {validator.schema_registry.list()}")


# ============================================================================
# PACKAGING CONFIGURATION FILES
# ============================================================================

"""
This section shows the various configuration files needed for packaging.
In a real project, these would be separate files in the project root.

1. setup.py (LEGACY APPROACH - Still works but being phased out)
----------------------------------------------------------------
Note: Modern projects should use pyproject.toml instead.

# setup.py
from setuptools import setup, find_packages
import os

# Read version from package
version = {}
with open("data_validator/__init__.py") as fp:
    exec(fp.read(), version)
__version__ = version['__version__']

# Read long description from README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="data-validator",
    version=__version__,
    author="Data Validation Team",
    author_email="team@datavalidation.example.com",
    description="A comprehensive data validation library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/data-validator",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/data-validator/issues",
        "Documentation": "https://data-validator.readthedocs.io/",
        "Source Code": "https://github.com/yourusername/data-validator",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(include=["data_validator", "data_validator.*"]),
    python_requires=">=3.8",
    install_requires=[
        "pyyaml>=6.0",
        "tomli>=2.0.0; python_version < '3.11'",
    ],
    extras_require={
        "pandas": ["pandas>=1.3.0"],
        "excel": ["pandas>=1.3.0", "openpyxl>=3.0.0"],
        "all": ["pandas>=1.3.0", "openpyxl>=3.0.0", "numpy>=1.20.0"],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
            "sphinx>=7.0.0",
        ],
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "sphinx-autodoc-typehints>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "data-validator=data_validator:main_cli",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)

2. pyproject.toml (MODERN APPROACH - PEP 517/518)
--------------------------------------------------
This is the modern standard. It supports multiple build backends.

# pyproject.toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "data-validator"
version = "1.0.0a1"
description = "A comprehensive data validation library"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}
authors = [
    {name = "Data Validation Team", email = "team@datavalidation.example.com"}
]
maintainers = [
    {name = "Maintainer Name", email = "maintainer@example.com"}
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Software Development :: Quality Assurance",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Operating System :: OS Independent",
]

keywords = ["validation", "data", "schema", "quality", "yaml", "json", "csv"]

dependencies = [
    "pyyaml>=6.0",
    "tomli>=2.0.0; python_version < '3.11'",
]

[project.optional-dependencies]
pandas = ["pandas>=1.3.0"]
excel = ["pandas>=1.3.0", "openpyxl>=3.0.0"]
all = ["pandas>=1.3.0", "openpyxl>=3.0.0", "numpy>=1.20.0"]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "black>=23.0.0",
    "flake8>=6.0.0",
    "mypy>=1.0.0",
    "pre-commit>=3.0.0",
    "sphinx>=7.0.0",
]
docs = [
    "sphinx>=7.0.0",
    "sphinx-rtd-theme>=1.0.0",
    "sphinx-autodoc-typehints>=1.0.0",
]

[project.urls]
Homepage = "https://github.com/yourusername/data-validator"
Documentation = "https://data-validator.readthedocs.io/"
Repository = "https://github.com/yourusername/data-validator"
Changelog = "https://github.com/yourusername/data-validator/releases"
Issues = "https://github.com/yourusername/data-validator/issues"

[project.scripts]
data-validator = "data_validator:main_cli"

[tool.setuptools]
packages = ["data_validator"]

[tool.setuptools.package-data]
data_validator = ["py.typed", "schemas/*.json"]

[tool.black]
line-length = 88
target-version = ['py38']

[tool.isort]
profile = "black"
multi_line_output = 3

[tool.mypy]
python_version = "3.8"
warn_return_any = true
disallow_untyped_defs = true
ignore_missing_imports = true

[tool.pytest.ini_options]
minversion = "7.0"
addopts = "-ra -q --cov=data_validator --cov-report=term-missing"
testpaths = ["tests"]

3. setup.cfg (ALTERNATIVE LEGACY APPROACH)
------------------------------------------
# setup.cfg (alternative to setup.py)
[metadata]
name = data-validator
version = attr: data_validator.__version__
author = Data Validation Team
author_email = team@datavalidation.example.com
description = A comprehensive data validation library
long_description = file: README.md
long_description_content_type = text/markdown
url = https://github.com/yourusername/data-validator
project_urls =
    Bug Tracker = https://github.com/yourusername/data-validator/issues
    Documentation = https://data-validator.readthedocs.io/
    Source Code = https://github.com/yourusername/data-validator
classifiers =
    Development Status :: 4 - Beta
    Intended Audience :: Developers
    Topic :: Software Development :: Libraries :: Python Modules
    Topic :: Software Development :: Quality Assurance
    License :: OSI Approved :: MIT License
    Programming Language :: Python :: 3
    Programming Language :: Python :: 3.8
    Programming Language :: Python :: 3.9
    Programming Language :: Python :: 3.10
    Programming Language :: Python :: 3.11
    Programming Language :: Python :: 3.12
    Operating System :: OS Independent

[options]
packages = find:
python_requires = >=3.8
install_requires =
    pyyaml>=6.0
    tomli>=2.0.0; python_version < '3.11'
    
package_dir =
    = src

[options.packages.find]
where = src

[options.extras_require]
pandas = pandas>=1.3.0
excel = pandas>=1.3.0, openpyxl>=3.0.0
all = pandas>=1.3.0, openpyxl>=3.0.0, numpy>=1.20.0
dev =
    pytest>=7.0.0
    pytest-cov>=4.0.0
    black>=23.0.0
    flake8>=6.0.0
    mypy>=1.0.0
    pre-commit>=3.0.0
    sphinx>=7.0.0
docs =
    sphinx>=7.0.0
    sphinx-rtd-theme>=1.0.0
    sphinx-autodoc-typehints>=1.0.0

[options.entry_points]
console_scripts =
    data-validator = data_validator:main_cli

4. MANIFEST.in (For including non-code files)
---------------------------------------------
# MANIFEST.in
include LICENSE
include README.md
include CHANGELOG.md
include pyproject.toml

# Include package data
include data_validator/schemas/*.json
include data_validator/py.typed

# Include tests
recursive-include tests *.py
recursive-include tests *.json
recursive-include tests *.yaml

# Exclude certain files
global-exclude __pycache__
global-exclude *.py[cod]
global-exclude *~
global-exclude .*.swp

5. README.md (Essential for PyPI)
---------------------------------
# Data Validator

A comprehensive data validation library for Python.

## Features

- Validate JSON, YAML, TOML, CSV, and Excel files
- Schema-based validation with custom rules
- Extensible architecture
- Detailed validation reports
- Command-line interface

## Installation

```bash
pip install data-validator