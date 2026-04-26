// ============================================================================
// MFC SDI/MDI APPLICATIONS
// File: 06_sdi_mdi_apps.cpp
// Covers: SDI vs MDI, document templates, multiple views, CMDIFrameWnd
// ============================================================================

#ifdef _MFC_VER

// ============================================================================
// 1. SDI VS MDI OVERVIEW
// ============================================================================

/*
SDI (Single Document Interface):
- One document open at a time
- Uses CSingleDocTemplate
- Frame: CFrameWnd
- Simpler, less resource intensive
- Examples: Notepad, Paint

MDI (Multiple Document Interface):
- Multiple documents open simultaneously
- Uses CMultiDocTemplate
- Main frame: CMDIFrameWnd
- Child frames: CMDIChildWnd
- Examples: Visual Studio (classic), Excel
- MDI client window manages child windows
*/

// ============================================================================
// 2. SDI APPLICATION
// ============================================================================

/*
SDI Application Structure:
- CWinApp-derived application class
- CSingleDocTemplate connects Document/View/Frame
- One CFrameWnd (reused for each document)
- File New/Open replaces current document

SDI InitInstance:
BOOL CMyApp::InitInstance()
{
    // Register document template
    CSingleDocTemplate* pDocTemplate;
    pDocTemplate = new CSingleDocTemplate(
        IDR_MAINFRAME,
        RUNTIME_CLASS(CMyDocument),
        RUNTIME_CLASS(CMainFrame),     // CFrameWnd-derived
        RUNTIME_CLASS(CMyView));
    AddDocTemplate(pDocTemplate);
    
    // Parse command line
    CCommandLineInfo cmdInfo;
    ParseCommandLine(cmdInfo);
    
    // Dispatch commands (File New, Open, etc.)
    if (!ProcessShellCommand(cmdInfo))
        return FALSE;
    
    return TRUE;
}
*/

// ============================================================================
// 3. MDI APPLICATION
// ============================================================================

/*
MDI Application Structure:
- CWinApp-derived application class
- CMDIFrameWnd for main frame
- CMDIChildWnd for child frames
- CMultiDocTemplate for each document type
- Window menu for managing child windows

MDI InitInstance:
BOOL CMyApp::InitInstance()
{
    // Register document template
    CMultiDocTemplate* pDocTemplate;
    pDocTemplate = new CMultiDocTemplate(
        IDR_MYDOCTYPE,
        RUNTIME_CLASS(CMyDocument),
        RUNTIME_CLASS(CChildFrame),    // CMDIChildWnd-derived
        RUNTIME_CLASS(CMyView));
    AddDocTemplate(pDocTemplate);
    
    // Create main MDI frame
    CMainFrame* pMainFrame = new CMainFrame;
    if (!pMainFrame->LoadFrame(IDR_MAINFRAME))
        return FALSE;
    m_pMainWnd = pMainFrame;
    
    // Parse command line
    CCommandLineInfo cmdInfo;
    ParseCommandLine(cmdInfo);
    
    // Dispatch commands
    if (!ProcessShellCommand(cmdInfo))
        return FALSE;
    
    pMainFrame->ShowWindow(m_nCmdShow);
    pMainFrame->UpdateWindow();
    
    return TRUE;
}
*/

// ============================================================================
// 4. MDI MAIN FRAME WINDOW
// ============================================================================

class CMainFrame : public CMDIFrameWnd
{
public:
    CMainFrame();
    
    // MDI-specific methods
    CMDIChildWnd* MDIGetActive(BOOL* pbMaximized = nullptr);
    void MDICascade(int nType = MDITILE_SKIPDISABLED);
    void MDITile(int nType = MDITILE_HORIZONTAL);
    void MDIIconArrange();
    void MDINext();
    void MDIPrev();
    
    // Window menu management
    void OnUpdateWindowMenu(CCmdUI* pCmdUI);
    
protected:
    // Toolbar and status bar
    CToolBar m_wndToolBar;
    CStatusBar m_wndStatusBar;
    
