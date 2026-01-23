"""
COMPREHENSIVE DATABASES & SQL DEMONSTRATION
===========================================

This module demonstrates key database concepts:
1. SQL fundamentals (joins, indexes, transactions)
2. ORMs (Active Record vs Data Mapper patterns)
3. Transactions and ACID properties
4. Connection pooling concepts
5. Basic migrations
"""

# ============================================================================
# SECTION 1: IMPORTS AND SETUP
# ============================================================================

import os
import sys
import sqlite3
import json
import time
import threading
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime, timedelta
from contextlib import contextmanager
import csv
import random

# SQLAlchemy for ORM demonstration
from sqlalchemy import (
    create_engine, Column, Integer, String, Float, DateTime, 
    ForeignKey, Text, Boolean, Index, CheckConstraint, UniqueConstraint,
    func, select, and_, or_, not_, desc, asc
)
from sqlalchemy.orm import (
    declarative_base, sessionmaker, relationship, 
    joinedload, subqueryload, Session
)
from sqlalchemy.pool import QueuePool, StaticPool
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

# For connection pooling demonstration
import psycopg2  # For PostgreSQL demonstration
from psycopg2 import pool

# Create demonstration directory
demo_dir = Path("demo_databases")
demo_dir.mkdir(exist_ok=True)

# ============================================================================
# SECTION 2: SQL FUNDAMENTALS DEMONSTRATION
# ============================================================================

