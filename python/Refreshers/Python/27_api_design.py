"""
COMPREHENSIVE API DESIGN GUIDE WITH PYTHON IMPLEMENTATION
===========================================================
This comprehensive script demonstrates:
1. RESTful API principles
2. API versioning strategies
3. Rate limiting implementation
4. Caching headers and strategies
"""

print("=" * 70)
print("API DESIGN PRINCIPLES & IMPLEMENTATION")
print("=" * 70)

# ============================================================================
# PART 1: RESTFUL API PRINCIPLES
# ============================================================================

print("\n" + "=" * 30)
print("RESTFUL API PRINCIPLES")
print("=" * 30)

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum

print("\n--- RESTful Resource Design ---")

class HTTPMethod(Enum):
    """RESTful HTTP methods mapped to CRUD operations"""
    GET = "GET"      # Read/Retrieve
    POST = "POST"    # Create
    PUT = "PUT"      # Update/Replace
    PATCH = "PATCH"  # Partial Update
    DELETE = "DELETE"# Delete

class BookStatus(Enum):
    """Domain model for book status"""
    AVAILABLE = "available"
    BORROWED = "borrowed"
    RESERVED = "reserved"

@dataclass
class Book:
    """Resource representation following REST principles"""
    id: str
    title: str
    author: str
    isbn: str
    status: BookStatus
    created_at: datetime
    updated_at: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to API response format"""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "_links": {  # HATEOAS links
                "self": f"/api/v1/books/{self.id}",
                "borrow": f"/api/v1/books/{self.id}/borrow",
                "return": f"/api/v1/books/{self.id}/return"
            }
        }


class RESTfulBookAPI:
    """
    Demonstrates RESTful principles:
    1. Resource-based URLs
    2. Proper HTTP methods
    3. Statelessness
    4. Representations (JSON)
    5. HATEOAS (Hypermedia as the Engine of Application State)
    """
    
    def __init__(self):
        # In-memory "database"
        self.books: Dict[str, Book] = {}
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample books"""
        now = datetime.now()
        sample_books = [
            Book("1", "Clean Code", "Robert Martin", "9780132350884", 
                 BookStatus.AVAILABLE, now, now),
            Book("2", "Design Patterns", "Gang of Four", "9780201633610",
                 BookStatus.BORROWED, now, now),
            Book("3", "The Pragmatic Programmer", "Andrew Hunt", "9780201616224",
                 BookStatus.AVAILABLE, now, now)
        ]
        for book in sample_books:
            self.books[book.id] = book
    
    # RESTful endpoints implementation
    def handle_request(self, method: HTTPMethod, path: str, 
                       data: Optional[Dict] = None, 
                       query_params: Optional[Dict] = None) -> Dict:
        """
        Unified request handler demonstrating RESTful routing
        """
        print(f"\n[{method.value}] {path}")
        
        # Parse path to determine resource
        path_parts = path.strip("/").split("/")
        
        # Collection endpoint: /books
        if len(path_parts) == 1 and path_parts[0] == "books":
            if method == HTTPMethod.GET:
                return self._get_books(query_params)
            elif method == HTTPMethod.POST:
                return self._create_book(data)
        
        # Resource endpoint: /books/{id}
        elif len(path_parts) == 2 and path_parts[0] == "books":
            book_id = path_parts[1]
            if method == HTTPMethod.GET:
                return self._get_book(book_id)
            elif method == HTTPMethod.PUT:
                return self._update_book(book_id, data)
            elif method == HTTPMethod.PATCH:
                return self._partial_update_book(book_id, data)
            elif method == HTTPMethod.DELETE:
                return self._delete_book(book_id)
        
        # Sub-resource endpoint: /books/{id}/borrow
        elif len(path_parts) == 3 and path_parts[0] == "books":
            book_id = path_parts[1]
            action = path_parts[2]
            if method == HTTPMethod.POST:
                if action == "borrow":
                    return self._borrow_book(book_id, data)
                elif action == "return":
                    return self._return_book(book_id)
        
        return {
            "error": "Not Found",
            "message": f"Endpoint {path} not found"
        }, 404
    
    def _get_books(self, query_params: Optional[Dict]) -> Dict:
        """GET /books - Retrieve collection with filtering"""
        books_list = list(self.books.values())
        
        # Query parameter filtering (RESTful filtering)
        if query_params:
            status = query_params.get("status")
            author = query_params.get("author")
            
            if status:
                books_list = [b for b in books_list 
                             if b.status == BookStatus(status)]
            if author:
                books_list = [b for b in books_list 
                             if author.lower() in b.author.lower()]
        
        return {
            "count": len(books_list),
            "books": [book.to_dict() for book in books_list],
            "_links": {
                "self": "/api/v1/books",
                "create": "/api/v1/books"
            }
        }, 200
    
    def _get_book(self, book_id: str) -> Dict:
        """GET /books/{id} - Retrieve specific resource"""
        book = self.books.get(book_id)
        if not book:
            return {
                "error": "Not Found",
                "message": f"Book {book_id} not found"
            }, 404
        
        return book.to_dict(), 200
    
    def _create_book(self, data: Dict) -> Dict:
        """POST /books - Create new resource"""
        if not data:
            return {"error": "Bad Request", "message": "No data provided"}, 400
        
        # Generate ID (in real app, use UUID)
        import uuid
        book_id = str(uuid.uuid4())[:8]
        
        now = datetime.now()
        book = Book(
            id=book_id,
            title=data.get("title", ""),
            author=data.get("author", ""),
            isbn=data.get("isbn", ""),
            status=BookStatus.AVAILABLE,
            created_at=now,
            updated_at=now
        )
        
        self.books[book_id] = book
        
        # RESTful response: 201 Created with Location header
        return {
            "message": "Book created successfully",
            "book": book.to_dict(),
            "location": f"/api/v1/books/{book_id}"
        }, 201
    
    def _update_book(self, book_id: str, data: Dict) -> Dict:
        """PUT /books/{id} - Replace entire resource"""
        if not data:
            return {"error": "Bad Request", "message": "No data provided"}, 400
        
        book = self.books.get(book_id)
        if not book:
            return {"error": "Not Found", "message": f"Book {book_id} not found"}, 404
        
        # Full update (replace all fields)
        updated_book = Book(
            id=book_id,
            title=data.get("title", book.title),
            author=data.get("author", book.author),
            isbn=data.get("isbn", book.isbn),
            status=BookStatus(data.get("status", book.status.value)),
            created_at=book.created_at,
            updated_at=datetime.now()
        )
        
        self.books[book_id] = updated_book
        
        return {
            "message": "Book updated successfully",
            "book": updated_book.to_dict()
        }, 200
    
    def _partial_update_book(self, book_id: str, data: Dict) -> Dict:
        """PATCH /books/{id} - Partial update"""
        book = self.books.get(book_id)
        if not book:
            return {"error": "Not Found", "message": f"Book {book_id} not found"}, 404
        
        # Partial update (only provided fields)
        if "title" in data:
            book.title = data["title"]
        if "author" in data:
            book.author = data["author"]
        if "status" in data:
            book.status = BookStatus(data["status"])
        
        book.updated_at = datetime.now()
        
        return {
            "message": "Book partially updated",
            "book": book.to_dict()
        }, 200
    
    def _delete_book(self, book_id: str) -> Dict:
        """DELETE /books/{id} - Remove resource"""
        if book_id not in self.books:
            return {"error": "Not Found", "message": f"Book {book_id} not found"}, 404
        
        del self.books[book_id]
        
        return {
            "message": f"Book {book_id} deleted successfully"
        }, 204  # No Content
    
    def _borrow_book(self, book_id: str, data: Dict) -> Dict:
        """POST /books/{id}/borrow - Action on resource"""
        book = self.books.get(book_id)
        if not book:
            return {"error": "Not Found", "message": f"Book {book_id} not found"}, 404
        
        if book.status != BookStatus.AVAILABLE:
            return {
                "error": "Conflict",
                "message": f"Book is not available. Current status: {book.status.value}"
            }, 409
        
        # Update status
        book.status = BookStatus.BORROWED
        book.updated_at = datetime.now()
        
        borrower = data.get("borrower", "Unknown")
        due_date = data.get("due_date", "2024-12-31")
        
        return {
            "message": f"Book borrowed by {borrower}",
            "due_date": due_date,
            "book": book.to_dict()
        }, 200
    
    def _return_book(self, book_id: str) -> Dict:
        """POST /books/{id}/return - Another action"""
        book = self.books.get(book_id)
        if not book:
            return {"error": "Not Found", "message": f"Book {book_id} not found"}, 404
        
        book.status = BookStatus.AVAILABLE
        book.updated_at = datetime.now()
        
        return {
            "message": "Book returned successfully",
            "book": book.to_dict()
        }, 200


