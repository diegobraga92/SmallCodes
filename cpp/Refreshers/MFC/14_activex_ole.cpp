// ============================================================================
// MFC ACTIVEX AND OLE
// File: 14_activex_ole.cpp
// Covers: COleControl, COleDocument, drag/drop, clipboard, embedding
// ============================================================================

#ifdef _MFC_VER

// ============================================================================
// 1. OLE OVERVIEW
// ============================================================================

/*
OLE (Object Linking and Embedding) enables:
- Compound documents (embedding/linking)
- Drag and drop
- Clipboard operations
- Automation (COM)
- ActiveX controls

Key classes:
- COleDocument - Document with OLE support
- COleLinkingDoc - Document with linking support
- COleServerDoc - Server-side document
- COleClientItem - Client-side embedded/linked item
- COleServerItem - Server-side item
- COleDropTarget - Drag/drop target
- COleDataSource - Data source for clipboard/drag
- COleDataObject - Data object for clipboard/drag
- COleInsertDialog - Insert Object dialog
- COlePasteSpecialDialog - Paste Special dialog
- COleConvertDialog - Convert dialog
*/

// ============================================================================
// 2. OLE DOCUMENTS
// ============================================================================

/*
COleDocument extends CDocument with OLE container support.
COleLinkingDoc adds linking support.
COleServerDoc adds server support.

Key methods:
- GetNextItem() - Iterate OLE items
- GetStartPosition() - Start iteration
- GetNextClientItem() - Get next client item
- GetNextServerItem() - Get next server item
- NotifyAllItems() - Notify all items
- UpdateAllItems() - Update all items
*/

class CMyOleDocument : public COleDocument
{
    DECLARE_DYNCREATE(CMyOleDocument)
    
public:
    virtual BOOL OnNewDocument();
    virtual void Serialize(CArchive& ar);
    
protected:
    DECLARE_MESSAGE_MAP()
};

IMPLEMENT_DYNCREATE(CMyOleDocument, COleDocument)

BOOL CMyOleDocument::OnNewDocument()
{
    if (!COleDocument::OnNewDocument())
        return FALSE;
    
    // Enable compound document support
    // EnableDocking(CBRS_ALIGN_ANY);
    
    return TRUE;
}

void CMyOleDocument::Serialize(CArchive& ar)
{
    if (ar.IsStoring())
    {
        // Store document data
    }
    else
    {
        // Load document data
    }
    
    // Serialize OLE items
    COleDocument::Serialize(ar);
}

// ============================================================================
// 3. OLE CLIENT ITEMS
// ============================================================================

/*
COleClientItem represents an embedded or linked object in a container.

Key methods:
- CreateFromFile() - Create from file
- CreateFromClipboard() - Create from clipboard
- CreateStaticFromClipboard() - Create static from clipboard
- CreateLinkFromClipboard() - Create link from clipboard
- CreateNewItem() - Create new embedded object
- GetDocument() - Get parent document
- GetActiveView() - Get active view
- Activate() - Activate object
- Deactivate() - Deactivate object
- DoVerb() - Execute verb (open, edit, etc.)
- CopyToClipboard() - Copy to clipboard
- Draw() - Draw object
- SetItemRects() - Set position rectangles
- GetExtent() / SetExtent() - Object size
- IsModified() - Check if modified
*/

class CMyOleClientItem : public COleClientItem
{
    DECLARE_SERIAL(CMyOleClientItem)
    
public:
    CMyOleClientItem(CMyOleDocument* pContainer = nullptr);
    
    virtual void OnChange(OLE_NOTIFICATION nCode, DWORD dwParam);
    virtual void OnActivate();
    virtual void OnDeactivateUI(BOOL bUndoable);
    virtual BOOL OnChangeItemPosition(const CRect& rectPos);
    
    void Serialize(CArchive& ar);
    
    // Position
    CRect m_rect;
};

IMPLEMENT_SERIAL(CMyOleClientItem, COleClientItem, 0)

CMyOleClientItem::CMyOleClientItem(CMyOleDocument* pContainer /*= nullptr*/)
    : COleClientItem(pContainer)
{
}

void CMyOleClientItem::OnChange(OLE_NOTIFICATION nCode, DWORD dwParam)
{
    // Notify view to repaint
    GetDocument()->UpdateAllViews(nullptr);
    
    COleClientItem::OnChange(nCode, dwParam);
}