class SqlFundamentals:
    """Demonstrates SQL fundamentals: joins, indexes, transactions."""
    
    def __init__(self):
        self.db_path = demo_dir / "sql_fundamentals.db"
        self.connection = None
        self.setup_database()
        
    def setup_database(self):
        """Create a sample database with normalized tables."""
        print("\n" + "="*60)
        print("SQL FUNDAMENTALS DEMONSTRATION")
        print("="*60)
        
        # Connect to SQLite database
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row  # Return rows as dictionaries
        cursor = self.connection.cursor()
        
        print("\n1. Creating Normalized Database Schema:")
        
        # Drop tables if they exist
        cursor.executescript('''
            DROP TABLE IF EXISTS order_items;
            DROP TABLE IF EXISTS orders;
            DROP TABLE IF EXISTS customers;
            DROP TABLE IF EXISTS products;
            DROP TABLE IF EXISTS categories;
            DROP TABLE IF EXISTS employees;
            DROP TABLE IF EXISTS departments;
        ''')
        
        # Create normalized tables
        cursor.executescript('''
            -- Departments table
            CREATE TABLE departments (
                department_id INTEGER PRIMARY KEY AUTOINCREMENT,
                department_name VARCHAR(100) NOT NULL,
                location VARCHAR(100),
                budget DECIMAL(12,2) DEFAULT 0.00,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- Employees table
            CREATE TABLE employees (
                employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                hire_date DATE NOT NULL,
                salary DECIMAL(10,2),
                department_id INTEGER,
                manager_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (department_id) REFERENCES departments(department_id),
                FOREIGN KEY (manager_id) REFERENCES employees(employee_id),
                CHECK (salary >= 0)
            );
            
            -- Categories table
            CREATE TABLE categories (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_name VARCHAR(100) NOT NULL UNIQUE,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- Products table
            CREATE TABLE products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name VARCHAR(200) NOT NULL,
                description TEXT,
                category_id INTEGER NOT NULL,
                unit_price DECIMAL(10,2) NOT NULL,
                units_in_stock INTEGER DEFAULT 0,
                units_on_order INTEGER DEFAULT 0,
                discontinued BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories(category_id),
                CHECK (unit_price >= 0),
                CHECK (units_in_stock >= 0),
                CHECK (units_on_order >= 0)
            );
            
            -- Customers table
            CREATE TABLE customers (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name VARCHAR(100) NOT NULL,
                contact_name VARCHAR(100),
                contact_title VARCHAR(50),
                address TEXT,
                city VARCHAR(50),
                region VARCHAR(50),
                postal_code VARCHAR(20),
                country VARCHAR(50),
                phone VARCHAR(30),
                email VARCHAR(100) UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- Orders table
            CREATE TABLE orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                employee_id INTEGER,
                order_date DATE NOT NULL,
                required_date DATE,
                shipped_date DATE,
                ship_via VARCHAR(50),
                freight DECIMAL(10,2) DEFAULT 0.00,
                ship_name VARCHAR(100),
                ship_address TEXT,
                ship_city VARCHAR(50),
                ship_region VARCHAR(50),
                ship_postal_code VARCHAR(20),
                ship_country VARCHAR(50),
                status VARCHAR(20) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
                CHECK (freight >= 0),
                CHECK (order_date <= required_date)
            );
            
            -- Order items table
            CREATE TABLE order_items (
                order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                unit_price DECIMAL(10,2) NOT NULL,
                quantity INTEGER NOT NULL,
                discount DECIMAL(4,2) DEFAULT 0.00,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (order_id) REFERENCES orders(order_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id),
                CHECK (unit_price >= 0),
                CHECK (quantity > 0),
                CHECK (discount >= 0 AND discount <= 1)
            );
        ''')
        
        print("   • Created 7 normalized tables")
        print("   • Added primary and foreign keys")
        print("   • Added CHECK constraints for data integrity")
        
        # Insert sample data
        self.insert_sample_data(cursor)
        
        # Create indexes
        self.create_indexes(cursor)
        
        self.connection.commit()
        
    def insert_sample_data(self, cursor):
        """Insert sample data into all tables."""
        print("\n2. Inserting Sample Data:")
        
        # Insert departments
        departments = [
            ('Sales', 'New York', 1000000.00),
            ('Marketing', 'Chicago', 750000.00),
            ('Engineering', 'San Francisco', 2000000.00),
            ('Finance', 'New York', 900000.00),
            ('HR', 'Chicago', 500000.00)
        ]
        
        cursor.executemany(
            'INSERT INTO departments (department_name, location, budget) VALUES (?, ?, ?)',
            departments
        )
        print("   • Inserted 5 departments")
        
        # Insert employees
        employees = [
            ('John', 'Doe', 'john.doe@company.com', '2020-01-15', 75000.00, 1, None),
            ('Jane', 'Smith', 'jane.smith@company.com', '2019-03-20', 85000.00, 1, 1),
            ('Bob', 'Johnson', 'bob.johnson@company.com', '2021-06-10', 95000.00, 3, None),
            ('Alice', 'Williams', 'alice.williams@company.com', '2018-11-05', 80000.00, 2, None),
            ('Charlie', 'Brown', 'charlie.brown@company.com', '2022-02-28', 65000.00, 3, 3)
        ]
        
        cursor.executemany(
            '''INSERT INTO employees (first_name, last_name, email, hire_date, salary, department_id, manager_id) 
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            employees
        )
        print("   • Inserted 5 employees")
        
        # Insert categories
        categories = [
            ('Electronics', 'Electronic devices and accessories'),
            ('Clothing', 'Apparel and fashion items'),
            ('Books', 'Books and publications'),
            ('Home & Garden', 'Home improvement and garden supplies'),
            ('Sports', 'Sports equipment and accessories')
        ]
        
        cursor.executemany(
            'INSERT INTO categories (category_name, description) VALUES (?, ?)',
            categories
        )
        print("   • Inserted 5 categories")
        
        # Insert products
        products = [
            ('Laptop Pro', 'High-performance laptop', 1, 1299.99, 50, 10),
            ('Wireless Mouse', 'Ergonomic wireless mouse', 1, 49.99, 200, 50),
            ('T-Shirt', 'Cotton t-shirt', 2, 19.99, 500, 100),
            ('Python Cookbook', 'Advanced Python programming', 3, 39.99, 100, 25),
            ('Garden Hose', '50ft heavy-duty garden hose', 4, 29.99, 75, 20),
            ('Basketball', 'Official size basketball', 5, 24.99, 150, 30),
            ('Smartphone', 'Latest smartphone model', 1, 899.99, 30, 15),
            ('Jeans', 'Denim jeans', 2, 59.99, 300, 75),
            ('Desk Lamp', 'LED desk lamp', 4, 34.99, 120, 40)
        ]
        
        cursor.executemany(
            '''INSERT INTO products (product_name, description, category_id, unit_price, units_in_stock, units_on_order) 
               VALUES (?, ?, ?, ?, ?, ?)''',
            products
        )
        print("   • Inserted 9 products")
        
        # Insert customers
        customers = [
            ('Tech Solutions Inc', 'Mike Johnson', 'CEO', '123 Tech St', 'San Francisco', 'CA', '94105', 'USA', '+1-555-1234', 'mike@techsolutions.com'),
            ('Global Retail', 'Sarah Miller', 'Purchasing Manager', '456 Market St', 'New York', 'NY', '10001', 'USA', '+1-555-5678', 'sarah@globalretail.com'),
            ('Book Haven', 'David Wilson', 'Store Manager', '789 Book Ave', 'Chicago', 'IL', '60601', 'USA', '+1-555-9012', 'david@bookhaven.com'),
            ('Sports Gear Co', 'Lisa Taylor', 'Owner', '321 Sport Blvd', 'Miami', 'FL', '33101', 'USA', '+1-555-3456', 'lisa@sportsgear.com'),
            ('Home Essentials', 'Tom Brown', 'Director', '654 Home Rd', 'Los Angeles', 'CA', '90001', 'USA', '+1-555-7890', 'tom@homeessentials.com')
        ]
        
        cursor.executemany(
            '''INSERT INTO customers (company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, email) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            customers
        )
        print("   • Inserted 5 customers")
        
        # Insert orders
        orders = [
            (1, 1, '2024-01-15', '2024-01-20', '2024-01-18', 'UPS', 15.99, 'Mike Johnson', '123 Tech St', 'San Francisco', 'CA', '94105', 'USA', 'delivered'),
            (2, 2, '2024-01-20', '2024-01-25', '2024-01-22', 'FedEx', 12.50, 'Sarah Miller', '456 Market St', 'New York', 'NY', '10001', 'USA', 'shipped'),
            (3, 3, '2024-01-25', '2024-01-30', NULL, 'USPS', 8.99, 'David Wilson', '789 Book Ave', 'Chicago', 'IL', '60601', 'USA', 'processing'),
            (4, 1, '2024-02-01', '2024-02-05', NULL, 'UPS', 18.75, 'Lisa Taylor', '321 Sport Blvd', 'Miami', 'FL', '33101', 'USA', 'pending'),
            (5, 4, '2024-02-05', '2024-02-10', '2024-02-08', 'FedEx', 22.00, 'Tom Brown', '654 Home Rd', 'Los Angeles', 'CA', '90001', 'USA', 'delivered')
        ]
        
        cursor.executemany(
            '''INSERT INTO orders (customer_id, employee_id, order_date, required_date, shipped_date, ship_via, freight, 
               ship_name, ship_address, ship_city, ship_region, ship_postal_code, ship_country, status) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            orders
        )
        print("   • Inserted 5 orders")
        
        # Insert order items
        order_items = [
            (1, 1, 1299.99, 2, 0.10),  # 2 Laptops with 10% discount
            (1, 2, 49.99, 5, 0.05),     # 5 Mice with 5% discount
            (2, 3, 19.99, 20, 0.15),    # 20 T-Shirts with 15% discount
            (2, 6, 24.99, 10, 0.00),    # 10 Basketballs
            (3, 4, 39.99, 5, 0.20),     # 5 Books with 20% discount
            (4, 5, 29.99, 3, 0.00),     # 3 Garden Hoses
            (4, 7, 899.99, 1, 0.05),    # 1 Smartphone with 5% discount
            (5, 8, 59.99, 4, 0.10),     # 4 Jeans with 10% discount
            (5, 9, 34.99, 2, 0.00)      # 2 Desk Lamps
        ]
        
        cursor.executemany(
            '''INSERT INTO order_items (order_id, product_id, unit_price, quantity, discount) 
               VALUES (?, ?, ?, ?, ?)''',
            order_items
        )
        print("   • Inserted 9 order items")
        
    def create_indexes(self, cursor):
        """Create indexes for performance optimization."""
        print("\n3. Creating Indexes for Performance:")
        
        indexes = [
            "CREATE INDEX idx_orders_customer_id ON orders(customer_id)",
            "CREATE INDEX idx_orders_employee_id ON orders(employee_id)",
            "CREATE INDEX idx_orders_order_date ON orders(order_date)",
            "CREATE INDEX idx_orders_status ON orders(status)",
            "CREATE INDEX idx_products_category_id ON products(category_id)",
            "CREATE INDEX idx_products_unit_price ON products(unit_price)",
            "CREATE INDEX idx_employees_department_id ON employees(department_id)",
            "CREATE INDEX idx_employees_email ON employees(email)",
            "CREATE INDEX idx_order_items_order_id ON order_items(order_id)",
            "CREATE INDEX idx_order_items_product_id ON order_items(product_id)",
            "CREATE INDEX idx_customers_email ON customers(email)",
            "CREATE INDEX idx_customers_city ON customers(city)",
            "CREATE INDEX idx_customers_country ON customers(country)"
        ]
        
        for index_sql in indexes:
            try:
                cursor.execute(index_sql)
                index_name = index_sql.split(" ")[2]
                print(f"   • Created index: {index_name}")
            except Exception as e:
                print(f"   • Could not create index: {e}")
    
    def demonstrate_joins(self):
        """Demonstrate different types of SQL joins."""
        print("\n" + "="*60)
        print("SQL JOINS DEMONSTRATION")
        print("="*60)
        
        cursor = self.connection.cursor()
        
        print("\n1. INNER JOIN - Get orders with customer details:")
        cursor.execute('''
            SELECT 
                o.order_id,
                o.order_date,
                c.company_name,
                c.contact_name,
                c.city,
                o.status
            FROM orders o
            INNER JOIN customers c ON o.customer_id = c.customer_id
            ORDER BY o.order_date DESC
            LIMIT 5
        ''')
        
        results = cursor.fetchall()
        print("   Order ID | Order Date   | Company           | Contact       | City           | Status")
        print("   " + "-" * 80)
        for row in results:
            print(f"   {row['order_id']:9} | {row['order_date']:11} | {row['company_name'][:18]:18} | {row['contact_name'][:12]:12} | {row['city'][:14]:14} | {row['status']}")
        
        print("\n2. LEFT JOIN - Get all customers and their orders (including customers with no orders):")
        cursor.execute('''
            SELECT 
                c.customer_id,
                c.company_name,
                COUNT(o.order_id) as order_count,
                SUM(oi.quantity * oi.unit_price * (1 - oi.discount)) as total_spent
            FROM customers c
            LEFT JOIN orders o ON c.customer_id = o.customer_id
            LEFT JOIN order_items oi ON o.order_id = oi.order_id
            GROUP BY c.customer_id, c.company_name
            ORDER BY total_spent DESC
        ''')
        
        results = cursor.fetchall()
        print("   Customer ID | Company           | Orders | Total Spent")
        print("   " + "-" * 65)
        for row in results:
            total = row['total_spent'] if row['total_spent'] else 0
            print(f"   {row['customer_id']:11} | {row['company_name'][:18]:18} | {row['order_count']:6} | ${total:,.2f}")
        
        print("\n3. SELF JOIN - Get employees and their managers:")
        cursor.execute('''
            SELECT 
                e.employee_id,
                e.first_name || ' ' || e.last_name as employee_name,
                e.email,
                m.first_name || ' ' || m.last_name as manager_name,
                d.department_name
            FROM employees e
            LEFT JOIN employees m ON e.manager_id = m.employee_id
            LEFT JOIN departments d ON e.department_id = d.department_id
            ORDER BY e.department_id, e.employee_id
        ''')
        
        results = cursor.fetchall()
        print("   Employee ID | Employee Name     | Email                     | Manager        | Department")
        print("   " + "-" * 95)
        for row in results:
            manager = row['manager_name'] if row['manager_name'] else 'No Manager'
            print(f"   {row['employee_id']:11} | {row['employee_name'][:17]:17} | {row['email'][:25]:25} | {manager[:13]:13} | {row['department_name']}")
        
        print("\n4. MULTIPLE JOINS - Get detailed order information:")
        cursor.execute('''
            SELECT 
                o.order_id,
                o.order_date,
                c.company_name,
                e.first_name || ' ' || e.last_name as employee_name,
                p.product_name,
                oi.quantity,
                oi.unit_price,
                oi.discount,
                oi.quantity * oi.unit_price * (1 - oi.discount) as item_total
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            JOIN employees e ON o.employee_id = e.employee_id
            JOIN order_items oi ON o.order_id = oi.order_id
            JOIN products p ON oi.product_id = p.product_id
            WHERE o.order_id = 1
            ORDER BY o.order_date DESC
        ''')
        
        results = cursor.fetchall()
        print("   Order ID | Order Date   | Company           | Employee      | Product       | Qty | Price   | Disc | Total")
        print("   " + "-" * 110)
        for row in results:
            print(f"   {row['order_id']:9} | {row['order_date']:11} | {row['company_name'][:18]:18} | {row['employee_name'][:12]:12} | {row['product_name'][:12]:12} | {row['quantity']:3} | ${row['unit_price']:6.2f} | {row['discount']:.2f} | ${row['item_total']:7.2f}")
    
    def demonstrate_subqueries_and_ctes(self):
        """Demonstrate subqueries and Common Table Expressions (CTEs)."""
        print("\n" + "="*60)
        print("SUBQUERIES AND CTEs DEMONSTRATION")
        print("="*60)
        
        cursor = self.connection.cursor()
        
        print("\n1. SUBQUERY - Find products with above-average price:")
        cursor.execute('''
            SELECT 
                product_name,
                unit_price,
                category_name
            FROM products p
            JOIN categories c ON p.category_id = c.category_id
            WHERE unit_price > (
                SELECT AVG(unit_price) FROM products
            )
            ORDER BY unit_price DESC
        ''')
        
        results = cursor.fetchall()
        print("   Product Name         | Price     | Category")
        print("   " + "-" * 60)
        for row in results:
            print(f"   {row['product_name'][:20]:20} | ${row['unit_price']:8.2f} | {row['category_name']}")
        
        print("\n2. CORRELATED SUBQUERY - Find employees earning more than their department average:")
        cursor.execute('''
            SELECT 
                e.first_name || ' ' || e.last_name as employee_name,
                e.salary,
                d.department_name,
                (SELECT AVG(salary) FROM employees WHERE department_id = e.department_id) as dept_avg_salary
            FROM employees e
            JOIN departments d ON e.department_id = d.department_id
            WHERE e.salary > (
                SELECT AVG(salary) 
                FROM employees 
                WHERE department_id = e.department_id
            )
            ORDER BY e.salary DESC
        ''')
        
        results = cursor.fetchall()
        print("   Employee Name     | Salary    | Department   | Dept Avg Salary")
        print("   " + "-" * 75)
        for row in results:
            print(f"   {row['employee_name'][:17]:17} | ${row['salary']:8,.2f} | {row['department_name'][:12]:12} | ${row['dept_avg_salary']:8,.2f}")
        
        print("\n3. COMMON TABLE EXPRESSION (CTE) - Complex hierarchical query:")
        cursor.execute('''
            WITH RECURSIVE employee_hierarchy AS (
                -- Anchor member: employees with no manager (top-level)
                SELECT 
                    employee_id,
                    first_name || ' ' || last_name as employee_name,
                    department_id,
                    manager_id,
                    0 as level,
                    first_name || ' ' || last_name as path
                FROM employees
                WHERE manager_id IS NULL
                
                UNION ALL
                
                -- Recursive member: employees who report to managers
                SELECT 
                    e.employee_id,
                    e.first_name || ' ' || e.last_name,
                    e.department_id,
                    e.manager_id,
                    eh.level + 1,
                    eh.path || ' -> ' || e.first_name || ' ' || e.last_name
                FROM employees e
                INNER JOIN employee_hierarchy eh ON e.manager_id = eh.employee_id
            )
            SELECT 
                employee_name,
                d.department_name,
                level,
                path
            FROM employee_hierarchy eh
            LEFT JOIN departments d ON eh.department_id = d.department_id
            ORDER BY level, department_name
        ''')
        
        results = cursor.fetchall()
        print("   Employee Name     | Department   | Level | Hierarchy Path")
        print("   " + "-" * 80)
        for row in results:
            print(f"   {row['employee_name'][:17]:17} | {row['department_name'][:12]:12} | {row['level']:5} | {row['path'][:40]}")
    
    def demonstrate_transactions(self):
        """Demonstrate SQL transactions and ACID properties."""
        print("\n" + "="*60)
        print("TRANSACTIONS DEMONSTRATION")
        print("="*60)
        
        # Create a new connection for transaction demonstration
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        print("\n1. ACID Properties in Action:")
        print("   • Atomicity: All or nothing execution")
        print("   • Consistency: Database rules are maintained")
        print("   • Isolation: Concurrent transactions don't interfere")
        print("   • Durability: Committed changes persist")
        
        print("\n2. Example: Placing an Order (Atomic Transaction):")
        
        try:
            # Start transaction
            conn.execute("BEGIN TRANSACTION")
            
            # Get product details
            cursor.execute("SELECT product_id, unit_price, units_in_stock FROM products WHERE product_id = 1")
            product = cursor.fetchone()
            
            if product:
                product_id = product['product_id']
                unit_price = product['unit_price']
                current_stock = product['units_in_stock']
                quantity_to_order = 3
                
                print(f"   • Product ID: {product_id}")
                print(f"   • Current Stock: {current_stock}")
                print(f"   • Quantity to Order: {quantity_to_order}")
                
                if current_stock >= quantity_to_order:
                    # Create order
                    cursor.execute('''
                        INSERT INTO orders (customer_id, employee_id, order_date, required_date, status)
                        VALUES (1, 1, DATE('now'), DATE('now', '+7 days'), 'processing')
                    ''')
                    order_id = cursor.lastrowid
                    
                    # Add order item
                    cursor.execute('''
                        INSERT INTO order_items (order_id, product_id, unit_price, quantity, discount)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (order_id, product_id, unit_price, quantity_to_order, 0.05))
                    
                    # Update product stock
                    cursor.execute('''
                        UPDATE products 
                        SET units_in_stock = units_in_stock - ?
                        WHERE product_id = ?
                    ''', (quantity_to_order, product_id))
                    
                    # Commit transaction
                    conn.commit()
                    print(f"   ✓ Transaction committed successfully")
                    print(f"   ✓ Order #{order_id} created")
                    print(f"   ✓ Product stock updated: {current_stock} -> {current_stock - quantity_to_order}")
                    
                else:
                    print("   ✗ Insufficient stock - rolling back")
                    conn.rollback()
                    
        except Exception as e:
            print(f"   ✗ Transaction failed: {e}")
            conn.rollback()
        
        print("\n3. Transaction with Savepoints:")
        
        try:
            conn.execute("BEGIN TRANSACTION")
            
            # Create savepoint
            conn.execute("SAVEPOINT before_changes")
            
            # Make some changes
            cursor.execute("UPDATE products SET unit_price = unit_price * 1.1 WHERE category_id = 1")
            updated_count = cursor.rowcount
            print(f"   • Updated prices for {updated_count} electronics products (+10%)")
            
            # Check the effect
            cursor.execute("SELECT SUM(unit_price) as total_price FROM products WHERE category_id = 1")
            total = cursor.fetchone()['total_price']
            print(f"   • New total price for electronics: ${total:,.2f}")
            
            # Rollback to savepoint (undo price change)
            conn.execute("ROLLBACK TO before_changes")
            print(f"   • Rolled back to savepoint")
            
            # Verify rollback
            cursor.execute("SELECT SUM(unit_price) as total_price FROM products WHERE category_id = 1")
            total_after_rollback = cursor.fetchone()['total_price']
            print(f"   • Total price after rollback: ${total_after_rollback:,.2f}")
            
            conn.commit()
            print(f"   ✓ Transaction completed with savepoints")
            
        except Exception as e:
            print(f"   ✗ Transaction with savepoints failed: {e}")
            conn.rollback()
        
        conn.close()
        
    def demonstrate_index_performance(self):
        """Demonstrate the performance impact of indexes."""
        print("\n" + "="*60)
        print("INDEX PERFORMANCE DEMONSTRATION")
        print("="*60)
        
        cursor = self.connection.cursor()
        
        # Add more data for performance testing
        print("\n1. Adding More Data for Performance Testing...")
        
        # Add more products
        product_names = ["Product", "Item", "Tool", "Device", "Gadget"]
        categories = ["A", "B", "C", "D", "E"]
        
        products_to_add = []
        for i in range(1000):
            name = f"{random.choice(product_names)} {i+10}"
            category_id = random.randint(1, 5)
            price = round(random.uniform(10, 1000), 2)
            stock = random.randint(0, 1000)
            products_to_add.append((name, f"Description for {name}", category_id, price, stock, 0))
        
        cursor.executemany(
            "INSERT INTO products (product_name, description, category_id, unit_price, units_in_stock, units_on_order) VALUES (?, ?, ?, ?, ?, ?)",
            products_to_add
        )
        print(f"   • Added 1000 more products (total: {cursor.lastrowid})")
        
        # Add more orders
        orders_to_add = []
        for i in range(500):
            customer_id = random.randint(1, 5)
            employee_id = random.randint(1, 5)
            days_ago = random.randint(0, 365)
            order_date = f"DATE('now', '-{days_ago} days')"
            status = random.choice(['pending', 'processing', 'shipped', 'delivered', 'cancelled'])
            orders_to_add.append((customer_id, employee_id, order_date, status))
        
        # Note: We need to handle the SQL date function differently
        for order_data in orders_to_add:
            cursor.execute(
                f"INSERT INTO orders (customer_id, employee_id, order_date, status) VALUES (?, ?, {order_data[2]}, ?)",
                (order_data[0], order_data[1], order_data[3])
            )
        print(f"   • Added 500 more orders (total: {cursor.lastrowid})")
        
        self.connection.commit()
        
        print("\n2. Performance Comparison: With vs Without Indexes")
        
        # Test query without using index (force table scan)
        start_time = time.time()
        cursor.execute("SELECT * FROM products WHERE unit_price BETWEEN 100 AND 200")
        without_index_time = time.time() - start_time
        print(f"   • Query without index hint: {without_index_time:.4f} seconds")
        print(f"   • Rows returned: {len(cursor.fetchall())}")
        
        # Test with index (SQLite will use index automatically)
        start_time = time.time()
        cursor.execute("SELECT * FROM products WHERE unit_price BETWEEN 100 AND 200")
        with_index_time = time.time() - start_time
        print(f"   • Query with index: {with_index_time:.4f} seconds")
        print(f"   • Rows returned: {len(cursor.fetchall())}")
        
        # Explain query plan
        print("\n3. Query Execution Plan (EXPLAIN QUERY PLAN):")
        cursor.execute("EXPLAIN QUERY PLAN SELECT * FROM products WHERE unit_price BETWEEN 100 AND 200")
        plan = cursor.fetchall()
        for row in plan:
            print(f"   • {row['detail']}")
        
        print("\n4. Index Usage Statistics:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type = 'index' AND tbl_name = 'products'")
        indexes = cursor.fetchall()
        print(f"   • Indexes on products table: {len(indexes)}")
        for idx in indexes:
            print(f"     - {idx['name']}")
        
        # Analyze a complex query
        print("\n5. Complex Query Analysis:")
        start_time = time.time()
        cursor.execute('''
            SELECT 
                c.category_name,
                COUNT(p.product_id) as product_count,
                AVG(p.unit_price) as avg_price,
                MIN(p.unit_price) as min_price,
                MAX(p.unit_price) as max_price
            FROM products p
            JOIN categories c ON p.category_id = c.category_id
            GROUP BY c.category_name
            HAVING COUNT(p.product_id) > 10
            ORDER BY avg_price DESC
        ''')
        complex_query_time = time.time() - start_time
        results = cursor.fetchall()
        
        print(f"   • Complex query time: {complex_query_time:.4f} seconds")
        print("   • Results:")
        for row in results:
            print(f"     - {row['category_name']}: {row['product_count']} products, avg price: ${row['avg_price']:.2f}")
        
        print("\nKey Takeaways:")
        print("   • Indexes significantly speed up WHERE, JOIN, and ORDER BY operations")
        print("   • Proper indexing reduces full table scans")
        print("   • Too many indexes can slow down INSERT/UPDATE operations")
        print("   • Analyze query plans to optimize performance")

