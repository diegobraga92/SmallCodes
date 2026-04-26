// ============================================================================
// MFC MESSAGE MAP SYSTEM
// File: 01_message_map_system.cpp
// Covers: Message maps, command routing, ON_WM_*, ON_COMMAND, ON_BN_CLICKED
// ============================================================================

#ifdef _MFC_VER

// ============================================================================
// 1. MESSAGE MAP FUNDAMENTALS
// ============================================================================

/*
MFC uses message maps instead of the traditional Windows giant switch statement
in WndProc. Message maps are macros that create a static table mapping Windows
messages to class member functions.

Key concepts:
- DECLARE_MESSAGE_MAP() - Goes in class declaration (header)
- BEGIN_MESSAGE_MAP() / END_MESSAGE_MAP() - Goes in implementation (.cpp)
- Each ON_* macro maps a message to a handler function
- Message maps are inherited - child classes can override parent handlers
- Multiple message map entries can map to the same handler
*/

// ============================================================================
// 2. MESSAGE MAP MACROS BY CATEGORY
// ============================================================================

/*
Standard Windows Messages (ON_WM_*):
ON_WM_PAINT()       -> void OnPaint()
ON_WM_SIZE()        -> void OnSize(UINT nType, int cx, int cy)
ON_WM_CLOSE()       -> void OnClose()
ON_WM_DESTROY()     -> void OnDestroy()
ON_WM_CREATE()      -> int OnCreate(LPCREATESTRUCT lpCreateStruct)
ON_WM_LBUTTONDOWN() -> void OnLButtonDown(UINT nFlags, CPoint point)
ON_WM_RBUTTONDOWN() -> void OnRButtonDown(UINT nFlags, CPoint point)
ON_WM_MOUSEMOVE()   -> void OnMouseMove(UINT nFlags, CPoint point)
ON_WM_KEYDOWN()     -> void OnKeyDown(UINT nChar, UINT nRepCnt, UINT nFlags)
ON_WM_CHAR()        -> void OnChar(UINT nChar, UINT nRepCnt, UINT nFlags)
ON_WM_TIMER()       -> void OnTimer(UINT_PTR nIDEvent)
ON_WM_HSCROLL()     -> void OnHScroll(UINT nSBCode, UINT nPos, CScrollBar* pScrollBar)
ON_WM_VSCROLL()     -> void OnVScroll(UINT nSBCode, UINT nPos, CScrollBar* pScrollBar)
ON_WM_ERASEBKGND()  -> BOOL OnEraseBkgnd(CDC* pDC)
ON_WM_SETCURSOR()   -> BOOL OnSetCursor(CWnd* pWnd, UINT nHitTest, UINT message)
ON_WM_NCHITTEST()   -> LRESULT OnNcHitTest(CPoint point)
ON_WM_CTLCOLOR()    -> HBRUSH OnCtlColor(CDC* pDC, CWnd* pWnd, UINT nCtlColor)
ON_WM_DROPFILES()   -> void OnDropFiles(HDROP hDropInfo)
ON_WM_MOUSEWHEEL()  -> BOOL OnMouseWheel(UINT nFlags, short zDelta, CPoint pt)

Command Messages:
ON_COMMAND(id, handler)           -> void OnCommandHandler()
ON_COMMAND_EX(id, handler)        -> BOOL OnCommandHandler(UINT nID)
ON_UPDATE_COMMAND_UI(id, handler) -> void OnUpdateHandler(CCmdUI* pCmdUI)

Control Notification Messages:
ON_BN_CLICKED(id, handler)       -> Button clicked
ON_BN_DOUBLECLICKED(id, handler) -> Button double-clicked
ON_EN_CHANGE(id, handler)        -> Edit control text changed
ON_EN_UPDATE(id, handler)        -> Edit control about to display changed text
ON_EN_SETFOCUS(id, handler)      -> Edit control got focus
ON_EN_KILLFOCUS(id, handler)     -> Edit control lost focus
ON_CBN_SELCHANGE(id, handler)    -> Combo box selection changed
ON_CBN_EDITCHANGE(id, handler)   -> Combo box edit text changed
ON_CBN_DROPDOWN(id, handler)     -> Combo box dropdown opened
ON_LBN_SELCHANGE(id, handler)    -> List box selection changed
ON_LBN_DBLCLK(id, handler)       -> List box double-clicked
ON_STN_CLICKED(id, handler)      -> Static control clicked
ON_NOTIFY(id, handler)           -> Generic notification (NM_* codes)
ON_NOTIFY_RANGE(id, handler)     -> Notification from range of IDs

Reflected Messages (for parent reflection):
ON_CONTROL_REFLECT(id, handler)  -> Reflect notification back to control
ON_NOTIFY_REFLECT(id, handler)   -> Reflect notify back to control
ON_WM_CTLCOLOR_REFLECT()         -> Reflect WM_CTLCOLOR
*/

