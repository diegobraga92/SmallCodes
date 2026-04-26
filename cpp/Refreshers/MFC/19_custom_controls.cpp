// ============================================================================
// MFC CUSTOM CONTROLS AND SUBCLASSING
// File: 19_custom_controls.cpp
// Covers: owner-draw, custom drawing, subclassing, custom controls
// ============================================================================

#ifdef _MFC_VER

// ============================================================================
// 1. SUBCLASSING WINDOWS CONTROLS
// ============================================================================

/*
Subclassing replaces a control's window procedure with your own.
MFC provides two types:
1. Dynamic subclassing - Subclass existing control at runtime
2. Static subclassing - Via dialog data exchange (DDX_Control)

Key methods:
- SubclassDlgItem() - Subclass a dialog control
- SubclassWindow() - Subclass any window
- UnsubclassWindow() - Remove subclass
- PreSubclassWindow() - Called before subclassing
- WindowProc() - Custom window procedure
- DefWindowProc() - Default processing
*/

class CMyEdit : public CEdit
{
public:
    virtual void PreSubclassWindow();
    
protected:
    afx_msg void OnChar(UINT nChar, UINT nRepCnt, UINT nFlags);
    afx_msg void OnKeyDown(UINT nChar, UINT nRepCnt, UINT nFlags);
    afx_msg LRESULT OnPaste(WPARAM wParam, LPARAM lParam);
    
    DECLARE_MESSAGE_MAP()
};

void CMyEdit::PreSubclassWindow()
{
    // Set custom styles before subclassing
    ModifyStyle(0, ES_NUMBER);  // Only allow digits
    
    CEdit::PreSubclassWindow();
}

void CMyEdit::OnChar(UINT nChar, UINT nRepCnt, UINT nFlags)
{
    // Custom character handling
    if (nChar >= '0' && nChar <= '9')
    {
        CEdit::OnChar(nChar, nRepCnt, nFlags);
    }
    else if (nChar == VK_BACK || nChar == VK_DELETE)
    {
        CEdit::OnChar(nChar, nRepCnt, nFlags);
    }
    // Ignore other characters
}

void CMyEdit::OnKeyDown(UINT nChar, UINT nRepCnt, UINT nFlags)
{
    // Handle special keys
    if (nChar == VK_RETURN)
    {
        // Notify parent
        GetParent()->SendMessage(WM_COMMAND,
            MAKEWPARAM(GetDlgCtrlID(), EN_ENTER),
            (LPARAM)m_hWnd);
    }
    
    CEdit::OnKeyDown(nChar, nRepCnt, nFlags);
}

LRESULT CMyEdit::OnPaste(WPARAM wParam, LPARAM lParam)
{
    // Intercept paste to filter content
    if (OpenClipboard())
    {
        HGLOBAL hData = GetClipboardData(CF_TEXT);
        if (hData != nullptr)
        {
            char* pText = (char*)GlobalLock(hData);
            if (pText != nullptr)
            {
                // Filter pasted text
                CString filtered;
                for (int i = 0; pText[i] != '\0'; i++)
                {
                    if (pText[i] >= '0' && pText[i] <= '9')
                        filtered += pText[i];
                }
                
                // Set filtered text
                SetWindowText(filtered);
                GlobalUnlock(hData);
            }
        }
        CloseClipboard();
        return 0;
    }
    
    return Default();
}

// ============================================================================
// 2. OWNER-DRAW CONTROLS
// ============================================================================

/*
Owner-draw controls let you custom-draw the control appearance.

Steps:
1. Set owner-draw style (BS_OWNERDRAW for buttons)
2. Override DrawItem() or handle WM_DRAWITEM
3. Use DRAWITEMSTRUCT for drawing information

DRAWITEMSTRUCT members:
- CtlType - Control type (ODT_BUTTON, ODT_LISTBOX, etc.)
- CtlID - Control ID
- itemID - Item index
- itemAction - Drawing action
- itemState - Item state (selected, focused, etc.)
- hwndItem - Control window handle
- hDC - Device context
- rcItem - Drawing rectangle
- itemData - Application-defined data
*/

class COwnerDrawButton : public CButton
{
public:
    virtual void DrawItem(LPDRAWITEMSTRUCT lpDrawItemStruct);
    
    void SetColor(COLORREF color) { m_color = color; }
    void SetText(const CString& text) { m_text = text; }
    
protected:
    COLORREF m_color = RGB(0, 120, 215);
    CString m_text;
};