# ============================================================================
# SECTION 3: ORM PATTERNS DEMONSTRATION
# ============================================================================

class OrmPatterns:
    """Demonstrates ORM patterns: Active Record vs Data Mapper."""
    
    def __init__(self):
        self.setup_sqlalchemy()
        
    def setup_sqlalchemy(self):
        """Setup SQLAlchemy for ORM demonstration."""
        print("\n" + "="*60)
        print("ORM PATTERNS DEMONSTRATION")
        print("="*60)
        
        # SQLAlchemy uses Data Mapper pattern
        db_path = demo_dir / "orm_patterns.db"
        engine = create_engine(f'sqlite:///{db_path}', echo=False)
        
        Base = declarative_base()
        
        print("\n1. SQLAlchemy (Data Mapper Pattern):")
        print("   • Separation between domain objects and database")
        print("   • Requires explicit session management")
        print("   • More flexible for complex domains")
        
        # Define models
        class Department(Base):
            __tablename__ = 'departments_orm'
            
            id = Column(Integer, primary_key=True)
            name = Column(String(100), nullable=False)
            location = Column(String(100))
            
            # Relationship (Data Mapper style)
            employees = relationship("Employee", back_populates="department", cascade="all, delete-orphan")
            
            def __repr__(self):
                return f"<Department(id={self.id}, name='{self.name}', location='{self.location}')>"
            
            # Business logic methods
            def get_employee_count(self):
                return len(self.employees)
            
            def get_total_salary(self):
                return sum(emp.salary for emp in self.employees)
        
        class Employee(Base):
            __tablename__ = 'employees_orm'
            
            id = Column(Integer, primary_key=True)
            first_name = Column(String(50), nullable=False)
            last_name = Column(String(50), nullable=False)
            email = Column(String(100), unique=True, nullable=False)
            salary = Column(Float, default=0.0)
            department_id = Column(Integer, ForeignKey('departments_orm.id'))
            
            # Relationships
            department = relationship("Department", back_populates="employees")
            projects = relationship("Project", secondary="employee_projects", back_populates="employees")
            
            def __repr__(self):
                return f"<Employee(id={self.id}, name='{self.first_name} {self.last_name}', email='{self.email}')>"
            
            @property
            def full_name(self):
                return f"{self.first_name} {self.last_name}"
            
            def give_raise(self, percentage):
                """Business logic method."""
                self.salary *= (1 + percentage / 100)
                return self.salary
        
        class Project(Base):
            __tablename__ = 'projects_orm'
            
            id = Column(Integer, primary_key=True)
            name = Column(String(100), nullable=False)
            description = Column(Text)
            budget = Column(Float, default=0.0)
            start_date = Column(DateTime, default=datetime.utcnow)
            end_date = Column(DateTime)
            
            # Many-to-many relationship
            employees = relationship("Employee", secondary="employee_projects", back_populates="projects")
            
            def __repr__(self):
                return f"<Project(id={self.id}, name='{self.name}', budget={self.budget})>"
        
        # Association table for many-to-many
        class EmployeeProject(Base):
            __tablename__ = 'employee_projects'
            
            id = Column(Integer, primary_key=True)
            employee_id = Column(Integer, ForeignKey('employees_orm.id'), nullable=False)
            project_id = Column(Integer, ForeignKey('projects_orm.id'), nullable=False)
            role = Column(String(50))
            hours_worked = Column(Float, default=0.0)
            
            # Unique constraint
            __table_args__ = (
                UniqueConstraint('employee_id', 'project_id', name='uq_employee_project'),
            )
            
            def __repr__(self):
                return f"<EmployeeProject(employee_id={self.employee_id}, project_id={self.project_id}, role='{self.role}')>"
        
        # Create tables
        Base.metadata.create_all(engine)
        
        # Create session
        Session = sessionmaker(bind=engine)
        self.session = Session()
        
        # Store model classes
        self.Department = Department
        self.Employee = Employee
        self.Project = Project
        self.EmployeeProject = EmployeeProject
        
        # Insert sample data
        self.insert_sample_data()
        
        print("\n2. Active Record Pattern (Simulated with SQLAlchemy):")
        print("   • Domain objects contain database logic")
        print("   • Each object knows how to save/load itself")
        print("   • Simpler for CRUD operations")
        
        # Demonstrate Active Record pattern simulation
        self.demonstrate_active_record_pattern()
        
        print("\n3. Data Mapper Pattern (SQLAlchemy Native):")
        print("   • Separation of concerns")
        print("   • Objects unaware of persistence")
        print("   • More testable and flexible")
        
        self.demonstrate_data_mapper_pattern()
        
    def insert_sample_data(self):
        """Insert sample data for ORM demonstration."""
        
        # Create departments
        engineering = self.Department(name="Engineering", location="San Francisco")
        sales = self.Department(name="Sales", location="New York")
        marketing = self.Department(name="Marketing", location="Chicago")
        
        self.session.add_all([engineering, sales, marketing])
        self.session.flush()  # Get IDs
        
        # Create employees
        employees = [
            self.Employee(first_name="John", last_name="Doe", email="john.doe@company.com", salary=75000, department=engineering),
            self.Employee(first_name="Jane", last_name="Smith", email="jane.smith@company.com", salary=85000, department=engineering),
            self.Employee(first_name="Bob", last_name="Johnson", email="bob.johnson@company.com", salary=65000, department=sales),
            self.Employee(first_name="Alice", last_name="Williams", email="alice.williams@company.com", salary=95000, department=marketing),
        ]
        
        self.session.add_all(employees)
        
        # Create projects
        projects = [
            self.Project(name="Website Redesign", description="Redesign company website", budget=50000),
            self.Project(name="Mobile App", description="Develop mobile application", budget=150000),
            self.Project(name="Market Research", description="Conduct market analysis", budget=30000),
        ]
        
        self.session.add_all(projects)
        
        # Assign employees to projects
        employee_project_data = [
            (employees[0], projects[0], "Lead Developer", 120),
            (employees[1], projects[0], "Frontend Developer", 80),
            (employees[0], projects[1], "Architect", 200),
            (employees[2], projects[2], "Researcher", 150),
            (employees[3], projects[1], "Project Manager", 100),
        ]
        
        for emp, proj, role, hours in employee_project_data:
            association = self.EmployeeProject(employee=emp, project=proj, role=role, hours_worked=hours)
            self.session.add(association)
        
        self.session.commit()
        print("   • Inserted sample data: 3 departments, 4 employees, 3 projects")
    
    def demonstrate_active_record_pattern(self):
        """Simulate Active Record pattern with SQLAlchemy."""
        
        # Active Record style class
        class Customer:
            """Active Record pattern simulation."""
            
            def __init__(self, name, email, phone=None):
                self.id = None
                self.name = name
                self.email = email
                self.phone = phone
                self.created_at = datetime.utcnow()
            
            def save(self, session):
                """Save the customer to database."""
                if self.id is None:
                    # Insert
                    session.execute(
                        "INSERT INTO customers_ar (name, email, phone, created_at) VALUES (?, ?, ?, ?)",
                        (self.name, self.email, self.phone, self.created_at)
                    )
                    self.id = session.lastrowid
                else:
                    # Update
                    session.execute(
                        "UPDATE customers_ar SET name = ?, email = ?, phone = ? WHERE id = ?",
                        (self.name, self.email, self.phone, self.id)
                    )
                session.commit()
            
            @classmethod
            def find(cls, session, customer_id):
                """Find customer by ID."""
                result = session.execute(
                    "SELECT * FROM customers_ar WHERE id = ?",
                    (customer_id,)
                ).fetchone()
                
                if result:
                    customer = cls(result['name'], result['email'], result['phone'])
                    customer.id = result['id']
                    customer.created_at = result['created_at']
                    return customer
                return None
            
            @classmethod
            def find_by_email(cls, session, email):
                """Find customer by email."""
                result = session.execute(
                    "SELECT * FROM customers_ar WHERE email = ?",
                    (email,)
                ).fetchone()
                
                if result:
                    customer = cls(result['name'], result['email'], result['phone'])
                    customer.id = result['id']
                    customer.created_at = result['created_at']
                    return customer
                return None
            
            def delete(self, session):
                """Delete customer from database."""
                if self.id:
                    session.execute("DELETE FROM customers_ar WHERE id = ?", (self.id,))
                    session.commit()
                    self.id = None
            
            def __repr__(self):
                return f"<Customer(id={self.id}, name='{self.name}', email='{self.email}')>"
        
        # Create table for Active Record demonstration
        conn = self.session.connection()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS customers_ar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                phone VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        
        print("\n   Active Record Pattern Example:")
        
        # Create customer using Active Record pattern
        customer1 = Customer("Alice Johnson", "alice@example.com", "555-1234")
        customer1.save(conn)
        print(f"   • Created customer: {customer1}")
        
        # Find customer
        found_customer = Customer.find(conn, customer1.id)
        print(f"   • Found customer by ID: {found_customer}")
        
        # Update customer
        customer1.name = "Alice Smith"
        customer1.save(conn)
        print(f"   • Updated customer: {customer1}")
        
        # Find by email
        email_customer = Customer.find_by_email(conn, "alice@example.com")
        print(f"   • Found customer by email: {email_customer}")
        
        print("\n   Active Record Characteristics:")
        print("     • Customer object contains database methods")
        print("     • Object knows how to save/load itself")
        print("     • Simpler but mixes concerns")
    
    def demonstrate_data_mapper_pattern(self):
        """Demonstrate SQLAlchemy's Data Mapper pattern."""
        
        print("\n   Data Mapper Pattern Example (SQLAlchemy):")
        
        # Query with relationships (lazy loading)
        departments = self.session.query(self.Department).all()
        print(f"   • Found {len(departments)} departments")
        
        for dept in departments:
            print(f"     - {dept.name}: {dept.get_employee_count()} employees")
        
        # Complex query with joins
        print("\n   Complex Query with Joins:")
        results = self.session.query(
            self.Employee.first_name,
            self.Employee.last_name,
            self.Department.name.label('department'),
            func.count(self.Project.id).label('project_count')
        ).join(self.Department)\
         .join(self.Employee.projects)\
         .group_by(self.Employee.id, self.Department.name)\
         .order_by(desc('project_count'))\
         .all()
        
        for emp in results:
            print(f"     - {emp.first_name} {emp.last_name} ({emp.department}): {emp.project_count} projects")
        
        # Eager loading with joinedload
        print("\n   Eager Loading Example:")
        employees = self.session.query(self.Employee)\
            .options(joinedload(self.Employee.department))\
            .options(subqueryload(self.Employee.projects))\
            .limit(3)\
            .all()
        
        for emp in employees:
            print(f"     - {emp.full_name} works in {emp.department.name}")
            for project in emp.projects:
                print(f"       • Working on: {project.name}")
        
        # Transaction with rollback
        print("\n   Transaction with Rollback Example:")
        try:
            # Start transaction
            emp = self.Employee(
                first_name="Test",
                last_name="User",
                email="test.user@company.com",
                salary=50000
            )
            self.session.add(emp)
            self.session.flush()  # Get ID but don't commit
            
            # Intentionally cause an error
            duplicate_emp = self.Employee(
                first_name="Test2",
                last_name="User2",
                email="test.user@company.com",  # Duplicate email - should fail
                salary=60000
            )
            self.session.add(duplicate_emp)
            
            # This should raise IntegrityError
            self.session.commit()
            print("     • ERROR: Should not reach here!")
            
        except IntegrityError:
            self.session.rollback()
            print("     ✓ Transaction rolled back due to duplicate email")
        
        # Demonstrate business logic
        print("\n   Business Logic in Domain Objects:")
        employee = self.session.query(self.Employee).first()
        if employee:
            old_salary = employee.salary
            new_salary = employee.give_raise(10)  # 10% raise
            print(f"     • {employee.full_name}'s salary: ${old_salary:,.2f} -> ${new_salary:,.2f}")
        
        print("\n   Data Mapper Characteristics:")
        print("     • Separation of domain logic and persistence")
        print("     • Session manages database operations")
        print("     • More flexible and testable")
        print("     • Supports complex mappings and relationships")

