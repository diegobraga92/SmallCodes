// ============================================================================
// MFC DEBUGGING AND ERROR HANDLING
// File: 18_debugging_error_handling.cpp
// Covers: TRACE, ASSERT, exceptions, error codes, debugging techniques
// ============================================================================

#ifdef _MFC_VER

// ============================================================================
// 1. DEBUG MACROS
// ============================================================================

/*
MFC provides several debug macros that are only active in Debug builds.

TRACE macros:
- TRACE(format, ...) - Formatted debug output
- TRACE0(string) - String output (no format)
- TRACE1(format, arg1) - One argument
- TRACE2(format, arg1, arg2) - Two arguments
- TRACE3(format, arg1, arg2, arg3) - Three arguments

Output goes to:
- Visual Studio Output window (Debug view)
- DebugView (Sysinternals)
- Any debug output listener

ASSERT macros:
- ASSERT(condition) - Debug assertion
- ASSERT_VALID(pObject) - Check CObject validity
- ASSERT_KINDOF(class, pObject) - Check runtime class
- VERIFY(expression) - Evaluate in debug/release
- ENSURE(condition) - Check and throw if failed
*/

void DebugMacroExample()
{
    int value = 42;
    CString name = _T("Test");
    
    // TRACE output
    TRACE(_T("Value = %d, Name = %s\n"), value, name);
    TRACE0("Simple string\n");
    TRACE1("One arg: %d\n", value);
    TRACE2("Two args: %d, %s\n", value, name);
    
    // ASSERT - only in debug builds
    ASSERT(value > 0);
    ASSERT(name.GetLength() > 0);
    
    // ASSERT_VALID - checks CObject integrity
    // ASSERT_VALID(pDocument);
    
    // ASSERT_KINDOF - checks runtime class
    // ASSERT_KINDOF(CView, pView);
    
    // VERIFY - evaluates in both debug and release
    // In debug: asserts if FALSE
    // In release: just evaluates
    VERIFY(value == 42);
    
    // ENSURE - throws exception if condition fails
    ENSURE(value > 0);
}

// ============================================================================
// 2. CObject DIAGNOSTICS
// ============================================================================

/*
CObject provides diagnostic support through virtual functions.

Key methods:
- AssertValid() - Override to validate object state
- Dump(CDumpContext&) - Override to dump object data
- GetRuntimeClass() - Get CRuntimeClass
- IsKindOf() - Check runtime class
- IsSerializable() - Check serialization support
*/

class CMyDiagnosticObject : public CObject
{
    DECLARE_DYNAMIC(CMyDiagnosticObject)
    
public:
    CMyDiagnosticObject() : m_id(0), m_name(_T("")) {}
    
#ifdef _DEBUG
    virtual void AssertValid() const;
    virtual void Dump(CDumpContext& dc) const;
#endif
    
    int m_id;
    CString m_name;
};

IMPLEMENT_DYNAMIC(CMyDiagnosticObject, CObject)

#ifdef _DEBUG
void CMyDiagnosticObject::AssertValid() const
{
    // Call base class
    CObject::AssertValid();
    
    // Validate member variables
    ASSERT(m_id >= 0);
    ASSERT(!m_name.IsEmpty());
}

void CMyDiagnosticObject::Dump(CDumpContext& dc) const
{
    // Call base class
    CObject::Dump(dc);
    
    // Dump member variables
    dc << _T("ID: ") << m_id << _T("\n");
    dc << _T("Name: ") << m_name << _T("\n");
}
#endif

// ============================================================================
// 3. CDumpContext
// ============================================================================

/*
CDumpContext provides formatted diagnostic output.
afxDump is the global CDumpContext object.

Usage:
afxDump << "Debug output" << value << "\n";
*/

void DumpContextExample()
{
#ifdef _DEBUG
    // Use afxDump for diagnostic output
    afxDump << _T("Debug information\n");
    afxDump << _T("Value: ") << 42 << _T("\n");
    
    // Dump MFC objects
    CString text = _T("Hello");
    afxDump << _T("String: ") << text << _T("\n");
    
    // Dump rectangles
    CRect rect(0, 0, 100, 100);
    afxDump << _T("Rect: ") << rect << _T("\n");
    
    // Dump points
    CPoint pt(10, 20);
    afxDump << _T("Point: ") << pt << _T("\n");
    
    // Dump sizes
    CSize size(50, 30);
    afxDump << _T("Size: ") << size << _T("\n");
#endif
}

// ============================================================================
// 4. MFC EXCEPTIONS
// ============================================================================

/*
MFC provides exception classes derived from CException:

- CMemoryException - Out of memory
- CFileException - File I/O errors
- CArchiveException - Serialization errors
- CDBException - Database errors
- COleException - OLE errors
- COleDispatchException - OLE automation errors
- CResourceException - Resource loading errors
- CUserException - User-cancelled operation
- CNotSupportedException - Unsupported operation
- CInvalidArgException - Invalid argument

Key methods:
- GetErrorMessage() - Get error description
- ReportError() - Show error message box
- Delete() - Delete exception object
*/