void COwnerDrawButton::DrawItem(LPDRAWITEMSTRUCT lpDrawItemStruct)
{
    CDC* pDC = CDC::FromHandle(lpDrawItemStruct->hDC);
    CRect rect = lpDrawItemStruct->rcItem;
    UINT state = lpDrawItemStruct->itemState;
    
    // Draw background
    if (state & ODS_SELECTED)
    {
        pDC->FillSolidRect(rect, RGB(0, 90, 180));
    }
    else if (state & ODS_DISABLED)
    {
        pDC->FillSolidRect(rect, RGB(200, 200, 200));
    }
    else
    {
        pDC->FillSolidRect(rect, m_color);
    }
    
    // Draw border
    if (state & ODS_FOCUS)
    {
        CPen pen(PS_SOLID, 2, RGB(0, 0, 0));
        CPen* pOldPen = pDC->SelectObject(&pen);
        pDC->SelectStockObject(NULL_BRUSH);
        pDC->Rectangle(rect);
        pDC->SelectObject(pOldPen);
    }
    
    // Draw text
    if (!m_text.IsEmpty())
    {
        pDC->SetBkMode(TRANSPARENT);
        pDC->SetTextColor(state & ODS_DISABLED ?
            RGB(128, 128, 128) : RGB(255, 255, 255));
        
        CFont* pOldFont = pDC->SelectObject(
            &afxGlobalData.fontRegular);
        
        pDC->DrawText(m_text, rect,
            DT_CENTER | DT_VCENTER | DT_SINGLELINE);
        
        pDC->SelectObject(pOldFont);
    }
}

// ============================================================================
// 3. CUSTOM DRAW (NM_CUSTOMDRAW)
// ============================================================================

/*
Custom draw allows customizing common controls without full owner-draw.
Supports list controls, tree controls, header controls, etc.

Notification stages:
- CDDS_PREPAINT - Before control draws
- CDDS_POSTPAINT - After control draws
- CDDS_PREERASE - Before erasing
- CDDS_POSTERASE - After erasing
- CDDS_ITEM - Item-specific
- CDDS_ITEMPREPAINT - Before item draws
- CDDS_ITEMPOSTPAINT - After item draws
- CDDS_SUBITEM - Subitem-specific
*/

class CMyListCtrl : public CListCtrl
{
protected:
    afx_msg void OnCustomDraw(NMHDR* pNMHDR, LRESULT* pResult);
    
    DECLARE_MESSAGE_MAP()
};

void CMyListCtrl::OnCustomDraw(NMHDR* pNMHDR, LRESULT* pResult)
{
    NMLVCUSTOMDRAW* pLVCD = reinterpret_cast<NMLVCUSTOMDRAW*>(pNMHDR);
    *pResult = CDRF_DODEFAULT;
    
    switch (pLVCD->nmcd.dwDrawStage)
    {
    case CDDS_PREPAINT:
        // Request item notifications
        *pResult = CDRF_NOTIFYITEMDRAW;
        break;
        
    case CDDS_ITEMPREPAINT:
        // Customize item appearance
        if (pLVCD->nmcd.dwItemSpec % 2 == 0)
        {
            // Alternate row color
            pLVCD->clrTextBk = RGB(240, 248, 255);  // Light blue
        }
        
        // Request subitem notifications
        *pResult = CDRF_NOTIFYSUBITEMDRAW;
        break;
        
    case CDDS_SUBITEM | CDDS_ITEMPREPAINT:
        // Customize subitem
        if (pLVCD->iSubItem == 1)  // Second column
        {
            pLVCD->clrText = RGB(0, 0, 255);  // Blue text
        }
        break;
    }
}

// ============================================================================
// 4. CUSTOM CONTROL FROM SCRATCH
// ============================================================================

/*
Creating a custom control from scratch:
1. Derive from CWnd
2. Register window class
3. Handle WM_PAINT, WM_LBUTTONDOWN, etc.
4. Provide custom properties and methods
*/

class CGaugeControl : public CWnd
{
public:
    CGaugeControl();
    
    BOOL Create(DWORD dwStyle, const CRect& rect,
        CWnd* pParentWnd, UINT nID);
    
    void SetRange(int nMin, int nMax);
    void SetPos(int nPos);
    void SetColor(COLORREF color);
    
    int GetPos() const { return m_nPos; }
    
protected:
    int m_nMin, m_nMax, m_nPos;
    COLORREF m_color;
    
    afx_msg void OnPaint();
    afx_msg LRESULT OnSetFont(WPARAM wParam, LPARAM lParam);
    
    DECLARE_MESSAGE_MAP()
};

CGaugeControl::CGaugeControl()
    : m_nMin(0), m_nMax(100), m_nPos(0)
    , m_color(RGB(0, 255, 0))
{
}

