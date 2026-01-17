"""
COMPREHENSIVE PYTHON NETWORKING & DATA PROCESSING DEMONSTRATION
================================================================

This module demonstrates key Python concepts including:
1. Networking & APIs (HTTP, REST, JSON, HTTP clients)
2. File operations & data processing (os, sys, pathlib, parsing, streaming)
"""

# ============================================================================
# SECTION 1: IMPORTS AND SETUP
# ============================================================================

import os
import sys
import json
import csv
import yaml  # Requires PyYAML: pip install PyYAML
import time
import tempfile
from pathlib import Path
from typing import Dict, List, Any, Optional, Generator
import requests  # pip install requests
import httpx     # pip install httpx

# For demonstration purposes - we'll use a mock API
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import urllib.parse

# ============================================================================
# SECTION 2: FILESYSTEM OPERATIONS WITH os, sys, AND pathlib
# ============================================================================

class FileSystemOperations:
    """Demonstrates filesystem operations using os, sys, and pathlib modules."""
    
    def __init__(self, base_dir: str = "demo_data"):
        self.base_dir = Path(base_dir)
        self.setup_directories()
    
    def setup_directories(self):
        """Create necessary directories for our demonstration."""
        # Using pathlib for modern path handling
        self.data_dir = self.base_dir / "json_data"
        self.csv_dir = self.base_dir / "csv_data"
        self.logs_dir = self.base_dir / "logs"
        self.temp_dir = self.base_dir / "temp"
        
        # Create directories if they don't exist
        for directory in [self.base_dir, self.data_dir, self.csv_dir, 
                         self.logs_dir, self.temp_dir]:
            directory.mkdir(exist_ok=True)
            print(f"✓ Directory ensured: {directory}")
    
    def demonstrate_os_operations(self):
        """Show various os module operations."""
        print("\n" + "="*60)
        print("OS MODULE OPERATIONS")
        print("="*60)
        
        # Get current working directory
        cwd = os.getcwd()
        print(f"Current working directory: {cwd}")
        
        # List files in directory
        print(f"\nFiles in {self.base_dir}:")
        for item in os.listdir(self.base_dir):
            item_path = os.path.join(self.base_dir, item)
            is_dir = os.path.isdir(item_path)
            print(f"  {'📁' if is_dir else '📄'} {item}")
        
        # Get file information
        if (self.base_dir / "test.txt").exists():
            stat_info = os.stat(self.base_dir / "test.txt")
            print(f"\nFile stats - Size: {stat_info.st_size} bytes, "
                  f"Modified: {time.ctime(stat_info.st_mtime)}")
    
    def demonstrate_sys_operations(self):
        """Show sys module operations."""
        print("\n" + "="*60)
        print("SYS MODULE OPERATIONS")
        print("="*60)
        
        # Python version and platform information
        print(f"Python version: {sys.version_info.major}.{sys.version_info.minor}")
        print(f"Platform: {sys.platform}")
        
        # Command line arguments
        print(f"\nScript name: {sys.argv[0]}")
        print(f"Command line arguments: {sys.argv[1:] if len(sys.argv) > 1 else 'None'}")
        
        # Module search path
        print(f"\nFirst 3 entries in sys.path:")
        for path in sys.path[:3]:
            print(f"  {path}")
    
    def demonstrate_pathlib_operations(self):
        """Show modern path handling with pathlib."""
        print("\n" + "="*60)
        print("PATHLIB OPERATIONS")
        print("="*60)
        
        # Create paths using pathlib
        config_file = self.base_dir / "config" / "settings.json"
        
        # Path operations
        print(f"Base directory: {self.base_dir}")
        print(f"Parent directory: {self.base_dir.parent}")
        print(f"File name: {config_file.name}")
        print(f"File suffix: {config_file.suffix}")
        print(f"File stem (without suffix): {config_file.stem}")
        
        # Check path properties
        print(f"\nPath exists: {self.base_dir.exists()}")
        print(f"Is directory: {self.base_dir.is_dir()}")
        print(f"Is file: {config_file.is_file()}")
        
        # Create a test file
        test_file = self.base_dir / "test.txt"
        test_file.write_text("Hello, Pathlib!")
        print(f"\nCreated test file: {test_file}")
        
        # Read it back
        content = test_file.read_text()
        print(f"File content: {content}")