void ExceptionHandlingExample()
{
    // CFileException
    try
    {
        CFile file;
        CFileException ex;
        
        if (!file.Open(_T("nonexistent.txt"),
            CFile::modeRead, &ex))
        {
            // Get error message
            TCHAR errorMsg[256];
            ex.GetErrorMessage(errorMsg, 256);
            AfxMessageBox(errorMsg);
        }
    }
    catch (CFileException* e)
    {
        // Handle file exception
        e->ReportError();  // Show error dialog
        e->Delete();       // Delete exception
    }
    
    // CMemoryException
    try
    {
        char* pBuffer = new char[1024 * 1024 * 100];  // Large allocation
        if (pBuffer == nullptr)
        {
            AfxThrowMemoryException();
        }
        delete[] pBuffer;
    }
    catch (CMemoryException* e)
    {
        e->ReportError();
        e->Delete();
    }
    
    // CArchiveException
    try
    {
        CFile file;
        file.Open(_T("data.dat"), CFile::modeRead);
        CArchive ar(&file, CArchive::load);
        
        // Read data
        int value;
        ar >> value;
        
        ar.Close();
        file.Close();
    }
    catch (CArchiveException* e)
    {
        e->ReportError();
        e->Delete();
    }
    catch (CFileException* e)
    {
        e->ReportError();
        e->Delete();
    }
}

// ============================================================================
// 5. THROWING MFC EXCEPTIONS
// ============================================================================

/*
Use AfxThrow*Exception() functions to throw MFC exceptions.

Functions:
- AfxThrowMemoryException()
- AfxThrowFileException(cause, lOsError, lpszFileName)
- AfxThrowArchiveException(cause, lpszArchiveName)
- AfxThrowOleException(nCode)
- AfxThrowOleDispatchException(nCode, lpszDescription)
- AfxThrowUserException()
- AfxThrowNotSupportedException()
- AfxThrowResourceException()
- AfxThrowInvalidArgException()
*/

void ThrowingExceptions()
{
    // Check memory allocation
    void* pData = malloc(1024);
    if (pData == nullptr)
    {
        AfxThrowMemoryException();
    }
    
    // Check file operation
    CFile file;
    if (!file.Open(_T("config.ini"), CFile::modeRead))
    {
        AfxThrowFileException(CFileException::fileNotFound,
            GetLastError(), _T("config.ini"));
    }
    
    // Check resource
    HICON hIcon = AfxGetApp()->LoadIcon(IDI_MYICON);
    if (hIcon == nullptr)
    {
        AfxThrowResourceException();
    }
}

// ============================================================================
// 6. ERROR CODES AND REPORTING
// ============================================================================

/*
Common error handling patterns in MFC.

GetLastError() - Get Windows error code
FormatMessage() - Format error message
CException::GetErrorMessage() - Get MFC error message
*/

void ErrorReportingExample()
{
    // Get Windows error
    DWORD dwError = GetLastError();
    
    // Format Windows error message
    LPTSTR lpMsgBuf;
    FormatMessage(
        FORMAT_MESSAGE_ALLOCATE_BUFFER |
        FORMAT_MESSAGE_FROM_SYSTEM |
        FORMAT_MESSAGE_IGNORE_INSERTS,
        nullptr, dwError,
        MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
        (LPTSTR)&lpMsgBuf, 0, nullptr);
    
    // Display error
    AfxMessageBox(lpMsgBuf);
    
    // Free buffer
    LocalFree(lpMsgBuf);
    
    // Check HRESULT
    HRESULT hr = CoInitialize(nullptr);
    if (FAILED(hr))
    {
        _com_error err(hr);
        AfxMessageBox(err.ErrorMessage());
    }
}

// ============================================================================
// 7. DEBUGGING TECHNIQUES
// ============================================================================

/*
MFC debugging techniques:

1. Memory leak detection
2. Object dump
3. Call stack analysis
4. Message logging
5. Performance profiling
*/

// Enable memory leak detection
#ifdef _DEBUG
#define new DEBUG_NEW
#endif

void DebuggingTechniques()
{
    // Check for memory leaks
    // _CrtDumpMemoryLeaks() at program exit
    
    // Dump all MFC objects
    // AfxDumpStack() - Dump call stack
    
    // Check object count
    // AfxCheckMemory() - Check heap integrity
    
    // Enable debug heap
    int tmpDbgFlag = _CrtSetDbgFlag(_CRTDBG_REPORT_FLAG);
    tmpDbgFlag |= _CRTDBG_LEAK_CHECK_DF;
    _CrtSetDbgFlag(tmpDbgFlag);
}

// ============================================================================
// 8. BEST PRACTICES
// ============================================================================

/*
1. Use TRACE for debug output (not AfxMessageBox)
2. Use ASSERT for internal invariants
3. Use VERIFY for function return values
4. Use ENSURE for parameter validation
5. Override AssertValid() and Dump() for custom classes
6. Use try/catch for file and database operations
7. Use AfxThrow*Exception() for throwing MFC exceptions
8. Use GetErrorMessage() for user-friendly error messages
9. Use DEBUG_NEW for memory leak detection
10. Use AfxCheckMemory() to detect heap corruption
*/

#endif // _MFC_VER
