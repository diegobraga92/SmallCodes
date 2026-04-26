// ============================================================================
// MFC APPLICATION ARCHITECTURE
// File: 00_mfc_architecture.cpp
// Covers: CWinApp, CFrameWnd, WinMain, application lifecycle, initialization
// ============================================================================

#ifdef _MFC_VER

// ============================================================================
// 1. MFC APPLICATION FUNDAMENTALS
// ============================================================================

/*
MFC wraps the Windows API into C++ classes. Every MFC application has:

1. Application object (CWinApp-derived) - one global instance
2. Frame window (CFrameWnd-derived) - the main window
3. Message map - routes Windows messages to handler functions
4. Document/View architecture (optional) - separates data from presentation

The CWinApp object is constructed first (as a global variable), and MFC's
internal WinMain() calls InitInstance() to start the application.
*/

// ============================================================================
// 2. CWinApp - THE APPLICATION CLASS
// ============================================================================

/*
CWinApp is the base class for the application object. It provides:
- Application initialization and cleanup
- Message loop (Run)
- Document template management
- Command-line parsing
- Help support

Key virtual methods to override:
- InitInstance() - Called once at startup. Create main window here.
- ExitInstance() - Called when application exits. Cleanup here.
- OnIdle() - Called when message queue is empty. For background tasks.
*/

// Basic CWinApp declaration
class CMyApp : public CWinApp
{
public:
    // Override InitInstance to create the main window
    virtual BOOL InitInstance();
    
    // Override ExitInstance for cleanup
    virtual int ExitInstance();
    
    // DECLARE_MESSAGE_MAP() - Required for message handling
    DECLARE_MESSAGE_MAP()
};

// ============================================================================
// 3. CFrameWnd - THE MAIN WINDOW
// ============================================================================

/*
CFrameWnd manages the application's main window. It provides:
- Window creation and destruction
- Title bar, system menu, minimize/maximize buttons
- Client area for views or child controls
- Menu bar, toolbars, status bar management
- Window positioning and sizing

Key methods:
- Create() or LoadFrame() - Create the window
- ShowWindow() - Show/hide the window
- UpdateWindow() - Force window repaint
- SetWindowText() - Change window title
- GetClientRect() - Get client area dimensions
*/

class CMainFrame : public CFrameWnd
{
public:
    CMainFrame();
    
    // Window creation
    BOOL CreateWindow();
    
    // Menu and toolbar management
    CMenu* GetMenu() const { return m_pMenu; }
    
protected:
    CMenu* m_pMenu;
    
    DECLARE_MESSAGE_MAP()
};

// ============================================================================
// 4. APPLICATION LIFECYCLE
// ============================================================================

/*
MFC Application Lifecycle:

1. Global CMyApp object constructed (before WinMain)
2. WinMain() called by Windows
3. CMyApp::InitInstance() called
   - Register window classes (AfxRegisterWndClass)
   - Create main frame window
   - Show and update the window
   - Parse command line
   - Return TRUE to continue
4. CWinApp::Run() enters message loop
   - Dispatches Windows messages to window procedures
   - Calls OnIdle() when idle
5. User closes application
6. CMyApp::ExitInstance() called
7. Application terminates
*/

// ============================================================================
// 5. COMPLETE MINIMAL MFC APPLICATION
// ============================================================================

// The global application object - must be at global scope
// CMyApp theApp;  // Uncomment in a real MFC project

// InitInstance - called once at startup
BOOL CMyApp::InitInstance()
{
    // Enable 3D controls (for older MFC versions)
    // Enable3dControls();  // Deprecated in VS 2008+
    
    // Create the main frame window
    CMainFrame* pFrame = new CMainFrame;
    
    if (!pFrame->CreateWindow())
    {
        // Window creation failed - cleanup and exit
        delete pFrame;
        return FALSE;
    }
    
    // Store pointer to main window
    m_pMainWnd = pFrame;
    
    // Show the window (nCmdShow comes from command line)
    pFrame->ShowWindow(m_nCmdShow);
    pFrame->UpdateWindow();
    
    return TRUE;  // Continue running
}

int CMyApp::ExitInstance()
{
    // Cleanup code here
    // Note: m_pMainWnd is destroyed automatically
    return CWinApp::ExitInstance();
}

// ============================================================================
// 6. FRAME WINDOW IMPLEMENTATION
// ============================================================================

CMainFrame::CMainFrame()
    : m_pMenu(nullptr)
{
    // Constructor - initialize members
}

BOOL CMainFrame::CreateWindow()
{
    // Register a window class with MFC
    // AfxRegisterWndClass parameters:
    //   - Style flags (CS_HREDRAW | CS_VREDRAW)
    //   - Cursor handle (LoadCursor(NULL, IDC_ARROW))
    //   - Background brush (COLOR_WINDOW + 1)
    //   - Icon handle (LoadIcon(IDR_MAINFRAME))
    
    LPCTSTR lpszClass = AfxRegisterWndClass(
        CS_HREDRAW | CS_VREDRAW,           // Redraw on resize
        ::LoadCursor(NULL, IDC_ARROW),      // Standard arrow cursor
        (HBRUSH)(COLOR_WINDOW + 1),         // White background
        ::LoadIcon(NULL, IDI_APPLICATION)   // Default icon
    );
    
    // Create the window
    // Create() parameters:
    //   - Window class name
    //   - Window title
    //   - Window style (WS_OVERLAPPEDWINDOW)
    //   - Position (CW_USEDEFAULT for default)
    //   - Size (CW_USEDEFAULT for default)
    //   - Parent window (NULL for main window)
    //   - Menu (NULL for default)
    
    return Create(
        lpszClass,
        _T("MFC Application"),
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT,
        CW_USEDEFAULT,
        CW_USEDEFAULT,
        CW_USEDEFAULT,
        NULL,
        NULL
    );
}

