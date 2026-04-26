// ============================================================================
// MFC COMPREHENSIVE REVIEW
// File: _mfc_review.cpp
// Quick reference for all MFC topics covered in this refresher series
// ============================================================================

#ifdef _MFC_VER

// ============================================================================
// 1. MFC ARCHITECTURE
// ============================================================================

/*
CWinApp      - Application object (one per app)
CFrameWnd    - Main window frame
CDocument    - Data storage
CView        - Data display
CDocTemplate - Associates Document/View/Frame

Application flow:
1. CMyApp theApp (global)
2. InitInstance() creates document template
3. OnNewDocument() creates document
4. OnCreate() creates frame and views
5. Serialize() reads/writes document data
*/

// ============================================================================
// 2. MESSAGE MAP SYSTEM
// ============================================================================

/*
DECLARE_MESSAGE_MAP() - In header
BEGIN_MESSAGE_MAP / END_MESSAGE_MAP() - In .cpp

Common macros:
ON_WM_PAINT()       - WM_PAINT
ON_WM_LBUTTONDOWN() - Left mouse button
ON_WM_SIZE()        - Window resize
ON_WM_TIMER()       - Timer
ON_BN_CLICKED()     - Button click
ON_EN_CHANGE()      - Edit control change
ON_COMMAND()        - Menu/toolbar command
ON_UPDATE_COMMAND_UI() - UI update
ON_NOTIFY()         - Common control notification
ON_MESSAGE()        - Custom message
ON_REGISTERED_MESSAGE() - Registered message
*/

// ============================================================================
// 3. DIALOG BASICS
// ============================================================================

/*
CDialogEx - Base class for dialogs
DoModal() - Modal dialog
Create()  - Modeless dialog
DoDataExchange() - DDX/DDV
UpdateData() - Transfer data

DDX macros:
DDX_Text()   - Edit control
DDX_Check()  - Checkbox
DDX_Radio()  - Radio button
DDX_Control() - Control variable
DDX_LBIndex() - List box

DDV macros:
DDV_MaxChars()   - Max text length
DDV_MinMaxInt()  - Integer range
DDV_MinMaxDouble() - Double range
*/

// ============================================================================
// 4. COMMON CONTROLS
// ============================================================================

/*
CStatic     - Static text, images
CEdit       - Text input
CButton     - Buttons, checkboxes, radios
CListBox    - List selection
CComboBox   - Dropdown selection
CScrollBar  - Scroll bar
CProgressCtrl - Progress bar
CSliderCtrl - Slider/trackbar
CSpinButtonCtrl - Up-down control
CDateTimeCtrl - Date/time picker
CMonthCalCtrl - Month calendar
CIPAddressCtrl - IP address
CHotKeyCtrl - Hot key
CAnimateCtrl - AVI animation
*/

// ============================================================================
// 5. DOCUMENT/VIEW ARCHITECTURE
// ============================================================================

/*
CView types:
CView        - Base view
CScrollView  - Scrollable view
CFormView    - Dialog-based view
CEditView    - Text editor view
CListView    - List control view
CTreeView    - Tree control view
CRichEditView - Rich text view

Document/View communication:
GetDocument() - View gets document
UpdateAllViews() - Document notifies views
OnUpdate() - View receives update
SetModifiedFlag() - Mark document modified
DeleteContents() - Clear document data
*/

// ============================================================================
// 6. SDI/MDI APPLICATIONS
// ============================================================================

/*
CSingleDocTemplate - SDI (one document)
CMultiDocTemplate - MDI (multiple documents)
CMDIFrameWndEx    - MDI frame (feature pack)
CMDIChildWndEx    - MDI child (feature pack)

Window messages:
WM_CLOSE    - Close window
WM_DESTROY  - Window destroyed
WM_QUIT     - Application quit
WM_SIZE     - Window resized
WM_MOVE     - Window moved
WM_CREATE   - Window created
WM_PAINT    - Window needs repaint
*/

// ============================================================================
// 7. MENUS, TOOLBARS, STATUS BARS
// ============================================================================

/*
CMenu       - Menu handling
CToolBar    - Toolbar control
CStatusBar  - Status bar
CReBar      - Rebar container
CDialogBar  - Dialog bar

CCmdUI methods:
Enable()    - Enable/disable
SetCheck()  - Check/uncheck
SetRadio()  - Radio state
SetText()   - Change text
*/

