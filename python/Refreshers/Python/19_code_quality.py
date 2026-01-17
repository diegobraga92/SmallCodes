"""
COMPREHENSIVE PYTHON CODE QUALITY DEMONSTRATION

This module illustrates best practices for Python code quality including:
1. PEP 8 and style guides
2. Type hints (typing module)
3. mypy for static type checking
4. Linting with flake8 and ruff
5. Code formatting with black and isort
6. Documentation with docstrings and Sphinx
7. Static vs runtime checks

We'll create a data processing pipeline for analyzing e-commerce orders
to demonstrate these concepts in practice.
"""

# ============================================================================
# IMPORTS WITH CLEAN ORGANIZATION (PEP 8 Section 7)
# ============================================================================

# Standard library imports (alphabetical)
import csv
import datetime
import json
import logging
import os
import sys
from abc import ABC, abstractmethod
from collections import defaultdict, namedtuple
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum, auto
from pathlib import Path
from typing import (
    Any,  # Use sparingly - only when type cannot be expressed
    Callable,
    ClassVar,
    Dict,
    Generic,
    Iterable,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
    get_type_hints,
)

# Third-party imports (alphabetical, separated by blank line)
try:
    import pandas as pd  # type: ignore
    import numpy as np  # type: ignore
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    # Create dummy classes for type checking
    class pd:  # type: ignore
        class DataFrame:
            pass
    
    class np:  # type: ignore
        class ndarray:
            pass

# Local application imports (alphabetical)
# In a real project, these would be separate modules
# from .exceptions import ValidationError
# from .types import Currency, Status

# ============================================================================
# CONSTANTS AND GLOBAL VARIABLES (PEP 8 Section 4)
# ============================================================================

# Constants should be ALL_CAPS_WITH_UNDERSCORES (PEP 8)
DEFAULT_CURRENCY: str = "USD"
MAX_ORDER_ITEMS: int = 100
MIN_ORDER_VALUE: Decimal = Decimal("0.01")
VALID_COUNTRIES: Tuple[str, ...] = ("US", "CA", "GB", "AU", "DE", "FR")

# Module-level variables should be lowercase_with_underscores
logger: logging.Logger = logging.getLogger(__name__)


# ============================================================================
# TYPE ALIASES AND GENERICS (PEP 484)
# ============================================================================

# Type aliases make complex types readable
CustomerID = str
OrderID = str
ProductID = str
Currency = str

# Generic type variables for flexible typing
T = TypeVar("T")  # Generic type
Numeric = TypeVar("Numeric", int, float, Decimal)  # Constrained generic

# Complex type aliases
OrderDict = Dict[str, Union[str, float, List[Dict[str, Any]]]]
ValidationResult = Tuple[bool, List[str]]


# ============================================================================
# CUSTOM EXCEPTIONS WITH PROPER DOCUMENTATION
# ============================================================================

class OrderProcessingError(Exception):
    """Base exception for all order processing errors."""
    
    def __init__(self, message: str, order_id: Optional[OrderID] = None):
        self.order_id = order_id
        self.message = message
        super().__init__(f"Order {order_id}: {message}" if order_id else message)


class ValidationError(OrderProcessingError):
    """Raised when order data fails validation."""
    
    def __init__(
        self,
        message: str,
        order_id: Optional[OrderID] = None,
        validation_errors: Optional[List[str]] = None,
    ):
        super().__init__(message, order_id)
        self.validation_errors = validation_errors or []
    
    def __str__(self) -> str:
        base = super().__str__()
        if self.validation_errors:
            return f"{base} - Errors: {', '.join(self.validation_errors)}"
        return base


class CurrencyConversionError(OrderProcessingError):
    """Raised when currency conversion fails."""
    pass


# ============================================================================
# ENUMS FOR TYPE SAFETY
# ============================================================================

class OrderStatus(Enum):
    """Enum representing possible order statuses."""
    
    PENDING = auto()
    PROCESSING = auto()
    SHIPPED = auto()
    DELIVERED = auto()
    CANCELLED = auto()
    REFUNDED = auto()
    
    @classmethod
    def from_string(cls, status_str: str) -> "OrderStatus":
        """Convert string to OrderStatus enum."""
        try:
            return cls[status_str.upper()]
        except KeyError:
            valid_statuses = ", ".join(s.name for s in cls)
            raise ValueError(
                f"Invalid status '{status_str}'. "
                f"Valid options: {valid_statuses}"
            )


class ProductCategory(Enum):
    """Product categories with their tax rates."""
    
    ELECTRONICS = ("Electronics", Decimal("0.08"))  # 8% tax
    CLOTHING = ("Clothing", Decimal("0.06"))        # 6% tax
    BOOKS = ("Books", Decimal("0.00"))              # 0% tax (exempt)
    FOOD = ("Food", Decimal("0.03"))                # 3% tax
    OTHER = ("Other", Decimal("0.07"))              # 7% tax
    
    def __init__(self, display_name: str, tax_rate: Decimal):
        self.display_name = display_name
        self.tax_rate = tax_rate
    
    @property
    def tax_percentage(self) -> float:
        """Return tax rate as percentage."""
        return float(self.tax_rate * 100)
    
    @classmethod
    def get_by_name(cls, name: str) -> "ProductCategory":
        """Get category by name (case-insensitive)."""
        name_lower = name.lower()
        for category in cls:
            if category.display_name.lower() == name_lower:
                return category
        return cls.OTHER


