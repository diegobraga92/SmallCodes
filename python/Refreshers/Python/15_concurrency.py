"""
COMPREHENSIVE GUIDE TO PYTHON CONCURRENCY & PARALLELISM

This script demonstrates and explains concurrency and parallelism concepts in Python,
including GIL, threads vs processes, async/await, and common concurrency problems.
"""

import time
import threading
import multiprocessing
import asyncio
import concurrent.futures
import random
from queue import Queue
from typing import List, Dict, Any
import sys
import os

# ============================================================================
# PART 1: GIL (GLOBAL INTERPRETER LOCK) - THE HEART OF PYTHON CONCURRENCY
# ============================================================================

def gil_explanation():
    """
    GIL (GLOBAL INTERPRETER LOCK):
    ------------------------------
    
    WHAT IT IS:
    - A mutex (mutual exclusion lock) that allows only one thread to execute 
      Python bytecode at a time in a single process
    - Protects Python's internal data structures from concurrent access
    - Ensures thread-safe memory management
    
    WHAT IT ISN'T:
    - It is NOT a limitation of Python itself, but of CPython (reference implementation)
    - It does NOT prevent multi-threading entirely
    - It does NOT affect I/O-bound operations as much as CPU-bound operations
    
    KEY TAKEAWAYS:
    - GIL prevents true parallelism in threads for CPU-bound tasks
    - Only one thread executes Python bytecode at a time per process
    - Threads can still be useful for I/O-bound operations
    """
    
    print("\n" + "="*60)
    print("GIL (GLOBAL INTERPRETER LOCK) EXPLANATION")
    print("="*60)
    
    print("""
    GIL Analogy:
    ------------
    Imagine a Python interpreter as a kitchen with:
    - One chef (CPU core) that can only use one recipe book at a time (GIL)
    - Multiple assistants (threads) waiting to use the recipe book
    - The chef can only read one recipe (execute one thread) at a time
    
    Why GIL Exists:
    ---------------
    1. Memory Management: Python uses reference counting for garbage collection
    2. C Extension Safety: Many C extensions are not thread-safe
    3. Simplicity: Makes CPython implementation simpler
    
    GIL Impact:
    -----------
    ✓ Threads CAN run concurrently for I/O operations (file, network, database)
    ✗ Threads CANNOT run in parallel for CPU-bound operations (math, processing)
    ✓ Multiple PROCESSES can run in parallel (each has its own GIL)
    
    CPython Implementations without GIL:
    ------------------------------------
    - Jython (JVM-based): No GIL
    - IronPython (.NET-based): No GIL
    - PyPy (with STM): Can disable GIL
    """)

# ============================================================================
# PART 2: THREADS VS PROCESSES - WHEN TO USE EACH
# ============================================================================