print("\n--- RESTful API Demonstration ---")
api = RESTfulBookAPI()

# Demonstrate RESTful endpoints
print("\n1. GET /books (Retrieve collection):")
response, status = api.handle_request(HTTPMethod.GET, "/books")
print(f"   Status: {status}")
print(f"   Count: {response.get('count')} books")

print("\n2. GET /books with query parameters:")
response, status = api.handle_request(
    HTTPMethod.GET, 
    "/books", 
    query_params={"status": "available"}
)
print(f"   Status: {status}")
print(f"   Available books: {response.get('count')}")

print("\n3. GET /books/{id} (Retrieve specific resource):")
response, status = api.handle_request(HTTPMethod.GET, "/books/1")
print(f"   Status: {status}")
print(f"   Book: {response.get('title')}")

print("\n4. POST /books (Create new resource):")
new_book = {
    "title": "API Design Patterns",
    "author": "JJ Geewax",
    "isbn": "9781617295850"
}
response, status = api.handle_request(HTTPMethod.POST, "/books", new_book)
print(f"   Status: {status}")
print(f"   Message: {response.get('message')}")
print(f"   Location: {response.get('location')}")

print("\n5. PATCH /books/{id} (Partial update):")
update_data = {"status": "reserved"}
response, status = api.handle_request(HTTPMethod.PATCH, "/books/3", update_data)
print(f"   Status: {status}")
print(f"   Updated status: {response['book']['status']}")