    afx_msg int OnCreate(LPCREATESTRUCT lpCreateStruct);
    afx_msg void OnWindowCascade();
    afx_msg void OnWindowTileHorz();
    afx_msg void OnWindowTileVert();
    afx_msg void OnWindowArrangeIcons();
    
    DECLARE_MESSAGE_MAP()
};

CMainFrame::CMainFrame()
{
    // Constructor
}

int CMainFrame::OnCreate(LPCREATESTRUCT lpCreateStruct)
{
    if (CMDIFrameWnd::OnCreate(lpCreateStruct) == -1)
        return -1;
    
    // Create toolbar
    if (!m_wndToolBar.CreateEx(this, TBSTYLE_FLAT, WS_CHILD | WS_VISIBLE |
        CBRS_TOP | CBRS_GRIPPER | CBRS_TOOLTIPS | CBRS_FLYBY | CBRS_SIZE_DYNAMIC) ||
        !m_wndToolBar.LoadToolBar(IDR_MAINFRAME))
    {
        TRACE0("Failed to create toolbar\n");
        return -1;
    }
    
    // Create status bar
    if (!m_wndStatusBar.Create(this) ||
        !m_wndStatusBar.SetIndicators(indicators, sizeof(indicators)/sizeof(UINT)))
    {
        TRACE0("Failed to create status bar\n");
        return -1;
    }
    
    // Enable docking
    m_wndToolBar.EnableDocking(CBRS_ALIGN_ANY);
    EnableDocking(CBRS_ALIGN_ANY);
    DockControlBar(&m_wndToolBar);
    
    return 0;
}

// ============================================================================
// 5. MDI CHILD FRAME
// ============================================================================

class CChildFrame : public CMDIChildWnd
{
public:
    CChildFrame();
    
    // Override to customize child frame
    virtual BOOL PreCreateWindow(CREATESTRUCT& cs);
    
protected:
    afx_msg int OnCreate(LPCREATESTRUCT lpCreateStruct);
    
    DECLARE_MESSAGE_MAP()
};

CChildFrame::CChildFrame()
{
    // Constructor
}

BOOL CChildFrame::PreCreateWindow(CREATESTRUCT& cs)
{
    if (!CMDIChildWnd::PreCreateWindow(cs))
        return FALSE;
    
    // Customize child window style
    cs.style = WS_CHILD | WS_VISIBLE | WS_OVERLAPPEDWINDOW |
               WS_CLIPCHILDREN | FWS_ADDTOTITLE;
    
    // Set default size
    cs.cx = 600;
    cs.cy = 400;
    
    return TRUE;
}

int CChildFrame::OnCreate(LPCREATESTRUCT lpCreateStruct)
{
    if (CMDIChildWnd::OnCreate(lpCreateStruct) == -1)
        return -1;
    
    // Enable docking for child frame
    // (if child has its own toolbars)
    
    return 0;
}

// ============================================================================
// 6. MDI WINDOW MANAGEMENT
// ============================================================================

/*
MDI Window Menu Commands:

Window > Cascade - MDICascade()
Window > Tile Horizontally - MDITile(MDITILE_HORIZONTAL)
Window > Tile Vertically - MDITile(MDITILE_VERTICAL)
Window > Arrange Icons - MDIIconArrange()
Window > Close All - Close all child windows

Window list (dynamic):
MFC automatically adds open document list to Window menu.
The last item is "Windows..." dialog.
*/

void CMainFrame::OnWindowCascade()
{
    MDICascade();
}

void CMainFrame::OnWindowTileHorz()
{
    MDITile(MDITILE_HORIZONTAL);
}

void CMainFrame::OnWindowTileVert()
{
    MDITile(MDITILE_VERTICAL);
}

void CMainFrame::OnWindowArrangeIcons()
{
    MDIIconArrange();
}

// ============================================================================
// 7. MULTIPLE DOCUMENT TYPES
// ============================================================================