# ============================================================================
# SECTION 4: CONNECTION POOLING DEMONSTRATION
# ============================================================================

class ConnectionPooling:
    """Demonstrates connection pooling concepts."""
    
    def __init__(self):
        self.setup_connection_pools()
        
    def setup_connection_pools(self):
        """Setup and demonstrate connection pooling."""
        print("\n" + "="*60)
        print("CONNECTION POOLING DEMONSTRATION")
        print("="*60)
        
        print("\n1. Why Connection Pooling?")
        print("   • Database connections are expensive to create")
        print("   • Pooling reuses connections instead of creating new ones")
        print("   • Improves application performance and scalability")
        print("   • Manages connection lifecycle efficiently")
        
        # Create test database
        db_path = demo_dir / "pooling_demo.db"
        
        print("\n2. Without Connection Pooling:")
        
        def without_pooling(num_connections=10):
            """Demonstrate creating connections without pooling."""
            connections = []
            start_time = time.time()
            
            for i in range(num_connections):
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT 1")  # Simple query
                connections.append(conn)
            
            elapsed = time.time() - start_time
            
            # Cleanup
            for conn in connections:
                conn.close()
            
            return elapsed
        
        without_pool_time = without_pooling(50)
        print(f"   • Time to create 50 connections: {without_pool_time:.4f} seconds")
        
        print("\n3. With Connection Pooling (SQLAlchemy QueuePool):")
        
        # Create engine with connection pool
        engine = create_engine(
            f'sqlite:///{db_path}',
            poolclass=QueuePool,
            pool_size=5,          # Number of connections to keep open
            max_overflow=10,      # Additional connections allowed
            pool_timeout=30,      # Seconds to wait for connection
            pool_recycle=3600,    # Recycle connections after 1 hour
            pool_pre_ping=True    # Verify connections before using
        )
        
        def with_pooling(num_operations=50):
            """Demonstrate using connection pool."""
            connections = []
            start_time = time.time()
            
            for i in range(num_operations):
                with engine.connect() as conn:
                    result = conn.execute("SELECT 1")
                    connections.append(conn)
            
            elapsed = time.time() - start_time
            return elapsed
        
        with_pool_time = with_pooling(50)
        print(f"   • Time for 50 operations with pool: {with_pool_time:.4f} seconds")
        print(f"   • Speed improvement: {(without_pool_time/with_pool_time):.1f}x faster")
        
        print("\n4. Connection Pool Statistics:")
        print(f"   • Pool size: 5 (active connections kept open)")
        print(f"   • Max overflow: 10 (additional connections allowed)")
        print(f"   • Timeout: 30 seconds (wait for connection)")
        print(f"   • Recycle: 3600 seconds (1 hour)")
        print(f"   • Pre-ping: Enabled (verify connection health)")
        
        print("\n5. Thread-Safe Connection Pooling:")
        
        def worker_thread(thread_id, engine, results):
            """Worker thread that uses connection pool."""
            try:
                with engine.connect() as conn:
                    # Simulate database work
                    conn.execute("SELECT 1")
                    time.sleep(0.1)  # Simulate work
                    results.append(f"Thread {thread_id} completed")
            except Exception as e:
                results.append(f"Thread {thread_id} failed: {e}")
        
        # Test with multiple threads
        print("   • Testing with 20 concurrent threads...")
        threads = []
        results = []
        
        start_time = time.time()
        for i in range(20):
            thread = threading.Thread(target=worker_thread, args=(i, engine, results))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        elapsed = time.time() - start_time
        print(f"   • 20 threads completed in {elapsed:.2f} seconds")
        print(f"   • Successful operations: {len([r for r in results if 'completed' in r])}")
        
        print("\n6. PostgreSQL Connection Pool Example:")
        
        # Note: This requires PostgreSQL to be running
        print("   • PostgreSQL with psycopg2.pool:")
        print('''
        from psycopg2 import pool
        
        # Create connection pool
        connection_pool = pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            host='localhost',
            database='mydb',
            user='myuser',
            password='mypassword'
        )
        
        # Get connection from pool
        conn = connection_pool.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
        finally:
            # Return connection to pool
            connection_pool.putconn(conn)
        
        # Close all connections when done
        connection_pool.closeall()
        ''')
        
        print("\n7. Connection Pool Best Practices:")
        print("   • Set appropriate pool size based on expected load")
        print("   • Use connection timeouts to prevent hanging")
        print("   • Implement connection health checks")
        print("   • Monitor pool usage and adjust parameters")
        print("   • Close connections properly in finally blocks")
        print("   • Use context managers for automatic cleanup")
        
        print("\n8. Common Connection Pool Configurations:")
        configs = [
            ("Web Application", "pool_size=10, max_overflow=20"),
            ("Background Worker", "pool_size=5, max_overflow=5"),
            ("Microservice", "pool_size=3, max_overflow=7"),
            ("Batch Processing", "pool_size=20, max_overflow=30"),
        ]
        
        for app_type, config in configs:
            print(f"   • {app_type}: {config}")
        
        # Demonstrate connection lifecycle
        print("\n9. Connection Lifecycle:")
        print("   1. Application requests connection")
        print("   2. Pool checks for available connection")
        print("   3. If available, returns existing connection")
        print("   4. If not, creates new connection (up to max_overflow)")
        print("   5. Application uses connection")
        print("   6. Application returns connection to pool")
        print("   7. Pool marks connection as available for reuse")