// ============================================================================
// 7. WINDOW STYLES AND EXTENDED STYLES
// ============================================================================

/*
Common Window Styles (WS_*):
WS_OVERLAPPED       - Overlapped window with title bar and border
WS_OVERLAPPEDWINDOW - Overlapped + caption + sysmenu + thickframe + minimize + maximize
WS_POPUP            - Popup window (no title bar)
WS_CHILD            - Child window (must have parent)
WS_BORDER           - Window with border
WS_CAPTION          - Window with title bar
WS_SYSMENU          - Window with system menu
WS_THICKFRAME       - Resizable window
WS_MINIMIZEBOX      - Minimize button
WS_MAXIMIZEBOX      - Maximize button
WS_VSCROLL          - Vertical scroll bar
WS_HSCROLL          - Horizontal scroll bar
WS_DISABLED         - Initially disabled

Extended Styles (WS_EX_*):
WS_EX_CLIENTEDGE    - Sunken edge (3D look)
WS_EX_WINDOWEDGE    - Raised edge
WS_EX_TOOLWINDOW    - Tool window (small title bar)
WS_EX_TOPMOST       - Always on top
WS_EX_ACCEPTFILES   - Accepts drag-drop files
WS_EX_APPWINDOW     - Forces top-level window on taskbar
*/

// ============================================================================
// 8. WINDOW PLACEMENT AND STATE
// ============================================================================

/*
Saving and restoring window position:

// Save window placement
WINDOWPLACEMENT wp;
wp.length = sizeof(WINDOWPLACEMENT);
GetWindowPlacement(&wp);
// Save wp.rcNormalPosition, wp.showCmd to registry

// Restore window placement
WINDOWPLACEMENT wp;
// Load wp.rcNormalPosition, wp.showCmd from registry
SetWindowPlacement(&wp);

Window states:
SW_SHOWNORMAL      - Show and restore
SW_SHOWMINIMIZED   - Show minimized
SW_SHOWMAXIMIZED   - Show maximized
SW_HIDE            - Hide
SW_SHOW            - Show in current state
*/

// ============================================================================
// 9. COMMAND LINE PARSING
// ============================================================================

/*
CWinApp provides command line parsing:

// Access command line
CString cmdLine = m_lpCmdLine;

// Parse command line
CCommandLineInfo cmdInfo;
ParseCommandLine(cmdInfo);

// CCommandLineInfo fields:
// cmdInfo.m_bShowSplash    - /Splash flag
// cmdInfo.m_bRunEmbedded   - /Embedding flag (OLE)
// cmdInfo.m_bRunAutomated  - /Automation flag (OLE)
// cmdInfo.m_nShellCommand - FileNew, FileOpen, FilePrint, etc.
// cmdInfo.m_strFileName   - File name for FileOpen/FilePrint

// Process command line (creates document/view)
// ProcessShellCommand(cmdInfo);
*/

// ============================================================================
// 10. BEST PRACTICES
// ============================================================================

/*
1. Always check return values from Create() and other MFC functions
2. Use AfxRegisterWndClass for custom window classes
3. Store m_pMainWnd for proper application shutdown
4. Override ExitInstance() for cleanup (not destructor)
5. Use CCommandLineInfo for command line parsing
6. Enable 3D controls only for legacy MFC versions
7. Use LoadFrame() instead of Create() for SDI/MDI apps
8. Set m_pMainWnd before showing the window
9. Use AfxGetApp() to access the application object globally
10. Use AfxGetInstanceHandle() to get the HINSTANCE
*/

// ============================================================================
// 11. COMMON MFC MACROS AND GLOBALS
// ============================================================================

/*
Global Functions:
AfxGetApp()           - Returns pointer to CWinApp object
AfxGetInstanceHandle()- Returns application instance handle
AfxGetMainWnd()       - Returns main window pointer
AfxMessageBox()       - Displays message box
AfxAbort()            - Aborts application
AfxRegisterWndClass() - Registers window class
AfxBeginThread()      - Creates a new thread
AfxEndThread()        - Terminates current thread
AfxFormatString1()    - Formats string with one substitution
AfxFormatString2()    - Formats string with two substitutions

Common Macros:
DECLARE_MESSAGE_MAP() - Declares message map
BEGIN_MESSAGE_MAP()   - Begins message map definition
END_MESSAGE_MAP()     - Ends message map definition
ON_WM_PAINT()         - Maps WM_PAINT message
ON_WM_SIZE()          - Maps WM_SIZE message
ON_WM_CLOSE()         - Maps WM_CLOSE message
ON_COMMAND()          - Maps command message
ON_UPDATE_COMMAND_UI()- Maps command UI update
*/

// Message map for CMyApp
BEGIN_MESSAGE_MAP(CMyApp, CWinApp)
    // No standard messages for CWinApp
END_MESSAGE_MAP()

// Message map for CMainFrame
BEGIN_MESSAGE_MAP(CMainFrame, CFrameWnd)
    ON_WM_PAINT()
    ON_WM_SIZE()
    ON_WM_CLOSE()
END_MESSAGE_MAP()

#endif // _MFC_VER