print("\n6. POST /books/{id}/borrow (Action on resource):")
borrow_data = {"borrower": "John Doe", "due_date": "2024-12-25"}
response, status = api.handle_request(HTTPMethod.POST, "/books/1/borrow", borrow_data)
print(f"   Status: {status}")
print(f"   Message: {response.get('message')}")

print("\n7. DELETE /books/{id} (Delete resource):")
response, status = api.handle_request(HTTPMethod.DELETE, "/books/2")
print(f"   Status: {status}")
print(f"   Message: {response.get('message')}")

# ============================================================================
# PART 2: API VERSIONING STRATEGIES
# ============================================================================

print("\n" + "=" * 30)
print("API VERSIONING STRATEGIES")
print("=" * 30)

class APIVersion(Enum):
    """Supported API versions"""
    V1 = "v1"
    V2 = "v2"
    V3 = "v3"

class VersionedBookAPI:
    """
    Demonstrates different API versioning strategies:
    1. URL Path Versioning (/api/v1/books)
    2. Header Versioning (Accept: application/vnd.myapi.v1+json)
    3. Query Parameter Versioning (/api/books?version=1)
    4. Content Negotiation
    """
    
    def __init__(self):
        # Different implementations for different versions
        self.versions = {
            "v1": self._v1_handler,
            "v2": self._v2_handler,
            "v3": self._v3_handler
        }
    
    def handle_request(self, method: str, path: str, 
                      headers: Optional[Dict] = None,
                      query_params: Optional[Dict] = None) -> Dict:
        """
        Route request based on versioning strategy
        """
        # Strategy 1: Check URL path first
        path_version = self._extract_version_from_path(path)
        if path_version:
            return self._route_to_version(path_version, method, path, headers, query_params)
        
        # Strategy 2: Check Accept header
        header_version = self._extract_version_from_headers(headers)
        if header_version:
            return self._route_to_version(header_version, method, path, headers, query_params)
        
        # Strategy 3: Check query parameter
        query_version = self._extract_version_from_query(query_params)
        if query_version:
            return self._route_to_version(query_version, method, path, headers, query_params)
        
        # Default to latest version
        return self._route_to_version("v3", method, path, headers, query_params)
    
    def _extract_version_from_path(self, path: str) -> Optional[str]:
        """Extract version from URL path: /api/v1/books"""
        parts = path.strip("/").split("/")
        if len(parts) >= 2 and parts[0] == "api" and parts[1].startswith("v"):
            return parts[1]
        return None
    
    def _extract_version_from_headers(self, headers: Dict) -> Optional[str]:
        """Extract version from Accept header"""
        if not headers:
            return None
        
        accept_header = headers.get("Accept", "")
        # Check for versioned media type
        if "vnd.myapi.v1" in accept_header:
            return "v1"
        elif "vnd.myapi.v2" in accept_header:
            return "v2"
        elif "vnd.myapi.v3" in accept_header:
            return "v3"
        
        return None
    
    def _extract_version_from_query(self, query_params: Dict) -> Optional[str]:
        """Extract version from query parameter"""
        if not query_params:
            return None
        
        version = query_params.get("version")
        if version:
            return f"v{version}"
        return None
    
    def _route_to_version(self, version: str, method: str, path: str,
                         headers: Optional[Dict], query_params: Optional[Dict]) -> Dict:
        """Route to appropriate version handler"""
        handler = self.versions.get(version)
        if not handler:
            return {"error": f"Unsupported API version: {version}"}, 400
        
        # Remove version from path for version-specific handlers
        clean_path = path.replace(f"/api/{version}", "/api")
        
        return handler(method, clean_path, headers, query_params)
    
    def _v1_handler(self, method: str, path: str, headers: Dict, query_params: Dict) -> Dict:
        """Version 1 API - Simple response format"""
        return {
            "data": {"message": "API v1 response"},
            "version": "v1",
            "deprecated": True,
            "sunset_date": "2024-12-31"
        }, 200
    
    def _v2_handler(self, method: str, path: str, headers: Dict, query_params: Dict) -> Dict:
        """Version 2 API - Enhanced response format"""
        return {
            "success": True,
            "data": {"message": "API v2 response with improved format"},
            "metadata": {
                "version": "v2",
                "timestamp": datetime.now().isoformat(),
                "pagination": {"page": 1, "limit": 10}
            },
            "links": {
                "self": path,
                "docs": "https://api.example.com/docs/v2"
            }
        }, 200
    
    def _v3_handler(self, method: str, path: str, headers: Dict, query_params: Dict) -> Dict:
        """Version 3 API - Latest with breaking changes"""
        return {
            "result": {"message": "API v3 response with breaking changes"},
            "meta": {
                "api_version": "v3",
                "request_id": "req_123",
                "timestamp": datetime.now().isoformat()
            },
            "_embedded": {
                "related_resources": [
                    {"href": "/api/v3/authors", "rel": "authors"}
                ]
            }
        }, 200