void CMyOleClientItem::OnActivate()
{
    // Object is being activated
    COleClientItem::OnActivate();
}

void CMyOleClientItem::OnDeactivateUI(BOOL bUndoable)
{
    COleClientItem::OnDeactivateUI(bUndoable);
    
    // Hide toolbars, etc.
}

BOOL CMyOleClientItem::OnChangeItemPosition(const CRect& rectPos)
{
    m_rect = rectPos;
    return COleClientItem::OnChangeItemPosition(rectPos);
}

void CMyOleClientItem::Serialize(CArchive& ar)
{
    COleClientItem::Serialize(ar);
    
    if (ar.IsStoring())
    {
        ar << m_rect;
    }
    else
    {
        ar >> m_rect;
    }
}

// ============================================================================
// 4. INSERT OBJECT DIALOG
// ============================================================================

/*
Standard OLE dialogs:
- COleInsertDialog - Insert Object (Create New/Create from File)
- COlePasteSpecialDialog - Paste Special
- COleConvertDialog - Convert
- COleChangeIconDialog - Change Icon
- COleLinksDialog - Edit Links
- COleUpdateDialog - Update Links
- COleBusyDialog - Server Busy
- COlePropertiesDialog - Object Properties
*/

void InsertObjectDialog(CView* pView)
{
    COleInsertDialog dlg;
    
    if (dlg.DoModal() == IDOK)
    {
        CMyOleDocument* pDoc = (CMyOleDocument*)pView->GetDocument();
        
        // Create new client item
        CMyOleClientItem* pItem = new CMyOleClientItem(pDoc);
        
        if (!dlg.CreateItem(pItem))
        {
            delete pItem;
            return;
        }
        
        // Set item position
        pItem->m_rect.SetRect(10, 10, 200, 200);
        pItem->SetItemRects(pItem->m_rect);
        
        // Update document
        pDoc->UpdateAllViews(nullptr);
        pDoc->SetModifiedFlag();
    }
}

// ============================================================================
// 5. DRAG AND DROP
// ============================================================================

/*
COleDropTarget enables a window as a drop target.
COleDataSource provides data for drag source.

Key methods:
- COleDropTarget::Register() - Register as drop target
- COleDropTarget::Revoke() - Unregister
- OnDragEnter() - Drag enters window
- OnDragOver() - Drag over window
- OnDragScroll() - Auto-scroll
- OnDropEx() - Drop (extended)
- OnDrop() - Drop
- COleDataSource::CacheGlobalData() - Cache data
- COleDataSource::DoDragDrop() - Start drag
*/

class CDropTargetView : public CView
{
public:
    COleDropTarget m_dropTarget;
    
    virtual void OnInitialUpdate();
    
protected:
    virtual DROPEFFECT OnDragEnter(COleDataObject* pDataObject,
        DWORD dwKeyState, CPoint point);
    virtual DROPEFFECT OnDragOver(COleDataObject* pDataObject,
        DWORD dwKeyState, CPoint point);
    virtual BOOL OnDrop(COleDataObject* pDataObject,
        DROPEFFECT dropEffect, CPoint point);
    
    DECLARE_MESSAGE_MAP()
};

void CDropTargetView::OnInitialUpdate()
{
    CView::OnInitialUpdate();
    
    // Register as drop target
    m_dropTarget.Register(this);
}

DROPEFFECT CDropTargetView::OnDragEnter(COleDataObject* pDataObject,
    DWORD dwKeyState, CPoint point)
{
    // Check if data format is acceptable
    if (pDataObject->IsDataAvailable(CF_TEXT))
        return DROPEFFECT_COPY;
    
    return DROPEFFECT_NONE;
}

DROPEFFECT CDropTargetView::OnDragOver(COleDataObject* pDataObject,
    DWORD dwKeyState, CPoint point)
{
    // Check key state for copy/move
    if (dwKeyState & MK_CONTROL)
        return DROPEFFECT_COPY;
    
    return DROPEFFECT_MOVE;
}

