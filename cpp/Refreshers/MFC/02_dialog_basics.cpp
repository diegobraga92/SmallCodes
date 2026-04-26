// ============================================================================
// MFC DIALOG BASICS
// File: 02_dialog_basics.cpp
// Covers: CDialog, CDialogEx, modal/modeless, DoModal, DDX/DDV, common dialogs
// ============================================================================

#ifdef _MFC_VER

// ============================================================================
// 1. DIALOG FUNDAMENTALS
// ============================================================================

/*
MFC provides two types of dialogs:
1. Modal dialogs - Block user interaction with parent until closed
2. Modeless dialogs - Allow user interaction with parent while open

Key classes:
- CDialog - Base class for all dialogs
- CDialogEx - Extended dialog class (Visual Studio 2008+)
- CCommonDialog - Base for common dialogs (File, Color, Font, etc.)

Dialog lifecycle:
1. Constructor - Create dialog object
2. DoModal() (modal) or Create() (modeless) - Show dialog
3. OnInitDialog() - Initialize controls (virtual override)
4. User interacts with controls
5. OnOK() or OnCancel() - Close dialog
6. Destructor - Cleanup
*/

// ============================================================================
// 2. MODAL DIALOG
// ============================================================================

/*
Modal dialogs block execution until closed. Use DoModal() to display.

DoModal() return values:
IDOK   - User clicked OK (OnOK called)
IDCANCEL - User clicked Cancel (OnCancel called)
-1     - Dialog creation failed
*/

class CMyModalDialog : public CDialogEx
{
public:
    // Constructor - takes dialog resource ID
    CMyModalDialog(CWnd* pParent = nullptr);
    
    // Dialog Data Exchange / Dialog Data Validation
    enum { IDD = IDD_MY_DIALOG };
    
    // Control member variables (for DDX)
    CString m_name;
    int     m_age;
    BOOL    m_isEmployed;
    CString m_country;
    
protected:
    virtual void DoDataExchange(CDataExchange* pDX);  // DDX/DDV
    virtual BOOL OnInitDialog();                       // Initialization
    
    // Handlers
    afx_msg void OnBnClickedOk();
    afx_msg void OnBnClickedCancel();
    afx_msg void OnEnChangeName();
    
    DECLARE_MESSAGE_MAP()
};

// Constructor
CMyModalDialog::CMyModalDialog(CWnd* pParent /*= nullptr*/)
    : CDialogEx(IDD_MY_DIALOG, pParent)
    , m_name(_T(""))
    , m_age(0)
    , m_isEmployed(FALSE)
    , m_country(_T(""))
{
}

// DDX/DDV - Maps controls to member variables
void CMyModalDialog::DoDataExchange(CDataExchange* pDX)
{
    CDialogEx::DoDataExchange(pDX);
    
    // DDX - Dialog Data Exchange (control <-> variable)
    DDX_Text(pDX, IDC_NAME_EDIT, m_name);
    DDX_Text(pDX, IDC_AGE_EDIT, m_age);
    DDX_Check(pDX, IDC_EMPLOYED_CHECK, m_isEmployed);
    DDX_CBString(pDX, IDC_COUNTRY_COMBO, m_country);
    
    // DDV - Dialog Data Validation
    DDV_MaxChars(pDX, m_name, 100);       // Name max 100 chars
    DDV_MinMaxInt(pDX, m_age, 0, 150);    // Age between 0 and 150
}

BOOL CMyModalDialog::OnInitDialog()
{
    CDialogEx::OnInitDialog();
    
    // Initialize controls here
    // Set combo box items
    CComboBox* pCountry = (CComboBox*)GetDlgItem(IDC_COUNTRY_COMBO);
    pCountry->AddString(_T("USA"));
    pCountry->AddString(_T("Canada"));
    pCountry->AddString(_T("UK"));
    pCountry->AddString(_T("Germany"));
    pCountry->AddString(_T("Japan"));
    
    // Set default values
    m_name = _T("John Doe");
    m_age = 30;
    m_isEmployed = TRUE;
    m_country = _T("USA");
    
    // Update controls with member variable values
    UpdateData(FALSE);  // FALSE = variables -> controls
    
    return TRUE;  // TRUE = set focus to first control
}

void CMyModalDialog::OnBnClickedOk()
{
    // Validate and save data
    UpdateData(TRUE);  // TRUE = controls -> variables
    
    // Custom validation
    if (m_name.IsEmpty())
    {
        AfxMessageBox(_T("Name cannot be empty"));
        GetDlgItem(IDC_NAME_EDIT)->SetFocus();
        return;
    }
    
    CDialogEx::OnOK();  // Close dialog with IDOK
}

void CMyModalDialog::OnBnClickedCancel()
{
    // Ask for confirmation before canceling
    if (AfxMessageBox(_T("Discard changes?"), MB_YESNO) == IDYES)
    {
        CDialogEx::OnCancel();  // Close dialog with IDCANCEL
    }
}