print("\n--- API Versioning Strategies Demonstration ---")
versioned_api = VersionedBookAPI()

print("\n1. URL Path Versioning (/api/v1/books):")
response, status = versioned_api.handle_request("GET", "/api/v1/books")
print(f"   Version: {response.get('version', response.get('meta', {}).get('api_version'))}")

print("\n2. Header Versioning (Accept: application/vnd.myapi.v2+json):")
headers = {"Accept": "application/vnd.myapi.v2+json"}
response, status = versioned_api.handle_request("GET", "/api/books", headers=headers)
print(f"   Version: {response.get('metadata', {}).get('version')}")

print("\n3. Query Parameter Versioning (/api/books?version=3):")
query_params = {"version": "3"}
response, status = versioned_api.handle_request("GET", "/api/books", query_params=query_params)
print(f"   Version: {response.get('meta', {}).get('api_version')}")

print("\n4. Default to latest version (no version specified):")
response, status = versioned_api.handle_request("GET", "/api/books")
print(f"   Version: {response.get('meta', {}).get('api_version')}")

# ============================================================================
# PART 3: RATE LIMITING IMPLEMENTATION
# ============================================================================

print("\n" + "=" * 30)
print("RATE LIMITING STRATEGIES")
print("=" * 30)

import time
from collections import defaultdict
from threading import Lock

class RateLimiter:
    """
    Implements different rate limiting algorithms:
    1. Fixed Window
    2. Sliding Window
    3. Token Bucket
    4. Leaky Bucket
    """
    
    def __init__(self):
        # Storage for rate limit data
        self.fixed_window_counts = defaultdict(int)
        self.sliding_window_requests = defaultdict(list)
        self.token_buckets = defaultdict(lambda: {"tokens": 10, "last_refill": time.time()})
        self.locks = defaultdict(Lock)
        
        # Configuration
        self.config = {
            "fixed_window": {"limit": 5, "window_seconds": 60},
            "sliding_window": {"limit": 10, "window_seconds": 60},
            "token_bucket": {"capacity": 10, "refill_rate": 1},  # tokens per second
            "leaky_bucket": {"capacity": 10, "leak_rate": 0.1}   # requests per second
        }
    
    def fixed_window_limit(self, client_id: str) -> bool:
        """
        Fixed Window Algorithm
        - Simple but can allow bursts at window boundaries
        """
        window_size = self.config["fixed_window"]["window_seconds"]
        limit = self.config["fixed_window"]["limit"]
        
        current_window = int(time.time() / window_size)
        key = f"{client_id}:{current_window}"
        
        with self.locks[client_id]:
            if self.fixed_window_counts[key] >= limit:
                return False
            self.fixed_window_counts[key] += 1
        
        return True
    
    def sliding_window_limit(self, client_id: str) -> bool:
        """
        Sliding Window Algorithm
        - More accurate but more memory intensive
        """
        window_seconds = self.config["sliding_window"]["window_seconds"]
        limit = self.config["sliding_window"]["limit"]
        
        now = time.time()
        window_start = now - window_seconds
        
        with self.locks[client_id]:
            # Clean old requests
            requests = self.sliding_window_requests[client_id]
            requests = [req_time for req_time in requests if req_time > window_start]
            
            if len(requests) >= limit:
                return False
            
            # Add current request
            requests.append(now)
            self.sliding_window_requests[client_id] = requests
        
        return True
    
    def token_bucket_limit(self, client_id: str) -> bool:
        """
        Token Bucket Algorithm
        - Allows bursts up to bucket capacity
        """
        capacity = self.config["token_bucket"]["capacity"]
        refill_rate = self.config["token_bucket"]["refill_rate"]  # tokens per second
        
        with self.locks[client_id]:
            bucket = self.token_buckets[client_id]
            now = time.time()
            
            # Refill tokens based on elapsed time
            time_passed = now - bucket["last_refill"]
            tokens_to_add = time_passed * refill_rate
            
            bucket["tokens"] = min(capacity, bucket["tokens"] + tokens_to_add)
            bucket["last_refill"] = now
            
            if bucket["tokens"] < 1:
                return False
            
            # Consume one token
            bucket["tokens"] -= 1
        
        return True
    
    def leaky_bucket_limit(self, client_id: str) -> bool:
        """
        Leaky Bucket Algorithm
        - Smooths out request rate
        - Implemented as queue-based
        """
        capacity = self.config["leaky_bucket"]["capacity"]
        leak_rate = self.config["leaky_bucket"]["leak_rate"]  # requests per second
        
        # Simulated implementation (in production would use Redis or similar)
        if client_id not in self.token_buckets:  # Reusing dict for simplicity
            self.token_buckets[client_id] = {
                "queue": [],
                "last_leak": time.time()
            }
        
        with self.locks[client_id]:
            bucket = self.token_buckets[client_id]
            now = time.time()
            
            # Leak requests based on elapsed time
            time_passed = now - bucket["last_leak"]
            requests_to_remove = int(time_passed * leak_rate)
            
            if requests_to_remove > 0:
                bucket["queue"] = bucket["queue"][requests_to_remove:]
                bucket["last_leak"] = now
            
            if len(bucket["queue"]) >= capacity:
                return False
            
            # Add request to queue
            bucket["queue"].append(now)
        
        return True


