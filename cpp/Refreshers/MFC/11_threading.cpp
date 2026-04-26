// ============================================================================
// MFC THREADING
// File: 11_threading.cpp
// Covers: CWinThread, AfxBeginThread, worker threads, UI threads, sync
// ============================================================================

#ifdef _MFC_VER

// ============================================================================
// 1. THREADING OVERVIEW
// ============================================================================

/*
MFC supports two types of threads:
1. Worker threads - Perform background tasks (no message pump)
2. UI threads - Have their own message pump (can create windows)

Key classes:
- CWinThread - Base class for all threads
- CSyncObject - Base class for synchronization objects
- CCriticalSection - Critical section (fast, same process)
- CMutex - Mutex (can be cross-process)
- CSemaphore - Semaphore (resource counting)
- CEvent - Event (signaling)
- CMultiLock - Lock multiple sync objects
- CSingleLock - Lock single sync object
*/

// ============================================================================
// 2. WORKER THREADS
// ============================================================================

/*
Worker threads perform background tasks. Created with AfxBeginThread.

AfxBeginThread signatures:
- CWinThread* AfxBeginThread(
    AFX_THREADPROC pfnThreadProc,  // Thread function
    LPVOID pParam,                 // Parameter
    int nPriority = THREAD_PRIORITY_NORMAL,
    UINT nStackSize = 0,
    DWORD dwCreateFlags = 0,
    LPSECURITY_ATTRIBUTES lpSecurityAttrs = nullptr);

- CWinThread* AfxBeginThread(
    CRuntimeClass* pThreadClass,   // CWinThread-derived class
    int nPriority = THREAD_PRIORITY_NORMAL,
    UINT nStackSize = 0,
    DWORD dwCreateFlags = 0,
    LPSECURITY_ATTRIBUTES lpSecurityAttrs = nullptr);
*/

// Thread function (must be UINT CallingConvention(LPVOID))
UINT MyWorkerThread(LPVOID pParam)
{
    int* pData = (int*)pParam;
    
    // Thread work
    for (int i = 0; i < 10; i++)
    {
        // Simulate work
        Sleep(100);
        
        // Check if thread should exit
        if (AfxGetThread()->m_bAutoDelete == FALSE)
        {
            // Handle exit request
        }
    }
    
    return 0;  // Thread exit code
}

void StartWorkerThread()
{
    int data = 42;
    
    // Start worker thread
    CWinThread* pThread = AfxBeginThread(MyWorkerThread, &data,
        THREAD_PRIORITY_NORMAL, 0, CREATE_SUSPENDED);
    
    if (pThread != nullptr)
    {
        // Set thread properties before resuming
        pThread->m_bAutoDelete = TRUE;  // Auto-delete on exit
        
        // Resume thread
        pThread->ResumeThread();
    }
}

// ============================================================================
// 3. UI THREADS
// ============================================================================

/*
UI threads have their own message pump and can create windows.
Derive from CWinThread and override InitInstance.

Key overrides:
- InitInstance() - Initialize thread (create windows)
- ExitInstance() - Cleanup
- Run() - Message pump (rarely overridden)
- PreTranslateMessage() - Message filtering
*/

class CMyUIThread : public CWinThread
{
    DECLARE_DYNCREATE(CMyUIThread)
    
public:
    virtual BOOL InitInstance();
    virtual int ExitInstance();
    
    // Thread window
    CMyFrameWnd* m_pFrameWnd;
};

IMPLEMENT_DYNCREATE(CMyUIThread, CWinThread)

BOOL CMyUIThread::InitInstance()
{
    // Create a frame window for this thread
    m_pFrameWnd = new CMyFrameWnd();
    m_pFrameWnd->Create(nullptr, _T("UI Thread Window"));
    m_pFrameWnd->ShowWindow(SW_SHOW);
    m_pFrameWnd->UpdateWindow();
    
    // Set main window for this thread
    m_pMainWnd = m_pFrameWnd;
    
    return TRUE;
}

int CMyUIThread::ExitInstance()
{
    // Cleanup
    return CWinThread::ExitInstance();
}

void StartUIThread()
{
    // Start UI thread
    CWinThread* pThread = AfxBeginThread(RUNTIME_CLASS(CMyUIThread));
    
    if (pThread != nullptr)
    {
        // Send message to UI thread
        pThread->PostThreadMessage(WM_USER + 100, 0, 0);
    }
}

// ============================================================================
// 4. THREAD SYNCHRONIZATION
// ============================================================================

/*
CCriticalSection - Fast, same-process only
- Lock() / Unlock() - Manual locking
- CSingleLock - RAII locking
*/

// Global critical section
CCriticalSection g_cs;

class CSharedData
{
public:
    void UpdateData(int value)
    {
        // Method 1: Manual lock/unlock
        g_cs.Lock();
        m_value = value;
        g_cs.Unlock();
        
        // Method 2: RAII with CSingleLock
        CSingleLock singleLock(&g_cs);
        singleLock.Lock();
        m_value = value;
        // Auto-unlocked when singleLock goes out of scope
    }
    