// ============================================================================
// 8. GDI DRAWING
// ============================================================================

/*
CDC         - Device context
CPaintDC    - WM_PAINT DC
CClientDC   - Client area DC
CWindowDC   - Full window DC
CPen        - Line drawing
CBrush      - Shape filling
CFont       - Text rendering
CBitmap     - Bitmap images
CRect       - Rectangle operations
CPoint      - 2D point
CSize       - 2D size

Double buffering:
1. Create compatible DC
2. Create compatible bitmap
3. Draw to memory DC
4. BitBlt to screen DC
*/

// ============================================================================
// 9. FILE I/O AND SERIALIZATION
// ============================================================================

/*
CFile       - Binary file I/O
CMemFile    - Memory file
CStdioFile  - Text file I/O
CArchive    - Serialization
CFileDialog - Open/Save dialogs

Serialization:
DECLARE_SERIAL / IMPLEMENT_SERIAL
Serialize(CArchive& ar)
ar << value  (store)
ar >> value  (load)
*/

// ============================================================================
// 10. COLLECTIONS
// ============================================================================

/*
CArray<T,A>     - Dynamic array
CList<T,A>      - Doubly-linked list
CMap<K,AK,V,AV> - Hash map
CStringArray    - String array
CPtrList        - Pointer list
CObList         - CObject list
CMapStringToString - String map

POSITION - Iterator type
GetNextAssoc() - Map iteration
*/

// ============================================================================
// 11. THREADING
// ============================================================================

/*
CWinThread      - Thread class
AfxBeginThread  - Create thread
CCriticalSection - Fast lock
CMutex          - Cross-process lock
CSemaphore      - Resource counting
CEvent          - Signaling
CSingleLock     - RAII lock
CMultiLock      - Multiple locks

Worker threads: No message pump
UI threads: Have message pump
*/

// ============================================================================
// 12. PROPERTY SHEETS
// ============================================================================

/*
CPropertySheet - Tab container
CPropertyPage  - Individual page
SetWizardMode() - Wizard mode
SetWizardButtons() - Navigation buttons
SetFinishText() - Finish button text
SetModified()  - Enable Apply button
*/

// ============================================================================
// 13. SPLITTER WINDOWS
// ============================================================================

/*
CSplitterWnd - Splitter window
CreateStatic() - Fixed panes
Create() - Dynamic splitter
CreateView() - Create pane view
GetPane() - Access pane
SetRowInfo() / SetColumnInfo() - Pane sizes
*/

// ============================================================================
// 14. OLE/ACTIVEX
// ============================================================================

/*
COleDocument - OLE document
COleClientItem - Embedded/linked item
COleDropTarget - Drag/drop target
COleDataSource - Data source
COleInsertDialog - Insert Object dialog
*/

// ============================================================================
// 15. DATABASE (ODBC)
// ============================================================================

/*
CDatabase   - Database connection
CRecordset  - Record set
CRecordView - Form view
CFieldExchange - RFX mechanism
CDBException - Database exception

RFX macros:
RFX_Long()  - Integer field
RFX_Text()  - Text field
RFX_Double() - Double field
RFX_Date()  - Date field
*/

// ============================================================================
// 16. NETWORKING
// ============================================================================

/*
CAsyncSocket - Async socket
CSocket      - Sync socket
CSocketFile  - Socket file interface
CArchive     - Socket serialization

TCP: Create(), Connect(), Send(), Receive()
UDP: Create(), SendTo(), ReceiveFrom()
*/

// ============================================================================
// 17. FEATURE PACK
// ============================================================================

/*
CMFCRibbonBar - Ribbon interface
CMFCMenuBar   - Modern menu
CMFCToolBar   - Enhanced toolbar
CMFCStatusBar - Enhanced status bar
CDockablePane - Docking pane
CMFCPropertyGridCtrl - Property grid
CMFCTaskDialog - Modern dialog
*/

// ============================================================================
// 18. DEBUGGING
// ============================================================================

/*
TRACE()     - Debug output
ASSERT()    - Debug assertion
VERIFY()    - Evaluate in debug/release
ENSURE()    - Check and throw
afxDump     - Diagnostic output
AssertValid() - Object validation
Dump()      - Object dump
DEBUG_NEW   - Memory leak detection
*/