# ============================================================================
# DATA CLASSES WITH TYPE HINTS
# ============================================================================

class OrderItem:
    """Represents a single item in an order.
    
    Attributes:
        product_id: Unique identifier for the product
        name: Human-readable product name
        quantity: Number of units ordered (must be > 0)
        unit_price: Price per unit in specified currency
        category: Product category for tax calculation
        currency: Currency code (ISO 4217)
    
    Raises:
        ValueError: If quantity or unit_price is invalid
    """
    
    def __init__(
        self,
        product_id: ProductID,
        name: str,
        quantity: int,
        unit_price: Decimal,
        category: ProductCategory,
        currency: Currency = DEFAULT_CURRENCY,
    ):
        # Input validation
        if quantity <= 0:
            raise ValueError(f"Quantity must be positive, got {quantity}")
        if unit_price < 0:
            raise ValueError(f"Unit price cannot be negative, got {unit_price}")
        
        self.product_id = product_id
        self.name = name
        self.quantity = quantity
        self.unit_price = unit_price
        self.category = category
        self.currency = currency
    
    @property
    def subtotal(self) -> Decimal:
        """Calculate subtotal for this item (quantity × unit_price)."""
        return self.unit_price * self.quantity
    
    @property
    def tax_amount(self) -> Decimal:
        """Calculate tax for this item."""
        return self.subtotal * self.category.tax_rate
    
    @property
    def total(self) -> Decimal:
        """Calculate total for this item (subtotal + tax)."""
        return self.subtotal + self.tax_amount
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "product_id": self.product_id,
            "name": self.name,
            "quantity": self.quantity,
            "unit_price": float(self.unit_price),
            "category": self.category.display_name,
            "currency": self.currency,
            "subtotal": float(self.subtotal),
            "tax_amount": float(self.tax_amount),
            "total": float(self.total),
        }
    
    def __repr__(self) -> str:
        """Machine-readable representation."""
        return (
            f"OrderItem("
            f"product_id={self.product_id!r}, "
            f"name={self.name!r}, "
            f"quantity={self.quantity}, "
            f"unit_price={self.unit_price}, "
            f"category={self.category.name})"
        )
    
    def __eq__(self, other: Any) -> bool:
        """Compare two OrderItem instances."""
        if not isinstance(other, OrderItem):
            return NotImplemented
        return (
            self.product_id == other.product_id
            and self.quantity == other.quantity
            and self.unit_price == other.unit_price
        )