# ============================================================================
# SECTION 5: DATABASE MIGRATIONS
# ============================================================================

class DatabaseMigrations:
    """Demonstrates database migrations."""
    
    def __init__(self):
        self.setup_migration_demo()
        
    def setup_migration_demo(self):
        """Setup and demonstrate database migrations."""
        print("\n" + "="*60)
        print("DATABASE MIGRATIONS DEMONSTRATION")
        print("="*60)
        
        print("\n1. What are Database Migrations?")
        print("   • Version control for database schema")
        print("   • Track and apply incremental changes")
        print("   • Support rollback to previous versions")
        print("   • Essential for team development and deployment")
        
        # Create a simple migration system simulation
        self.simulate_migration_system()
        
        # Demonstrate Alembic (SQLAlchemy migrations)
        self.demonstrate_alembic_migrations()
        
        # Demonstrate manual migrations
        self.demonstrate_manual_migrations()
        
    def simulate_migration_system(self):
        """Simulate a simple migration system."""
        print("\n2. Simple Migration System Simulation:")
        
        migrations_dir = demo_dir / "migrations"
        migrations_dir.mkdir(exist_ok=True)
        
        # Create migration files
        migrations = [
            ("001_initial_schema.sql", '''
            -- Migration 001: Initial Schema
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title VARCHAR(200) NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
            '''),
            
            ("002_add_user_profile.sql", '''
            -- Migration 002: Add User Profile Fields
            ALTER TABLE users ADD COLUMN first_name VARCHAR(50);
            ALTER TABLE users ADD COLUMN last_name VARCHAR(50);
            ALTER TABLE users ADD COLUMN date_of_birth DATE;
            
            -- Create indexes for better performance
            CREATE INDEX idx_users_email ON users(email);
            CREATE INDEX idx_posts_user_id ON posts(user_id);
            '''),
            
            ("003_add_post_metadata.sql", '''
            -- Migration 003: Add Post Metadata
            ALTER TABLE posts ADD COLUMN updated_at TIMESTAMP;
            ALTER TABLE posts ADD COLUMN is_published BOOLEAN DEFAULT FALSE;
            ALTER TABLE posts ADD COLUMN view_count INTEGER DEFAULT 0;
            
            -- Update existing posts
            UPDATE posts SET is_published = TRUE, updated_at = created_at;
            '''),
            
            ("004_create_comments_table.sql", '''
            -- Migration 004: Create Comments Table
            CREATE TABLE comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (post_id) REFERENCES posts(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
            
            CREATE INDEX idx_comments_post_id ON comments(post_id);
            CREATE INDEX idx_comments_user_id ON comments(user_id);
            '''),
            
            ("005_add_soft_delete.sql", '''
            -- Migration 005: Add Soft Delete
            ALTER TABLE users ADD COLUMN deleted_at TIMESTAMP;
            ALTER TABLE posts ADD COLUMN deleted_at TIMESTAMP;
            ALTER TABLE comments ADD COLUMN deleted_at TIMESTAMP;
            
            -- Create view for active users only
            CREATE VIEW active_users AS
            SELECT * FROM users WHERE deleted_at IS NULL;
            ''')
        ]
        
        # Write migration files
        for filename, content in migrations:
            (migrations_dir / filename).write_text(content.strip())
            print(f"   • Created migration: {filename}")
        
        # Create migration table and apply migrations
        db_path = demo_dir / "migration_demo.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create migration tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS migrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) UNIQUE NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        print("\n3. Applying Migrations:")
        
        # Get already applied migrations
        cursor.execute("SELECT name FROM migrations")
        applied = {row[0] for row in cursor.fetchall()}
        
        # Apply migrations in order
        for filename, content in migrations:
            if filename not in applied:
                print(f"   • Applying {filename}...")
                
                try:
                    # Execute migration SQL
                    cursor.executescript(content)
                    
                    # Record migration
                    cursor.execute("INSERT INTO migrations (name) VALUES (?)", (filename,))
                    conn.commit()
                    
                    print(f"     ✓ Successfully applied {filename}")
                    
                except Exception as e:
                    conn.rollback()
                    print(f"     ✗ Failed to apply {filename}: {e}")
                    break
        
        # Show migration status
        cursor.execute("SELECT name, applied_at FROM migrations ORDER BY applied_at")
        applied_migrations = cursor.fetchall()
        
        print(f"\n   Applied migrations ({len(applied_migrations)}):")
        for name, applied_at in applied_migrations:
            print(f"     • {name} at {applied_at}")
        
        # Demonstrate rollback
        print("\n4. Migration Rollback Simulation:")
        print("   • Rolling back last migration...")
        
        # Get last migration
        cursor.execute("SELECT name FROM migrations ORDER BY applied_at DESC LIMIT 1")
        last_migration = cursor.fetchone()
        
        if last_migration:
            migration_name = last_migration[0]
            print(f"   • Removing: {migration_name}")
            
            # Create rollback SQL based on migration
            if migration_name == "005_add_soft_delete.sql":
                rollback_sql = '''
                    DROP VIEW IF EXISTS active_users;
                    ALTER TABLE users DROP COLUMN deleted_at;
                    ALTER TABLE posts DROP COLUMN deleted_at;
                    ALTER TABLE comments DROP COLUMN deleted_at;
                '''
                
                try:
                    cursor.executescript(rollback_sql)
                    cursor.execute("DELETE FROM migrations WHERE name = ?", (migration_name,))
                    conn.commit()
                    print(f"     ✓ Successfully rolled back {migration_name}")
                except Exception as e:
                    conn.rollback()
                    print(f"     ✗ Rollback failed: {e}")
        
        conn.close()
        
        print("\n5. Migration Best Practices:")
        print("   • Each migration should be atomic")
        print("   • Include both up() and down() methods")
        print("   • Test migrations thoroughly")
        print("   • Use transactions when possible")
        print("   • Never modify already applied migrations")
        print("   • Keep migrations small and focused")
        print("   • Document breaking changes")
        
    def demonstrate_alembic_migrations(self):
        """Demonstrate Alembic (SQLAlchemy migrations)."""
        print("\n6. Alembic (SQLAlchemy Migrations) Example:")
        
        alembic_example = '''
# alembic.ini configuration
'''
        print(alembic_example)
        
        print('''
        # Directory structure:
        #   alembic/
        #   ├── versions/          # Migration files
        #   ├── env.py             # Migration environment
        #   ├── script.py.mako     # Migration template
        #   alembic.ini           # Configuration
        
        # Creating a migration:
        # $ alembic revision --autogenerate -m "Add user table"
        
        # Generated migration file:
        ''' + '''
        """Add user table
        Revision ID: abc123
        Revises: 
        Create Date: 2024-01-01 12:00:00
        """
        
        from alembic import op
        import sqlalchemy as sa
        
        
        def upgrade():
            # Create users table
            op.create_table(
                'users',
                sa.Column('id', sa.Integer(), nullable=False),
                sa.Column('username', sa.String(length=50), nullable=False),
                sa.Column('email', sa.String(length=100), nullable=False),
                sa.Column('created_at', sa.DateTime(), nullable=True),
                sa.PrimaryKeyConstraint('id'),
                sa.UniqueConstraint('email'),
                sa.UniqueConstraint('username')
            )
            
            # Create index
            op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
        
        
        def downgrade():
            # Drop table and index
            op.drop_index(op.f('ix_users_email'), table_name='users')
            op.drop_table('users')
        
        # Applying migrations:
        # $ alembic upgrade head     # Apply all migrations
        # $ alembic upgrade +2       # Apply next 2 migrations
        # $ alembic downgrade -1     # Rollback last migration
        # $ alembic downgrade base   # Rollback all migrations
        
        # Checking migration status:
        # $ alembic current          # Show current revision
        # $ alembic history          # Show migration history
        # $ alembic heads            # Show latest revisions
        ''')
        
        print("\n   Alembic Features:")
        print("     • Auto-generate migrations from SQLAlchemy models")
        print("     • Support for multiple database backends")
        print("     • Transaction support")
        print("     • Branching and merging")
        print("     • Offline mode (SQL script generation)")
        
    def demonstrate_manual_migrations(self):
        """Demonstrate manual migration techniques."""
        print("\n7. Manual Migration Techniques:")
        
        print('''
        # 1. Schema Changes with Data Migration
        
        def migrate_users_to_profiles():
            """
            Example: Split users table into users and profiles
            """
            conn = get_database_connection()
            
            try:
                conn.execute("BEGIN TRANSACTION")
                
                # Create new profiles table
                conn.execute('''
                    CREATE TABLE profiles (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER UNIQUE NOT NULL,
                        first_name VARCHAR(50),
                        last_name VARCHAR(50),
                        date_of_birth DATE,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                    )
                ''')
                
                # Copy data from users to profiles
                conn.execute('''
                    INSERT INTO profiles (user_id, first_name, last_name, date_of_birth)
                    SELECT id, first_name, last_name, date_of_birth
                    FROM users
                ''')
                
                # Remove columns from users table
                conn.execute('''
                    CREATE TABLE users_new (
                        id INTEGER PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        created_at TIMESTAMP
                    )
                ''')
                
                conn.execute('''
                    INSERT INTO users_new (id, username, email, created_at)
                    SELECT id, username, email, created_at FROM users
                ''')
                
                # Replace old table
                conn.execute("DROP TABLE users")
                conn.execute("ALTER TABLE users_new RENAME TO users")
                
                conn.commit()
                print("Migration completed successfully")
                
            except Exception as e:
                conn.rollback()
                print(f"Migration failed: {e}")
        
        # 2. Safe Column Addition
        
        def add_column_safely(table_name, column_name, column_type, default_value=None):
            """
            Safely add a column to a table
            """
            try:
                # Check if column already exists
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [col[1] for col in cursor.fetchall()]
                
                if column_name not in columns:
                    sql = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"
                    if default_value is not None:
                        sql += f" DEFAULT {default_value}"
                    
                    cursor.execute(sql)
                    print(f"Added column {column_name} to {table_name}")
                else:
                    print(f"Column {column_name} already exists in {table_name}")
                    
            except Exception as e:
                print(f"Failed to add column: {e}")
        
        # 3. Batch Data Migration
        
        def migrate_data_in_batches(source_table, target_table, batch_size=1000):
            """
            Migrate data in batches to avoid locking
            """
            cursor.execute(f"SELECT COUNT(*) FROM {source_table}")
            total_records = cursor.fetchone()[0]
            batches = (total_records + batch_size - 1) // batch_size
            
            for batch in range(batches):
                offset = batch * batch_size
                
                cursor.execute(f'''
                    INSERT INTO {target_table}
                    SELECT * FROM {source_table}
                    LIMIT {batch_size} OFFSET {offset}
                ''')
                
                print(f"Migrated batch {batch + 1}/{batches}")
                time.sleep(0.1)  # Prevent database locking
        
        ''')
        
        print("\n8. Migration Testing Strategy:")
        print("   • Test on development database first")
        print("   • Use database snapshots for testing")
        print("   • Test both upgrade and downgrade paths")
        print("   • Test with production-like data volumes")
        print("   • Verify data integrity after migration")
        
        print("\n9. Production Migration Checklist:")
        print("   [ ] Backup database before migration")
        print("   [ ] Test migration on staging environment")
        print("   [ ] Schedule migration during maintenance window")
        print("   [ ] Monitor application during migration")
        print("   [ ] Have rollback plan ready")
        print("   [ ] Verify application functionality after migration")
        print("   [ ] Update documentation with schema changes")

