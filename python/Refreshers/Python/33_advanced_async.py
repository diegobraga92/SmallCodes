"""
ADVANCED ASYNCIO PATTERNS
==========================
Beyond basic async/await: advanced patterns, performance optimization,
and production-ready async code.
"""

print("=" * 80)
print("ADVANCED ASYNCIO PATTERNS")
print("=" * 80)

import asyncio
import aiohttp
import aiofiles
from typing import List, Dict, Any, Coroutine, Optional
from datetime import datetime
import time

# ============================================================================
# 1. CONCURRENT TASK EXECUTION
# ============================================================================

"""
CONCURRENT PATTERNS:
- asyncio.gather: Run multiple coroutines concurrently
- asyncio.wait: More control over completion
- asyncio.as_completed: Process as they complete
- TaskGroup (Python 3.11+): Structured concurrency
"""

async def fetch_data(url: str, delay: float) -> Dict[str, Any]:
    """Simulate async API call"""
    await asyncio.sleep(delay)
    return {"url": url, "data": f"Data from {url}"}

async def demo_gather():
    """
    asyncio.gather: Run tasks concurrently, wait for all
    Returns results in order
    """
    print("\n=== asyncio.gather ===")
    
    # Run multiple tasks concurrently
    results = await asyncio.gather(
        fetch_data("api1.com", 0.5),
        fetch_data("api2.com", 0.3),
        fetch_data("api3.com", 0.4)
    )
    
    for result in results:
        print(f"Result: {result}")
    
    # With return_exceptions=True, exceptions don't stop other tasks
    results = await asyncio.gather(
        fetch_data("api1.com", 0.1),
        asyncio.sleep(0),  # This will work
        # async_function_that_fails(),  # This would raise exception
        return_exceptions=True  # Return exception objects instead of raising
    )
    print(f"With exceptions: {results}")

async def demo_wait():
    """
    asyncio.wait: More control over task completion
    """
    print("\n=== asyncio.wait ===")
    
    # Create tasks
    tasks = {
        asyncio.create_task(fetch_data(f"api{i}.com", i * 0.1))
        for i in range(1, 4)
    }
    
    # Wait for all tasks
    done, pending = await asyncio.wait(tasks)
    
    print(f"Done: {len(done)}, Pending: {len(pending)}")
    
    for task in done:
        result = task.result()
        print(f"Result: {result}")
    
    # Wait for first task to complete
    done, pending = await asyncio.wait(
        tasks,
        return_when=asyncio.FIRST_COMPLETED
    )
    
    # Cancel remaining tasks
    for task in pending:
        task.cancel()

async def demo_as_completed():
    """
    asyncio.as_completed: Process results as they complete
    Good for showing progress
    """
    print("\n=== asyncio.as_completed ===")
    
    tasks = [
        fetch_data(f"api{i}.com", (5 - i) * 0.1)  # Reversed delays
        for i in range(1, 6)
    ]
    
    # Process results as they complete (not in order!)
    for coro in asyncio.as_completed(tasks):
        result = await coro
        print(f"Completed: {result}")


# ============================================================================
# 2. TIMEOUTS AND CANCELLATION
# ============================================================================

async def slow_operation(duration: float) -> str:
    """Simulate slow operation"""
    await asyncio.sleep(duration)
    return f"Completed after {duration}s"

async def demo_timeouts():
    """
    Handling timeouts with asyncio
    """
    print("\n=== Timeouts ===")
    
    # timeout with wait_for
    try:
        result = await asyncio.wait_for(
            slow_operation(2.0),
            timeout=1.0
        )
        print(f"Result: {result}")
    except asyncio.TimeoutError:
        print("Operation timed out")
    
    # timeout with wait
    tasks = {asyncio.create_task(slow_operation(i)) for i in range(1, 4)}
    
    done, pending = await asyncio.wait(tasks, timeout=1.5)
    
    print(f"Completed: {len(done)}, Timed out: {len(pending)}")
    
    # Cancel timed-out tasks
    for task in pending:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            print(f"Task cancelled")