class Order:
    """Represents a customer order with items and metadata.
    
    This class handles order validation, calculation, and serialization.
    
    Example:
        >>> order = Order(
        ...     order_id="ORD-123",
        ...     customer_id="CUST-456",
        ...     items=[
        ...         OrderItem("PROD-1", "Laptop", 1, Decimal("999.99"), ProductCategory.ELECTRONICS)
        ...     ],
        ...     currency="USD"
        ... )
        >>> order.total
        Decimal('1079.99')
    
    Attributes:
        order_id: Unique order identifier
        customer_id: Customer who placed the order
        items: List of items in the order
        status: Current order status
        currency: Currency for all monetary values
        created_at: Timestamp when order was created
        shipping_country: Country code for shipping
    """
    
    # Class variables
    _order_counter: ClassVar[int] = 0
    
    def __init__(
        self,
        order_id: OrderID,
        customer_id: CustomerID,
        items: List[OrderItem],
        currency: Currency = DEFAULT_CURRENCY,
        status: OrderStatus = OrderStatus.PENDING,
        shipping_country: Optional[str] = None,
        created_at: Optional[datetime.datetime] = None,
    ):
        self.order_id = order_id
        self.customer_id = customer_id
        self._items: List[OrderItem] = []
        self.currency = currency
        self.status = status
        self.shipping_country = shipping_country
        self.created_at = created_at or datetime.datetime.now()
        
        # Add items with validation
        for item in items:
            self.add_item(item)
        
        # Validate the complete order
        self._validate_order()
        
        # Update class counter
        Order._order_counter += 1
    
    def add_item(self, item: OrderItem) -> None:
        """Add an item to the order with validation."""
        # Check currency consistency
        if item.currency != self.currency:
            raise ValidationError(
                f"Item currency {item.currency} doesn't match "
                f"order currency {self.currency}",
                self.order_id,
            )
        
        # Check for duplicates and update quantity if found
        for existing_item in self._items:
            if existing_item == item:
                existing_item.quantity += item.quantity
                return
        
        self._items.append(item)
        
        # Check maximum items limit
        if len(self._items) > MAX_ORDER_ITEMS:
            raise ValidationError(
                f"Order cannot have more than {MAX_ORDER_ITEMS} unique items",
                self.order_id,
            )
    
    @property
    def items(self) -> List[OrderItem]:
        """Get a copy of the items list to prevent external modification."""
        return self._items.copy()
    
    @property
    def subtotal(self) -> Decimal:
        """Calculate order subtotal (sum of all item subtotals)."""
        total = Decimal("0.00")
        for item in self._items:
            total += item.subtotal
        return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    
    @property
    def tax_amount(self) -> Decimal:
        """Calculate total tax for the order."""
        total = Decimal("0.00")
        for item in self._items:
            total += item.tax_amount
        return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    
    @property
    def total(self) -> Decimal:
        """Calculate order total (subtotal + tax)."""
        return (self.subtotal + self.tax_amount).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
    
    def _validate_order(self) -> None:
        """Internal method to validate order consistency."""
        errors: List[str] = []
        
        if not self.order_id:
            errors.append("Order ID cannot be empty")
        
        if not self.customer_id:
            errors.append("Customer ID cannot be empty")
        
        if not self._items:
            errors.append("Order must contain at least one item")
        
        if self.subtotal < MIN_ORDER_VALUE:
            errors.append(f"Order value must be at least {MIN_ORDER_VALUE}")
        
        if self.shipping_country and self.shipping_country not in VALID_COUNTRIES:
            errors.append(f"Invalid shipping country: {self.shipping_country}")
        
        if errors:
            raise ValidationError(
                "Order validation failed",
                self.order_id,
                validation_errors=errors,
            )
    
    def update_status(self, new_status: OrderStatus) -> None:
        """Update order status with validation.
        
        Args:
            new_status: The new status to set
            
        Raises:
            ValueError: If status transition is invalid
        """
        # Define valid status transitions
        valid_transitions: Dict[OrderStatus, List[OrderStatus]] = {
            OrderStatus.PENDING: [OrderStatus.PROCESSING, OrderStatus.CANCELLED],
            OrderStatus.PROCESSING: [OrderStatus.SHIPPED, OrderStatus.CANCELLED],
            OrderStatus.SHIPPED: [OrderStatus.DELIVERED],
            OrderStatus.DELIVERED: [OrderStatus.REFUNDED],
            OrderStatus.CANCELLED: [],
            OrderStatus.REFUNDED: [],
        }
        
        if new_status not in valid_transitions.get(self.status, []):
            raise ValueError(
                f"Cannot transition from {self.status.name} to {new_status.name}"
            )
        
        logger.info(
            "Updating order %s status: %s -> %s",
            self.order_id,
            self.status.name,
            new_status.name,
        )
        self.status = new_status
    
    def to_dict(self, include_items: bool = True) -> Dict[str, Any]:
        """Convert order to dictionary for serialization.
        
        Args:
            include_items: Whether to include detailed item information
            
        Returns:
            Dictionary representation of the order
        """
        result: Dict[str, Any] = {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "status": self.status.name,
            "currency": self.currency,
            "subtotal": float(self.subtotal),
            "tax_amount": float(self.tax_amount),
            "total": float(self.total),
            "item_count": len(self._items),
            "created_at": self.created_at.isoformat(),
        }
        
        if self.shipping_country:
            result["shipping_country"] = self.shipping_country
        
        if include_items:
            result["items"] = [item.to_dict() for item in self._items]
        
        return result
    
    def to_json(self, indent: Optional[int] = 2) -> str:
        """Convert order to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)
    
    @classmethod
    def from_dict(cls, data: OrderDict) -> "Order":
        """Create an Order instance from a dictionary.
        
        Args:
            data: Dictionary containing order data
            
        Returns:
            New Order instance
            
        Raises:
            ValidationError: If data is invalid
        """
        try:
            # Extract items data
            items_data = data.get("items", [])
            items: List[OrderItem] = []
            
            for item_data in items_data:
                item = OrderItem(
                    product_id=str(item_data["product_id"]),
                    name=str(item_data["name"]),
                    quantity=int(item_data["quantity"]),
                    unit_price=Decimal(str(item_data["unit_price"])),
                    category=ProductCategory.get_by_name(str(item_data["category"])),
                    currency=str(item_data.get("currency", DEFAULT_CURRENCY)),
                )
                items.append(item)
            
            # Create order
            return cls(
                order_id=str(data["order_id"]),
                customer_id=str(data["customer_id"]),
                items=items,
                currency=str(data.get("currency", DEFAULT_CURRENCY)),
                status=OrderStatus.from_string(str(data.get("status", "PENDING"))),
                shipping_country=(
                    str(data["shipping_country"])
                    if "shipping_country" in data else None
                ),
            )
        except (KeyError, ValueError, TypeError) as e:
            raise ValidationError(f"Invalid order data: {e}")
    
    def __repr__(self) -> str:
        """Machine-readable representation."""
        return (
            f"Order(order_id={self.order_id!r}, "
            f"customer_id={self.customer_id!r}, "
            f"item_count={len(self._items)}, "
            f"total={self.total})"
        )
    
    def __str__(self) -> str:
        """Human-readable representation."""
        return (
            f"Order {self.order_id} "
            f"({self.status.display_name if hasattr(self.status, 'display_name') else self.status.name}) - "
            f"{self.total} {self.currency}"
        )
    
    def __len__(self) -> int:
        """Return number of items in the order."""
        return len(self._items)
    
    @classmethod
    def get_total_orders(cls) -> int:
        """Get total number of orders created."""
        return cls._order_counter


# ============================================================================
# ABSTRACT BASE CLASSES AND INTERFACES
# ============================================================================

class DataExporter(ABC, Generic[T]):
    """Abstract base class for exporting data to different formats.
    
    This demonstrates the use of ABCs and Generics for creating
    extensible interfaces.
    
    Type Parameters:
        T: The type of data being exported
    """
    
    @abstractmethod
    def export(self, data: T, destination: Union[str, Path]) -> bool:
        """Export data to destination.
        
        Args:
            data: Data to export
            destination: Path or location to export to
            
        Returns:
            True if export succeeded, False otherwise
        """
        pass
    
    @abstractmethod
    def get_extension(self) -> str:
        """Get file extension for this exporter."""
        pass


class JSONExporter(DataExporter[Order]):
    """Export orders to JSON format."""
    
    def export(self, data: Order, destination: Union[str, Path]) -> bool:
        """Export order to JSON file."""
        try:
            path = Path(destination)
            path.write_text(data.to_json())
            logger.info("Exported order %s to %s", data.order_id, destination)
            return True
        except (IOError, OSError) as e:
            logger.error("Failed to export order: %s", e)
            return False
    
    def get_extension(self) -> str:
        return ".json"


class CSVExporter(DataExporter[List[Order]]):
    """Export multiple orders to CSV format."""
    
    def export(self, data: List[Order], destination: Union[str, Path]) -> bool:
        """Export orders to CSV file."""
        try:
            with open(destination, "w", newline="") as f:
                writer = csv.writer(f)
                # Write header
                writer.writerow([
                    "order_id", "customer_id", "status", "item_count",
                    "subtotal", "tax_amount", "total", "currency",
                    "created_at", "shipping_country"
                ])
                
                # Write data rows
                for order in data:
                    writer.writerow([
                        order.order_id,
                        order.customer_id,
                        order.status.name,
                        len(order),
                        float(order.subtotal),
                        float(order.tax_amount),
                        float(order.total),
                        order.currency,
                        order.created_at.isoformat(),
                        order.shipping_country or "",
                    ])
            
            logger.info("Exported %d orders to %s", len(data), destination)
            return True
        except (IOError, OSError) as e:
            logger.error("Failed to export orders: %s", e)
            return False
    
    def get_extension(self) -> str:
        return ".csv"


# ============================================================================
# FUNCTIONAL PROGRAMMING UTILITIES
# ============================================================================

def process_orders(
    orders: Iterable[Order],
    processor: Callable[[Order], Any],
    filter_func: Optional[Callable[[Order], bool]] = None,
) -> List[Any]:
    """Process orders with optional filtering.
    
    This demonstrates functional programming concepts:
    - Higher-order functions
    - Callable types
    - Optional parameters with None defaults
    
    Args:
        orders: Iterable of Order objects
        processor: Function to apply to each order
        filter_func: Optional filter function
    
    Returns:
        List of results from processor
    
    Example:
        >>> def get_total(order: Order) -> Decimal:
        ...     return order.total
        >>> totals = process_orders(orders, get_total)
    """
    results: List[Any] = []
    
    for order in orders:
        if filter_func is None or filter_func(order):
            try:
                result = processor(order)
                results.append(result)
            except Exception as e:
                logger.warning("Failed to process order %s: %s", order.order_id, e)
    
    return results


def filter_by_status(status: OrderStatus) -> Callable[[Order], bool]:
    """Create a filter function for specific order status.
    
    This is a function factory that returns a closure.
    
    Args:
        status: Status to filter by
    
    Returns:
        Filter function that takes an Order and returns bool
    """
    def status_filter(order: Order) -> bool:
        return order.status == status
    
    return status_filter


# ============================================================================
# CONTEXT MANAGERS FOR RESOURCE MANAGEMENT
# ============================================================================

class OrderBatchProcessor:
    """Context manager for batch processing orders.
    
    Demonstrates proper resource management and context manager protocol.
    """
    
    def __init__(self, output_dir: Union[str, Path]):
        self.output_dir = Path(output_dir)
        self.processed_count = 0
        self.failed_count = 0
        self._log_file = None
    
    def __enter__(self) -> "OrderBatchProcessor":
        """Set up batch processing context."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create log file
        log_path = self.output_dir / "processing.log"
        self._log_file = open(log_path, "w")
        self._log_file.write(f"Batch processing started at {datetime.datetime.now()}\n")
        
        logger.info("Started batch processing in %s", self.output_dir)
        return self
    
    def process_order(self, order: Order, exporter: DataExporter) -> bool:
        """Process a single order."""
        try:
            filename = f"order_{order.order_id}_{order.created_at:%Y%m%d}{exporter.get_extension()}"
            output_path = self.output_dir / filename
            
            success = exporter.export(order, output_path)
            
            if success:
                self.processed_count += 1
                self._log_file.write(f"SUCCESS: Order {order.order_id}\n")
                return True
            else:
                self.failed_count += 1
                self._log_file.write(f"FAILED: Order {order.order_id}\n")
                return False
                
        except Exception as e:
            self.failed_count += 1
            self._log_file.write(f"ERROR: Order {order.order_id} - {e}\n")
            return False
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Clean up batch processing context."""
        if self._log_file:
            self._log_file.write(f"\nProcessing completed at {datetime.datetime.now()}\n")
            self._log_file.write(f"Processed: {self.processed_count}, Failed: {self.failed_count}\n")
            self._log_file.close()
        
        logger.info(
            "Batch processing completed: %d processed, %d failed",
            self.processed_count,
            self.failed_count,
        )
        
        if exc_type:
            logger.error("Batch processing failed with error: %s", exc_val)


# ============================================================================
# MAIN APPLICATION WITH PROPER ERROR HANDLING
# ============================================================================

def calculate_order_statistics(
    orders: List[Order],
    currency: Optional[Currency] = None,
) -> Dict[str, Union[Decimal, int, Dict[str, Decimal]]]:
    """Calculate comprehensive statistics for a list of orders.
    
    This function demonstrates:
    - Complex return types with Dict and Union
    - Optional parameters
    - Type-safe calculations
    
    Args:
        orders: List of Order objects
        currency: Optional filter for specific currency
    
    Returns:
        Dictionary containing various statistics
    
    Raises:
        ValueError: If no orders provided
    """
    if not orders:
        raise ValueError("No orders provided")
    
    # Filter by currency if specified
    filtered_orders = (
        orders
        if currency is None
        else [o for o in orders if o.currency == currency]
    )
    
    if not filtered_orders:
        raise ValueError(f"No orders found for currency {currency}")
    
    # Calculate statistics
    order_count = len(filtered_orders)
    total_value = Decimal("0.00")
    total_tax = Decimal("0.00")
    category_totals: Dict[str, Decimal] = defaultdict(Decimal)
    
    for order in filtered_orders:
        total_value += order.total
        total_tax += order.tax_amount
        
        for item in order.items:
            category_totals[item.category.display_name] += item.total
    
    avg_order_value = total_value / order_count if order_count > 0 else Decimal("0.00")
    
    # Find most valuable order
    most_valuable = max(filtered_orders, key=lambda o: o.total, default=None)
    
    return {
        "order_count": order_count,
        "total_value": total_value.quantize(Decimal("0.01")),
        "total_tax": total_tax.quantize(Decimal("0.01")),
        "average_order_value": avg_order_value.quantize(Decimal("0.01")),
        "category_breakdown": dict(category_totals),
        "currency": currency or filtered_orders[0].currency,
        "most_valuable_order": {
            "order_id": most_valuable.order_id if most_valuable else None,
            "value": most_valuable.total if most_valuable else Decimal("0.00"),
        } if most_valuable else None,
    }


def load_orders_from_json(filepath: Union[str, Path]) -> List[Order]:
    """Load orders from JSON file.
    
    Demonstrates file I/O with proper error handling.
    """
    orders: List[Order] = []
    
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
        
        # Handle both single order and list of orders
        if isinstance(data, dict):
            # Single order
            orders.append(Order.from_dict(data))
        elif isinstance(data, list):
            # List of orders
            for order_data in data:
                try:
                    orders.append(Order.from_dict(order_data))
                except ValidationError as e:
                    logger.warning("Skipping invalid order data: %s", e)
        else:
            raise ValidationError("Invalid JSON structure")
        
        logger.info("Loaded %d orders from %s", len(orders), filepath)
        return orders
        
    except FileNotFoundError:
        logger.error("File not found: %s", filepath)
        return []
    except json.JSONDecodeError as e:
        logger.error("Invalid JSON in %s: %s", filepath, e)
        return []
    except Exception as e:
        logger.error("Error loading orders from %s: %s", filepath, e)
        return []


# ============================================================================
# CONFIGURATION AND SETUP
# ============================================================================

def setup_logging(level: int = logging.INFO) -> None:
    """Configure logging for the application.
    
    Demonstrates proper logging setup and configuration.
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("order_processing.log"),
        ],
    )