// ============================================================================
// 3. MESSAGE MAP EXAMPLE
// ============================================================================

class CMyFrameWnd : public CFrameWnd
{
public:
    // Window messages
    afx_msg void OnPaint();
    afx_msg void OnSize(UINT nType, int cx, int cy);
    afx_msg void OnClose();
    afx_msg int OnCreate(LPCREATESTRUCT lpCreateStruct);
    afx_msg void OnLButtonDown(UINT nFlags, CPoint point);
    afx_msg void OnMouseMove(UINT nFlags, CPoint point);
    afx_msg void OnKeyDown(UINT nChar, UINT nRepCnt, UINT nFlags);
    afx_msg void OnTimer(UINT_PTR nIDEvent);
    
    // Command handlers
    afx_msg void OnFileNew();
    afx_msg void OnFileOpen();
    afx_msg void OnFileSave();
    afx_msg void OnAppAbout();
    afx_msg void OnEditCopy();
    afx_msg void OnEditPaste();
    
    // Command UI handlers (for enabling/disabling menu items)
    afx_msg void OnUpdateEditCopy(CCmdUI* pCmdUI);
    afx_msg void OnUpdateEditPaste(CCmdUI* pCmdUI);
    
    // Control notification handlers
    afx_msg void OnBnClickedOk();
    afx_msg void OnBnClickedCancel();
    afx_msg void OnEnChangeName();
    afx_msg void OnCbnSelchangeCategory();
    
    DECLARE_MESSAGE_MAP()
};

// ============================================================================
// 4. MESSAGE MAP IMPLEMENTATION
// ============================================================================

BEGIN_MESSAGE_MAP(CMyFrameWnd, CFrameWnd)
    // Standard Windows messages
    ON_WM_PAINT()
    ON_WM_SIZE()
    ON_WM_CLOSE()
    ON_WM_CREATE()
    ON_WM_LBUTTONDOWN()
    ON_WM_MOUSEMOVE()
    ON_WM_KEYDOWN()
    ON_WM_TIMER()
    
    // File menu commands
    ON_COMMAND(ID_FILE_NEW, &CMyFrameWnd::OnFileNew)
    ON_COMMAND(ID_FILE_OPEN, &CMyFrameWnd::OnFileOpen)
    ON_COMMAND(ID_FILE_SAVE, &CMyFrameWnd::OnFileSave)
    ON_COMMAND(ID_APP_ABOUT, &CMyFrameWnd::OnAppAbout)
    
    // Edit menu commands
    ON_COMMAND(ID_EDIT_COPY, &CMyFrameWnd::OnEditCopy)
    ON_COMMAND(ID_EDIT_PASTE, &CMyFrameWnd::OnEditPaste)
    
    // Command UI handlers
    ON_UPDATE_COMMAND_UI(ID_EDIT_COPY, &CMyFrameWnd::OnUpdateEditCopy)
    ON_UPDATE_COMMAND_UI(ID_EDIT_PASTE, &CMyFrameWnd::OnUpdateEditPaste)
    
    // Control notifications
    ON_BN_CLICKED(IDOK, &CMyFrameWnd::OnBnClickedOk)
    ON_BN_CLICKED(IDCANCEL, &CMyFrameWnd::OnBnClickedCancel)
    ON_EN_CHANGE(IDC_NAME_EDIT, &CMyFrameWnd::OnEnChangeName)
    ON_CBN_SELCHANGE(IDC_CATEGORY_COMBO, &CMyFrameWnd::OnCbnSelchangeCategory)
END_MESSAGE_MAP()

// ============================================================================
// 5. HANDLER IMPLEMENTATIONS
// ============================================================================

void CMyFrameWnd::OnPaint()
{
    // Standard WM_PAINT handling
    CPaintDC dc(this);  // Device context for painting
    
    // Custom drawing code here
    CRect rect;
    GetClientRect(&rect);
    dc.DrawText(_T("Hello MFC"), -1, &rect, DT_CENTER | DT_VCENTER | DT_SINGLELINE);
    
    // Do not call CFrameWnd::OnPaint() for custom painting
}