async def demo_cancellation():
    """
    Graceful task cancellation
    """
    print("\n=== Cancellation ===")
    
    async def cancellable_task():
        try:
            print("Task started")
            await asyncio.sleep(5)
            print("Task completed")
        except asyncio.CancelledError:
            print("Task cancelled, cleaning up...")
            # Cleanup code here
            raise  # Re-raise to propagate cancellation
    
    task = asyncio.create_task(cancellable_task())
    
    await asyncio.sleep(1)
    task.cancel()
    
    try:
        await task
    except asyncio.CancelledError:
        print("Task cancellation confirmed")


# ============================================================================
# 3. ASYNC CONTEXT MANAGERS AND GENERATORS
# ============================================================================

class AsyncDatabaseConnection:
    """
    Async context manager for database connection
    """
    
    async def __aenter__(self):
        print("Opening database connection...")
        await asyncio.sleep(0.1)  # Simulate connection
        self.connected = True
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Closing database connection...")
        await asyncio.sleep(0.1)  # Simulate cleanup
        self.connected = False
    
    async def query(self, sql: str):
        if not self.connected:
            raise RuntimeError("Not connected")
        await asyncio.sleep(0.1)
        return f"Result for: {sql}"

async def demo_async_context_manager():
    """Using async context managers"""
    print("\n=== Async Context Manager ===")
    
    async with AsyncDatabaseConnection() as db:
        result = await db.query("SELECT * FROM users")
        print(result)
    
    # Connection automatically closed

async def async_generator_example():
    """
    Async generator: produces values asynchronously
    """
    for i in range(5):
        await asyncio.sleep(0.1)
        yield i

async def demo_async_generator():
    """Using async generators"""
    print("\n=== Async Generator ===")
    
    async for value in async_generator_example():
        print(f"Received: {value}")


# ============================================================================
# 4. ASYNC ITERATION AND COMPREHENSIONS
# ============================================================================

class AsyncIterator:
    """
    Async iterator: fetches data in chunks
    """
    
    def __init__(self, max_items: int):
        self.max_items = max_items
        self.current = 0
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.current >= self.max_items:
            raise StopAsyncIteration
        
        await asyncio.sleep(0.1)
        self.current += 1
        return self.current

async def demo_async_iteration():
    """Async iteration patterns"""
    print("\n=== Async Iteration ===")
    
    # Async for loop
    async for item in AsyncIterator(5):
        print(f"Item: {item}")
    
    # Async comprehension
    results = [item async for item in AsyncIterator(3)]
    print(f"Comprehension results: {results}")
    
    # Async generator expression
    squared = (item ** 2 async for item in AsyncIterator(3))
    async for value in squared:
        print(f"Squared: {value}")


# ============================================================================
# 5. SYNCHRONIZATION PRIMITIVES
# ============================================================================

async def demo_lock():
    """
    asyncio.Lock: Mutual exclusion
    """
    print("\n=== Lock ===")
    
    lock = asyncio.Lock()
    shared_resource = 0
    
    async def critical_section(worker_id: int):
        nonlocal shared_resource
        
        async with lock:
            print(f"Worker {worker_id} acquired lock")
            current = shared_resource
            await asyncio.sleep(0.1)  # Simulate work
            shared_resource = current + 1
            print(f"Worker {worker_id} released lock")
    
    # Run multiple workers concurrently
    await asyncio.gather(*[
        critical_section(i) for i in range(3)
    ])
    
    print(f"Final value: {shared_resource}")

async def demo_semaphore():
    """
    asyncio.Semaphore: Limit concurrent access
    """
    print("\n=== Semaphore ===")
    
    # Allow max 2 concurrent operations
    semaphore = asyncio.Semaphore(2)
    
    async def limited_operation(worker_id: int):
        async with semaphore:
            print(f"Worker {worker_id} started (semaphore acquired)")
            await asyncio.sleep(1)
            print(f"Worker {worker_id} finished")
    
    # Try to run 5 workers (only 2 at a time)
    await asyncio.gather(*[
        limited_operation(i) for i in range(5)
    ])