class Config:
    """Application configuration with type hints and validation."""
    
    def __init__(self, config_file: Optional[Union[str, Path]] = None):
        self.default_currency: Currency = DEFAULT_CURRENCY
        self.max_order_items: int = MAX_ORDER_ITEMS
        self.min_order_value: Decimal = MIN_ORDER_VALUE
        self.valid_countries: List[str] = list(VALID_COUNTRIES)
        self.log_level: int = logging.INFO
        
        if config_file:
            self._load_from_file(config_file)
    
    def _load_from_file(self, config_file: Union[str, Path]) -> None:
        """Load configuration from JSON file."""
        try:
            with open(config_file, "r") as f:
                config_data = json.load(f)
            
            # Update configuration with type checking
            if "default_currency" in config_data:
                self.default_currency = str(config_data["default_currency"])
            
            if "max_order_items" in config_data:
                self.max_order_items = int(config_data["max_order_items"])
            
            if "min_order_value" in config_data:
                self.min_order_value = Decimal(str(config_data["min_order_value"]))
            
            if "valid_countries" in config_data:
                self.valid_countries = [str(c) for c in config_data["valid_countries"]]
            
            if "log_level" in config_data:
                level_str = str(config_data["log_level"]).upper()
                self.log_level = getattr(logging, level_str, logging.INFO)
                
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.warning("Could not load config file %s: %s", config_file, e)