BOOL CGaugeControl::Create(DWORD dwStyle, const CRect& rect,
    CWnd* pParentWnd, UINT nID)
{
    // Register window class
    static CString className = AfxRegisterWndClass(
        CS_HREDRAW | CS_VREDRAW,
        AfxGetApp()->LoadStandardCursor(IDC_ARROW),
        (HBRUSH)(COLOR_WINDOW + 1),
        nullptr);
    
    return CWnd::Create(className, _T("Gauge"),
        dwStyle, rect, pParentWnd, nID);
}

void CGaugeControl::SetRange(int nMin, int nMax)
{
    m_nMin = nMin;
    m_nMax = nMax;
    Invalidate();
}

void CGaugeControl::SetPos(int nPos)
{
    m_nPos = max(m_nMin, min(m_nMax, nPos));
    Invalidate();
}

void CGaugeControl::SetColor(COLORREF color)
{
    m_color = color;
    Invalidate();
}

void CGaugeControl::OnPaint()
{
    CPaintDC dc(this);
    
    CRect rect;
    GetClientRect(&rect);
    
    // Draw border
    dc.DrawEdge(rect, EDGE_SUNKEN, BF_RECT);
    
    // Calculate fill area
    rect.DeflateRect(2, 2);
    int fillWidth = (rect.Width() * (m_nPos - m_nMin)) /
        (m_nMax - m_nMin);
    
    // Draw filled portion
    if (fillWidth > 0)
    {
        CRect fillRect(rect.left, rect.top,
            rect.left + fillWidth, rect.bottom);
        dc.FillSolidRect(fillRect, m_color);
    }
    
    // Draw empty portion
    if (fillWidth < rect.Width())
    {
        CRect emptyRect(rect.left + fillWidth, rect.top,
            rect.right, rect.bottom);
        dc.FillSolidRect(emptyRect, RGB(255, 255, 255));
    }
    
    // Draw percentage text
    CString text;
    text.Format(_T("%d%%"), (m_nPos * 100) / (m_nMax - m_nMin));
    dc.SetBkMode(TRANSPARENT);
    dc.DrawText(text, rect,
        DT_CENTER | DT_VCENTER | DT_SINGLELINE);
}

LRESULT CGaugeControl::OnSetFont(WPARAM wParam, LPARAM lParam)
{
    Invalidate();
    return Default();
}

// ============================================================================
// 5. USING CUSTOM CONTROLS
// ============================================================================

void CustomControlUsage(CWnd* pParent)
{
    // Subclass existing edit control
    CMyEdit* pEdit = new CMyEdit();
    pEdit->SubclassDlgItem(IDC_MY_EDIT, pParent);
    
    // Owner-draw button
    COwnerDrawButton* pButton = new COwnerDrawButton();
    pButton->Create(_T("Custom"),
        WS_CHILD | WS_VISIBLE | BS_OWNERDRAW,
        CRect(10, 10, 100, 30), pParent, IDC_MY_BUTTON);
    pButton->SetColor(RGB(0, 150, 0));
    pButton->SetText(_T("Click Me"));
    
    // Custom gauge control
    CGaugeControl* pGauge = new CGaugeControl();
    pGauge->Create(WS_CHILD | WS_VISIBLE,
        CRect(10, 50, 200, 80), pParent, IDC_MY_GAUGE);
    pGauge->SetRange(0, 100);
    pGauge->SetPos(75);
    pGauge->SetColor(RGB(0, 200, 0));
}

// ============================================================================
// 6. BEST PRACTICES
// ============================================================================

/*
1. Use SubclassDlgItem for modifying existing controls
2. Use PreSubclassWindow for initialization
3. Use owner-draw for completely custom appearance
4. Use custom draw for partial customization
5. Register window class for custom controls
6. Handle WM_PAINT for custom drawing
7. Use DRAWITEMSTRUCT for owner-draw information
8. Use NM_CUSTOMDRAW for common control customization
9. Invalidate() after property changes
10. Clean up subclassed windows in DestroyWindow()
*/

BEGIN_MESSAGE_MAP(CMyEdit, CEdit)
    ON_WM_CHAR()
    ON_WM_KEYDOWN()
    ON_MESSAGE(WM_PASTE, OnPaste)
END_MESSAGE_MAP()

BEGIN_MESSAGE_MAP(CMyListCtrl, CListCtrl)
    ON_NOTIFY_REFLECT(NM_CUSTOMDRAW, OnCustomDraw)
END_MESSAGE_MAP()

BEGIN_MESSAGE_MAP(CGaugeControl, CWnd)
    ON_WM_PAINT()
    ON_WM_SETFONT()
END_MESSAGE_MAP()

#endif // _MFC_VER