async def demo_event():
    """
    asyncio.Event: Wait for event signal
    """
    print("\n=== Event ===")
    
    event = asyncio.Event()
    
    async def waiter(worker_id: int):
        print(f"Worker {worker_id} waiting for event...")
        await event.wait()
        print(f"Worker {worker_id} received event!")
    
    async def setter():
        await asyncio.sleep(1)
        print("Setting event...")
        event.set()
    
    await asyncio.gather(
        waiter(1),
        waiter(2),
        waiter(3),
        setter()
    )


# ============================================================================
# 6. ASYNC QUEUES
# ============================================================================

async def demo_queue():
    """
    asyncio.Queue: Producer-consumer pattern
    """
    print("\n=== Queue ===")
    
    queue = asyncio.Queue(maxsize=3)
    
    async def producer(items: List[int]):
        for item in items:
            await queue.put(item)
            print(f"Produced: {item} (queue size: {queue.qsize()})")
            await asyncio.sleep(0.1)
        
        # Signal completion
        await queue.put(None)
    
    async def consumer(consumer_id: int):
        while True:
            item = await queue.get()
            
            if item is None:
                # Put None back for other consumers
                await queue.put(None)
                break
            
            print(f"Consumer {consumer_id} processing: {item}")
            await asyncio.sleep(0.2)
            queue.task_done()
    
    # Start producer and consumers
    await asyncio.gather(
        producer(list(range(1, 6))),
        consumer(1),
        consumer(2)
    )
    
    await queue.join()  # Wait for all tasks to be processed


# ============================================================================
# 7. ASYNC HTTP WITH AIOHTTP
# ============================================================================

async def demo_aiohttp():
    """
    Concurrent HTTP requests with aiohttp
    """
    print("\n=== Async HTTP ===")
    
    urls = [
        "https://api.github.com/repos/python/cpython",
        "https://api.github.com/repos/pallets/flask",
        "https://api.github.com/repos/django/django"
    ]
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.create_task(fetch_url(session, url))
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        
        for result in results:
            print(f"Repo: {result.get('name')}, Stars: {result.get('stargazers_count')}")

async def fetch_url(session: aiohttp.ClientSession, url: str) -> Dict:
    """Fetch URL with aiohttp"""
    async with session.get(url) as response:
        return await response.json()


# ============================================================================
# 8. ASYNC FILE I/O
# ============================================================================

async def demo_async_files():
    """
    Async file operations with aiofiles
    """
    print("\n=== Async File I/O ===")
    
    # Async write
    async with aiofiles.open('async_test.txt', 'w') as f:
        await f.write('Line 1\n')
        await f.write('Line 2\n')
        await f.write('Line 3\n')
    
    # Async read
    async with aiofiles.open('async_test.txt', 'r') as f:
        async for line in f:
            print(f"Read: {line.strip()}")
    
    # Clean up
    import os
    os.remove('async_test.txt')


# ============================================================================
# 9. ASYNC RETRY PATTERN
# ============================================================================

async def retry_async(
    coro: Coroutine,
    max_retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0
):
    """
    Retry async operation with exponential backoff
    """
    for attempt in range(max_retries):
        try:
            return await coro
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            
            wait_time = delay * (backoff ** attempt)
            print(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait_time}s...")
            await asyncio.sleep(wait_time)

async def demo_retry():
    """Demonstrate retry pattern"""
    print("\n=== Retry Pattern ===")
    
    attempts = 0
    
    async def flaky_operation():
        nonlocal attempts
        attempts += 1
        
        if attempts < 3:
            raise ValueError(f"Attempt {attempts} failed")
        
        return "Success!"
    
    try:
        result = await retry_async(flaky_operation())
        print(f"Result: {result}")
    except Exception as e:
        print(f"Final failure: {e}")


# ============================================================================
# 10. ASYNC RATE LIMITING
# ============================================================================