# ============================================================================
# MAIN EXECUTION WITH PROPER GUARD
# ============================================================================

def main() -> None:
    """Main entry point for the order processing application."""
    
    # Setup
    setup_logging()
    config = Config()
    
    logger.info("Starting order processing application")
    
    try:
        # Create sample orders
        electronics_item = OrderItem(
            product_id="LAPTOP-001",
            name="Gaming Laptop",
            quantity=1,
            unit_price=Decimal("1299.99"),
            category=ProductCategory.ELECTRONICS,
        )
        
        clothing_item = OrderItem(
            product_id="SHIRT-001",
            name="T-Shirt",
            quantity=3,
            unit_price=Decimal("19.99"),
            category=ProductCategory.CLOTHING,
        )
        
        book_item = OrderItem(
            product_id="BOOK-001",
            name="Python Cookbook",
            quantity=2,
            unit_price=Decimal("39.99"),
            category=ProductCategory.BOOKS,
        )
        
        # Create orders
        order1 = Order(
            order_id="ORD-001",
            customer_id="CUST-001",
            items=[electronics_item, clothing_item],
            shipping_country="US",
        )
        
        order2 = Order(
            order_id="ORD-002",
            customer_id="CUST-002",
            items=[book_item],
            shipping_country="GB",
        )
        
        logger.info("Created %d orders", Order.get_total_orders())
        
        # Demonstrate order processing
        orders = [order1, order2]
        
        # Calculate statistics
        stats = calculate_order_statistics(orders)
        logger.info("Order statistics: %s", json.dumps(stats, default=str, indent=2))
        
        # Process orders in batch
        output_dir = Path("output")
        with OrderBatchProcessor(output_dir) as processor:
            json_exporter = JSONExporter()
            
            for order in orders:
                processor.process_order(order, json_exporter)
        
        # Demonstrate functional programming
        total_processor = lambda o: o.total  # Simple lambda
        totals = process_orders(orders, total_processor)
        logger.info("Order totals: %s", totals)
        
        # Filter orders by status
        pending_filter = filter_by_status(OrderStatus.PENDING)
        pending_orders = [o for o in orders if pending_filter(o)]
        logger.info("Pending orders: %d", len(pending_orders))
        
        # Type checking demonstration
        print("\n" + "="*60)
        print("TYPE HINTS DEMONSTRATION")
        print("="*60)
        
        # Get type hints programmatically
        type_hints = get_type_hints(Order.__init__)
        print("Order.__init__ type hints:")
        for param, hint in type_hints.items():
            print(f"  {param}: {hint}")
        
        print(f"\nTotal orders created: {Order.get_total_orders()}")
        
    except Exception as e:
        logger.error("Application error: %s", e, exc_info=True)
        sys.exit(1)
    
    logger.info("Application completed successfully")


