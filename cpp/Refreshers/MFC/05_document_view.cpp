// ============================================================================
// MFC DOCUMENT/VIEW ARCHITECTURE
// File: 05_document_view.cpp
// Covers: CDocument, CView, CScrollView, CFormView, Serialize, UpdateAllViews
// ============================================================================

#ifdef _MFC_VER

// ============================================================================
// 1. DOCUMENT/VIEW ARCHITECTURE OVERVIEW
// ============================================================================

/*
The Document/View architecture separates data (document) from presentation (view).

Key classes:
- CDocument - Stores and manages application data
- CView - Displays document data and handles user interaction
- CFrameWnd - Frame window containing the view
- CDocTemplate - Manages document/view/frame relationships
- CWinApp - Creates document templates in InitInstance

Benefits:
- Multiple views of the same data (splitter, MDI)
- Simplified data management (Serialize)
- Automatic command routing
- Clean separation of concerns
*/

// ============================================================================
// 2. CDocument - THE DATA CLASS
// ============================================================================

/*
CDocument manages application data. Key responsibilities:
- Store and manage data
- Serialize data to/from files
- Notify views when data changes
- Handle document commands (File New, Open, Save)

Key methods:
- OnNewDocument() - Initialize new document
- OnOpenDocument() - Open existing document
- DeleteContents() - Clear document data
- Serialize() - Read/write data
- UpdateAllViews() - Notify views of changes
- SetModifiedFlag() - Mark document as modified
- IsModified() - Check if modified
- GetTitle() / SetTitle() - Document title
- GetPathName() - Document file path
- DoFileSave() - Save document
- OnSaveDocument() - Save to file
- OnCloseDocument() - Close document
*/

class CMyDocument : public CDocument
{
public:
    // Document data
    CString m_name;
    int     m_value;
    CArray<double, double> m_dataPoints;
    
    // Override Serialize for file I/O
    virtual void Serialize(CArchive& ar);
    
    // Override document initialization
    virtual BOOL OnNewDocument();
    
    // Override to clear data
    virtual void DeleteContents();
    
protected:
    DECLARE_MESSAGE_MAP()
};

BOOL CMyDocument::OnNewDocument()
{
    if (!CDocument::OnNewDocument())
        return FALSE;
    
    // Initialize new document data
    m_name = _T("New Document");
    m_value = 0;
    m_dataPoints.RemoveAll();
    
    return TRUE;
}

void CMyDocument::DeleteContents()
{
    // Clear document data
    m_name.Empty();
    m_value = 0;
    m_dataPoints.RemoveAll();
    
    CDocument::DeleteContents();
}

// ============================================================================
// 3. SERIALIZATION
// ============================================================================

/*
CArchive provides type-safe serialization for MFC objects.
Works with CFile to read/write data.

CArchive modes:
CArchive::store - Writing data
CArchive::load - Reading data

Serialization operators:
<< - Store data (ar << value)
>> - Load data (ar >> value)

Serializable types:
- All MFC collections
- CString, CPoint, CRect, CSize
- CTime, COleDateTime
- CObject-derived classes with DECLARE_SERIAL/DECLARE_DYNCREATE
- Standard types (int, double, etc.)
*/

void CMyDocument::Serialize(CArchive& ar)
{
    if (ar.IsStoring())
    {
        // Writing to file
        ar << m_name;
        ar << m_value;
        m_dataPoints.Serialize(ar);
    }
    else
    {
        // Reading from file
        ar >> m_name;
        ar >> m_value;
        m_dataPoints.Serialize(ar);
    }
}

// ============================================================================
// 4. CView - THE PRESENTATION CLASS
// ============================================================================

/*
CView displays document data and handles user interaction.

Key methods:
- OnDraw() - Render document data (pure virtual)
- OnUpdate() - Called when document data changes
- GetDocument() - Get associated document
- OnInitialUpdate() - First update after view creation
- OnPrepareDC() - Prepare device context before drawing

View types:
- CView - Base class (requires OnDraw override)
- CScrollView - Adds scrolling support
- CFormView - Dialog-based view
- CListView - List control view
- CTreeView - Tree control view
- CRichEditView - Rich text editing
- CEditView - Text editing
*/

class CMyView : public CView
{
public:
    // Get the document
    CMyDocument* GetDocument() const
    {
        return (CMyDocument*)m_pDocument;
    }
    