def demonstrate_threads_vs_processes():
    """
    THREADS VS PROCESSES:
    --------------------
    
    THREADS (threading module):
    - Share same memory space (shared state)
    - Lightweight (faster to create)
    - Limited by GIL for CPU-bound tasks
    - Good for I/O-bound operations
    
    PROCESSES (multiprocessing module):
    - Separate memory space (IPC needed)
    - Heavier (slower to create)
    - Bypass GIL (true parallelism)
    - Good for CPU-bound operations
    
    CPU-BOUND vs I/O-BOUND:
    ----------------------
    CPU-Bound: Computation intensive (math, processing)
    I/O-Bound: Waiting for input/output (network, disk, database)
    """
    
    print("\n" + "="*60)
    print("THREADS VS PROCESSES DEMONSTRATION")
    print("="*60)
    
    # CPU-bound task example
    def cpu_bound_task(n: int) -> float:
        """Simulate CPU-intensive work."""
        result = 0
        for i in range(n):
            result += i ** 2
        return result
    
    # I/O-bound task example  
    def io_bound_task(wait_time: float) -> float:
        """Simulate I/O wait (network/disk)."""
        time.sleep(wait_time)
        return wait_time
    
    # Sequential execution baseline
    print("1. SEQUENTIAL EXECUTION BASELINE:")
    
    start = time.time()
    
    # CPU-bound tasks
    results_cpu = []
    for _ in range(4):
        results_cpu.append(cpu_bound_task(10**6))
    
    cpu_time_seq = time.time() - start
    print(f"   CPU-bound tasks (sequential): {cpu_time_seq:.3f} seconds")
    
    # I/O-bound tasks
    start = time.time()
    results_io = []
    for _ in range(4):
        results_io.append(io_bound_task(0.5))
    
    io_time_seq = time.time() - start
    print(f"   I/O-bound tasks (sequential): {io_time_seq:.3f} seconds")
    
    # Threading demonstration
    print("\n2. THREADING (Shared Memory, GIL-limited):")
    
    # Threading for CPU-bound (ineffective due to GIL)
    print("   CPU-bound with threading (GIL limits parallelism):")
    start = time.time()
    
    threads = []
    cpu_results = []
    
    def cpu_thread_task():
        result = cpu_bound_task(10**6)
        cpu_results.append(result)
    
    for _ in range(4):
        t = threading.Thread(target=cpu_thread_task)
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    cpu_time_threads = time.time() - start
    print(f"   Time: {cpu_time_threads:.3f} seconds")
    print(f"   Speedup vs sequential: {cpu_time_seq/cpu_time_threads:.2f}x")
    
    # Threading for I/O-bound (effective)
    print("\n   I/O-bound with threading (GIL doesn't block I/O):")
    start = time.time()
    
    threads = []
    io_results = []
    
    def io_thread_task(wait_time):
        result = io_bound_task(wait_time)
        io_results.append(result)
    
    for i in range(4):
        t = threading.Thread(target=io_thread_task, args=(0.5,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    io_time_threads = time.time() - start
    print(f"   Time: {io_time_threads:.3f} seconds")
    print(f"   Speedup vs sequential: {io_time_seq/io_time_threads:.2f}x")
    print(f"   Ideal: ~{4/1:.1f}x (4 threads, each 0.5 seconds)")
    
    # Multiprocessing demonstration
    print("\n3. MULTIPROCESSING (Separate Memory, True Parallelism):")
    
    # Multiprocessing for CPU-bound (effective)
    print("   CPU-bound with multiprocessing (bypasses GIL):")
    start = time.time()
    
    processes = []
    manager = multiprocessing.Manager()
    cpu_results_mp = manager.list()
    
    def cpu_process_task(results_list):
        result = cpu_bound_task(10**6)
        results_list.append(result)
    
    for _ in range(4):
        p = multiprocessing.Process(target=cpu_process_task, args=(cpu_results_mp,))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    cpu_time_mp = time.time() - start
    print(f"   Time: {cpu_time_mp:.3f} seconds")
    print(f"   Speedup vs sequential: {cpu_time_seq/cpu_time_mp:.2f}x")
    print(f"   Speedup vs threading: {cpu_time_threads/cpu_time_mp:.2f}x")
    
    # Multiprocessing overhead demonstration
    print("\n   Multiprocessing overhead (process creation is expensive):")
    
    def quick_task():
        return 42
    
    # Measure overhead for small tasks
    start = time.time()
    processes = []
    for _ in range(100):
        p = multiprocessing.Process(target=quick_task)
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    mp_overhead_time = time.time() - start
    
    start = time.time()
    threads = []
    for _ in range(100):
        t = threading.Thread(target=quick_task)
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    thread_overhead_time = time.time() - start
    
    print(f"   Creating 100 processes: {mp_overhead_time:.3f} seconds")
    print(f"   Creating 100 threads: {thread_overhead_time:.3f} seconds")
    print(f"   Threads are {mp_overhead_time/thread_overhead_time:.1f}x faster to create")
    
    print("\n" + "-"*40)
    print("DECISION GUIDE:")
    print("-"*40)
    print("""
    USE THREADS WHEN:
    - Tasks are I/O-bound (network, disk, database)
    - Need shared memory/state
    - Many lightweight tasks
    - Quick task switching needed
    
    USE PROCESSES WHEN:
    - Tasks are CPU-bound (computation intensive)
    - Need true parallelism
    - Tasks are independent
    - Can tolerate IPC overhead
    
    AVOID THREADS FOR:
    - CPU-intensive computations
    - When you need linear speedup
    - When tasks don't involve waiting
    
    AVOID PROCESSES FOR:
    - Many small, quick tasks
    - When memory sharing is critical
    - When process creation overhead dominates
    """)

# ============================================================================
# PART 3: THREADING MODULE - BASIC THREAD OPERATIONS
# ============================================================================

def threading_module_demo():
    """
    threading MODULE:
    ----------------
    Basic thread operations and patterns.
    """
    
    print("\n" + "="*60)
    print("THREADING MODULE DEMONSTRATION")
    print("="*60)
    
    # 1. Basic Thread Creation
    print("\n1. BASIC THREAD CREATION:")
    
    def worker(name: str, delay: float):
        """Simple worker function."""
        print(f"   Worker {name} started")
        time.sleep(delay)
        print(f"   Worker {name} finished after {delay}s")
    
    # Create and start threads
    threads = []
    for i in range(3):
        t = threading.Thread(target=worker, args=(f"T{i}", 1 + i*0.5))
        threads.append(t)
        t.start()
        print(f"   Started thread {t.name}")
    
    # Wait for all threads to complete
    for t in threads:
        t.join()
    
    print("   All threads completed")
    
    # 2. Thread with Return Values
    print("\n2. THREADS WITH RETURN VALUES:")
    
    results = []
    results_lock = threading.Lock()
    
    def worker_with_return(id: int, results_list: list, lock: threading.Lock):
        """Worker that returns a value."""
        time.sleep(random.uniform(0.1, 0.5))
        result = id * 10
        
        with lock:  # Thread-safe list append
            results_list.append(result)
    
    threads = []
    for i in range(5):
        t = threading.Thread(
            target=worker_with_return,
            args=(i, results, results_lock)
        )
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print(f"   Results (unordered due to threads): {sorted(results)}")
    
    # 3. Daemon Threads
    print("\n3. DAEMON THREADS (Background Threads):")
    
    def background_worker():
        """Daemon thread that runs in background."""
        count = 0
        while True:
            print(f"   Daemon: Running... ({count})")
            count += 1
            time.sleep(1)
    
    # Create daemon thread
    daemon = threading.Thread(target=background_worker, daemon=True)
    daemon.start()
    
    print("   Daemon thread started (will terminate when main thread ends)")
    print("   Main thread working for 3 seconds...")
    time.sleep(3)
    print("   Main thread finished - daemon will be terminated automatically")
    
    # 4. Thread Synchronization - Locks
    print("\n4. THREAD SYNCHRONIZATION (LOCKS):")
    
    class BankAccount:
        """Simple bank account with thread-safe operations."""
        
        def __init__(self, initial_balance: float = 0):
            self.balance = initial_balance
            self.lock = threading.Lock()
        
        def deposit(self, amount: float):
            """Thread-safe deposit."""
            with self.lock:
                old_balance = self.balance
                time.sleep(0.001)  # Simulate processing delay
                self.balance = old_balance + amount
        
        def withdraw(self, amount: float) -> bool:
            """Thread-safe withdrawal."""
            with self.lock:
                if self.balance >= amount:
                    old_balance = self.balance
                    time.sleep(0.001)  # Simulate processing delay
                    self.balance = old_balance - amount
                    return True
                return False
        
        def get_balance(self) -> float:
            """Thread-safe balance check."""
            with self.lock:
                return self.balance
    
    # Test thread-safe account
    account = BankAccount(1000)
    
    def deposit_worker(acc: BankAccount, amount: float, times: int):
        for _ in range(times):
            acc.deposit(amount)
    
    def withdraw_worker(acc: BankAccount, amount: float, times: int):
        for _ in range(times):
            acc.withdraw(amount)
    
    # Create multiple threads accessing the same account
    deposit_threads = []
    withdraw_threads = []
    
    for i in range(5):
        t = threading.Thread(target=deposit_worker, args=(account, 100, 100))
        deposit_threads.append(t)
        
        t = threading.Thread(target=withdraw_worker, args=(account, 50, 100))
        withdraw_threads.append(t)
    
    # Start all threads
    for t in deposit_threads + withdraw_threads:
        t.start()
    
    # Wait for completion
    for t in deposit_threads + withdraw_threads:
        t.join()
    
    expected = 1000 + (5 * 100 * 100) - (5 * 50 * 100)
    actual = account.get_balance()
    
    print(f"   Initial balance: 1000")
    print(f"   Deposits: 5 threads × 100 deposits × $100 = +$50,000")
    print(f"   Withdrawals: 5 threads × 100 withdrawals × $50 = -$25,000")
    print(f"   Expected balance: ${expected}")
    print(f"   Actual balance: ${actual}")
    print(f"   Thread-safe: {expected == actual}")
    
    # 5. Thread Communication - Queues
    print("\n5. THREAD COMMUNICATION (QUEUES):")
    
    def producer(queue: Queue, items: list):
        """Produce items and put them in queue."""
        for item in items:
            print(f"   Producer: Adding '{item}' to queue")
            queue.put(item)
            time.sleep(random.uniform(0.1, 0.3))
        queue.put(None)  # Sentinel value to signal completion
    
    def consumer(queue: Queue, name: str):
        """Consume items from queue."""
        while True:
            item = queue.get()
            if item is None:
                queue.put(None)  # Allow other consumers to terminate
                print(f"   Consumer {name}: Finished")
                break
            
            print(f"   Consumer {name}: Processing '{item}'")
            time.sleep(random.uniform(0.2, 0.4))
            queue.task_done()
    
    # Create queue and threads
    queue = Queue()
    items = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    
    producer_thread = threading.Thread(target=producer, args=(queue, items))
    consumer_threads = [
        threading.Thread(target=consumer, args=(queue, "1")),
        threading.Thread(target=consumer, args=(queue, "2"))
    ]
    
    # Start threads
    producer_thread.start()
    for t in consumer_threads:
        t.start()
    
    # Wait for completion
    producer_thread.join()
    queue.join()  # Wait for all tasks to be processed
    
    print("   All tasks processed")

# ============================================================================
# PART 4: MULTIPROCESSING MODULE - PARALLEL PROCESSING
# ============================================================================

def multiprocessing_module_demo():
    """
    multiprocessing MODULE:
    -----------------------
    Process-based parallelism to bypass GIL.
    """
    
    print("\n" + "="*60)
    print("MULTIPROCESSING MODULE DEMONSTRATION")
    print("="*60)
    
    # 1. Basic Process Creation
    print("\n1. BASIC PROCESS CREATION:")
    
    def process_worker(name: str, data: list):
        """Worker function running in separate process."""
        pid = os.getpid()
        print(f"   Process {name} (PID: {pid}): Processing {len(data)} items")
        
        # Simulate work
        result = sum(x ** 2 for x in data)
        
        print(f"   Process {name}: Result = {result}")
        return result
    
    # Create process pool
    data_chunks = [
        list(range(1, 1000001)),
        list(range(1000001, 2000001)),
        list(range(2000001, 3000001))
    ]
    
    processes = []
    results = []
    
    start = time.time()
    
    for i, chunk in enumerate(data_chunks):
        p = multiprocessing.Process(
            target=lambda: results.append(process_worker(f"P{i}", chunk))
        )
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    process_time = time.time() - start
    print(f"   Total time with processes: {process_time:.3f} seconds")
    
    # 2. Process Pool (Better for many tasks)
    print("\n2. PROCESS POOL (Managed Worker Pool):")
    
    def square(x: int) -> int:
        """Simple CPU-bound task."""
        return x ** 2
    
    # Create pool of worker processes
    with multiprocessing.Pool(processes=4) as pool:
        # Map function to data (parallel execution)
        numbers = list(range(1, 101))
        
        start = time.time()
        results = pool.map(square, numbers)
        pool_time = time.time() - start
        
        print(f"   Squared {len(numbers)} numbers in {pool_time:.3f} seconds")
        print(f"   Sample results: {results[:5]}...{results[-5:]}")
    
    # 3. Shared Memory between Processes
    print("\n3. SHARED MEMORY BETWEEN PROCESSES:")
    
    # Different ways to share data between processes
    
    # a) Value and Array (for simple types)
    print("\n   a) Value and Array (for primitive types):")
    
    shared_value = multiprocessing.Value('i', 0)  # 'i' = integer
    shared_array = multiprocessing.Array('d', [0.0, 1.0, 2.0, 3.0, 4.0])  # 'd' = double
    
    def modify_shared(value, array, index):
        with value.get_lock():  # Need lock for Value
            value.value += 1
        
        array[index] = array[index] * 2  # Array access is atomic for single elements
    
    processes = []
    for i in range(5):
        p = multiprocessing.Process(
            target=modify_shared,
            args=(shared_value, shared_array, i % len(shared_array))
        )
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    print(f"   Shared value: {shared_value.value}")
    print(f"   Shared array: {list(shared_array)}")
    
    # b) Manager (for complex objects)
    print("\n   b) Manager (for complex Python objects):")
    
    with multiprocessing.Manager() as manager:
        shared_list = manager.list()
        shared_dict = manager.dict()
        
        def manager_worker(worker_id, s_list, s_dict):
            s_list.append(worker_id)
            s_dict[worker_id] = f"Worker_{worker_id}"
            time.sleep(0.1)
        
        processes = []
        for i in range(5):
            p = multiprocessing.Process(
                target=manager_worker,
                args=(i, shared_list, shared_dict)
            )
            processes.append(p)
            p.start()
        
        for p in processes:
            p.join()
        
        print(f"   Shared list: {list(shared_list)}")
        print(f"   Shared dict: {dict(shared_dict)}")
    
    # 4. Process Communication (Pipes and Queues)
    print("\n4. INTER-PROCESS COMMUNICATION (IPC):")
    
    # a) Pipe (bidirectional communication)
    print("\n   a) Pipe (bidirectional):")
    
    def pipe_worker(conn, worker_id):
        """Worker that communicates through pipe."""
        conn.send(f"Hello from worker {worker_id}")
        message = conn.recv()
        print(f"   Worker {worker_id} received: {message}")
        conn.close()
    
    parent_conn, child_conn = multiprocessing.Pipe()
    
    p = multiprocessing.Process(target=pipe_worker, args=(child_conn, 1))
    p.start()
    
    # Parent receives message
    message = parent_conn.recv()
    print(f"   Parent received: {message}")
    
    # Parent sends response
    parent_conn.send("ACK from parent")
    
    p.join()
    
    # b) Queue (multiprocessing-safe queue)
    print("\n   b) Queue (multiprocessing-safe):")
    
    def queue_producer(queue, items):
        for item in items:
            queue.put(item)
            time.sleep(0.1)
    
    def queue_consumer(queue, name):
        while True:
            try:
                item = queue.get(timeout=1)
                print(f"   Consumer {name} got: {item}")
            except:
                break
    
    mp_queue = multiprocessing.Queue()
    
    producer = multiprocessing.Process(
        target=queue_producer,
        args=(mp_queue, ['A', 'B', 'C', 'D', 'E'])
    )
    
    consumers = [
        multiprocessing.Process(target=queue_consumer, args=(mp_queue, "1")),
        multiprocessing.Process(target=queue_consumer, args=(mp_queue, "2"))
    ]
    
    producer.start()
    for c in consumers:
        c.start()
    
    producer.join()
    for c in consumers:
        c.join()
    
    print("   Queue communication complete")
    
    # 5. Process Synchronization (Locks, Semaphores)
    print("\n5. PROCESS SYNCHRONIZATION:")
    
    def synchronized_worker(lock, resource, worker_id):
        """Worker that uses a lock to synchronize."""
        with lock:
            print(f"   Worker {worker_id} acquired lock")
            resource.value += 1
            time.sleep(0.5)
            print(f"   Worker {worker_id} releasing lock, resource = {resource.value}")
    
    lock = multiprocessing.Lock()
    resource = multiprocessing.Value('i', 0)
    
    processes = []
    for i in range(3):
        p = multiprocessing.Process(
            target=synchronized_worker,
            args=(lock, resource, i)
        )
        processes.append(p)
        p.start()
        time.sleep(0.1)  # Stagger starts
    
    for p in processes:
        p.join()
    
    print(f"   Final resource value: {resource.value}")

# ============================================================================
# PART 5: CONCURRENT.FUTURES - HIGH-LEVEL CONCURRENCY
# ============================================================================

def concurrent_futures_demo():
    """
    concurrent.futures MODULE:
    --------------------------
    High-level interface for asynchronously executing callables.
    Provides ThreadPoolExecutor and ProcessPoolExecutor.
    """
    
    print("\n" + "="*60)
    print("CONCURRENT.FUTURES DEMONSTRATION")
    print("="*60)
    
    # 1. ThreadPoolExecutor (for I/O-bound tasks)
    print("\n1. ThreadPoolExecutor (I/O-bound tasks):")
    
    def fetch_url(url_id: int) -> str:
        """Simulate fetching a URL."""
        time.sleep(random.uniform(0.1, 0.5))  # Simulate network delay
        return f"Response from URL_{url_id}"
    
    urls = list(range(1, 11))  # 10 URLs to fetch
    
    # Sequential approach
    start = time.time()
    sequential_results = [fetch_url(url) for url in urls]
    seq_time = time.time() - start
    print(f"   Sequential time: {seq_time:.3f} seconds")
    
    # ThreadPoolExecutor approach
    start = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Submit tasks and get futures
        futures = [executor.submit(fetch_url, url) for url in urls]
        
        # Collect results as they complete
        thread_results = []
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            thread_results.append(result)
    
    thread_time = time.time() - start
    print(f"   ThreadPoolExecutor time (5 workers): {thread_time:.3f} seconds")
    print(f"   Speedup: {seq_time/thread_time:.2f}x")
    print(f"   Results (first 3): {thread_results[:3]}")
    
    # 2. ProcessPoolExecutor (for CPU-bound tasks)
    print("\n2. ProcessPoolExecutor (CPU-bound tasks):")
    
    def cpu_intensive(n: int) -> int:
        """CPU-intensive calculation."""
        return sum(i * i for i in range(n))
    
    tasks = [1000000, 2000000, 3000000, 4000000, 5000000]
    
    # Sequential
    start = time.time()
    seq_results = [cpu_intensive(n) for n in tasks]
    seq_time = time.time() - start
    print(f"   Sequential time: {seq_time:.3f} seconds")
    
    # ProcessPoolExecutor
    start = time.time()
    
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        # Using map for simple parallel execution
        proc_results = list(executor.map(cpu_intensive, tasks))
    
    proc_time = time.time() - start
    print(f"   ProcessPoolExecutor time (4 workers): {proc_time:.3f} seconds")
    print(f"   Speedup: {seq_time/proc_time:.2f}x")
    print(f"   Results: {proc_results}")
    
    # 3. Future callbacks and exception handling
    print("\n3. Future Callbacks and Exception Handling:")
    
    def task_with_errors(x: int) -> float:
        """Task that might fail."""
        if x % 3 == 0:
            raise ValueError(f"Error with {x}")
        return x ** 0.5
    
    def handle_result(future: concurrent.futures.Future):
        """Callback to handle completed future."""
        try:
            result = future.result()
            print(f"   Success: {result}")
        except Exception as e:
            print(f"   Failed: {type(e).__name__}: {e}")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = []
        
        for i in range(1, 7):
            future = executor.submit(task_with_errors, i)
            future.add_done_callback(handle_result)
            futures.append(future)
        
        # Wait for all to complete
        concurrent.futures.wait(futures)
    
    # 4. Timeouts and cancellation
    print("\n4. Timeouts and Cancellation:")
    
    def slow_task(task_id: int, duration: float) -> str:
        """Task that takes variable time."""
        time.sleep(duration)
        return f"Task {task_id} completed in {duration}s"
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Submit tasks with different durations
        futures = {
            executor.submit(slow_task, i, dur): i
            for i, dur in enumerate([0.5, 1.0, 1.5, 2.0, 2.5])
        }
        
        # Process results with timeout
        try:
            for future in concurrent.futures.as_completed(futures, timeout=1.2):
                task_id = futures[future]
                try:
                    result = future.result(timeout=0.1)
                    print(f"   {result}")
                except concurrent.futures.TimeoutError:
                    print(f"   Task {task_id} result not ready in time")
        except concurrent.futures.TimeoutError:
            print("   Overall timeout reached!")
        
        # Cancel remaining tasks
        remaining = [f for f in futures if not f.done()]
        for future in remaining:
            future.cancel()
            print(f"   Cancelled task {futures[future]}")
    
    print("\n" + "-"*40)
    print("CONCURRENT.FUTURES ADVANTAGES:")
    print("-"*40)
    print("""
    ✓ Simple, high-level API
    ✓ Unified interface for threads and processes
    ✓ Automatic resource management (context manager)
    ✓ Future objects for result/exception handling
    ✓ Built-in timeouts and cancellation
    ✓ Easier migration between threads/processes
    """)

# ============================================================================
# PART 6: ASYNCIO - ASYNCHRONOUS I/O
# ============================================================================

def asyncio_demo():
    """
    ASYNCIO MODULE:
    ---------------
    Asynchronous I/O using async/await syntax.
    
    KEY CONCEPTS:
    - Event Loop: Central execution device that runs async tasks
    - Coroutines: async def functions that can be paused/resumed
    - Tasks: Wrapped coroutines scheduled on event loop
    - Await: Pause coroutine until awaitable completes
    
    WHEN ASYNC HELPS:
    - High concurrency I/O operations (10K+ connections)
    - Network servers (WebSocket, HTTP)
    - When you need fine-grained control over I/O
    
    WHEN ASYNC DOESN'T HELP:
    - CPU-bound tasks (use multiprocessing instead)
    - Simple scripts with few I/O operations
    - When blocking libraries are required
    """
    
    print("\n" + "="*60)
    print("ASYNCIO (ASYNC/AWAIT) DEMONSTRATION")
    print("="*60)
    
    # 1. Basic async/await syntax
    print("\n1. BASIC ASYNC/AWAIT SYNTAX:")
    
    async def say_hello(name: str, delay: float):
        """Simple async coroutine."""
        print(f"   Starting hello for {name}")
        await asyncio.sleep(delay)  # Non-blocking sleep
        print(f"   Hello, {name}!")
        return f"Greeted {name}"
    
    async def basic_async():
        """Run basic async operations."""
        print("   Running basic async example...")
        
        # Run coroutines sequentially (not concurrent)
        result1 = await say_hello("Alice", 1.0)
        result2 = await say_hello("Bob", 0.5)
        
        print(f"   Results: {result1}, {result2}")
    
    # Run the async function
    asyncio.run(basic_async())
    
    # 2. Running coroutines concurrently
    print("\n2. RUNNING COROUTINES CONCURRENTLY:")
    
    async def concurrent_example():
        """Run multiple coroutines concurrently."""
        print("   Starting concurrent tasks...")
        
        # Create tasks (coroutines scheduled to run)
        task1 = asyncio.create_task(say_hello("Charlie", 1.0))
        task2 = asyncio.create_task(say_hello("Diana", 0.5))
        task3 = asyncio.create_task(say_hello("Eve", 0.3))
        
        # Wait for all tasks to complete
        results = await asyncio.gather(task1, task2, task3)
        print(f"   All tasks completed: {results}")
    
    asyncio.run(concurrent_example())
    
    # 3. Async I/O vs Threading comparison
    print("\n3. ASYNC I/O vs THREADING (I/O-BOUND TASKS):")
    
    async def async_io_task(task_id: int):
        """Simulate async I/O operation."""
        # Simulate network/database call
        await asyncio.sleep(0.1)
        return f"Async task {task_id} completed"
    
    def thread_io_task(task_id: int):
        """Simulate I/O operation for threading."""
        time.sleep(0.1)
        return f"Thread task {task_id} completed"
    
    async def compare_async_vs_threads():
        """Compare async and threading approaches."""
        num_tasks = 100
        
        # Async approach
        print(f"   Running {num_tasks} async tasks...")
        start = time.time()
        
        tasks = [async_io_task(i) for i in range(num_tasks)]
        results = await asyncio.gather(*tasks)
        
        async_time = time.time() - start
        print(f"   Async time: {async_time:.3f} seconds")
        print(f"   Rate: {num_tasks/async_time:.1f} tasks/second")
        
        # Threading approach
        print(f"\n   Running {num_tasks} thread tasks...")
        start = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(thread_io_task, i) for i in range(num_tasks)]
            thread_results = [f.result() for f in futures]
        
        thread_time = time.time() - start
        print(f"   Thread time: {thread_time:.3f} seconds")
        print(f"   Rate: {num_tasks/thread_time:.1f} tasks/second")
        
        print(f"\n   Comparison:")
        print(f"   Async is {thread_time/async_time:.1f}x faster")
        print(f"   Async uses 1 thread, Threading uses 50 threads")
        print(f"   Async memory: ~1KB/task, Threading: ~8MB/thread")
    
    asyncio.run(compare_async_vs_threads())
    
    # 4. Real-world example: Web scraper
    print("\n4. REAL-WORLD EXAMPLE: ASYNC WEB SCRAPER SIMULATION:")
    
    class AsyncWebScraper:
        """Simulated async web scraper."""
        
        def __init__(self):
            self.semaphore = asyncio.Semaphore(10)  # Limit concurrent requests
        
        async def fetch_url(self, url: str) -> dict:
            """Fetch a URL with rate limiting."""
            async with self.semaphore:  # Limit concurrency
                # Simulate network delay
                delay = random.uniform(0.05, 0.2)
                await asyncio.sleep(delay)
                
                # Simulate response
                return {
                    'url': url,
                    'status': 200,
                    'content': f"Content from {url}",
                    'size': random.randint(100, 10000)
                }
        
        async def scrape_urls(self, urls: list):
            """Scrape multiple URLs concurrently."""
            print(f"   Starting scrape of {len(urls)} URLs...")
            
            # Create fetch tasks
            tasks = [self.fetch_url(url) for url in urls]
            
            # Process results as they complete
            results = []
            for task in asyncio.as_completed(tasks):
                result = await task
                results.append(result)
                print(f"   Fetched: {result['url']} ({len(results)}/{len(urls)})")
            
            # Summary
            total_size = sum(r['size'] for r in results)
            print(f"   Scraped {len(results)} URLs, total {total_size} bytes")
            return results
    
    # Simulate scraping
    async def run_scraper():
        urls = [f"https://example.com/page{i}" for i in range(1, 51)]
        scraper = AsyncWebScraper()
        await scraper.scrape_urls(urls)
    
    asyncio.run(run_scraper())
    
    # 5. Common async pitfalls and solutions
    print("\n5. COMMON ASYNC PITFALLS AND SOLUTIONS:")
    
    async def demonstrate_pitfalls():
        """Demonstrate common async pitfalls."""
        
        print("   Pitfall 1: Blocking the event loop")
        
        # BAD: Blocking call in async function
        async def bad_blocking():
            time.sleep(1)  # Blocks entire event loop!
            return "Done"
        
        # GOOD: Use async alternatives
        async def good_non_blocking():
            await asyncio.sleep(1)  # Yields control to event loop
            return "Done"
        
        print("\n   Pitfall 2: Forgetting 'await'")
        
        async def print_with_delay(message):
            await asyncio.sleep(0.1)
            print(f"      {message}")
        
        # BAD: Forgetting await creates a coroutine object, doesn't run it
        print("   BAD: coroutine = print_with_delay('Hello')  # Forgot await")
        
        # GOOD: Use await
        print("   GOOD: await print_with_delay('Hello')")
        
        print("\n   Pitfall 3: Mixing async and sync code improperly")
        
        # Solution: Run sync code in thread pool
        def blocking_operation():
            time.sleep(0.5)
            return "Sync result"
        
        async def mixed_code():
            # Run blocking operation in thread pool
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(None, blocking_operation)
            return result
        
        print("   Use loop.run_in_executor() for blocking operations")
    
    asyncio.run(demonstrate_pitfalls())
    
    print("\n" + "-"*40)
    print("ASYNCIO DECISION GUIDE:")
    print("-"*40)
    print("""
    USE ASYNCIO WHEN:
    - High concurrency I/O (1000+ connections)
    - Building network servers
    - Working with async libraries
    - Need low memory footprint per connection
    
    AVOID ASYNCIO WHEN:
    - CPU-bound computations
    - Simple scripts with few I/O calls
    - Team unfamiliar with async/await
    - Required libraries don't support async
    
    BEST PRACTICES:
    - Never use blocking calls in async functions
    - Use semaphores to limit concurrency
    - Handle exceptions in tasks
    - Use async context managers (async with)
    - Monitor event loop health
    """)

# ============================================================================
# PART 7: COMMON CONCURRENCY PROBLEMS
# ============================================================================

def concurrency_problems_demo():
    """
    COMMON CONCURRENCY PROBLEMS:
    ----------------------------
    1. Race Conditions: When outcome depends on execution order
    2. Deadlocks: Two or more operations waiting for each other
    3. Starvation: A process/thread never gets resources
    4. Livelock: Processes keep changing state but make no progress
    """
    
    print("\n" + "="*60)
    print("COMMON CONCURRENCY PROBLEMS DEMONSTRATION")
    print("="*60)
    
    # 1. Race Conditions
    print("\n1. RACE CONDITIONS:")
    print("   When multiple threads access shared data without synchronization.")
    
    class UnsafeCounter:
        """Counter vulnerable to race conditions."""
        
        def __init__(self):
            self.value = 0
        
        def increment(self):
            """NOT thread-safe! Race condition here."""
            current = self.value
            time.sleep(0.001)  # Increase chance of race condition
            self.value = current + 1
    
    class SafeCounter:
        """Thread-safe counter."""
        
        def __init__(self):
            self.value = 0
            self.lock = threading.Lock()
        
        def increment(self):
            """Thread-safe increment."""
            with self.lock:
                current = self.value
                time.sleep(0.001)
                self.value = current + 1
    
    def test_counter(counter_class, num_threads=10, increments=100):
        """Test counter for race conditions."""
        counter = counter_class()
        threads = []
        
        def worker():
            for _ in range(increments):
                counter.increment()
        
        # Create and start threads
        for _ in range(num_threads):
            t = threading.Thread(target=worker)
            threads.append(t)
            t.start()
        
        # Wait for all threads
        for t in threads:
            t.join()
        
        expected = num_threads * increments
        actual = counter.value
        
        return expected, actual
    
    # Test unsafe counter
    print("\n   Testing UNSAFE counter (expect race condition):")
    expected, actual = test_counter(UnsafeCounter, num_threads=5, increments=100)
    print(f"   Expected: {expected}, Actual: {actual}")
    print(f"   Data lost: {expected - actual}")
    
    # Test safe counter
    print("\n   Testing SAFE counter (with locking):")
    expected, actual = test_counter(SafeCounter, num_threads=5, increments=100)
    print(f"   Expected: {expected}, Actual: {actual}")
    print(f"   Data lost: {expected - actual}")
    
    # 2. Deadlocks
    print("\n2. DEADLOCKS:")
    print("   When two or more threads wait for each other indefinitely.")
    
    def demonstrate_deadlock():
        """Demonstrate a classic deadlock scenario."""
        
        lock_a = threading.Lock()
        lock_b = threading.Lock()
        
        def worker1():
            print("   Worker 1: Acquiring lock A")
            lock_a.acquire()
            time.sleep(0.1)  # Simulate work
            
            print("   Worker 1: Trying to acquire lock B")
            lock_b.acquire()  # This will wait forever if worker2 has lock B
            
            print("   Worker 1: Critical section")
            lock_b.release()
            lock_a.release()
            print("   Worker 1: Done")
        
        def worker2():
            print("   Worker 2: Acquiring lock B")
            lock_b.acquire()
            time.sleep(0.1)  # Simulate work
            
            print("   Worker 2: Trying to acquire lock A")
            lock_a.acquire()  # This will wait forever if worker1 has lock A
            
            print("   Worker 2: Critical section")
            lock_a.release()
            lock_b.release()
            print("   Worker 2: Done")
        
        # Create threads
        t1 = threading.Thread(target=worker1)
        t2 = threading.Thread(target=worker2)
        
        t1.start()
        t2.start()
        
        # Wait with timeout to avoid hanging forever
        t1.join(timeout=2)
        t2.join(timeout=2)
        
        if t1.is_alive() or t2.is_alive():
            print("   DEADLOCK DETECTED! Threads are stuck waiting for each other.")
            return True
        return False
    
    print("\n   Running deadlock demonstration...")
    deadlock_occurred = demonstrate_deadlock()
    
    # Deadlock prevention strategies
    print("\n   Deadlock Prevention Strategies:")
    print("   a) Lock Ordering: Always acquire locks in same order")
    print("   b) Timeouts: Use lock.acquire(timeout=X)")
    print("   c) Lock Hierarchy: Define order for all locks")
    print("   d) Deadlock Detection: Monitor and recover")
    
    # Demonstrate lock ordering solution
    print("\n   Solution: Lock Ordering")
    
    def worker_safe1():
        """Always acquire locks in order: A then B."""
        lock_a = threading.Lock()
        lock_b = threading.Lock()
        
        lock_a.acquire()
        lock_b.acquire()
        print("   Worker Safe 1: Got both locks")
        lock_b.release()
        lock_a.release()
    
    def worker_safe2():
        """Always acquire locks in order: A then B."""
        lock_a = threading.Lock()
        lock_b = threading.Lock()
        
        lock_a.acquire()
        lock_b.acquire()
        print("   Worker Safe 2: Got both locks")
        lock_b.release()
        lock_a.release()
    
    t1 = threading.Thread(target=worker_safe1)
    t2 = threading.Thread(target=worker_safe2)
    
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("   No deadlock with proper lock ordering!")
    
    # 3. Starvation
    print("\n3. STARVATION:")
    print("   When a thread never gets CPU time or resources.")
    
    def demonstrate_starvation():
        """Demonstrate thread starvation."""
        
        shared_resource = 0
        lock = threading.Lock()
        
        def greedy_worker(name, priority):
            """Worker that holds lock for a long time."""
            nonlocal shared_resource
            for i in range(3):
                with lock:
                    print(f"   {name} (priority {priority}): Got lock")
                    shared_resource += 1
                    time.sleep(0.5)  # Hold lock for long time
                    print(f"   {name}: Releasing lock")
        
        def polite_worker(name, priority):
            """Worker that needs lock briefly."""
            nonlocal shared_resource
            for i in range(3):
                with lock:
                    print(f"   {name} (priority {priority}): Got lock briefly")
                    shared_resource += 1
                    time.sleep(0.1)  # Brief lock hold
                    print(f"   {name}: Releasing lock")
        
        # Create threads (greedy ones start first)
        threads = []
        threads.append(threading.Thread(target=greedy_worker, args=("Greedy1", 1)))
        threads.append(threading.Thread(target=greedy_worker, args=("Greedy2", 1)))
        threads.append(threading.Thread(target=polite_worker, args=("Polite", 5)))
        
        for t in threads:
            t.start()
            time.sleep(0.1)  # Stagger starts
        
        for t in threads:
            t.join()
    
    print("   Running starvation demonstration...")
    demonstrate_starvation()
    
    # Starvation solutions
    print("\n   Starvation Solutions:")
    print("   a) Fair Locks: threading.Lock() is not fair, consider queue-based locks")
    print("   b) Priority Inversion Prevention: Priority inheritance protocols")
    print("   c) Timeouts: Give up after waiting too long")
    print("   d) Resource Allocation Strategies: Round-robin, shortest job first")
    
    # 4. Livelock
    print("\n4. LIVELOCK:")
    print("   Threads keep changing state but make no progress.")
    
    def demonstrate_livelock():
        """Demonstrate livelock (like two people trying to pass each other)."""
        
        class Person:
            def __init__(self, name):
                self.name = name
                self.moving_left = True
            
            def try_pass(self, other):
                """Try to pass another person."""
                if self.moving_left and other.moving_left:
                    # Both moving left, switch to right
                    self.moving_left = False
                    print(f"   {self.name}: Switched to right")
                    return False
                elif not self.moving_left and not other.moving_left:
                    # Both moving right, switch to left
                    self.moving_left = True
                    print(f"   {self.name}: Switched to left")
                    return False
                else:
                    # Different directions, can pass
                    print(f"   {self.name}: Passing successful!")
                    return True
        
        alice = Person("Alice")
        bob = Person("Bob")
        
        attempts = 0
        max_attempts = 10
        
        print("\n   Alice and Bob trying to pass each other in hallway...")
        
        while not alice.try_pass(bob) and attempts < max_attempts:
            attempts += 1
            time.sleep(0.2)
        
        if attempts >= max_attempts:
            print("   LIVELOCK! They keep switching but never pass.")
        else:
            print(f"   Success after {attempts} attempts")
    
    demonstrate_livelock()
    
    # Livelock solutions
    print("\n   Livelock Solutions:")
    print("   a) Randomized delays: Add random wait times")
    print("   b) Backoff algorithms: Exponential backoff")
    print("   c) Centralized coordinator: One entity makes decisions")
    print("   d) Priority-based resolution: Higher priority thread wins")
    
    # 5. Best Practices Summary
    print("\n" + "="*40)
    print("CONCURRENCY BEST PRACTICES:")
    print("="*40)
    print("""
    1. Minimize Shared State:
       - Use immutable data where possible
       - Prefer message passing over shared memory
       - Keep critical sections small
    
    2. Use Proper Synchronization:
       - Always use locks for shared mutable state
       - Use higher-level abstractions (Queues, Events)
       - Consider thread-safe data structures
    
    3. Avoid Common Pitfalls:
       - Always acquire locks in consistent order
       - Use timeouts to prevent deadlocks
       - Handle exceptions in threads/processes
    
    4. Choose the Right Tool:
       - I/O-bound: threading or asyncio
       - CPU-bound: multiprocessing
       - Simple cases: concurrent.futures
       - High concurrency: asyncio
    
    5. Test Thoroughly:
       - Test with different thread/process counts
       - Use stress testing
       - Implement proper logging and monitoring
    """)

# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """Run all concurrency and parallelism demonstrations."""
    
    print("PYTHON CONCURRENCY & PARALLELISM COMPREHENSIVE GUIDE")
    print("="*60)
    
    # Run demonstrations
    gil_explanation()
    demonstrate_threads_vs_processes()
    threading_module_demo()
    multiprocessing_module_demo()
    concurrent_futures_demo()
    asyncio_demo()
    concurrency_problems_demo()
    
    print("\n" + "="*60)
    print("FINAL SUMMARY")
    print("="*60)
    
    print("""
    KEY TAKEAWAYS:
    
    1. GIL (Global Interpreter Lock):
       - CPython only: One Python thread executes bytecode at a time
       - Affects CPU-bound threads, not I/O-bound
       - Bypass with multiprocessing or alternative Python implementations
    
    2. Threads vs Processes:
       - Threads: Shared memory, lightweight, GIL-limited for CPU
       - Processes: Separate memory, heavier, true parallelism
       - I/O-bound → Threads or Async
       - CPU-bound → Processes
    
    3. Async/Await:
       - Single-threaded concurrency for I/O
       - High scalability (10K+ connections)
       - Requires async-compatible libraries
    
    4. Common Problems:
       - Race Conditions: Use locks/synchronization
       - Deadlocks: Consistent lock ordering, timeouts
       - Starvation: Fair scheduling, priority management
       - Livelock: Randomized delays, backoff algorithms
    
    5. Tool Selection Guide:
    
       ┌─────────────────┬────────────────────┬────────────────────┐
       │ TASK TYPE       │ RECOMMENDED TOOL   │ ALTERNATIVES       │
       ├─────────────────┼────────────────────┼────────────────────┤
       │ Simple I/O      │ concurrent.futures │ threading          │
       │ Many I/O tasks  │ asyncio            │ ThreadPoolExecutor │
       │ CPU-intensive   │ multiprocessing    │ ProcessPoolExecutor│
       │ Mixed workload  │ Process pools      │ Combine tools      │
       │ Simple scripts  │ Sequential         │ Keep it simple     │
       └─────────────────┴────────────────────┴────────────────────┘
    
    REMEMBER:
    - "Premature optimization is the root of all evil" - Donald Knuth
    - Start simple, profile, then optimize
    - Concurrency adds complexity - only use when needed
    - Test thoroughly with different workloads
    - Monitor and measure real-world performance
    """)

if __name__ == "__main__":
    # Note: Some demonstrations create processes, so we use __name__ guard
    main()