void CMyFrameWnd::OnSize(UINT nType, int cx, int cy)
{
    CFrameWnd::OnSize(nType, cx, cy);  // Call base class
    
    // Resize child windows here
    // Example: Resize a child edit control to fill the client area
    CWnd* pEdit = GetDlgItem(IDC_EDIT1);
    if (pEdit != nullptr)
    {
        pEdit->SetWindowPos(nullptr, 0, 0, cx, cy, SWP_NOZORDER);
    }
}

void CMyFrameWnd::OnClose()
{
    // Ask user before closing
    if (AfxMessageBox(_T("Are you sure you want to close?"), MB_YESNO) == IDYES)
    {
        CFrameWnd::OnClose();  // Let default handler close the window
    }
    // If user clicked No, do nothing
}

int CMyFrameWnd::OnCreate(LPCREATESTRUCT lpCreateStruct)
{
    if (CFrameWnd::OnCreate(lpCreateStruct) == -1)
        return -1;  // Base class creation failed
    
    // Create child controls here
    // Example: Create an edit control
    // m_edit.Create(WS_CHILD | WS_VISIBLE | ES_MULTILINE, 
    //               CRect(10, 10, 200, 100), this, IDC_EDIT1);
    
    // Set a timer
    SetTimer(1, 1000, nullptr);  // Timer ID 1, fires every 1000ms
    
    return 0;  // Success
}

void CMyFrameWnd::OnLButtonDown(UINT nFlags, CPoint point)
{
    // Handle left mouse button click
    CString msg;
    msg.Format(_T("Mouse clicked at (%d, %d)"), point.x, point.y);
    SetWindowText(msg);
    
    CFrameWnd::OnLButtonDown(nFlags, point);
}

void CMyFrameWnd::OnMouseMove(UINT nFlags, CPoint point)
{
    // Track mouse movement (only if mouse button is down)
    if (nFlags & MK_LBUTTON)
    {
        // Dragging with left button
        CClientDC dc(this);
        dc.SetPixel(point, RGB(255, 0, 0));  // Draw a red pixel
    }
    
    CFrameWnd::OnMouseMove(nFlags, point);
}

void CMyFrameWnd::OnKeyDown(UINT nChar, UINT nRepCnt, UINT nFlags)
{
    // Handle keyboard input
    switch (nChar)
    {
    case VK_ESCAPE:
        PostMessage(WM_CLOSE);  // ESC closes the window
        break;
    case VK_F1:
        AfxMessageBox(_T("Help not available"));
        break;
    case 'A':
        // Handle 'A' key
        break;
    }
    
    CFrameWnd::OnKeyDown(nChar, nRepCnt, nFlags);
}

void CMyFrameWnd::OnTimer(UINT_PTR nIDEvent)
{
    // Timer fired
    if (nIDEvent == 1)
    {
        // Update clock or perform periodic task
        // Invalidate() to trigger repaint
    }
    
    CFrameWnd::OnTimer(nIDEvent);
}

// ============================================================================
// 6. COMMAND HANDLERS
// ============================================================================

void CMyFrameWnd::OnFileNew()
{
    // Create a new document/file
    AfxMessageBox(_T("File > New clicked"));
}

void CMyFrameWnd::OnFileOpen()
{
    // Open file dialog
    CFileDialog dlg(TRUE, _T("txt"), nullptr,
        OFN_HIDEREADONLY | OFN_FILEMUSTEXIST,
        _T("Text Files (*.txt)|*.txt|All Files (*.*)|*.*||"));
    
    if (dlg.DoModal() == IDOK)
    {
        CString pathName = dlg.GetPathName();
        // Open and read the file
    }
}

void CMyFrameWnd::OnFileSave()
{
    // Save file dialog
    CFileDialog dlg(FALSE, _T("txt"), nullptr,
        OFN_HIDEREADONLY | OFN_OVERWRITEPROMPT,
        _T("Text Files (*.txt)|*.txt|All Files (*.*)|*.*||"));
    
    if (dlg.DoModal() == IDOK)
    {
        CString pathName = dlg.GetPathName();
        // Save data to the file
    }
}

void CMyFrameWnd::OnAppAbout()
{
    // Show About dialog
    AfxMessageBox(_T("MFC Application v1.0\nCopyright 2024"));
}

void CMyFrameWnd::OnEditCopy()
{
    // Copy selected text to clipboard
    AfxMessageBox(_T("Copy"));
}