    // Override OnDraw to render data
    virtual void OnDraw(CDC* pDC);
    
    // Override OnUpdate when document changes
    virtual void OnUpdate(CView* pSender, LPARAM lHint, CObject* pHint);
    
protected:
    DECLARE_MESSAGE_MAP()
};

void CMyView::OnDraw(CDC* pDC)
{
    CMyDocument* pDoc = GetDocument();
    ASSERT_VALID(pDoc);
    
    // Get client area
    CRect clientRect;
    GetClientRect(&clientRect);
    
    // Draw document data
    CString text;
    text.Format(_T("Name: %s\nValue: %d\nData Points: %d"),
        pDoc->m_name, pDoc->m_value, pDoc->m_dataPoints.GetSize());
    
    pDC->DrawText(text, &clientRect, DT_LEFT | DT_TOP);
}

void CMyView::OnUpdate(CView* pSender, LPARAM lHint, CObject* pHint)
{
    // Called when document data changes
    // lHint and pHint can provide specific update information
    // For simple cases, just invalidate the view
    Invalidate();
}

// ============================================================================
// 5. CScrollView - SCROLLABLE VIEW
// ============================================================================

/*
CScrollView extends CView with scrolling support.

Key methods:
- SetScrollSizes() - Set logical size and scroll increments
- GetScrollPosition() - Current scroll position
- ScrollToPosition() - Scroll to specific position
- FillOutsideRect() - Fill area outside scrolling region
- GetTotalSize() - Total scrollable size
- ResizeParentToFit() - Resize frame to fit content
*/

class CMyScrollView : public CScrollView
{
public:
    virtual void OnInitialUpdate();
    virtual void OnDraw(CDC* pDC);
    
protected:
    DECLARE_MESSAGE_MAP()
};

void CMyScrollView::OnInitialUpdate()
{
    CScrollView::OnInitialUpdate();
    
    // Set scrollable area (2000 x 2000 logical units)
    CSize sizeTotal(2000, 2000);
    CSize sizePage(500, 500);    // Page scroll increment
    CSize sizeLine(50, 50);      // Line scroll increment
    SetScrollSizes(MM_TEXT, sizeTotal, sizePage, sizeLine);
}

void CMyScrollView::OnDraw(CDC* pDC)
{
    // Drawing in logical coordinates
    // The view handles scrolling automatically
    
    // Draw at specific logical position
    pDC->Rectangle(100, 100, 500, 300);
    pDC->TextOut(100, 100, _T("This text scrolls with the view"));
}

// ============================================================================
// 6. CFormView - DIALOG-BASED VIEW
// ============================================================================

/*
CFormView is a view that uses a dialog resource as its layout.
Combines the benefits of dialog controls with document/view architecture.

Key features:
- Uses dialog resource template
- Supports DDX/DDV like CDialog
- Can be used in splitter windows
- Supports scrolling (CScrollView base)
*/

class CMyFormView : public CFormView
{
public:
    CMyFormView() : CFormView(IDD_MY_FORM_VIEW) {}
    
    enum { IDD = IDD_MY_FORM_VIEW };
    
    // Control member variables
    CString m_name;
    int     m_age;
    
protected:
    virtual void DoDataExchange(CDataExchange* pDX);
    virtual void OnInitialUpdate();
    
    // Handlers
    afx_msg void OnBnClickedUpdate();
    
    DECLARE_MESSAGE_MAP()
};

void CMyFormView::DoDataExchange(CDataExchange* pDX)
{
    CFormView::DoDataExchange(pDX);
    DDX_Text(pDX, IDC_NAME_EDIT, m_name);
    DDX_Text(pDX, IDC_AGE_EDIT, m_age);
}

void CMyFormView::OnInitialUpdate()
{
    CFormView::OnInitialUpdate();
    
    // Load data from document
    CMyDocument* pDoc = (CMyDocument*)GetDocument();
    m_name = pDoc->m_name;
    m_age = pDoc->m_value;
    
    UpdateData(FALSE);  // Variables -> Controls
}

void CMyFormView::OnBnClickedUpdate()
{
    UpdateData(TRUE);  // Controls -> Variables
    
    // Update document
    CMyDocument* pDoc = (CMyDocument*)GetDocument();
    pDoc->m_name = m_name;
    pDoc->m_value = m_age;
    pDoc->SetModifiedFlag();
    
    // Notify other views
    pDoc->UpdateAllViews(this);
}