    int GetData()
    {
        CSingleLock lock(&g_cs, TRUE);  // TRUE = auto-lock
        return m_value;
        // Auto-unlocked
    }
    
private:
    int m_value;
};

// ============================================================================
// 5. CMutex - CROSS-PROCESS SYNCHRONIZATION
// ============================================================================

/*
CMutex can synchronize across processes.
Constructor: CMutex(BOOL bInitiallyOwn, LPCTSTR lpszName, LPSECURITY_ATTRIBUTES lpsaAttribute)
*/

void MutexExample()
{
    // Create named mutex (can be shared across processes)
    CMutex mutex(FALSE, _T("Global\\MyMutex"));
    
    // Wait for mutex
    CSingleLock lock(&mutex, TRUE);  // TRUE = wait indefinitely
    
    // Protected section
    // ...
    
    // Auto-unlocked
}

// ============================================================================
// 6. CSemaphore - RESOURCE COUNTING
// ============================================================================

/*
CSemaphore limits access to a resource pool.
Constructor: CSemaphore(LONG lInitialCount, LONG lMaxCount, LPCTSTR pstrName)
*/

void SemaphoreExample()
{
    // Allow up to 3 concurrent accesses
    CSemaphore semaphore(3, 3);
    
    // Wait for available slot
    CSingleLock lock(&semaphore, TRUE);
    
    // Access limited resource
    // ...
    
    // Auto-released
}

// ============================================================================
// 7. CEvent - SIGNALING
// ============================================================================

/*
CEvent signals between threads.
Types:
- Manual-reset: Must be explicitly reset (SetEvent/ResetEvent)
- Auto-reset: Automatically resets after releasing one waiter

Constructor: CEvent(BOOL bInitiallyOwn, BOOL bManualReset, LPCTSTR lpszName)
*/

CEvent g_eventStop(FALSE, FALSE);  // Auto-reset, initially non-signaled
CEvent g_eventDataReady(FALSE, FALSE, _T("Global\\DataReadyEvent"));

UINT ProducerThread(LPVOID pParam)
{
    // Produce data
    // ...
    
    // Signal consumer
    g_eventDataReady.SetEvent();
    
    return 0;
}

UINT ConsumerThread(LPVOID pParam)
{
    // Wait for data
    CSingleLock lock(&g_eventDataReady, TRUE);
    
    // Process data
    // ...
    
    return 0;
}

// ============================================================================
// 8. CMultiLock - MULTIPLE SYNCHRONIZATION OBJECTS
// ============================================================================

/*
CMultiLock can wait on multiple sync objects at once.

Wait flags:
- INFINITE - Wait forever
- 0 - Check and return immediately
- nMilliseconds - Timeout
*/

void MultiLockExample()
{
    CCriticalSection cs1, cs2;
    CEvent event1, event2;
    
    CSyncObject* objects[] = { &cs1, &cs2, &event1, &event2 };
    CMultiLock multiLock(objects, 4);
    
    // Wait for any object
    DWORD result = multiLock.Lock(INFINITE, FALSE);  // FALSE = wait for any
    
    switch (result)
    {
    case WAIT_OBJECT_0 + 0:  // cs1
        break;
    case WAIT_OBJECT_0 + 1:  // cs2
        break;
    case WAIT_OBJECT_0 + 2:  // event1
        break;
    case WAIT_OBJECT_0 + 3:  // event2
        break;
    case WAIT_TIMEOUT:
        break;
    }
    
    // Unlock all
    multiLock.Unlock();
}

// ============================================================================
// 9. THREAD COMMUNICATION
// ============================================================================

/*
Thread communication methods:
1. PostMessage/PostThreadMessage - Async message posting
2. SendMessage - Sync message (blocks until processed)
3. Shared variables (with synchronization)
4. CEvent - Signaling
5. Queue/pipe - Data transfer
*/

void ThreadCommunicationExample()
{
    // Post message to UI thread
    CWinThread* pUIThread = AfxGetApp()->m_pMainWnd->GetWindowThread();
    pUIThread->PostThreadMessage(WM_USER + 1, (WPARAM)100, (LPARAM)200);
    
    // Post message to specific window (thread-safe)
    HWND hWnd = AfxGetMainWnd()->GetSafeHwnd();
    ::PostMessage(hWnd, WM_USER + 2, 0, 0);
    
    // Send message (blocks until processed)
    ::SendMessage(hWnd, WM_USER + 3, 0, 0);
}

// ============================================================================
// 10. BEST PRACTICES
// ============================================================================

/*
1. Use worker threads for background computation
2. Use UI threads for independent windows
3. Use CSingleLock/CMultiLock for RAII locking
4. Use CCriticalSection for same-process synchronization
5. Use CEvent for signaling between threads
6. Use CSemaphore for resource pools
7. Use CMutex for cross-process synchronization
8. Never access MFC objects from another thread directly
9. Use PostMessage for cross-thread communication
10. Always check thread handle validity
*/

#endif // _MFC_VER