void CMyFrameWnd::OnEditPaste()
{
    // Paste from clipboard
    AfxMessageBox(_T("Paste"));
}

// ============================================================================
// 7. COMMAND UI HANDLERS
// ============================================================================

/*
Command UI handlers update the state of menu items and toolbar buttons.
They are called when the menu is displayed or when idle.

CCmdUI methods:
- Enable(BOOL bOn) - Enable/disable the item
- SetCheck(int nCheck) - Check/uncheck (0=unchecked, 1=checked, 2=indeterminate)
- SetRadio(BOOL bOn) - Set radio button state
- SetText(LPCTSTR lpszText) - Change item text
*/

void CMyFrameWnd::OnUpdateEditCopy(CCmdUI* pCmdUI)
{
    // Enable Copy only if text is selected
    // pCmdUI->Enable(m_edit.GetSelLength() > 0);
    pCmdUI->Enable(TRUE);  // Always enabled for now
}

void CMyFrameWnd::OnUpdateEditPaste(CCmdUI* pCmdUI)
{
    // Enable Paste only if clipboard has text
    pCmdUI->Enable(::IsClipboardFormatAvailable(CF_TEXT));
}

// ============================================================================
// 8. CONTROL NOTIFICATION HANDLERS
// ============================================================================

void CMyFrameWnd::OnBnClickedOk()
{
    // OK button clicked
    AfxMessageBox(_T("OK clicked"));
}

void CMyFrameWnd::OnBnClickedCancel()
{
    // Cancel button clicked
    AfxMessageBox(_T("Cancel clicked"));
}

void CMyFrameWnd::OnEnChangeName()
{
    // Edit control text changed
    // Get the new text
    CString name;
    GetDlgItemText(IDC_NAME_EDIT, name);
    
    // Update UI based on input
    GetDlgItem(IDOK)->EnableWindow(!name.IsEmpty());
}

void CMyFrameWnd::OnCbnSelchangeCategory()
{
    // Combo box selection changed
    CComboBox* pCombo = (CComboBox*)GetDlgItem(IDC_CATEGORY_COMBO);
    int sel = pCombo->GetCurSel();
    
    if (sel != CB_ERR)
    {
        CString text;
        pCombo->GetLBText(sel, text);
        AfxMessageBox(_T("Selected: ") + text);
    }
}

// ============================================================================
// 9. MESSAGE ROUTING AND COMMAND TARGETS
// ============================================================================

/*
MFC command routing order for SDI applications:

1. Active child frame window (if MDI)
2. Active view
3. Active document
4. Document template
5. Main frame window
6. Application object

For MDI applications:
1. Active MDI child frame
2. Active view
3. Active document
4. Document template
5. MDI main frame (CMDIFrameWnd)
6. Application object

This routing allows any class in the chain to handle a command.
If no handler is found, the command is disabled automatically.
*/

// ============================================================================
// 10. CUSTOM MESSAGES
// ============================================================================

/*
Defining custom Windows messages:

#define WM_MY_CUSTOM_MESSAGE (WM_APP + 100)

// In class declaration:
afx_msg LRESULT OnMyCustomMessage(WPARAM wParam, LPARAM lParam);

// In message map:
ON_MESSAGE(WM_MY_CUSTOM_MESSAGE, &CMyFrameWnd::OnMyCustomMessage)

// Sending custom messages:
// SendMessage(WM_MY_CUSTOM_MESSAGE, wParam, lParam);  // Synchronous
// PostMessage(WM_MY_CUSTOM_MESSAGE, wParam, lParam);  // Asynchronous

User-defined message ranges:
WM_APP to 0xBFFF     - Application-defined messages
WM_USER to 0x7FFF    - Control-defined messages (unique per window class)
RegisterWindowMessage - System-wide unique messages
*/

// ============================================================================
// 11. BEST PRACTICES
// ============================================================================

/*
1. Always call base class handler for standard messages (WM_SIZE, WM_CREATE, etc.)
2. Use afx_msg in handler declarations (documentation only, not enforced)
3. Keep message map entries in logical groups
4. Use ON_UPDATE_COMMAND_UI for enabling/disabling, not manual EnableWindow
5. Use ON_COMMAND_EX for multiple commands sharing one handler
6. Use ON_NOTIFY for common control notifications (NM_* codes)
7. Use RegisterWindowMessage for inter-application messages
8. Use PostMessage (async) instead of SendMessage (sync) when possible
9. Check return values from message handlers
10. Use ON_CONTROL_REFLECT for self-drawing controls
*/

#endif // _MFC_VER
