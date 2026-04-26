// ============================================================================
// MFC SPLITTER WINDOWS AND MULTIPLE VIEWS
// File: 13_splitter_views.cpp
// Covers: CSplitterWnd, dynamic/static splitters, multiple view types
// ============================================================================

#ifdef _MFC_VER

// ============================================================================
// 1. SPLITTER WINDOW OVERVIEW
// ============================================================================

/*
CSplitterWnd divides a window into multiple panes, each containing a view.

Types:
1. Static splitter - Fixed number of panes (created once)
2. Dynamic splitter - User can split/unsplit (max panes defined)

Key methods:
- Create() / CreateStatic() - Create splitter
- CreateView() - Create view in pane
- DeleteView() - Delete view from pane
- GetPane() - Get pane window
- SetRowInfo() / SetColumnInfo() - Set pane sizes
- GetRowInfo() / GetColumnInfo() - Get pane sizes
- SetScrollStyle() - Set scroll bar style
- IdFromRowCol() - Get child window ID
- IsChildPane() - Check if window is a pane
- ActivateNext() - Activate next pane
- CanSplit() / DoSplit() - Dynamic split operations
- ResizeClass() - Resize pane
*/

// ============================================================================
// 2. STATIC SPLITTER
// ============================================================================

/*
Static splitter has a fixed number of panes (rows x columns).
Panels cannot be split further by the user.

Common layouts:
- 1 row x 2 cols (side by side)
- 2 rows x 1 col (top/bottom)
- 2 rows x 2 cols (quadrants)
*/

class CMainFrame : public CFrameWnd
{
protected:
    CSplitterWnd m_wndSplitter;
    
    // Override to create splitter
    virtual BOOL OnCreateClient(LPCREATESTRUCT lpcs, CCreateContext* pContext);
    
    DECLARE_MESSAGE_MAP()
};

BOOL CMainFrame::OnCreateClient(LPCREATESTRUCT lpcs, CCreateContext* pContext)
{
    // Create static splitter: 1 row, 2 columns
    if (!m_wndSplitter.CreateStatic(this, 1, 2))
    {
        TRACE0("Failed to create splitter\n");
        return FALSE;
    }
    
    // Create views in each pane
    // Left pane: Tree view
    m_wndSplitter.CreateView(0, 0,
        RUNTIME_CLASS(CMyTreeView),
        CSize(250, 100), pContext);
    
    // Right pane: List view
    m_wndSplitter.CreateView(0, 1,
        RUNTIME_CLASS(CMyListView),
        CSize(250, 100), pContext);
    
    // Set initial pane sizes
    m_wndSplitter.SetColumnInfo(0, 250, 50);   // Min width 50
    m_wndSplitter.SetColumnInfo(1, 500, 100);  // Min width 100
    
    return TRUE;
}

// ============================================================================
// 3. DYNAMIC SPLITTER
// ============================================================================

/*
Dynamic splitter allows the user to split/unsplit panes.
Maximum panes defined at creation.

Create() parameters:
- pParentWnd - Parent window
- nMaxRows - Maximum rows (1-16)
- nMaxCols - Maximum columns (1-16)
- sizeMin - Minimum pane size
- pContext - Create context
- dwStyle - Window style
- nID - Child window ID
*/

class CDynamicSplitFrame : public CFrameWnd
{
protected:
    CSplitterWnd m_wndSplitter;
    
    virtual BOOL OnCreateClient(LPCREATESTRUCT lpcs, CCreateContext* pContext);
    
    DECLARE_MESSAGE_MAP()
};

BOOL CDynamicSplitFrame::OnCreateClient(LPCREATESTRUCT lpcs, CCreateContext* pContext)
{
    // Create dynamic splitter: max 2 rows, 2 cols
    return m_wndSplitter.Create(this,
        2,      // Max rows
        2,      // Max cols
        CSize(10, 10),  // Minimum pane size
        pContext);
}

// ============================================================================
// 4. SPLITTER WITH DIFFERENT VIEW TYPES
// ============================================================================

/*
Splitters can host different view types in each pane.
Common pattern: Tree view + List view (like Explorer)
*/

class CExplorerFrame : public CFrameWnd
{
protected:
    CSplitterWnd m_wndSplitter;
    
    virtual BOOL OnCreateClient(LPCREATESTRUCT lpcs, CCreateContext* pContext);
    
    DECLARE_MESSAGE_MAP()
};

BOOL CExplorerFrame::OnCreateClient(LPCREATESTRUCT lpcs, CCreateContext* pContext)
{
    // Create 1x2 static splitter
    if (!m_wndSplitter.CreateStatic(this, 1, 2))
        return FALSE;
    
    // Create form view in left pane
    m_wndSplitter.CreateView(0, 0,
        RUNTIME_CLASS(CMyFormView),
        CSize(300, 100), pContext);
    
    // Create scroll view in right pane
    m_wndSplitter.CreateView(0, 1,
        RUNTIME_CLASS(CMyScrollView),
        CSize(300, 100), pContext);
    
    return TRUE;
}

// ============================================================================
// 5. NESTED SPLITTERS
// ============================================================================

/*
Splitters can be nested for complex layouts.
Create a splitter in a pane of another splitter.

Example: 2 rows x 1 col, with bottom row split into 1 row x 2 cols
*/