void CMyModalDialog::OnEnChangeName()
{
    // Enable OK button only if name is not empty
    CString name;
    GetDlgItemText(IDC_NAME_EDIT, name);
    GetDlgItem(IDOK)->EnableWindow(!name.IsEmpty());
}

BEGIN_MESSAGE_MAP(CMyModalDialog, CDialogEx)
    ON_BN_CLICKED(IDOK, &CMyModalDialog::OnBnClickedOk)
    ON_BN_CLICKED(IDCANCEL, &CMyModalDialog::OnBnClickedCancel)
    ON_EN_CHANGE(IDC_NAME_EDIT, &CMyModalDialog::OnEnChangeName)
END_MESSAGE_MAP()

// ============================================================================
// 3. USING THE MODAL DIALOG
// ============================================================================

void ShowModalDialogExample()
{
    CMyModalDialog dlg;
    
    INT_PTR nResult = dlg.DoModal();
    
    if (nResult == IDOK)
    {
        // User clicked OK - data is in member variables
        CString msg;
        msg.Format(_T("Name: %s\nAge: %d\nEmployed: %s\nCountry: %s"),
            dlg.m_name, dlg.m_age,
            dlg.m_isEmployed ? _T("Yes") : _T("No"),
            dlg.m_country);
        AfxMessageBox(msg);
    }
    else if (nResult == IDCANCEL)
    {
        // User clicked Cancel
        AfxMessageBox(_T("Dialog cancelled"));
    }
}

// ============================================================================
// 4. MODELESS DIALOG
// ============================================================================

/*
Modeless dialogs remain open while the user interacts with the parent window.
Use Create() instead of DoModal(). Must be created on the heap (not stack).

Key differences from modal:
- Use Create() to show
- Must override OnOK/OnCancel to call DestroyWindow() instead of EndDialog()
- Must handle window deletion (PostNcDestroy)
- Can use WS_POPUP, WS_CAPTION, WS_SYSMENU styles
*/

class CMyModelessDialog : public CDialogEx
{
public:
    CMyModelessDialog(CWnd* pParent = nullptr);
    
    enum { IDD = IDD_MODELESS_DIALOG };
    
    // Show the modeless dialog
    BOOL ShowDialog();
    
protected:
    virtual void OnOK();        // Override to destroy instead of close
    virtual void OnCancel();    // Override to destroy instead of close
    virtual void PostNcDestroy();  // Delete self after window destroyed
    
    DECLARE_MESSAGE_MAP()
};

CMyModelessDialog::CMyModelessDialog(CWnd* pParent /*= nullptr*/)
    : CDialogEx(IDD_MODELESS_DIALOG, pParent)
{
}

BOOL CMyModelessDialog::ShowDialog()
{
    // Create the modeless dialog
    // WS_EX_TOOLWINDOW makes it a tool window (small title bar)
    return Create(IDD_MODELESS_DIALOG, GetParent());
}

void CMyModelessDialog::OnOK()
{
    // For modeless dialogs, destroy window instead of ending dialog
    if (!UpdateData(TRUE))
    {
        return;  // Validation failed
    }
    
    // Process data here
    
    DestroyWindow();  // Destroy the window (not EndDialog)
}

void CMyModelessDialog::OnCancel()
{
    // For modeless dialogs, destroy window
    DestroyWindow();  // Destroy the window (not EndDialog)
}

void CMyModelessDialog::PostNcDestroy()
{
    // Delete the C++ object after window is destroyed
    // Required for modeless dialogs created on the heap
    delete this;
}

// ============================================================================
// 5. SHOWING A MODELESS DIALOG
// ============================================================================

void ShowModelessDialogExample()
{
    // Modeless dialogs must be created on the heap
    CMyModelessDialog* pDlg = new CMyModelessDialog();
    
    if (pDlg->ShowDialog())
    {
        // Dialog created successfully
        // Note: pDlg will be deleted in PostNcDestroy when closed
    }
    else
    {
        // Creation failed - cleanup
        delete pDlg;
        AfxMessageBox(_T("Failed to create modeless dialog"));
    }
}

// ============================================================================
// 6. COMMON DIALOGS
// ============================================================================

/*
MFC provides wrapper classes for Windows common dialogs:

CFileDialog     - File Open/Save dialog
CColorDialog    - Color picker
CFontDialog     - Font selection
CFindReplaceDialog - Find/Replace (modeless)
CPageSetupDialog - Page setup
CPrintDialog    - Print dialog
*/