// ============================================================================
// 7. UPDATEALLVIEWS AND HINTS
// ============================================================================

/*
UpdateAllViews notifies all views (except the sender) that data has changed.

UpdateAllViews signatures:
UpdateAllViews(CView* pSender, LPARAM lHint = 0L, CObject* pHint = NULL)

Using hints for efficient updates:
- lHint - Integer hint (e.g., enum indicating what changed)
- pHint - Object hint (e.g., pointer to changed element)

Example hint usage:
enum ViewHint {
    HINT_NAME_CHANGED,
    HINT_VALUE_CHANGED,
    HINT_DATA_ADDED,
    HINT_DATA_REMOVED,
    HINT_ALL_CHANGED
};

// In document:
// UpdateAllViews(this, (LPARAM)HINT_NAME_CHANGED);

// In view's OnUpdate:
// switch (lHint) {
//     case HINT_NAME_CHANGED: UpdateName(); break;
//     case HINT_ALL_CHANGED: Invalidate(); break;
// }
*/

// ============================================================================
// 8. DOCUMENT TEMPLATES
// ============================================================================

/*
CDocTemplate connects document, view, and frame classes.

Types:
CSingleDocTemplate - SDI (Single Document Interface)
CMultiDocTemplate - MDI (Multiple Document Interface)

Created in CWinApp::InitInstance():

// SDI template
CSingleDocTemplate* pDocTemplate;
pDocTemplate = new CSingleDocTemplate(
    IDR_MAINFRAME,           // Menu and resources
    RUNTIME_CLASS(CMyDocument),
    RUNTIME_CLASS(CMainFrame),  // SDI frame (CFrameWnd)
    RUNTIME_CLASS(CMyView));
AddDocTemplate(pDocTemplate);

// MDI template
CMultiDocTemplate* pDocTemplate;
pDocTemplate = new CMultiDocTemplate(
    IDR_MYDOCTYPE,           // Menu and resources
    RUNTIME_CLASS(CMyDocument),
    RUNTIME_CLASS(CChildFrame),  // MDI child frame (CMDIChildWnd)
    RUNTIME_CLASS(CMyView));
AddDocTemplate(pDocTemplate);
*/

// ============================================================================
// 9. MULTIPLE VIEWS OF SAME DOCUMENT
// ============================================================================

/*
Creating multiple views of the same document:

// In frame window:
BOOL CMainFrame::OnCreateClient(LPCREATESTRUCT lpcs, CCreateContext* pContext)
{
    // Create splitter with two views
    if (!m_wndSplitter.CreateStatic(this, 1, 2))
        return FALSE;
    
    // First pane - form view
    m_wndSplitter.CreateView(0, 0,
        RUNTIME_CLASS(CMyFormView),
        CSize(300, 100), pContext);
    
    // Second pane - scroll view
    m_wndSplitter.CreateView(0, 1,
        RUNTIME_CLASS(CMyScrollView),
        CSize(300, 100), pContext);
    
    return TRUE;
}
*/

// ============================================================================
// 10. BEST PRACTICES
// ============================================================================

/*
1. Always call base class Serialize() for version support
2. Use DeleteContents() for cleanup, not destructor
3. Call SetModifiedFlag() when document data changes
4. Use UpdateAllViews() with hints for efficient updates
5. Override OnUpdate() to handle specific changes
6. Use CScrollView for large or zoomable documents
7. Use CFormView for data-entry views
8. Keep document data separate from presentation logic
9. Use Serialize for all persistent data
10. Override OnInitialUpdate() for view initialization
*/

// Message maps
BEGIN_MESSAGE_MAP(CMyDocument, CDocument)
END_MESSAGE_MAP()

BEGIN_MESSAGE_MAP(CMyView, CView)
END_MESSAGE_MAP()

BEGIN_MESSAGE_MAP(CMyScrollView, CScrollView)
END_MESSAGE_MAP()

BEGIN_MESSAGE_MAP(CMyFormView, CFormView)
    ON_BN_CLICKED(IDC_UPDATE_BTN, &CMyFormView::OnBnClickedUpdate)
END_MESSAGE_MAP()

#endif // _MFC_VER