if __name__ == "__main__":
    main()


# ============================================================================
# CODE QUALITY TOOLS DEMONSTRATION
# ============================================================================

"""
PYTHON CODE QUALITY TOOLS CHEAT SHEET
=====================================

1. PEP 8 AND STYLE GUIDES
   -----------------------
   - Use 4 spaces per indentation level (no tabs)
   - Max line length: 79 characters for code, 72 for docstrings/comments
   - Blank lines: 2 before class/function defs, 1 between methods
   - Imports: stdlib → third-party → local (alphabetical within groups)
   - Naming:
        ClassName (PascalCase)
        function_name (snake_case)
        variable_name (snake_case)
        CONSTANT_NAME (UPPER_SNAKE_CASE)
        _private_name (leading underscore)
        __mangled_name (double underscore)
   
   Tools: pycodestyle, autopep8

2. TYPE HINTS (typing module)
   ---------------------------
   - Added in Python 3.5+, improved in later versions
   - Use for function parameters, return values, variables
   - Common types: int, str, List[T], Dict[K, V], Optional[T], Union[A, B]
   - Type aliases for complex types: TypeAlias = Dict[str, List[int]]
   - Generics: class Container(Generic[T]):
   - TypeVar for generic functions: T = TypeVar('T')
   
   Example:
        def process(items: List[str]) -> Optional[int]:
            ...

3. MYPY BASICS
   ------------
   - Static type checker: pip install mypy
   - Run: mypy your_file.py
   - Configuration: mypy.ini or pyproject.toml
   - Common options:
        --strict              # Enable all checks
        --ignore-missing-imports
        --warn-unused-ignores
        --disallow-untyped-defs
   
   Example mypy.ini:
        [mypy]
        python_version = 3.9
        warn_return_any = true
        disallow_untyped_defs = true
        ignore_missing_imports = true

4. LINTING (flake8, ruff)
   -----------------------
   flake8:
        pip install flake8
        flake8 your_file.py
        # Checks: pycodestyle (PEP 8), pyflakes (logical errors), mccabe (complexity)
   
   ruff:
        pip install ruff
        ruff check your_file.py  # Much faster than flake8
        ruff format your_file.py  # Also formats code
   
   Common plugins:
        flake8-docstrings  # pydocstyle integration
        flake8-import-order  # Import ordering
        flake8-bugbear  # Additional checks

5. FORMATTING (black, isort)
   --------------------------
   black:
        pip install black
        black your_file.py  # Uncompromising code formatter
        black --check your_file.py  # Check without formatting
   
   isort:
        pip install isort
        isort your_file.py  # Sort imports
        isort --profile black your_file.py  # Black-compatible
   
   pre-commit:  # Automate formatting/linting
        pip install pre-commit
        # .pre-commit-config.yaml:
        repos:
          - repo: https://github.com/psf/black
            rev: stable
            hooks: [ {id: black} ]
          - repo: https://github.com/pycqa/isort
            rev: 5.10.1
            hooks: [ {id: isort} ]

6. DOCUMENTATION (docstrings, Sphinx)
   -----------------------------------
   Docstring styles:
        Google style:
            '''Short description.
            
            Args:
                param1: Description
                param2: Description
                
            Returns:
                Description of return value
            '''
        
        NumPy style:
            '''Short description.
            
            Parameters
            ----------
            param1 : type
                Description
                
            Returns
            -------
            type
                Description
            '''
   
   Sphinx:
        pip install sphinx
        sphinx-quickstart docs/
        # In conf.py: extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']
        sphinx-apidoc -o docs/source/ .
        make html  # Build HTML documentation

7. STATIC VS RUNTIME CHECKS
   -------------------------
   Static checks (compile-time):
        - Type checking (mypy)
        - Linting (flake8, ruff)
        - Complexity (radon, mccabe)
        - Security (bandit, safety)
   
   Runtime checks:
        - isinstance() for type validation
        - assert statements (disabled with -O flag)
        - Custom validation in __post_init__ (dataclasses)
        - pydantic for runtime type validation
   
   Example runtime validation:
        def process(value: Any) -> int:
            if not isinstance(value, (int, float)):
                raise TypeError(f"Expected numeric, got {type(value)}")
            return int(value)

TOOL INTEGRATION EXAMPLE (pyproject.toml):
------------------------------------------
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[tool.black]
line-length = 88
target-version = ['py39']

[tool.isort]
profile = "black"
multi_line_output = 3

[tool.mypy]
python_version = "3.9"
warn_return_any = true
disallow_untyped_defs = true
ignore_missing_imports = true

[tool.ruff]
line-length = 88
target-version = "py39"
select = [
    "E",  # pycodestyle errors
    "F",  # pyflakes
    "I",  # isort
    "B",  # flake8-bugbear
]

[tool.pytest.ini_options]
minversion = "6.0"
addopts = "-ra -q"
testpaths = ["tests"]

RUNNING ALL TOOLS:
------------------
# Create a Makefile or scripts
check: format lint type test

format:
    black .
    isort .

lint:
    ruff check .

type:
    mypy .

test:
    pytest tests/
"""