void CommonDialogsExample()
{
    // File Open dialog
    CFileDialog openDlg(TRUE, _T("txt"), _T("*.txt"),
        OFN_HIDEREADONLY | OFN_FILEMUSTEXIST,
        _T("Text Files (*.txt)|*.txt|All Files (*.*)|*.*||"));
    
    if (openDlg.DoModal() == IDOK)
    {
        CString fileName = openDlg.GetPathName();
        CString fileTitle = openDlg.GetFileTitle();
        CString fileExt = openDlg.GetFileExt();
        
        // Read file
        CFile file;
        if (file.Open(fileName, CFile::modeRead))
        {
            // Read file contents
            file.Close();
        }
    }
    
    // Color dialog
    CColorDialog colorDlg(RGB(255, 0, 0));  // Default = red
    
    if (colorDlg.DoModal() == IDOK)
    {
        COLORREF color = colorDlg.GetColor();
        // Use the selected color
    }
    
    // Font dialog
    CFontDialog fontDlg;
    
    if (fontDlg.DoModal() == IDOK)
    {
        LOGFONT lf;
        fontDlg.GetCurrentFont(&lf);
        // Use the selected font
    }
    
    // Print dialog
    CPrintDialog printDlg(FALSE);  // FALSE = Print dialog, TRUE = Page Setup
    
    if (printDlg.DoModal() == IDOK)
    {
        // Get printer DC
        HDC hPrinterDC = printDlg.GetPrinterDC();
        // Use the printer device context
    }
}

// ============================================================================
// 7. DDX AND DDV REFERENCE
// ============================================================================

/*
DDX Functions (Dialog Data Exchange):
DDX_Text(pDX, id, variable)       - Edit control <-> CString/int/double/etc.
DDX_Check(pDX, id, variable)      - Check box <-> BOOL/int
DDX_Radio(pDX, id, variable)      - Radio buttons <-> int (-1 = none)
DDX_LBString(pDX, id, variable)   - List box <-> CString
DDX_LBIndex(pDX, id, variable)    - List box <-> int (index)
DDX_CBString(pDX, id, variable)   - Combo box <-> CString
DDX_CBIndex(pDX, id, variable)    - Combo box <-> int (index)
DDX_Scroll(pDX, id, variable)     - Scroll bar <-> int
DDX_Slider(pDX, id, variable)     - Slider <-> int
DDX_DateTimeCtrl(pDX, id, variable) - Date time picker <-> CTime/COleDateTime
DDX_MonthCalCtrl(pDX, id, variable) - Month calendar <-> CTime/COleDateTime
DDX_Control(pDX, id, control)     - Attach control object to dialog member

DDV Functions (Dialog Data Validation):
DDV_MaxChars(pDX, string, nChars) - Maximum string length
DDV_MinMaxByte(pDX, byte, min, max) - Byte range
DDV_MinMaxInt(pDX, int, min, max) - Integer range
DDV_MinMaxUInt(pDX, uint, min, max) - Unsigned int range
DDV_MinMaxLong(pDX, long, min, max) - Long range
DDV_MinMaxDouble(pDX, double, min, max) - Double range
DDV_MinMaxDateTime(pDX, time, min, max) - DateTime range
*/

// ============================================================================
// 8. CUSTOM DDX/DDV
// ============================================================================

/*
Creating custom DDX/DDV functions:

void AFXAPI DDX_MyCustom(CDataExchange* pDX, int nIDC, CMyType& value)
{
    if (pDX->m_bSaveAndValidate)  // Control -> Variable
    {
        // Read from control, validate, store in value
    }
    else  // Variable -> Control
    {
        // Write value to control
    }
}

void AFXAPI DDV_MyCustom(CDataExchange* pDX, CMyType& value, CMyType& min, CMyType& max)
{
    if (pDX->m_bSaveAndValidate)
    {
        // Validate value is within range
    }
}
*/

// ============================================================================
// 9. DIALOG SIZING AND POSITIONING
// ============================================================================

/*
Dialog sizing techniques:

1. Fixed size - Default, controls stay in place
2. Resizable - Set dialog border to WS_THICKFRAME
3. Dynamic - Use GetDlgItem()->SetWindowPos() in OnSize()

Positioning:
CenterWindow() - Center on parent
SetWindowPos() - Set position and size
MoveWindow()   - Move and resize
GetWindowRect()- Get screen coordinates
GetClientRect()- Get client area coordinates
ScreenToClient()- Convert screen to client coordinates
ClientToScreen()- Convert client to screen coordinates
*/

// ============================================================================
// 10. BEST PRACTICES
// ============================================================================

/*
1. Always call UpdateData(FALSE) in OnInitDialog to initialize controls
2. Always call UpdateData(TRUE) before reading control values
3. Use DDX/DDV instead of manual GetDlgItemText/SetDlgItemText
4. Override OnOK/OnCancel for custom close behavior
5. Use CDialogEx instead of CDialog for modern MFC
6. Modeless dialogs must be heap-allocated with PostNcDestroy cleanup
7. Use CFileDialog for file operations (not custom file dialogs)
8. Validate user input in DoDataExchange with DDV functions
9. Use enum { IDD = IDD_xxx } for dialog resource binding
10. Call base class OnInitDialog before custom initialization
*/

#endif // _MFC_VER