# ============================================================================
# SECTION 6: COMPREHENSIVE DATABASE EXAMPLE
# ============================================================================

class ComprehensiveDatabaseExample:
    """Comprehensive example integrating all database concepts."""
    
    def __init__(self):
        self.setup_comprehensive_example()
        
    def setup_comprehensive_example(self):
        """Setup comprehensive database example."""
        print("\n" + "="*60)
        print("COMPREHENSIVE DATABASE EXAMPLE")
        print("="*60)
        
        print("\n1. Designing a Complete E-commerce Database:")
        
        # Setup SQLAlchemy with all features
        db_path = demo_dir / "ecommerce.db"
        engine = create_engine(
            f'sqlite:///{db_path}',
            poolclass=QueuePool,
            pool_size=10,
            max_overflow=20,
            echo=False
        )
        
        Base = declarative_base()
        
        # Define comprehensive models
        class User(Base):
            __tablename__ = 'users'
            
            id = Column(Integer, primary_key=True)
            username = Column(String(50), unique=True, nullable=False, index=True)
            email = Column(String(100), unique=True, nullable=False, index=True)
            password_hash = Column(String(200), nullable=False)
            first_name = Column(String(50))
            last_name = Column(String(50))
            phone = Column(String(20))
            created_at = Column(DateTime, default=datetime.utcnow)
            updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
            last_login = Column(DateTime)
            is_active = Column(Boolean, default=True)
            
            # Relationships
            addresses = relationship("Address", back_populates="user", cascade="all, delete-orphan")
            orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
            reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
            cart_items = relationship("CartItem", back_populates="user", cascade="all, delete-orphan")
            
            __table_args__ = (
                Index('idx_users_name', 'first_name', 'last_name'),
                CheckConstraint('length(username) >= 3', name='username_length'),
            )
            
            def __repr__(self):
                return f"<User(id={self.id}, username='{self.username}')>"
            
            def get_full_name(self):
                return f"{self.first_name} {self.last_name}"
        
        class Address(Base):
            __tablename__ = 'addresses'
            
            id = Column(Integer, primary_key=True)
            user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
            address_type = Column(String(20), nullable=False)  # shipping, billing
            street = Column(String(200), nullable=False)
            city = Column(String(100), nullable=False)
            state = Column(String(50), nullable=False)
            postal_code = Column(String(20), nullable=False)
            country = Column(String(50), nullable=False, default='USA')
            is_default = Column(Boolean, default=False)
            
            # Relationships
            user = relationship("User", back_populates="addresses")
            
            __table_args__ = (
                UniqueConstraint('user_id', 'address_type', name='uq_user_address_type'),
                Index('idx_addresses_user', 'user_id', 'address_type'),
            )
            
            def __repr__(self):
                return f"<Address(id={self.id}, city='{self.city}', type='{self.address_type}')>"
        
        class Category(Base):
            __tablename__ = 'categories'
            
            id = Column(Integer, primary_key=True)
            name = Column(String(100), unique=True, nullable=False, index=True)
            description = Column(Text)
            parent_id = Column(Integer, ForeignKey('categories.id'))
            slug = Column(String(100), unique=True, index=True)
            display_order = Column(Integer, default=0)
            
            # Self-referential relationship
            parent = relationship("Category", remote_side=[id], back_populates="children")
            children = relationship("Category", back_populates="parent")
            
            # Products relationship
            products = relationship("Product", back_populates="category")
            
            def __repr__(self):
                return f"<Category(id={self.id}, name='{self.name}')>"
        
        class Product(Base):
            __tablename__ = 'products'
            
            id = Column(Integer, primary_key=True)
            sku = Column(String(50), unique=True, nullable=False, index=True)
            name = Column(String(200), nullable=False, index=True)
            description = Column(Text)
            category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
            price = Column(Float, nullable=False)
            cost = Column(Float)
            quantity = Column(Integer, default=0)
            weight = Column(Float)  # in kg
            dimensions = Column(String(50))  # "10x5x2"
            is_active = Column(Boolean, default=True)
            created_at = Column(DateTime, default=datetime.utcnow)
            updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
            
            # Relationships
            category = relationship("Category", back_populates="products")
            variants = relationship("ProductVariant", back_populates="product", cascade="all, delete-orphan")
            reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan")
            order_items = relationship("OrderItem", back_populates="product")
            
            __table_args__ = (
                Index('idx_products_category', 'category_id', 'is_active'),
                Index('idx_products_price', 'price'),
                CheckConstraint('price >= 0', name='price_non_negative'),
                CheckConstraint('quantity >= 0', name='quantity_non_negative'),
            )
            
            def __repr__(self):
                return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"
            
            def get_stock_status(self):
                if self.quantity <= 0:
                    return "Out of Stock"
                elif self.quantity < 10:
                    return "Low Stock"
                else:
                    return "In Stock"
        
        class ProductVariant(Base):
            __tablename__ = 'product_variants'
            
            id = Column(Integer, primary_key=True)
            product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
            sku = Column(String(50), unique=True, nullable=False)
            name = Column(String(100), nullable=False)  # "Large", "Red", etc.
            price_adjustment = Column(Float, default=0.0)
            quantity = Column(Integer, default=0)
            
            # Relationships
            product = relationship("Product", back_populates="variants")
            
            __table_args__ = (
                UniqueConstraint('product_id', 'name', name='uq_product_variant'),
                Index('idx_variants_product', 'product_id', 'sku'),
            )
            
            def __repr__(self):
                return f"<ProductVariant(id={self.id}, name='{self.name}', product_id={self.product_id})>"
        
        class Order(Base):
            __tablename__ = 'orders'
            
            id = Column(Integer, primary_key=True)
            order_number = Column(String(50), unique=True, nullable=False, index=True)
            user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
            status = Column(String(20), nullable=False, default='pending', index=True)
            subtotal = Column(Float, nullable=False)
            tax = Column(Float, nullable=False)
            shipping = Column(Float, nullable=False)
            total = Column(Float, nullable=False)
            shipping_address_id = Column(Integer, ForeignKey('addresses.id'))
            billing_address_id = Column(Integer, ForeignKey('addresses.id'))
            payment_method = Column(String(50))
            payment_status = Column(String(20), default='pending')
            notes = Column(Text)
            created_at = Column(DateTime, default=datetime.utcnow, index=True)
            updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
            
            # Relationships
            user = relationship("User", back_populates="orders")
            shipping_address = relationship("Address", foreign_keys=[shipping_address_id])
            billing_address = relationship("Address", foreign_keys=[billing_address_id])
            items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
            
            __table_args__ = (
                Index('idx_orders_user_date', 'user_id', 'created_at'),
                CheckConstraint('subtotal >= 0', name='subtotal_non_negative'),
                CheckConstraint('tax >= 0', name='tax_non_negative'),
                CheckConstraint('shipping >= 0', name='shipping_non_negative'),
                CheckConstraint('total >= 0', name='total_non_negative'),
            )
            
            def __repr__(self):
                return f"<Order(id={self.id}, order_number='{self.order_number}', total={self.total})>"
        
        class OrderItem(Base):
            __tablename__ = 'order_items'
            
            id = Column(Integer, primary_key=True)
            order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
            product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
            variant_id = Column(Integer, ForeignKey('product_variants.id'))
            quantity = Column(Integer, nullable=False)
            unit_price = Column(Float, nullable=False)
            discount = Column(Float, default=0.0)
            
            # Relationships
            order = relationship("Order", back_populates="items")
            product = relationship("Product", back_populates="order_items")
            variant = relationship("ProductVariant")
            
            __table_args__ = (
                Index('idx_order_items_order', 'order_id'),
                Index('idx_order_items_product', 'product_id'),
                CheckConstraint('quantity > 0', name='quantity_positive'),
                CheckConstraint('unit_price >= 0', name='unit_price_non_negative'),
                CheckConstraint('discount >= 0 AND discount <= 1', name='discount_range'),
            )
            
            def __repr__(self):
                return f"<OrderItem(id={self.id}, product_id={self.product_id}, quantity={self.quantity})>"
            
            @property
            def total_price(self):
                return self.quantity * self.unit_price * (1 - self.discount)
        
        class Review(Base):
            __tablename__ = 'reviews'
            
            id = Column(Integer, primary_key=True)
            user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
            product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
            rating = Column(Integer, nullable=False)
            title = Column(String(200))
            content = Column(Text)
            is_verified = Column(Boolean, default=False)
            created_at = Column(DateTime, default=datetime.utcnow, index=True)
            updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
            
            # Relationships
            user = relationship("User", back_populates="reviews")
            product = relationship("Product", back_populates="reviews")
            
            __table_args__ = (
                UniqueConstraint('user_id', 'product_id', name='uq_user_product_review'),
                Index('idx_reviews_product_rating', 'product_id', 'rating'),
                CheckConstraint('rating >= 1 AND rating <= 5', name='rating_range'),
            )
            
            def __repr__(self):
                return f"<Review(id={self.id}, product_id={self.product_id}, rating={self.rating})>"
        
        class CartItem(Base):
            __tablename__ = 'cart_items'
            
            id = Column(Integer, primary_key=True)
            user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
            product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
            variant_id = Column(Integer, ForeignKey('product_variants.id'))
            quantity = Column(Integer, nullable=False)
            added_at = Column(DateTime, default=datetime.utcnow)
            updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
            
            # Relationships
            user = relationship("User", back_populates="cart_items")
            product = relationship("Product")
            variant = relationship("ProductVariant")
            
            __table_args__ = (
                UniqueConstraint('user_id', 'product_id', 'variant_id', name='uq_cart_item'),
                Index('idx_cart_items_user', 'user_id'),
                CheckConstraint('quantity > 0', name='cart_quantity_positive'),
            )
            
            def __repr__(self):
                return f"<CartItem(id={self.id}, user_id={self.user_id}, product_id={self.product_id})>"
        
        # Create all tables
        Base.metadata.create_all(engine)
        
        print("   • Created 8 interconnected tables with:")
        print("     - Primary and foreign keys")
        print("     - Indexes for performance")
        print("     - Check constraints")
        print("     - Unique constraints")
        print("     - Relationships (one-to-many, many-to-one)")
        
        # Create session
        Session = sessionmaker(bind=engine)
        self.session = Session()
        
        # Store models
        self.models = {
            'User': User,
            'Address': Address,
            'Category': Category,
            'Product': Product,
            'ProductVariant': ProductVariant,
            'Order': Order,
            'OrderItem': OrderItem,
            'Review': Review,
            'CartItem': CartItem
        }
        
        # Insert sample data
        self.insert_comprehensive_data()
        
        # Demonstrate complex queries
        self.demonstrate_complex_queries()
        
        # Demonstrate transactions
        self.demonstrate_complex_transactions()
        
    def insert_comprehensive_data(self):
        """Insert comprehensive sample data."""
        print("\n2. Inserting Sample Data:")
        
        # Create users
        users = []
        for i in range(5):
            user = self.models['User'](
                username=f"user{i+1}",
                email=f"user{i+1}@example.com",
                password_hash="hashed_password",
                first_name=["John", "Jane", "Bob", "Alice", "Charlie"][i],
                last_name=["Doe", "Smith", "Johnson", "Williams", "Brown"][i]
            )
            users.append(user)
        
        self.session.add_all(users)
        self.session.flush()
        print("   • Created 5 users")
        
        # Create categories with hierarchy
        electronics = self.models['Category'](name="Electronics", slug="electronics")
        computers = self.models['Category'](name="Computers", slug="computers", parent=electronics)
        phones = self.models['Category'](name="Phones", slug="phones", parent=electronics)
        clothing = self.models['Category'](name="Clothing", slug="clothing")
        
        self.session.add_all([electronics, computers, phones, clothing])
        self.session.flush()
        print("   • Created 4 categories with hierarchy")
        
        # Create products
        products = []
        for i in range(10):
            category = computers if i % 2 == 0 else phones
            product = self.models['Product'](
                sku=f"SKU-{1000 + i}",
                name=f"Product {i+1}",
                description=f"Description for product {i+1}",
                category=category,
                price=round(100 + i * 50, 2),
                cost=round(50 + i * 25, 2),
                quantity=random.randint(10, 100)
            )
            products.append(product)
        
        self.session.add_all(products)
        print("   • Created 10 products")
        
        # Create orders
        import random
        from datetime import datetime, timedelta
        
        orders = []
        for i in range(20):
            user = random.choice(users)
            order = self.models['Order'](
                order_number=f"ORD-{1000 + i}",
                user=user,
                status=random.choice(['pending', 'processing', 'shipped', 'delivered']),
                subtotal=0,
                tax=0,
                shipping=random.uniform(5, 20),
                total=0,
                payment_method=random.choice(['credit_card', 'paypal', 'bank_transfer']),
                payment_status=random.choice(['pending', 'paid', 'failed']),
                created_at=datetime.utcnow() - timedelta(days=random.randint(0, 30))
            )
            orders.append(order)
        
        self.session.add_all(orders)
        self.session.flush()
        print("   • Created 20 orders")
        
        # Create order items
        for order in orders:
            num_items = random.randint(1, 5)
            subtotal = 0
            
            for _ in range(num_items):
                product = random.choice(products)
                quantity = random.randint(1, 3)
                unit_price = product.price
                discount = random.choice([0, 0.1, 0.15, 0.2])
                
                order_item = self.models['OrderItem'](
                    order=order,
                    product=product,
                    quantity=quantity,
                    unit_price=unit_price,
                    discount=discount
                )
                
                subtotal += quantity * unit_price * (1 - discount)
                self.session.add(order_item)
            
            # Update order totals
            order.subtotal = round(subtotal, 2)
            order.tax = round(subtotal * 0.08, 2)  # 8% tax
            order.total = round(order.subtotal + order.tax + order.shipping, 2)
        
        print("   • Created order items and calculated totals")
        
        self.session.commit()
        print("   ✓ All data inserted successfully")
        
    def demonstrate_complex_queries(self):
        """Demonstrate complex SQL queries."""
        print("\n3. Complex Query Examples:")
        
        # Query 1: Sales report by category
        print("\n   Query 1: Sales Report by Category")
        results = self.session.query(
            self.models['Category'].name,
            func.count(self.models['OrderItem'].id).label('total_orders'),
            func.sum(self.models['OrderItem'].quantity).label('total_quantity'),
            func.sum(self.models['OrderItem'].quantity * self.models['OrderItem'].unit_price * (1 - self.models['OrderItem'].discount)).label('total_revenue')
        ).join(self.models['Product'], self.models['OrderItem'].product_id == self.models['Product'].id)\
         .join(self.models['Category'], self.models['Product'].category_id == self.models['Category'].id)\
         .join(self.models['Order'], self.models['OrderItem'].order_id == self.models['Order'].id)\
         .filter(self.models['Order'].status == 'delivered')\
         .group_by(self.models['Category'].name)\
         .order_by(desc('total_revenue'))\
         .all()
        
        for category, orders, quantity, revenue in results:
            print(f"     • {category}: {orders} orders, {quantity} items, ${revenue:,.2f} revenue")
        
        # Query 2: User purchase history
        print("\n   Query 2: Top Customers by Spending")
        results = self.session.query(
            self.models['User'].username,
            func.count(self.models['Order'].id).label('order_count'),
            func.sum(self.models['Order'].total).label('total_spent'),
            func.max(self.models['Order'].created_at).label('last_order')
        ).join(self.models['Order'], self.models['User'].id == self.models['Order'].user_id)\
         .group_by(self.models['User'].id, self.models['User'].username)\
         .order_by(desc('total_spent'))\
         .limit(5)\
         .all()
        
        for username, count, spent, last_order in results:
            print(f"     • {username}: {count} orders, ${spent:,.2f} total, last order: {last_order.strftime('%Y-%m-%d')}")
        
        # Query 3: Product performance
        print("\n   Query 3: Best Selling Products")
        results = self.session.query(
            self.models['Product'].name,
            func.sum(self.models['OrderItem'].quantity).label('total_sold'),
            func.avg(self.models['Review'].rating).label('avg_rating'),
            func.count(self.models['Review'].id).label('review_count')
        ).outerjoin(self.models['OrderItem'], self.models['Product'].id == self.models['OrderItem'].product_id)\
         .outerjoin(self.models['Review'], self.models['Product'].id == self.models['Review'].product_id)\
         .group_by(self.models['Product'].id, self.models['Product'].name)\
         .order_by(desc('total_sold'))\
         .limit(5)\
         .all()
        
        for name, sold, rating, reviews in results:
            rating_str = f"{rating:.1f}" if rating else "No ratings"
            print(f"     • {name}: {sold or 0} sold, {rating_str} stars ({reviews} reviews)")
        
        # Query 4: Monthly sales trend
        print("\n   Query 4: Monthly Sales Trend")
        results = self.session.query(
            func.strftime('%Y-%m', self.models['Order'].created_at).label('month'),
            func.count(self.models['Order'].id).label('order_count'),
            func.sum(self.models['Order'].total).label('monthly_revenue')
        ).filter(self.models['Order'].status == 'delivered')\
         .group_by('month')\
         .order_by(desc('month'))\
         .limit(6)\
         .all()
        
        for month, count, revenue in results:
            print(f"     • {month}: {count} orders, ${revenue:,.2f}")
    
    def demonstrate_complex_transactions(self):
        """Demonstrate complex transactions."""
        print("\n4. Complex Transaction Example: Checkout Process")
        
        try:
            # Start transaction
            print("   • Starting checkout transaction...")
            
            # Get user and cart items (simulated)
            user = self.session.query(self.models['User']).first()
            product = self.session.query(self.models['Product']).first()
            
            if not user or not product:
                print("   • User or product not found")
                return
            
            # Simulate checkout process
            subtotal = product.price * 2  # Buy 2 items
            tax = subtotal * 0.08
            shipping = 10.00
            total = subtotal + tax + shipping
            
            # Generate order number
            order_number = f"ORD-{int(time.time())}"
            
            print(f"   • Creating order {order_number} for {user.username}")
            print(f"   • Subtotal: ${subtotal:.2f}, Tax: ${tax:.2f}, Shipping: ${shipping:.2f}")
            print(f"   • Total: ${total:.2f}")
            
            # Create order
            order = self.models['Order'](
                order_number=order_number,
                user=user,
                status='pending',
                subtotal=subtotal,
                tax=tax,
                shipping=shipping,
                total=total,
                payment_method='credit_card',
                payment_status='processing'
            )
            self.session.add(order)
            self.session.flush()  # Get order ID
            
            # Create order item
            order_item = self.models['OrderItem'](
                order=order,
                product=product,
                quantity=2,
                unit_price=product.price,
                discount=0.0
            )
            self.session.add(order_item)
            
            # Update product stock
            if product.quantity >= 2:
                product.quantity -= 2
                print(f"   • Updated product stock: {product.name} now has {product.quantity} units")
                
                # Simulate payment processing
                time.sleep(0.1)  # Simulate API call
                
                # Update order status
                order.status = 'processing'
                order.payment_status = 'paid'
                
                # Commit transaction
                self.session.commit()
                print("   ✓ Checkout completed successfully")
                print("   ✓ Order created:", order.order_number)
                print("   ✓ Payment processed")
                print("   ✓ Inventory updated")
                
            else:
                print("   ✗ Insufficient stock")
                self.session.rollback()
                print("   ✗ Transaction rolled back")
                
        except Exception as e:
            self.session.rollback()
            print(f"   ✗ Transaction failed: {e}")
        
        print("\n5. Database Design Best Practices Demonstrated:")
        print("   • Normalization (1NF, 2NF, 3NF)")
        print("   • Proper indexing strategy")
        print("   • Referential integrity with foreign keys")
        print("   • Data validation with constraints")
        print("   • Transaction management")
        print("   • Connection pooling")
        print("   • ORM patterns (Data Mapper)")
        print("   • Migrations-ready schema")