# ============================================================================
# EXAMPLE OF PROBLEMATIC CODE FOR LINTERS TO CATCH
# ============================================================================

class BadCodeExample:
    """Example class with code quality issues for linters to detect."""
    
    def __init__(self):  # Missing return type hint
        self.data = {}  # Type not specified
        self._cache=[]  # Missing spaces around =
    
    def process(self, input):  # Missing type hints, line too long if we add more parameters here to exceed 79 characters
        result=[]
        for x in input:
            if x not in self.data.keys():  # Inefficient: .keys() not needed
                result.append(x)
            elif x>0:  # Missing spaces
                result.append(x*2)
        return result  # Inconsistent return type
    
    def unused_method(self):  # Method never used
        pass
    
    # Too many blank lines
    
    
    def another_method(self, a, b, c, d, e, f, g, h, i, j):  # Too many parameters
        return a + b + c + d + e + f + g + h + i + j


def problematic_function():
    """Function with various code quality issues."""
    x=1  # Missing spaces
    y = 2
    z = x + y
    print(z)
    
    # Unused variable
    unused = "This variable is never used"
    
    # Too broad exception
    try:
        result = 1 / 0
    except:
        pass
    
    # Comparison with literal
    if z == True:  # Should be 'if z:'
        pass
    
    return z  # Missing return type hint