/*
MDI supports multiple document types in the same application.

Example: Text editor + Image viewer

// In InitInstance:
// Text document template
CMultiDocTemplate* pTextTemplate;
pTextTemplate = new CMultiDocTemplate(
    IDR_TEXTTYPE,
    RUNTIME_CLASS(CTextDocument),
    RUNTIME_CLASS(CChildFrame),
    RUNTIME_CLASS(CTextView));
AddDocTemplate(pTextTemplate);

// Image document template
CMultiDocTemplate* pImageTemplate;
pImageTemplate = new CMultiDocTemplate(
    IDR_IMAGETYPE,
    RUNTIME_CLASS(CImageDocument),
    RUNTIME_CLASS(CChildFrame),
    RUNTIME_CLASS(CImageView));
AddDocTemplate(pImageTemplate);

Each document type has its own:
- Menu and toolbar resources (IDR_TEXTTYPE, IDR_IMAGETYPE)
- Document class
- View class
- Icon
- File extension
*/

// ============================================================================
// 8. MDI CHILD WINDOW STYLES
// ============================================================================

/*
MDI Child Window Styles:

FWS_ADDTOTITLE     - Add document title to window title
FWS_PREFIXTITLE    - Prefix document title (default)
FWS_SNAPTOACTIVE   - Snap to active MDI child

Common child window styles:
WS_OVERLAPPEDWINDOW - Standard window with caption, sysmenu, etc.
WS_MAXIMIZE         - Start maximized
WS_MINIMIZE         - Start minimized
WS_EX_MDICHILD      - MDI child (set automatically)

Child window title format:
FWS_ADDTOTITLE | FWS_PREFIXTITLE: "Document - Application"
FWS_ADDTOTITLE only: "Document"
Neither: Custom title
*/

// ============================================================================
// 9. SDI VS MDI COMPARISON
// ============================================================================

/*
Feature                | SDI                    | MDI
-----------------------|------------------------|------------------------
Documents at once      | 1                      | Multiple
Frame class            | CFrameWnd              | CMDIFrameWnd
Child frame            | N/A                    | CMDIChildWnd
Template class         | CSingleDocTemplate     | CMultiDocTemplate
File New behavior      | Replaces current       | Opens new child
Window menu            | Not needed             | Required
Resource usage         | Lower                  | Higher
Complexity             | Simpler                | More complex
User focus             | Single task            | Multiple tasks

When to use SDI:
- Simple applications
- Single-document workflow
- Limited resources
- Examples: Notepad, Calculator

When to use MDI:
- Multiple documents needed
- Document comparison
- Reference materials
- Examples: IDEs, Office apps
*/

// ============================================================================
// 10. BEST PRACTICES
// ============================================================================

/*
1. Use SDI for simple applications, MDI for complex ones
2. Provide Window menu for MDI applications
3. Use FWS_ADDTOTITLE for meaningful child window titles
4. Handle OnUpdateWindowMenu for dynamic menu updates
5. Use MDIGetActive to get active child window
6. Set default child window size in PreCreateWindow
7. Use separate resource IDs for each document type
8. Enable docking on main frame, not child frames
9. Use ProcessShellCommand for command line handling
10. Register all document templates before parsing command line
*/

// Message maps
BEGIN_MESSAGE_MAP(CMainFrame, CMDIFrameWnd)
    ON_WM_CREATE()
    ON_COMMAND(ID_WINDOW_CASCADE, &CMainFrame::OnWindowCascade)
    ON_COMMAND(ID_WINDOW_TILE_HORZ, &CMainFrame::OnWindowTileHorz)
    ON_COMMAND(ID_WINDOW_TILE_VERT, &CMainFrame::OnWindowTileVert)
    ON_COMMAND(ID_WINDOW_ARRANGE, &CMainFrame::OnWindowArrangeIcons)
END_MESSAGE_MAP()

BEGIN_MESSAGE_MAP(CChildFrame, CMDIChildWnd)
    ON_WM_CREATE()
END_MESSAGE_MAP()

#endif // _MFC_VER