# ============================================================================
# SECTION 3: HTTP BASICS & REST CONCEPTS
# ============================================================================

class MockRestAPI:
    """A simple mock REST API server for demonstration purposes."""
    
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.data_store = {
            'users': [
                {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
                {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'},
            ],
            'products': [
                {'id': 1, 'name': 'Laptop', 'price': 999.99},
                {'id': 2, 'name': 'Mouse', 'price': 25.50},
            ]
        }
        self.server = None
    
    def start(self):
        """Start the mock API server in a background thread."""
        handler = self.create_handler()
        self.server = HTTPServer((self.host, self.port), handler)
        thread = threading.Thread(target=self.server.serve_forever)
        thread.daemon = True
        thread.start()
        print(f"Mock API server started at http://{self.host}:{self.port}")
    
    def create_handler(self):
        """Create HTTP request handler class with REST endpoints."""
        
        class MockAPIHandler(BaseHTTPRequestHandler):
            api = self
            
            def _set_headers(self, status_code=200, content_type='application/json'):
                self.send_response(status_code)
                self.send_header('Content-type', content_type)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
            
            def do_GET(self):
                """Handle GET requests - Retrieve resources."""
                parsed_path = urllib.parse.urlparse(self.path)
                path_parts = parsed_path.path.strip('/').split('/')
                
                # API Documentation
                if self.path == '/':
                    self._set_headers(content_type='text/html')
                    response = """
                    <html><body>
                    <h1>Mock REST API</h1>
                    <h2>Available Endpoints:</h2>
                    <ul>
                        <li>GET /api/users - List all users</li>
                        <li>GET /api/users/{id} - Get specific user</li>
                        <li>GET /api/products - List all products</li>
                        <li>POST /api/users - Create new user</li>
                        <li>PUT /api/users/{id} - Update user</li>
                    </ul>
                    </body></html>
                    """
                    self.wfile.write(response.encode())
                    return
                
                # RESTful endpoints
                if len(path_parts) >= 2 and path_parts[0] == 'api':
                    resource = path_parts[1]
                    
                    if resource in self.api.data_store:
                        if len(path_parts) == 2:
                            # GET /api/{resource}
                            self._set_headers()
                            response = json.dumps(self.api.data_store[resource])
                            self.wfile.write(response.encode())
                        elif len(path_parts) == 3:
                            # GET /api/{resource}/{id}
                            resource_id = int(path_parts[2])
                            items = [item for item in self.api.data_store[resource] 
                                    if item['id'] == resource_id]
                            if items:
                                self._set_headers()
                                self.wfile.write(json.dumps(items[0]).encode())
                            else:
                                self._set_headers(404)
                                self.wfile.write(b'{"error": "Resource not found"}')
                        else:
                            self._set_headers(404)
                    else:
                        self._set_headers(404)
                        self.wfile.write(b'{"error": "Endpoint not found"}')
                else:
                    self._set_headers(404)
            
            def do_POST(self):
                """Handle POST requests - Create resources."""
                if self.path.startswith('/api/'):
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)
                    
                    try:
                        data = json.loads(post_data.decode())
                        path_parts = self.path.strip('/').split('/')
                        
                        if len(path_parts) >= 2 and path_parts[0] == 'api':
                            resource = path_parts[1]
                            
                            if resource in self.api.data_store:
                                # Generate new ID
                                new_id = max(item['id'] for item in self.api.data_store[resource]) + 1
                                data['id'] = new_id
                                self.api.data_store[resource].append(data)
                                
                                self._set_headers(201)
                                response = json.dumps(data)
                                self.wfile.write(response.encode())
                            else:
                                self._set_headers(404)
                        else:
                            self._set_headers(404)
                    except json.JSONDecodeError:
                        self._set_headers(400)
                        self.wfile.write(b'{"error": "Invalid JSON"}')
                else:
                    self._set_headers(404)
            
            def log_message(self, format, *args):
                """Suppress default logging."""
                pass
        
        return MockAPIHandler

# ============================================================================
# SECTION 4: HTTP CLIENTS (requests AND httpx)
# ============================================================================

class HttpClientDemonstration:
    """Demonstrates HTTP client operations with requests and httpx."""
    
    def __init__(self, base_url='http://localhost:8000'):
        self.base_url = base_url
    
    def demonstrate_requests_library(self):
        """Show HTTP operations using the requests library."""
        print("\n" + "="*60)
        print("REQUESTS LIBRARY DEMONSTRATION")
        print("="*60)
        
        try:
            # GET request
            print("\n1. GET Request to fetch all users:")
            response = requests.get(f"{self.base_url}/api/users")
            print(f"   Status Code: {response.status_code}")
            print(f"   Response Headers: {dict(response.headers)}")
            print(f"   Response Body: {response.json()}")
            
            # GET request with specific resource
            print("\n2. GET Request for specific user (ID: 1):")
            response = requests.get(f"{self.base_url}/api/users/1")
            print(f"   Status Code: {response.status_code}")
            print(f"   User Data: {response.json()}")
            
            # POST request to create new resource
            print("\n3. POST Request to create new user:")
            new_user = {
                "name": "Charlie",
                "email": "charlie@example.com"
            }
            response = requests.post(
                f"{self.base_url}/api/users",
                json=new_user,  # Automatically sets Content-Type to application/json
                headers={"User-Agent": "DemoClient/1.0"}
            )
            print(f"   Status Code: {response.status_code}")
            print(f"   Created User: {response.json()}")
            
            # GET request with query parameters (simulated)
            print("\n4. GET Request with query parameters:")
            response = requests.get(
                f"{self.base_url}/api/users",
                params={"limit": 2, "offset": 0}
            )
            print(f"   URL with params: {response.url}")
            print(f"   Response: {response.json()}")
            
            # Error handling
            print("\n5. Error handling demonstration:")
            try:
                response = requests.get(f"{self.base_url}/api/nonexistent")
                response.raise_for_status()  # Raises HTTPError for bad responses
            except requests.exceptions.HTTPError as e:
                print(f"   HTTP Error: {e}")
            except requests.exceptions.RequestException as e:
                print(f"   Request Error: {e}")
                
        except requests.exceptions.ConnectionError:
            print("   ERROR: Could not connect to the API server.")
            print("   Make sure the MockRestAPI is running.")
    
    def demonstrate_httpx_library(self):
        """Show HTTP operations using the httpx library (async support)."""
        print("\n" + "="*60)
        print("HTTPX LIBRARY DEMONSTRATION")
        print("="*60)
        
        try:
            # Synchronous client
            print("\n1. Synchronous HTTP requests with httpx:")
            with httpx.Client(timeout=10.0) as client:
                response = client.get(f"{self.base_url}/api/products")
                print(f"   Status: {response.status_code}")
                print(f"   Products: {response.json()}")
            
            # Async example (commented but shows structure)
            print("\n2. Asynchronous HTTP pattern (commented example):")
            print("""
            async def fetch_data():
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"{self.base_url}/api/users")
                    return response.json()
            
            # Run in asyncio event loop
            import asyncio
            users = asyncio.run(fetch_data())
            """)
            
            # More advanced features
            print("\n3. Advanced httpx features:")
            
            # Custom headers and timeout
            print("   Custom headers and timeout:")
            with httpx.Client() as client:
                response = client.get(
                    f"{self.base_url}/api/users/1",
                    headers={"X-API-Key": "demo-key", "Accept": "application/json"},
                    timeout=httpx.Timeout(5.0, connect=2.0)
                )
                print(f"   Response: {response.json()}")
            
            # Streaming response
            print("\n4. Streaming large responses:")
            with httpx.Client() as client:
                with client.stream("GET", f"{self.base_url}/") as response:
                    print(f"   Status: {response.status_code}")
                    print(f"   Headers: {dict(response.headers)}")
                    # For large responses, we could process in chunks here
            
        except httpx.RequestError as e:
            print(f"   HTTPX Error: {e}")

# ============================================================================
# SECTION 5: JSON SERIALIZATION AND PARSING
# ============================================================================

class JsonOperations:
    """Demonstrates JSON serialization and parsing."""
    
    def __init__(self, data_dir="demo_data/json_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
    
    def demonstrate_json_basics(self):
        """Show basic JSON operations."""
        print("\n" + "="*60)
        print("JSON SERIALIZATION AND PARSING")
        print("="*60)
        
        # Python data structure
        complex_data = {
            "company": "TechCorp",
            "employees": [
                {
                    "id": 1,
                    "name": "Alice",
                    "skills": ["Python", "JavaScript", "AWS"],
                    "active": True,
                    "salary": 85000.50
                },
                {
                    "id": 2,
                    "name": "Bob",
                    "skills": ["Java", "Docker", "Kubernetes"],
                    "active": True,
                    "salary": 92000.75
                }
            ],
            "departments": {
                "engineering": 15,
                "sales": 8,
                "marketing": 5
            }
        }
        
        # Serialize to JSON string
        print("\n1. Serialize Python object to JSON string:")
        json_string = json.dumps(complex_data, indent=2)
        print(f"   JSON String (first 200 chars):\n{json_string[:200]}...")
        
        # Save to file
        json_file = self.data_dir / "company_data.json"
        with open(json_file, 'w') as f:
            json.dump(complex_data, f, indent=2)
        print(f"\n2. Saved JSON to file: {json_file}")
        
        # Read from file
        print("\n3. Read and parse JSON from file:")
        with open(json_file, 'r') as f:
            loaded_data = json.load(f)
        print(f"   Loaded data - Company: {loaded_data['company']}")
        print(f"   Number of employees: {len(loaded_data['employees'])}")
        
        # Custom serialization with json.JSONEncoder
        print("\n4. Custom JSON serialization:")
        
        class Employee:
            def __init__(self, name, age):
                self.name = name
                self.age = age
            
            def to_dict(self):
                return {"name": self.name, "age": self.age}
        
        class EmployeeEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, Employee):
                    return obj.to_dict()
                return super().default(obj)
        
        employees = [Employee("Charlie", 30), Employee("Diana", 28)]
        custom_json = json.dumps({"team": employees}, cls=EmployeeEncoder, indent=2)
        print(f"   Custom encoded JSON:\n{custom_json}")
        
        # Handle datetime objects in JSON
        print("\n5. Handling datetime in JSON:")
        import datetime
        
        def datetime_handler(obj):
            if isinstance(obj, (datetime.datetime, datetime.date)):
                return obj.isoformat()
            raise TypeError(f"Type {type(obj)} not serializable")
        
        event = {
            "name": "Conference",
            "date": datetime.date(2024, 6, 15),
            "start_time": datetime.datetime(2024, 6, 15, 9, 0, 0)
        }
        
        event_json = json.dumps(event, default=datetime_handler, indent=2)
        print(f"   Datetime in JSON:\n{event_json}")

# ============================================================================
# SECTION 6: CSV AND YAML PROCESSING
# ============================================================================

class StructuredDataProcessing:
    """Demonstrates processing of structured data formats (CSV, YAML)."""
    
    def __init__(self, data_dir="demo_data"):
        self.data_dir = Path(data_dir)
        self.csv_dir = self.data_dir / "csv_data"
        self.csv_dir.mkdir(exist_ok=True)
    
    def demonstrate_csv_operations(self):
        """Show CSV reading and writing operations."""
        print("\n" + "="*60)
        print("CSV PROCESSING")
        print("="*60)
        
        # Sample data
        employees = [
            {"id": 1, "name": "Alice", "department": "Engineering", "salary": 85000},
            {"id": 2, "name": "Bob", "department": "Sales", "salary": 75000},
            {"id": 3, "name": "Charlie", "department": "Marketing", "salary": 65000},
            {"id": 4, "name": "Diana", "department": "Engineering", "salary": 90000}
        ]
        
        # Write to CSV
        csv_file = self.csv_dir / "employees.csv"
        print(f"\n1. Writing data to CSV: {csv_file}")
        
        with open(csv_file, 'w', newline='') as f:
            fieldnames = ["id", "name", "department", "salary"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            writer.writeheader()
            for employee in employees:
                writer.writerow(employee)
        
        print("   CSV file created successfully.")
        
        # Read CSV
        print("\n2. Reading CSV file:")
        with open(csv_file, 'r', newline='') as f:
            reader = csv.DictReader(f)
            print("   Header:", reader.fieldnames)
            print("   Data:")
            for row in reader:
                print(f"     {row}")
        
        # CSV with different delimiters
        print("\n3. CSV with different delimiters (TSV):")
        tsv_file = self.csv_dir / "employees.tsv"
        with open(tsv_file, 'w', newline='') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow(["id", "name", "department"])
            writer.writerow([1, "Alice", "Engineering"])
            writer.writerow([2, "Bob", "Sales"])
        
        # Read TSV
        with open(tsv_file, 'r', newline='') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                print(f"   {row}")
    
    def demonstrate_yaml_operations(self):
        """Show YAML reading and writing operations."""
        print("\n" + "="*60)
        print("YAML PROCESSING")
        print("="*60)
        
        try:
            # Sample configuration data
            config_data = {
                "application": "DataProcessor",
                "version": "1.0.0",
                "database": {
                    "host": "localhost",
                    "port": 5432,
                    "name": "production_db",
                    "credentials": {
                        "username": "admin",
                        "password": "secret"
                    }
                },
                "features": ["logging", "caching", "monitoring"],
                "thresholds": {
                    "memory": "2GB",
                    "timeout": 30
                }
            }
            
            # Write YAML
            yaml_file = self.data_dir / "config.yaml"
            print(f"\n1. Writing data to YAML: {yaml_file}")
            
            with open(yaml_file, 'w') as f:
                yaml.dump(config_data, f, default_flow_style=False)
            
            print("   YAML file created successfully.")
            
            # Read YAML
            print("\n2. Reading YAML file:")
            with open(yaml_file, 'r') as f:
                loaded_config = yaml.safe_load(f)
            
            print(f"   Application: {loaded_config['application']}")
            print(f"   Database host: {loaded_config['database']['host']}")
            print(f"   Features: {loaded_config['features']}")
            
            # YAML with multiple documents
            print("\n3. YAML with multiple documents:")
            multi_yaml = """
            ---
            server: production
            port: 8080
            ---
            server: staging
            port: 8081
            ---
            server: development
            port: 8082
            """
            
            documents = list(yaml.safe_load_all(multi_yaml))
            for i, doc in enumerate(documents, 1):
                print(f"   Document {i}: {doc}")
                
        except ImportError:
            print("   PyYAML not installed. Install with: pip install PyYAML")

# ============================================================================
# SECTION 7: STREAMING AND MEMORY-SAFE PROCESSING
# ============================================================================

class MemorySafeProcessing:
    """Demonstrates streaming and memory-safe file processing."""
    
    def __init__(self, data_dir="demo_data"):
        self.data_dir = Path(data_dir)
    
    def demonstrate_streaming_json(self):
        """Show how to stream large JSON files safely."""
        print("\n" + "="*60)
        print("STREAMING JSON PROCESSING")
        print("="*60)
        
        # Create a large JSON file for demonstration
        large_file = self.data_dir / "large_data.json"
        print(f"\n1. Creating large JSON file: {large_file}")
        
        # Generate large JSON file with array of objects
        with open(large_file, 'w') as f:
            f.write('[\n')
            for i in range(100):  # Reduced for demo, could be millions
                record = {
                    "id": i,
                    "name": f"User_{i}",
                    "data": "x" * 1000  # Add some data weight
                }
                f.write(json.dumps(record))
                if i < 99:
                    f.write(',\n')
            f.write('\n]')
        
        file_size = large_file.stat().st_size
        print(f"   File size: {file_size:,} bytes")
        
        # BAD APPROACH: Loading entire file into memory
        print("\n2. BAD APPROACH - Loading entire file:")
        try:
            with open(large_file, 'r') as f:
                data = json.load(f)  # Could crash with huge files
            print(f"   Loaded {len(data)} records (works for demo size)")
        except MemoryError:
            print("   ERROR: Out of memory!")
        
        # GOOD APPROACH: Streaming JSON with ijson (if installed)
        print("\n3. GOOD APPROACH - Streaming JSON:")
        print("   Using iterative parsing to process one record at a time.")
        
        # Manual streaming for JSON arrays
        def stream_json_array(filepath):
            """Generator that yields records from a JSON array one by one."""
            with open(filepath, 'r') as f:
                # Skip opening bracket and whitespace
                f.read(1)
                
                buffer = ""
                depth = 0
                in_string = False
                escape = False
                
                while True:
                    char = f.read(1)
                    if not char:
                        break
                    
                    buffer += char
                    
                    # Track JSON structure
                    if char == '"' and not escape:
                        in_string = not in_string
                    elif not in_string:
                        if char == '{':
                            depth += 1
                        elif char == '}':
                            depth -= 1
                            if depth == 0:
                                # Complete object found
                                yield json.loads(buffer)
                                buffer = ""
                                # Skip comma and whitespace
                                next_char = f.read(1)
                                while next_char in [' ', '\n', '\t', ',']:
                                    next_char = f.read(1)
                                if next_char:
                                    f.seek(f.tell() - 1)  # Put back non-whitespace char
                                continue
                    
                    escape = (char == '\\' and not escape)
        
        # Process records one by one
        print("   Processing records streamingly:")
        count = 0
        total_chars = 0
        
        for record in stream_json_array(large_file):
            count += 1
            total_chars += len(record['name'])
            if count <= 3:  # Show first 3 records
                print(f"     Record {count}: {record['name']}")
        
        print(f"   Processed {count} records with {total_chars} total characters")
        print("   Peak memory usage remained low!")
    
    def demonstrate_streaming_csv(self):
        """Show how to process large CSV files efficiently."""
        print("\n" + "="*60)
        print("STREAMING CSV PROCESSING")
        print("="*60)
        
        # Create a large CSV file
        large_csv = self.data_dir / "large_dataset.csv"
        print(f"\n1. Creating large CSV file: {large_csv}")
        
        with open(large_csv, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'value', 'timestamp'])
            for i in range(10000):  # 10,000 rows
                writer.writerow([i, i * 1.5, f'2024-01-{i % 30 + 1:02d}'])
        
        print(f"   Created {large_csv.stat().st_size:,} bytes CSV file")
        
        # Process CSV in chunks
        print("\n2. Processing CSV in chunks:")
        
        def process_csv_in_chunks(filepath, chunk_size=1000):
            """Process CSV file in manageable chunks."""
            chunk = []
            
            with open(filepath, 'r', newline='') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    chunk.append(row)
                    
                    if len(chunk) >= chunk_size:
                        # Process chunk
                        yield chunk
                        chunk = []
                
                # Yield remaining rows
                if chunk:
                    yield chunk
        
        # Process and analyze data
        print("   Analyzing data chunk by chunk:")
        
        total_rows = 0
        sum_values = 0
        
        for chunk_num, chunk in enumerate(process_csv_in_chunks(large_csv, 1000), 1):
            chunk_sum = sum(float(row['value']) for row in chunk)
            sum_values += chunk_sum
            total_rows += len(chunk)
            
            if chunk_num <= 3:  # Show first 3 chunks
                print(f"     Chunk {chunk_num}: {len(chunk)} rows, "
                      f"sum: {chunk_sum:.2f}")
        
        avg_value = sum_values / total_rows if total_rows > 0 else 0
        print(f"   Total: {total_rows} rows, Average value: {avg_value:.2f}")
        print("   Memory efficient: only one chunk in memory at a time")
    
    def demonstrate_generator_pattern(self):
        """Show generator pattern for memory-safe data processing."""
        print("\n" + "="*60)
        print("GENERATOR PATTERN FOR MEMORY SAFETY")
        print("="*60)
        
        print("\n1. Reading large file line by line:")
        
        large_file = self.data_dir / "large_text.txt"
        
        # Create a sample large text file
        with open(large_file, 'w') as f:
            for i in range(10000):
                f.write(f"This is line {i} with some data: {'x' * (i % 100)}\n")
        
        # Generator function to process lines
        def process_lines(filepath):
            with open(filepath, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    # Process line (could be complex operation)
                    processed = line.strip().upper()
                    yield line_num, processed
        
        # Process without loading entire file
        print("   Processing lines with generator:")
        line_count = 0
        
        for line_num, processed_line in process_lines(large_file):
            line_count += 1
            if line_num <= 3:  # Show first 3 lines
                print(f"     Line {line_num}: {processed_line[:50]}...")
            if line_num >= 100:  # Stop early for demo
                break
        
        print(f"   Processed {line_count} lines without loading file into memory")

# ============================================================================
# SECTION 8: INTEGRATED EXAMPLE - API DATA PIPELINE
# ============================================================================

class ApiDataPipeline:
    """Integrated example showing complete data pipeline."""
    
    def __init__(self, api_url='http://localhost:8000'):
        self.api_url = api_url
        self.data_dir = Path("demo_data/pipeline_output")
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def run_pipeline(self):
        """Run complete data pipeline."""
        print("\n" + "="*60)
        print("COMPLETE API DATA PIPELINE DEMONSTRATION")
        print("="*60)
        
        try:
            # Step 1: Fetch data from API
            print("\n1. Fetching data from REST API...")
            response = requests.get(f"{self.api_url}/api/users")
            users = response.json()
            print(f"   Retrieved {len(users)} users from API")
            
            # Step 2: Process data in memory-safe way
            print("\n2. Processing data...")
            
            def enrich_user_data(users):
                """Generator that enriches user data."""
                for user in users:
                    # Simulate data enrichment
                    user['processed'] = True
                    user['timestamp'] = time.time()
                    user['name_length'] = len(user['name'])
                    yield user
            
            enriched_users = list(enrich_user_data(users))
            
            # Step 3: Save to multiple formats
            print("\n3. Saving data to multiple formats...")
            
            # Save as JSON
            json_file = self.data_dir / "users.json"
            with open(json_file, 'w') as f:
                json.dump(enriched_users, f, indent=2)
            print(f"   ✓ Saved to JSON: {json_file}")
            
            # Save as CSV
            csv_file = self.data_dir / "users.csv"
            with open(csv_file, 'w', newline='') as f:
                if enriched_users:
                    fieldnames = enriched_users[0].keys()
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(enriched_users)
            print(f"   ✓ Saved to CSV: {csv_file}")
            
            # Save as YAML
            yaml_file = self.data_dir / "users.yaml"
            with open(yaml_file, 'w') as f:
                yaml.dump(enriched_users, f, default_flow_style=False)
            print(f"   ✓ Saved to YAML: {yaml_file}")
            
            # Step 4: Read and validate
            print("\n4. Reading back and validating data...")
            
            with open(json_file, 'r') as f:
                loaded_users = json.load(f)
            
            print(f"   Loaded {len(loaded_users)} users from disk")
            print(f"   First user: {loaded_users[0]['name']} "
                  f"(ID: {loaded_users[0]['id']})")
            
            # Step 5: Generate report
            print("\n5. Generating data report...")
            report_file = self.data_dir / "report.txt"
            
            total_name_length = sum(user['name_length'] for user in loaded_users)
            avg_name_length = total_name_length / len(loaded_users) if loaded_users else 0
            
            report_data = {
                "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "total_users": len(loaded_users),
                "average_name_length": avg_name_length,
                "data_files": [
                    str(json_file.relative_to(self.data_dir.parent)),
                    str(csv_file.relative_to(self.data_dir.parent)),
                    str(yaml_file.relative_to(self.data_dir.parent))
                ]
            }
            
            with open(report_file, 'w') as f:
                f.write("DATA PIPELINE REPORT\n")
                f.write("=" * 50 + "\n\n")
                for key, value in report_data.items():
                    f.write(f"{key.replace('_', ' ').title()}: {value}\n")
            
            print(f"   ✓ Report generated: {report_file}")
            
            print("\n" + "="*50)
            print("PIPELINE COMPLETED SUCCESSFULLY!")
            print("="*50)
            
        except Exception as e:
            print(f"\n✗ Pipeline error: {e}")
            import traceback
            traceback.print_exc()

# ============================================================================
# SECTION 9: MAIN EXECUTION
# ============================================================================

def main():
    """Main function to run all demonstrations."""
    
    print("\n" + "="*80)
    print("PYTHON NETWORKING & DATA PROCESSING COMPREHENSIVE DEMONSTRATION")
    print("="*80)
    
    # Clean up previous runs
    demo_dir = Path("demo_data")
    if demo_dir.exists():
        import shutil
        shutil.rmtree(demo_dir)
        print("Cleaned up previous demo directory")
    
    # Start mock API server
    print("\nStarting Mock REST API Server...")
    api = MockRestAPI()
    api.start()
    time.sleep(2)  # Give server time to start
    
    try:
        # SECTION 2: Filesystem Operations
        fs_ops = FileSystemOperations()
        fs_ops.demonstrate_os_operations()
        fs_ops.demonstrate_sys_operations()
        fs_ops.demonstrate_pathlib_operations()
        
        # SECTION 4: HTTP Clients
        http_demo = HttpClientDemonstration()
        http_demo.demonstrate_requests_library()
        http_demo.demonstrate_httpx_library()
        
        # SECTION 5: JSON Operations
        json_ops = JsonOperations()
        json_ops.demonstrate_json_basics()
        
        # SECTION 6: CSV and YAML
        data_ops = StructuredDataProcessing()
        data_ops.demonstrate_csv_operations()
        data_ops.demonstrate_yaml_operations()
        
        # SECTION 7: Streaming and Memory Safety
        memory_safe = MemorySafeProcessing()
        memory_safe.demonstrate_streaming_json()
        memory_safe.demonstrate_streaming_csv()
        memory_safe.demonstrate_generator_pattern()
        
        # SECTION 8: Integrated Pipeline
        pipeline = ApiDataPipeline()
        pipeline.run_pipeline()
        
        print("\n" + "="*80)
        print("DEMONSTRATION COMPLETE!")
        print("="*80)
        print("\nCreated files and directories:")
        for root, dirs, files in os.walk("demo_data"):
            level = root.replace("demo_data", "").count(os.sep)
            indent = " " * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = " " * 2 * (level + 1)
            for file in files[:5]:  # Show first 5 files
                print(f"{subindent}{file}")
            if len(files) > 5:
                print(f"{subindent}... and {len(files) - 5} more files")
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\n\nError during demonstration: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\n\nCleanup complete. Files are saved in 'demo_data' directory.")
        print("You can explore the generated files to see the output.")

if __name__ == "__main__":
    # Check if required packages are installed
    required_packages = ['requests', 'httpx']
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