# ============================================================================
# EXAMPLE OF GOOD CODE FOR COMPARISON
# ============================================================================

class GoodCodeExample:
    """Example class following all code quality guidelines."""
    
    def __init__(self) -> None:
        """Initialize with proper type hints."""
        self.data: Dict[str, int] = {}
        self._cache: List[str] = []
        self._initialized: bool = False
    
    def process(self, inputs: List[int]) -> List[int]:
        """Process list of integers with proper formatting.
        
        Args:
            inputs: List of integers to process
            
        Returns:
            Processed list of integers
        """
        result: List[int] = []
        
        for x in inputs:
            if x not in self.data:  # Direct dictionary lookup
                result.append(x)
            elif x > 0:  # Proper spacing
                result.append(x * 2)
        
        return result
    
    def calculate(
        self,
        values: List[float],
        multiplier: float = 1.0,
    ) -> float:
        """Calculate with reasonable number of parameters.
        
        Args:
            values: Numbers to calculate with
            multiplier: Scaling factor
            
        Returns:
            Calculated result
        """
        if not values:
            return 0.0
        
        total = sum(values)
        return total * multiplier
    
    def safe_division(self, numerator: float, denominator: float) -> float:
        """Perform safe division with specific exception handling.
        
        Args:
            numerator: Number to divide
            denominator: Number to divide by
            
        Returns:
            Result of division
            
        Raises:
            ZeroDivisionError: If denominator is zero
            ValueError: If inputs are invalid
        """
        if denominator == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        
        if not isinstance(numerator, (int, float)):
            raise TypeError(f"Numerator must be numeric, got {type(numerator)}")
        
        return numerator / denominator


def well_written_function(input_value: int) -> str:
    """Properly formatted and typed function.
    
    Args:
        input_value: Integer input
        
    Returns:
        String representation of processed input
    """
    x = 1  # Proper spacing
    y = 2
    z = x + y + input_value
    
    # Meaningful variable names
    processed_value = z * 2
    
    # Specific exception handling
    try:
        result = 100 / processed_value
    except ZeroDivisionError:
        result = 0
    
    # Proper boolean comparison
    if result > 0:
        return f"Positive result: {result}"
    
    return "Non-positive result"


# ============================================================================
# HOW TO RUN CODE QUALITY TOOLS
# ============================================================================

"""
1. INSTALL ALL TOOLS:
   pip install black isort flake8 ruff mypy pytest

2. CREATE CONFIGURATION FILES:

   pyproject.toml (modern approach):
   ---------------------------------
   [tool.black]
   line-length = 88
   target-version = ['py39']
   
   [tool.isort]
   profile = "black"
   
   [tool.mypy]
   python_version = "3.9"
   warn_return_any = true
   disallow_untyped_defs = true
   ignore_missing_imports = true
   
   [tool.ruff]
   line-length = 88
   target-version = "py39"
   select = ["E", "F", "I", "B", "C", "N"]

   setup.cfg (legacy):
   -------------------
   [flake8]
   max-line-length = 88
   extend-ignore = E203, W503
   
   [isort]
   profile = black
   multi_line_output = 3
   
   [mypy]
   python_version = 3.9
   warn_return_any = true
   disallow_untyped_defs = true

3. RUN TOOLS:

   # Format code
   black code_quality_demo.py
   isort code_quality_demo.py
   
   # Lint code
   flake8 code_quality_demo.py
   ruff check code_quality_demo.py
   
   # Type check
   mypy code_quality_demo.py
   
   # All in one (if using pre-commit)
   pre-commit run --all-files

4. INTEGRATE WITH IDE:

   VS Code Settings:
   {
     "python.formatting.provider": "black",
     "python.formatting.blackArgs": ["--line-length", "88"],
     "python.linting.enabled": true,
     "python.linting.flake8Enabled": true,
     "python.linting.mypyEnabled": true,
     "editor.formatOnSave": true,
     "editor.codeActionsOnSave": {
       "source.organizeImports": true
     }
   }

5. CI/CD PIPELINE EXAMPLE (.github/workflows/ci.yml):
   
   name: CI
   on: [push, pull_request]
   
   jobs:
     quality:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v2
         - uses: actions/setup-python@v2
           
         - name: Install dependencies
           run: pip install black isort flake8 mypy pytest
           
         - name: Check formatting
           run: black --check .
           
         - name: Check imports
           run: isort --check-only .
           
         - name: Lint
           run: flake8 .
           
         - name: Type check
           run: mypy .
           
         - name: Test
           run: pytest tests/
"""

print("\n" + "="*70)
print("CODE QUALITY SUMMARY")
print("="*70)
print("\nKey principles demonstrated in this file:")
print("1. PEP 8 compliance throughout")
print("2. Comprehensive type hints for all functions and methods")
print("3. Proper documentation with Google-style docstrings")
print("4. Clean import organization")
print("5. Meaningful variable and function names")
print("6. Error handling and validation")
print("7. Separation of concerns with classes and functions")
print("\nRun the tools to see this code in action!")