BOOL CDropTargetView::OnDrop(COleDataObject* pDataObject,
    DROPEFFECT dropEffect, CPoint point)
{
    // Get data
    HGLOBAL hGlobal = pDataObject->GetGlobalData(CF_TEXT);
    if (hGlobal == nullptr)
        return FALSE;
    
    // Lock and read data
    LPCSTR pText = (LPCSTR)GlobalLock(hGlobal);
    if (pText != nullptr)
    {
        // Process dropped text
        CString text(pText);
        GlobalUnlock(hGlobal);
    }
    
    GlobalFree(hGlobal);
    return TRUE;
}

// ============================================================================
// 6. CLIPBOARD OPERATIONS
// ============================================================================

/*
OLE clipboard operations use COleDataSource and COleDataObject.

Key methods:
- COleDataSource::CacheGlobalData() - Cache data
- COleDataSource::SetClipboard() - Copy to clipboard
- COleDataSource::DoDragDrop() - Start drag
- COleDataObject::AttachClipboard() - Attach clipboard
- COleDataObject::IsDataAvailable() - Check format
- COleDataObject::GetGlobalData() - Get data
*/

void CopyToClipboard(CView* pView)
{
    COleDataSource* pSource = new COleDataSource();
    
    // Cache data
    CString text = _T("Sample text");
    HGLOBAL hGlobal = GlobalAlloc(GMEM_MOVEABLE, (text.GetLength() + 1) * sizeof(TCHAR));
    if (hGlobal != nullptr)
    {
        LPTSTR pData = (LPTSTR)GlobalLock(hGlobal);
        lstrcpy(pData, text);
        GlobalUnlock(hGlobal);
        
        pSource->CacheGlobalData(CF_TEXT, hGlobal);
    }
    
    // Copy to clipboard
    pSource->SetClipboard();
}

void PasteFromClipboard()
{
    COleDataObject dataObject;
    dataObject.AttachClipboard();
    
    // Check for text
    if (dataObject.IsDataAvailable(CF_TEXT))
    {
        HGLOBAL hGlobal = dataObject.GetGlobalData(CF_TEXT);
        if (hGlobal != nullptr)
        {
            LPCSTR pText = (LPCSTR)GlobalLock(hGlobal);
            if (pText != nullptr)
            {
                CString text(pText);
                GlobalUnlock(hGlobal);
            }
            GlobalFree(hGlobal);
        }
    }
}

// ============================================================================
// 7. ACTIVEX CONTROLS
// ============================================================================

/*
ActiveX controls are COM components that can be embedded in dialogs.
Use CWnd::CreateControl() or dialog editor to add ActiveX controls.

Key methods:
- CWnd::CreateControl() - Create ActiveX control
- CWnd::GetControlUnknown() - Get IUnknown pointer
- CWnd::InvokeHelper() - Call method/property
- CWnd::SetProperty() - Set property
- CWnd::GetProperty() - Get property
*/

void ActiveXControlExample(CWnd* pParent)
{
    // Create WebBrowser control
    // CLSID for WebBrowser: {8856F961-340A-11D0-A96B-00C04FD705A2}
    
    CRect rect(10, 10, 400, 300);
    
    if (m_webControl.CreateControl(
        _T("{8856F961-340A-11D0-A96B-00C04FD705A2}"),
        _T(""), WS_VISIBLE | WS_CHILD, rect, pParent, IDC_WEBBROWSER))
    {
        // Navigate to URL
        m_webControl.InvokeHelper(DISPID_NAVIGATE,
            DISPATCH_METHOD, VT_EMPTY, nullptr,
            _T("https://www.example.com"));
    }
}

// ============================================================================
// 8. BEST PRACTICES
// ============================================================================

/*
1. Use COleDocument for compound document support
2. Use COleInsertDialog for Insert Object
3. Register drop targets in OnInitialUpdate()
4. Check data availability before accepting drops
5. Use CacheGlobalData for clipboard operations
6. Handle OnChange in client items for repainting
7. Use SetItemRects for object positioning
8. Serialize OLE items with base class Serialize()
9. Use COlePasteSpecialDialog for paste options
10. Handle OLE server busy conditions gracefully
*/

BEGIN_MESSAGE_MAP(CMyOleDocument, COleDocument)
END_MESSAGE_MAP()

BEGIN_MESSAGE_MAP(CDropTargetView, CView)
END_MESSAGE_MAP()

#endif // _MFC_VER