// ============================================================================
// 19. CUSTOM CONTROLS
// ============================================================================

/*
SubclassDlgItem() - Subclass control
DrawItem() - Owner-draw
NM_CUSTOMDRAW - Custom draw
AfxRegisterWndClass() - Register class
PreSubclassWindow() - Pre-subclass init
*/

// ============================================================================
// 20. COMMON CONTROLS (ADVANCED)
// ============================================================================

/*
CProgressCtrl - Progress bar
CSliderCtrl  - Slider
CSpinButtonCtrl - Spin control
CAnimateCtrl - AVI animation
CDateTimeCtrl - Date/time picker
CMonthCalCtrl - Month calendar
CIPAddressCtrl - IP address
CHotKeyCtrl  - Hot key
*/

// ============================================================================
// KEY MFC MACROS QUICK REFERENCE
// ============================================================================

/*
DECLARE_MESSAGE_MAP / BEGIN_MESSAGE_MAP / END_MESSAGE_MAP
DECLARE_DYNAMIC / IMPLEMENT_DYNAMIC
DECLARE_DYNCREATE / IMPLEMENT_DYNCREATE
DECLARE_SERIAL / IMPLEMENT_SERIAL
DECLARE_DIAGNOSTIC

RUNTIME_CLASS(class) - Get CRuntimeClass
ON_COMMAND(id, handler) - Command handler
ON_UPDATE_COMMAND_UI(id, handler) - UI update
ON_NOTIFY(wNotifyCode, id, handler) - Notification
ON_MESSAGE(message, handler) - Custom message
ON_REGISTERED_MESSAGE(message, handler) - Registered message
ON_CONTROL_RANGE(wNotifyCode, id1, id2, handler) - Range of IDs
*/

// ============================================================================
// COMMON MFC CLASS HIERARCHY
// ============================================================================

/*
CObject
  +-- CCmdTarget
  |     +-- CWinThread
  |     |     +-- CWinApp
  |     +-- CWnd
  |     |     +-- CFrameWnd
  |     |     |     +-- CMDIFrameWnd
  |     |     |     +-- CMDIChildWnd
  |     |     +-- CView
  |     |     |     +-- CScrollView
  |     |     |     +-- CFormView
  |     |     |     +-- CEditView
  |     |     |     +-- CListView
  |     |     |     +-- CTreeView
  |     |     +-- CDialog
  |     |     |     +-- CDialogEx
  |     |     |     +-- CPropertyPage
  |     |     |     +-- CPropertySheet
  |     |     |     +-- CFileDialog
  |     |     +-- CStatic, CEdit, CButton, CListBox, CComboBox
  |     |     +-- CProgressCtrl, CSliderCtrl, CSpinButtonCtrl
  |     |     +-- CDateTimeCtrl, CMonthCalCtrl
  |     |     +-- CAnimateCtrl, CIPAddressCtrl, CHotKeyCtrl
  |     |     +-- CTreeCtrl, CListCtrl
  |     |     +-- CSplitterWnd
  |     |     +-- CToolBar, CStatusBar, CMenuBar
  |     |     +-- CDockablePane
  |     +-- CDocument
  |     |     +-- COleDocument
  |     +-- CDocTemplate
  |           +-- CSingleDocTemplate
  |           +-- CMultiDocTemplate
  +-- CFile
  |     +-- CMemFile
  |     +-- CStdioFile
  |     +-- CSocketFile
  +-- CDC
  |     +-- CPaintDC
  |     +-- CClientDC
  |     +-- CWindowDC
  +-- CGdiObject
  |     +-- CPen, CBrush, CFont, CBitmap
  +-- CException
  |     +-- CFileException
  |     +-- CArchiveException
  |     +-- CDBException
  |     +-- COleException
  |     +-- CMemoryException
  |     +-- CNotSupportedException
  |     +-- CResourceException
  |     +-- CUserException
  +-- CRecordset
  +-- CAsyncSocket
  |     +-- CSocket
  +-- COleControl
  +-- CCriticalSection
  +-- CEvent
  +-- CMutex
  +-- CSemaphore
*/

#endif // _MFC_VER