class AsyncRateLimiter:
    """
    Rate limiter for async operations
    """
    
    def __init__(self, rate: int, per: float):
        """
        rate: number of operations
        per: time period in seconds
        """
        self.rate = rate
        self.per = per
        self.allowance = rate
        self.last_check = time.time()
        self.lock = asyncio.Lock()
    
    async def acquire(self):
        """Wait until operation is allowed"""
        async with self.lock:
            current = time.time()
            time_passed = current - self.last_check
            self.last_check = current
            
            # Replenish allowance
            self.allowance += time_passed * (self.rate / self.per)
            
            if self.allowance > self.rate:
                self.allowance = self.rate
            
            # Wait if needed
            if self.allowance < 1.0:
                sleep_time = (1.0 - self.allowance) * (self.per / self.rate)
                await asyncio.sleep(sleep_time)
                self.allowance = 0.0
            else:
                self.allowance -= 1.0

async def demo_rate_limiter():
    """Demonstrate rate limiting"""
    print("\n=== Rate Limiter ===")
    
    # Allow 2 operations per second
    limiter = AsyncRateLimiter(rate=2, per=1.0)
    
    async def rate_limited_operation(op_id: int):
        await limiter.acquire()
        print(f"Operation {op_id} at {datetime.now().strftime('%H:%M:%S.%f')}")
    
    # Try 6 operations (should be rate-limited)
    await asyncio.gather(*[
        rate_limited_operation(i) for i in range(6)
    ])


# ============================================================================
# 11. BEST PRACTICES
# ============================================================================

"""
ASYNC BEST PRACTICES:

1. DON'T BLOCK THE EVENT LOOP:
   ✗ time.sleep() - blocks everything
   ✓ await asyncio.sleep() - async
   ✗ requests.get() - blocking
   ✓ aiohttp - async
   ✗ open(file).read() - blocking
   ✓ aiofiles - async

2. USE CONTEXT MANAGERS:
   - Always use async with for resources
   - Proper cleanup guaranteed

3. HANDLE CANCELLATION:
   - Catch asyncio.CancelledError
   - Clean up resources
   - Re-raise to propagate

4. SET TIMEOUTS:
   - Use asyncio.wait_for
   - Prevent hanging operations
   - Handle TimeoutError

5. LIMIT CONCURRENCY:
   - Use asyncio.Semaphore
   - Prevent overwhelming resources
   - Respect rate limits

6. ERROR HANDLING:
   - Use return_exceptions in gather
   - Handle exceptions per task
   - Don't let one failure stop everything

7. MONITORING:
   - Track active tasks
   - Monitor event loop lag
   - Profile async performance

8. TESTING:
   - Use pytest-asyncio
   - Mock async functions
   - Test cancellation
   - Test timeouts
"""

# ============================================================================
# MAIN DEMONSTRATION
# ============================================================================

async def main():
    """Run all demonstrations"""
    
    await demo_gather()
    # await demo_wait()  # Commented to avoid conflicts
    await demo_as_completed()
    await demo_timeouts()
    await demo_cancellation()
    await demo_async_context_manager()
    await demo_async_generator()
    await demo_async_iteration()
    await demo_lock()
    await demo_semaphore()
    await demo_event()
    await demo_queue()
    # await demo_aiohttp()  # Requires internet
    # await demo_async_files()  # File operations
    await demo_retry()
    await demo_rate_limiter()

if __name__ == "__main__":
    asyncio.run(main())

print("\n=== Advanced Async Complete ===")

"""
KEY TAKEAWAYS:

1. asyncio.gather - run multiple tasks, wait for all
2. asyncio.wait - more control over task completion
3. asyncio.as_completed - process as tasks finish
4. Use timeouts to prevent hanging
5. Handle cancellation gracefully
6. Async context managers for resources
7. Synchronization: Lock, Semaphore, Event
8. asyncio.Queue for producer-consumer
9. aiohttp for concurrent HTTP
10. Rate limiting and retry patterns
11. Never block the event loop
12. Always set timeouts for external operations
"""