class CNestedSplitFrame : public CFrameWnd
{
protected:
    CSplitterWnd m_wndSplitter;      // Outer splitter
    CSplitterWnd m_wndSplitter2;     // Inner splitter
    
    virtual BOOL OnCreateClient(LPCREATESTRUCT lpcs, CCreateContext* pContext);
    
    DECLARE_MESSAGE_MAP()
};

BOOL CNestedSplitFrame::OnCreateClient(LPCREATESTRUCT lpcs, CCreateContext* pContext)
{
    // Create outer splitter: 2 rows, 1 column
    if (!m_wndSplitter.CreateStatic(this, 2, 1))
        return FALSE;
    
    // Create view in top pane
    m_wndSplitter.CreateView(0, 0,
        RUNTIME_CLASS(CMyTreeView),
        CSize(100, 200), pContext);
    
    // Create inner splitter in bottom pane
    if (!m_wndSplitter2.CreateStatic(
        &m_wndSplitter,     // Parent is the outer splitter
        1, 2,               // 1 row, 2 columns
        WS_CHILD | WS_VISIBLE,
        m_wndSplitter.IdFromRowCol(1, 0)))  // ID of bottom pane
    {
        return FALSE;
    }
    
    // Create views in inner splitter
    m_wndSplitter2.CreateView(0, 0,
        RUNTIME_CLASS(CMyListView),
        CSize(200, 100), pContext);
    
    m_wndSplitter2.CreateView(0, 1,
        CSize(200, 100), pContext);
    
    // Set initial sizes
    m_wndSplitter.SetRowInfo(0, 200, 50);   // Top pane
    m_wndSplitter.SetRowInfo(1, 300, 50);   // Bottom pane
    
    return TRUE;
}

// ============================================================================
// 6. ACCESSING SPLITTER PANES
// ============================================================================

/*
Access views in splitter panes for communication.
*/

void AccessSplitterPanes(CSplitterWnd* pSplitter)
{
    // Get view from specific pane
    CView* pView1 = (CView*)pSplitter->GetPane(0, 0);  // Row 0, Col 0
    CView* pView2 = (CView*)pSplitter->GetPane(0, 1);  // Row 0, Col 1
    
    // Get pane dimensions
    int cx, cy;
    pSplitter->GetColumnInfo(0, cx, cy);  // Column 0 info
    pSplitter->GetRowInfo(0, cx, cy);     // Row 0 info
    
    // Set pane dimensions
    pSplitter->SetColumnInfo(0, 300, 100);  // Width 300, min 100
    pSplitter->SetRowInfo(0, 200, 50);      // Height 200, min 50
    
    // Recalculate layout
    pSplitter->RecalcLayout();
    
    // Check if window is a pane
    BOOL bIsPane = pSplitter->IsChildPane(AfxGetMainWnd()->GetSafeHwnd());
    
    // Get ID from row/col
    int nID = pSplitter->IdFromRowCol(0, 0);
}

// ============================================================================
// 7. SPLITTER COMMUNICATION
// ============================================================================

/*
Views in different panes communicate through the document.
When one view changes data, it calls UpdateAllViews.
*/

void CMyTreeView::OnSelectionChanged(HTREEITEM hItem)
{
    // Get document
    CMyDocument* pDoc = (CMyDocument*)GetDocument();
    
    // Update document data
    pDoc->m_selectedItem = m_tree.GetItemData(hItem);
    
    // Notify other views (including list view in other pane)
    pDoc->UpdateAllViews(this);
}

void CMyListView::OnUpdate(CView* pSender, LPARAM lHint, CObject* pHint)
{
    // Update list view based on tree selection
    CMyDocument* pDoc = (CMyDocument*)GetDocument();
    
    // Refresh list based on selected item
    RefreshList(pDoc->m_selectedItem);
}

// ============================================================================
// 8. SPLITTER STYLES AND APPEARANCE
// ============================================================================

/*
Splitter window styles:
WS_CHILD | WS_VISIBLE - Standard
WS_BORDER - Border around splitter

Splitter bar appearance:
- Can be customized by overriding OnDrawSplitter()
- Default: 3D raised bar
- Can be flat, colored, or hidden

Custom splitter drawing:
virtual void OnDrawSplitter(CDC* pDC, ESplitType nType, const CRect& rect);
*/

// ============================================================================
// 9. BEST PRACTICES
// ============================================================================

/*
1. Use static splitters for fixed layouts
2. Use dynamic splitters for user-customizable layouts
3. Set minimum pane sizes to prevent hidden panes
4. Use nested splitters for complex layouts
5. Communicate between panes through the document
6. Use SetRowInfo/SetColumnInfo for initial sizes
7. Call RecalcLayout after changing pane sizes
8. Use IdFromRowCol for nested splitter IDs
9. Override OnDrawSplitter for custom appearance
10. Handle splitter bar double-click for auto-sizing
*/

BEGIN_MESSAGE_MAP(CMainFrame, CFrameWnd)
END_MESSAGE_MAP()

BEGIN_MESSAGE_MAP(CDynamicSplitFrame, CFrameWnd)
END_MESSAGE_MAP()

BEGIN_MESSAGE_MAP(CExplorerFrame, CFrameWnd)
END_MESSAGE_MAP()

BEGIN_MESSAGE_MAP(CNestedSplitFrame, CFrameWnd)
END_MESSAGE_MAP()

#endif // _MFC_VER