class RateLimitedAPI:
    """API with integrated rate limiting"""
    
    def __init__(self):
        self.rate_limiter = RateLimiter()
        self.request_log = []
    
    def handle_request(self, client_ip: str, endpoint: str, 
                      algorithm: str = "token_bucket") -> Dict:
        """
        Process request with rate limiting
        """
        # Choose rate limiting algorithm
        if algorithm == "fixed_window":
            allowed = self.rate_limiter.fixed_window_limit(client_ip)
        elif algorithm == "sliding_window":
            allowed = self.rate_limiter.sliding_window_limit(client_ip)
        elif algorithm == "leaky_bucket":
            allowed = self.rate_limiter.leaky_bucket_limit(client_ip)
        else:  # token_bucket default
            allowed = self.rate_limiter.token_bucket_limit(client_ip)
        
        if not allowed:
            return {
                "error": "Too Many Requests",
                "message": "Rate limit exceeded",
                "retry_after": 60
            }, 429
        
        # Process successful request
        self.request_log.append({
            "client_ip": client_ip,
            "endpoint": endpoint,
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "message": "Request processed successfully",
            "remaining_requests": "Check X-RateLimit headers",
            "endpoint": endpoint
        }, 200


print("\n--- Rate Limiting Demonstration ---")
rate_limited_api = RateLimitedAPI()

# Simulate multiple requests from same client
print("\nSimulating requests from client 192.168.1.100:")
for i in range(15):
    response, status = rate_limited_api.handle_request(
        "192.168.1.100", 
        "/api/books",
        algorithm="token_bucket"
    )
    
    if status == 429:
        print(f"  Request {i+1}: RATE LIMITED - {response['message']}")
        break
    else:
        print(f"  Request {i+1}: Allowed")

print("\nTesting different algorithms:")
algorithms = ["fixed_window", "sliding_window", "token_bucket", "leaky_bucket"]

for algo in algorithms:
    print(f"\n  Algorithm: {algo}")
    rate_limited_api = RateLimitedAPI()  # Fresh instance for each test
    
    success_count = 0
    for i in range(12):
        response, status = rate_limited_api.handle_request(
            "10.0.0.1",
            "/api/books",
            algorithm=algo
        )
        if status != 429:
            success_count += 1
    
    print(f"    Successful requests in burst: {success_count}/12")

# ============================================================================
# PART 4: CACHING HEADERS AND STRATEGIES
# ============================================================================

print("\n" + "=" * 30)
print("CACHING HEADERS & STRATEGIES")
print("=" * 30)

class CachingStrategy:
    """
    Demonstrates HTTP caching strategies:
    1. Cache-Control headers
    2. ETag for validation
    3. Last-Modified headers
    4. CDN caching strategies
    """
    
    def __init__(self):
        self.resource_cache = {}
        self.etags = {}
        self.last_modified = {}
    
    def get_resource_with_caching(self, resource_id: str, 
                                 if_none_match: Optional[str] = None,
                                 if_modified_since: Optional[str] = None) -> Dict:
        """
        Returns resource with appropriate caching headers
        """
        # Get resource data
        resource = self._get_resource_data(resource_id)
        
        # Generate ETag (simplified)
        current_etag = self._generate_etag(resource)
        self.etags[resource_id] = current_etag
        
        # Generate Last-Modified
        current_last_modified = self._get_last_modified(resource_id)
        
        # Check conditional requests
        if if_none_match and if_none_match == current_etag:
            return {
                "status_code": 304,  # Not Modified
                "headers": {
                    "ETag": current_etag,
                    "Cache-Control": "public, max-age=3600"
                },
                "body": None
            }
        
        if if_modified_since and if_modified_since >= current_last_modified:
            return {
                "status_code": 304,
                "headers": {
                    "Last-Modified": current_last_modified,
                    "Cache-Control": "public, max-age=3600"
                },
                "body": None
            }
        
        # Determine cache strategy based on resource type
        cache_headers = self._get_cache_headers(resource_id, resource)
        
        return {
            "status_code": 200,
            "headers": {
                **cache_headers,
                "ETag": current_etag,
                "Last-Modified": current_last_modified,
                "Content-Type": "application/json"
            },
            "body": resource
        }
    
    def _get_resource_data(self, resource_id: str) -> Dict:
        """Retrieve resource data"""
        if resource_id not in self.resource_cache:
            # Simulate database fetch
            self.resource_cache[resource_id] = {
                "id": resource_id,
                "name": f"Resource {resource_id}",
                "data": {"value": "example data"},
                "updated_at": datetime.now().isoformat()
            }
        
        return self.resource_cache[resource_id]
    
    def _generate_etag(self, resource: Dict) -> str:
        """Generate ETag from resource content"""
        import hashlib
        content = str(resource).encode()
        return hashlib.md5(content).hexdigest()
    
    def _get_last_modified(self, resource_id: str) -> str:
        """Get Last-Modified timestamp"""
        if resource_id not in self.last_modified:
            self.last_modified[resource_id] = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
        return self.last_modified[resource_id]
    
    def _get_cache_headers(self, resource_id: str, resource: Dict) -> Dict:
        """
        Return appropriate Cache-Control headers based on resource type
        """
        # Static resources (JS, CSS, images)
        if resource_id.startswith("static_"):
            return {
                "Cache-Control": "public, max-age=31536000, immutable",  # 1 year
                "CDN-Cache-Control": "public, max-age=31536000"
            }
        
        # User-specific data
        elif resource_id.startswith("user_"):
            return {
                "Cache-Control": "private, max-age=60, stale-while-revalidate=30",
                "Vary": "Authorization"
            }
        
        # Public API data
        elif resource_id.startswith("api_"):
            return {
                "Cache-Control": "public, max-age=300, s-maxage=600",  # CDN caches longer
                "Vary": "Accept-Encoding",
                "CDN-Cache-Control": "public, max-age=600"
            }
        
        # Dynamic content (default)
        else:
            return {
                "Cache-Control": "no-cache",  # Always validate
                "Pragma": "no-cache"
            }
    
    def update_resource(self, resource_id: str, new_data: Dict) -> Dict:
        """
        Update resource and invalidate cache
        """
        # Update resource
        self.resource_cache[resource_id] = {
            **self.resource_cache.get(resource_id, {}),
            **new_data,
            "updated_at": datetime.now().isoformat()
        }
        
        # Invalidate cache
        self.last_modified[resource_id] = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
        
        # Return headers for cache invalidation
        return {
            "status_code": 200,
            "headers": {
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
                "Clear-Site-Data": "\"cache\"",  # Optional: clear browser cache
            },
            "body": {"message": "Resource updated, cache invalidated"}
        }


print("\n--- Caching Strategies Demonstration ---")
caching = CachingStrategy()

print("\n1. First request for static resource:")
response = caching.get_resource_with_caching("static_logo")
print(f"   Status: {response['status_code']}")
print(f"   Cache-Control: {response['headers'].get('Cache-Control')}")
print(f"   ETag: {response['headers'].get('ETag')[:20]}...")

print("\n2. Conditional request with matching ETag (should return 304):")
etag = response['headers']['ETag']
response = caching.get_resource_with_caching("static_logo", if_none_match=etag)
print(f"   Status: {response['status_code']} (Not Modified)")

print("\n3. Request for user-specific data:")
response = caching.get_resource_with_caching("user_profile_123")
print(f"   Status: {response['status_code']}")
print(f"   Cache-Control: {response['headers'].get('Cache-Control')}")
print(f"   Vary header: {response['headers'].get('Vary')}")

print("\n4. Request for public API data:")
response = caching.get_resource_with_caching("api_books_list")
print(f"   Status: {response['status_code']}")
print(f"   Cache-Control: {response['headers'].get('Cache-Control')}")
print(f"   CDN-Cache-Control: {response['headers'].get('CDN-Cache-Control')}")

print("\n5. Update resource (invalidates cache):")
response = caching.update_resource("api_books_list", {"data": "updated"})
print(f"   Status: {response['status_code']}")
print(f"   Cache invalidation headers: {response['headers']}")

# ============================================================================
# PART 5: COMPREHENSIVE API GATEWAY EXAMPLE
# ============================================================================

print("\n" + "=" * 70)
print("COMPREHENSIVE API GATEWAY IMPLEMENTATION")
print("=" * 70)

class APIGateway:
    """
    Complete API Gateway implementing:
    1. RESTful routing
    2. Versioning
    3. Rate limiting
    4. Caching
    5. Authentication
    6. Logging
    """
    
    def __init__(self):
        self.rate_limiter = RateLimiter()
        self.caching = CachingStrategy()
        self.request_count = 0
        
        # API keys for demonstration
        self.api_keys = {
            "user_abc123": {"tier": "free", "rate_limit": 100},
            "user_premium": {"tier": "premium", "rate_limit": 1000},
            "admin_key": {"tier": "admin", "rate_limit": 10000}
        }
    
    def handle_incoming_request(self, request: Dict) -> Dict:
        """
        Process incoming API request through gateway
        """
        self.request_count += 1
        request_id = f"req_{self.request_count}"
        
        # Extract request details
        method = request.get("method", "GET")
        path = request.get("path", "/")
        headers = request.get("headers", {})
        query_params = request.get("query_params", {})
        api_key = headers.get("X-API-Key")
        
        print(f"\n[{request_id}] {method} {path}")
        
        # 1. Authentication
        auth_result = self._authenticate(api_key)
        if not auth_result["authenticated"]:
            return self._create_error_response(401, "Invalid API key")
        
        client_tier = auth_result["tier"]
        client_id = auth_result["client_id"]
        
        # 2. Rate Limiting
        if not self.rate_limiter.token_bucket_limit(client_id):
            return self._create_error_response(
                429, 
                "Rate limit exceeded",
                headers={"Retry-After": "60", "X-RateLimit-Tier": client_tier}
            )
        
        # 3. Path-based routing
        route_result = self._route_request(method, path, headers, query_params)
        
        # 4. Add gateway headers
        response_headers = {
            **route_result.get("headers", {}),
            "X-Request-ID": request_id,
            "X-API-Version": "1.0",
            "X-RateLimit-Tier": client_tier,
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Expose-Headers": "X-RateLimit-Remaining, X-Request-ID"
        }
        
        return {
            "status_code": route_result.get("status_code", 200),
            "headers": response_headers,
            "body": route_result.get("body", {}),
            "request_id": request_id
        }
    
    def _authenticate(self, api_key: Optional[str]) -> Dict:
        """Validate API key and get client tier"""
        if not api_key:
            return {"authenticated": False, "error": "Missing API key"}
        
        client_info = self.api_keys.get(api_key)
        if not client_info:
            return {"authenticated": False, "error": "Invalid API key"}
        
        return {
            "authenticated": True,
            "tier": client_info["tier"],
            "rate_limit": client_info["rate_limit"],
            "client_id": api_key[:8]  # Simplified client ID
        }
    
    def _route_request(self, method: str, path: str, headers: Dict, 
                      query_params: Dict) -> Dict:
        """Route to appropriate handler"""
        # Extract version from path
        path_parts = path.strip("/").split("/")
        
        if len(path_parts) >= 2 and path_parts[0] == "api":
            version = path_parts[1]
            
            # Route to version-specific handler
            if version == "v1":
                return self._handle_v1_request(method, "/".join(path_parts[2:]), 
                                              headers, query_params)
            elif version == "v2":
                return self._handle_v2_request(method, "/".join(path_parts[2:]), 
                                              headers, query_params)
        
        # Default to latest version or 404
        return {
            "status_code": 404,
            "body": {"error": "Not Found", "message": f"No handler for {path}"}
        }
    
    def _handle_v1_request(self, method: str, endpoint: str, 
                          headers: Dict, query_params: Dict) -> Dict:
        """Handle v1 API requests"""
        # Check cache first for GET requests
        if method == "GET":
            cache_key = f"v1_{endpoint}_{str(query_params)}"
            cached = self.caching.get_resource_with_caching(
                cache_key,
                headers.get("If-None-Match"),
                headers.get("If-Modified-Since")
            )
            
            if cached["status_code"] == 304:
                return cached
        
        # Process request
        if endpoint == "books":
            return self._get_books_v1(query_params)
        elif endpoint.startswith("books/"):
            book_id = endpoint.split("/")[1]
            return self._get_book_v1(book_id)
        
        return {
            "status_code": 404,
            "body": {"error": "Endpoint not found in v1"}
        }
    
    def _handle_v2_request(self, method: str, endpoint: str,
                          headers: Dict, query_params: Dict) -> Dict:
        """Handle v2 API requests"""
        if endpoint == "library/books":
            return self._get_books_v2(query_params)
        
        return {
            "status_code": 501,
            "body": {"error": "Not Implemented", "message": "v2 API under development"}
        }
    
    def _get_books_v1(self, query_params: Dict) -> Dict:
        """v1 books endpoint"""
        books = [
            {"id": 1, "title": "Book 1", "author": "Author 1"},
            {"id": 2, "title": "Book 2", "author": "Author 2"},
            {"id": 3, "title": "Book 3", "author": "Author 3"}
        ]
        
        # Filter based on query params
        if "author" in query_params:
            author_filter = query_params["author"].lower()
            books = [b for b in books if author_filter in b["author"].lower()]
        
        return {
            "status_code": 200,
            "headers": {
                "Cache-Control": "public, max-age=300",
                "X-Total-Count": str(len(books))
            },
            "body": {
                "books": books,
                "count": len(books),
                "version": "v1"
            }
        }
    
    def _get_book_v1(self, book_id: str) -> Dict:
        """v1 book detail endpoint"""
        return {
            "status_code": 200,
            "headers": {
                "Cache-Control": "public, max-age=600"
            },
            "body": {
                "id": book_id,
                "title": f"Book {book_id}",
                "author": f"Author {book_id}",
                "description": "Sample book description",
                "version": "v1"
            }
        }
    
    def _get_books_v2(self, query_params: Dict) -> Dict:
        """v2 books endpoint with enhanced features"""
        return {
            "status_code": 200,
            "headers": {
                "Cache-Control": "public, max-age=300, s-maxage=600"
            },
            "body": {
                "data": [
                    {"id": 1, "attributes": {"title": "Book 1", "author": "Author 1"}},
                    {"id": 2, "attributes": {"title": "Book 2", "author": "Author 2"}}
                ],
                "meta": {
                    "version": "v2",
                    "pagination": {"page": 1, "page_size": 20, "total": 2}
                },
                "links": {
                    "self": "/api/v2/library/books",
                    "next": None,
                    "prev": None
                }
            }
        }
    
    def _create_error_response(self, status_code: int, message: str, 
                              headers: Optional[Dict] = None) -> Dict:
        """Create standardized error response"""
        error_codes = {
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            429: "Too Many Requests",
            500: "Internal Server Error"
        }
        
        return {
            "status_code": status_code,
            "headers": headers or {},
            "body": {
                "error": error_codes.get(status_code, "Error"),
                "message": message,
                "timestamp": datetime.now().isoformat()
            }
        }


print("\n--- API Gateway in Action ---")
gateway = APIGateway()

# Test different scenarios
test_requests = [
    {
        "method": "GET",
        "path": "/api/v1/books",
        "headers": {"X-API-Key": "user_abc123"},
        "query_params": {"author": "1"}
    },
    {
        "method": "GET",
        "path": "/api/v1/books/2",
        "headers": {"X-API-Key": "user_premium", "If-None-Match": "dummy-etag"},
        "query_params": {}
    },
    {
        "method": "GET",
        "path": "/api/v2/library/books",
        "headers": {"X-API-Key": "admin_key"},
        "query_params": {}
    },
    {
        "method": "GET",
        "path": "/api/v1/books",
        "headers": {},  # No API key
        "query_params": {}
    }
]

for i, req in enumerate(test_requests, 1):
    print(f"\nRequest {i}:")
    response = gateway.handle_incoming_request(req)
    print(f"  Status: {response['status_code']}")
    print(f"  Request ID: {response['request_id']}")
    if response['status_code'] == 200:
        print(f"  Body keys: {list(response['body'].keys())}")
    else:
        print(f"  Error: {response['body'].get('message')}")

# ============================================================================
# SUMMARY & BEST PRACTICES
# ============================================================================

print("\n" + "=" * 70)
print("API DESIGN BEST PRACTICES SUMMARY")
print("=" * 70)

print("""
RESTFUL PRINCIPLES:
-------------------
1. Resource-Based URLs: Use nouns, not verbs (/books not /getBooks)
2. Proper HTTP Methods: GET, POST, PUT, PATCH, DELETE
3. Stateless: Each request contains all necessary information
4. Representations: Support multiple formats (JSON, XML)
5. HATEOAS: Include links to related resources
6. Status Codes: Use appropriate HTTP status codes
   - 200 OK, 201 Created, 204 No Content
   - 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found
   - 429 Too Many Requests, 500 Internal Server Error

API VERSIONING STRATEGIES:
--------------------------
1. URL Path Versioning: /api/v1/resource (Most common, cache-friendly)
2. Header Versioning: Accept: application/vnd.api.v1+json (Clean URLs)
3. Query Parameter: /api/resource?version=1 (Simple but less RESTful)
4. Media Type Versioning: Custom media types
   
Recommendation: Use URL path for public APIs, headers for internal APIs

RATE LIMITING:
--------------
1. Fixed Window: Simple but allows boundary bursts
2. Sliding Window: More accurate, prevents bursts
3. Token Bucket: Allows bursts up to capacity
4. Leaky Bucket: Smooths request rate
   
Include headers: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset

CACHING STRATEGIES:
-------------------
1. Cache-Control Headers:
   - public/private: Who can cache
   - max-age: How long to cache
   - s-maxage: CDN-specific cache duration
   - no-cache: Always validate with server
   - no-store: Never cache
   
2. Validation Headers:
   - ETag: Content-based fingerprint
   - Last-Modified: Timestamp-based
   
3. Vary Header: Indicates what request headers affect cache

4. CDN Caching:
   - Use CDN-Cache-Control for CDN-specific rules
   - Purge API for cache invalidation

SECURITY HEADERS:
-----------------
1. CORS: Access-Control-Allow-Origin
2. Security: X-Content-Type-Options, X-Frame-Options
3. Rate Limiting: X-RateLimit-* headers
4. Request Tracking: X-Request-ID

MONITORING & ANALYTICS:
-----------------------
1. Log all requests with request IDs
2. Track rate limit hits
3. Monitor cache hit ratios
4. API usage analytics per client
5. Error rate tracking

DOCUMENTATION:
--------------
1. OpenAPI/Swagger specification
2. Interactive API explorer
3. Version changelog
4. Rate limit documentation
5. Authentication guide
""")

print("\n" + "=" * 70)
print("API DESIGN DEMONSTRATION COMPLETE")
print("=" * 70)