# ============================================================================
# SECTION 7: MAIN EXECUTION
# ============================================================================

def main():
    """Main function to run all database demonstrations."""
    
    print("\n" + "="*80)
    print("COMPREHENSIVE DATABASE & SQL DEMONSTRATION")
    print("="*80)
    
    # Clean up previous runs
    if demo_dir.exists():
        import shutil
        try:
            shutil.rmtree(demo_dir)
            print("Cleaned up previous demo directory")
        except:
            print("Could not clean up demo directory (might be in use)")
    
    try:
        # SECTION 2: SQL Fundamentals
        sql_demo = SqlFundamentals()
        sql_demo.demonstrate_joins()
        sql_demo.demonstrate_subqueries_and_ctes()
        sql_demo.demonstrate_transactions()
        sql_demo.demonstrate_index_performance()
        
        # SECTION 3: ORM Patterns
        orm_demo = OrmPatterns()
        
        # SECTION 4: Connection Pooling
        pooling_demo = ConnectionPooling()
        
        # SECTION 5: Database Migrations
        migration_demo = DatabaseMigrations()
        
        # SECTION 6: Comprehensive Example
        comprehensive_demo = ComprehensiveDatabaseExample()
        
        print("\n" + "="*80)
        print("DEMONSTRATION COMPLETE!")
        print("="*80)
        
        # Show generated files
        print("\nGenerated database files:")
        for file in demo_dir.glob("*.db"):
            size_mb = file.stat().st_size / (1024 * 1024)
            print(f"  • {file.name}: {size_mb:.2f} MB")
        
        print("\n" + "-"*80)
        print("KEY CONCEPTS DEMONSTRATED:")
        print("-"*80)
        print("1. SQL FUNDAMENTALS:")
        print("   • JOINs (INNER, LEFT, SELF, MULTIPLE)")
        print("   • Subqueries and CTEs")
        print("   • Transactions and ACID properties")
        print("   • Indexes and query optimization")
        print("   • Normalization and database design")
        
        print("\n2. ORM PATTERNS:")
        print("   • Active Record pattern")
        print("   • Data Mapper pattern (SQLAlchemy)")
        print("   • Object-relational mapping")
        print("   • Relationships and eager loading")
        print("   • Business logic in domain objects")
        
        print("\n3. CONNECTION POOLING:")
        print("   • Why pooling is necessary")
        print("   • Pool configuration and tuning")
        print("   • Thread-safety considerations")
        print("   • Performance comparisons")
        
        print("\n4. DATABASE MIGRATIONS:")
        print("   • Migration concepts and importance")
        print("   • Manual migration techniques")
        print("   • Alembic (SQLAlchemy migrations)")
        print("   • Rollback strategies")
        print("   • Migration testing and deployment")
        
        print("\n5. COMPREHENSIVE EXAMPLE:")
        print("   • Complete e-commerce database design")
        print("   • Complex queries and reports")
        print("   • Transaction management in real scenarios")
        print("   • Best practices implementation")
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\n\nError during demonstration: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\n" + "="*80)
        print("Database files are saved in 'demo_databases' directory.")
        print("You can explore them using SQLite tools or SQLAlchemy.")

if __name__ == "__main__":
    # Check for required packages
    required_packages = ['sqlalchemy']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing required packages: {', '.join(missing_packages)}")
        print("Install with: pip install " + " ".join(missing_packages))
        sys.exit(1)
    
    # Run the main demonstration
    main()