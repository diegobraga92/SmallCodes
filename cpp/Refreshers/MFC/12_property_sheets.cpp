// ============================================================================
// MFC PROPERTY SHEETS AND WIZARDS
// File: 12_property_sheets.cpp
// Covers: CPropertySheet, CPropertyPage, wizards, Apply button
// ============================================================================

#ifdef _MFC_VER

// ============================================================================
// 1. PROPERTY SHEET OVERVIEW
// ============================================================================

/*
Property sheets (tab dialogs) organize many controls into pages.

Key classes:
- CPropertySheet - The container (dialog with tabs)
- CPropertyPage - Individual pages (derived from CDialogEx)

Types:
1. Standard property sheet - Tabs at top
2. Wizard - Next/Back/Finish buttons (no tabs)
3. Modeless property sheet - Stays open

Property sheet styles:
PSH_DEFAULT        - Default style
PSH_MODELESS       - Modeless property sheet
PSH_WIZARD         - Wizard style
PSH_WIZARD97       - Wizard 97 style
PSH_WIZARD_LITE    - Wizard with no header
PSH_NOAPPLYNOW     - Hide Apply button
PSH_PROPTITLE      - "Properties" in title
PSH_USEHICON       - Use custom icon
*/

// ============================================================================
// 2. PROPERTY PAGES
// ============================================================================

/*
Each page is a dialog resource with specific styles:
- Child style (not Popup)
- Thin border
- No caption or system menu
- DS_3DLOOK | DS_CONTROL | WS_CHILD | WS_VISIBLE

Key methods:
- OnSetActive() - Page becoming active
- OnKillActive() - Page losing active status
- OnWizardNext() - Next button (wizard)
- OnWizardBack() - Back button (wizard)
- OnWizardFinish() - Finish button (wizard)
- OnApply() - Apply button clicked
- OnReset() - Reset button clicked
- SetModified() - Mark page as modified
- CancelToClose() - Change Cancel to Close
- QuerySiblings() - Query other pages
*/

class CGeneralPage : public CPropertyPage
{
public:
    CGeneralPage() : CPropertyPage(IDD_GENERAL_PAGE) {}
    
    enum { IDD = IDD_GENERAL_PAGE };
    
    CString m_name;
    int     m_age;
    
protected:
    virtual void DoDataExchange(CDataExchange* pDX);
    virtual BOOL OnSetActive();
    virtual BOOL OnKillActive();
    virtual void OnOK();
    
    DECLARE_MESSAGE_MAP()
};

void CGeneralPage::DoDataExchange(CDataExchange* pDX)
{
    CPropertyPage::DoDataExchange(pDX);
    DDX_Text(pDX, IDC_NAME_EDIT, m_name);
    DDX_Text(pDX, IDC_AGE_EDIT, m_age);
}

BOOL CGeneralPage::OnSetActive()
{
    // Called when this page becomes active
    return CPropertyPage::OnSetActive();
}

BOOL CGeneralPage::OnKillActive()
{
    // Called when leaving this page
    if (!UpdateData(TRUE))
        return FALSE;  // Don't leave if validation fails
    
    return CPropertyPage::OnKillActive();
}

void CGeneralPage::OnOK()
{
    // Called when OK is clicked
    CPropertyPage::OnOK();
}

class CSettingsPage : public CPropertyPage
{
public:
    CSettingsPage() : CPropertyPage(IDD_SETTINGS_PAGE) {}
    
    enum { IDD = IDD_SETTINGS_PAGE };
    
    BOOL m_enableFeature;
    int  m_mode;
    
protected:
    virtual void DoDataExchange(CDataExchange* pDX);
    
    DECLARE_MESSAGE_MAP()
};

void CSettingsPage::DoDataExchange(CDataExchange* pDX)
{
    CPropertyPage::DoDataExchange(pDX);
    DDX_Check(pDX, IDC_ENABLE_CHECK, m_enableFeature);
    DDX_Radio(pDX, IDC_MODE_RADIO, m_mode);
}

class CAdvancedPage : public CPropertyPage
{
public:
    CAdvancedPage() : CPropertyPage(IDD_ADVANCED_PAGE) {}
    
    enum { IDD = IDD_ADVANCED_PAGE };
    
    CString m_path;
    int     m_timeout;
    
protected:
    virtual void DoDataExchange(CDataExchange* pDX);
    
    DECLARE_MESSAGE_MAP()
};

void CAdvancedPage::DoDataExchange(CDataExchange* pDX)
{
    CPropertyPage::DoDataExchange(pDX);
    DDX_Text(pDX, IDC_PATH_EDIT, m_path);
    DDX_Text(pDX, IDC_TIMEOUT_EDIT, m_timeout);
    DDV_MinMaxInt(pDX, m_timeout, 1, 3600);
}

// ============================================================================
// 3. PROPERTY SHEET
// ============================================================================

/*
CPropertySheet manages the pages and the dialog.

Key methods:
- AddPage() - Add a page
- RemovePage() - Remove a page
- SetActivePage() - Set active page
- GetActivePage() - Get active page
- GetPageIndex() / GetPage() - Page info
- GetPageCount() - Number of pages
- PressButton() - Simulate button click
- SetTitle() - Set sheet title
- SetWizardMode() - Enable wizard mode
- SetFinishText() - Set Finish button text
*/

class CMyPropertySheet : public CPropertySheet
{
public:
    CMyPropertySheet(CWnd* pParentWnd = nullptr);
    
    // Pages
    CGeneralPage   m_generalPage;
    CSettingsPage  m_settingsPage;
    CAdvancedPage  m_advancedPage;
    
protected:
    virtual BOOL OnInitDialog();
    
    DECLARE_MESSAGE_MAP()
};

CMyPropertySheet::CMyPropertySheet(CWnd* pParentWnd /*= nullptr*/)
    : CPropertySheet(_T("Application Settings"), pParentWnd, 0)
{
    // Add pages
    AddPage(&m_generalPage);
    AddPage(&m_settingsPage);
    AddPage(&m_advancedPage);
    
    // Set tab icons (optional)
    // m_psh.dwFlags |= PSH_USEHICON;
    // m_psh.hIcon = AfxGetApp()->LoadIcon(IDI_SETTINGS);
}

BOOL CMyPropertySheet::OnInitDialog()
{
    BOOL result = CPropertySheet::OnInitDialog();
    
    // Custom initialization
    // Set sheet icon
    // ModifyStyle(...)
    
    return result;
}

// ============================================================================
// 4. USING THE PROPERTY SHEET
// ============================================================================

void ShowPropertySheet()
{
    CMyPropertySheet propSheet;
    
    if (propSheet.DoModal() == IDOK)
    {
        // User clicked OK - data is in page member variables
        CString name = propSheet.m_generalPage.m_name;
        int age = propSheet.m_generalPage.m_age;
        BOOL enable = propSheet.m_settingsPage.m_enableFeature;
        int mode = propSheet.m_settingsPage.m_mode;
        CString path = propSheet.m_advancedPage.m_path;
        int timeout = propSheet.m_advancedPage.m_timeout;
        
        // Apply settings
    }
}

// ============================================================================
// 5. WIZARD MODE
// ============================================================================

/*
Wizard mode replaces tabs with Next/Back/Finish buttons.
Useful for step-by-step configuration.

Enable wizard mode:
propSheet.SetWizardMode();

Wizard page methods:
- OnWizardNext() - Validate and prepare for next page
- OnWizardBack() - Prepare for previous page
- OnWizardFinish() - Validate and finish

SetFinishText() - Change "Next" to "Finish" on last page
*/

class CWizardPage1 : public CPropertyPage
{
public:
    CWizardPage1() : CPropertyPage(IDD_WIZARD_PAGE1) {}
    
    enum { IDD = IDD_WIZARD_PAGE1 };
    
protected:
    virtual BOOL OnSetActive();
    virtual LRESULT OnWizardNext();
    
    DECLARE_MESSAGE_MAP()
};

BOOL CWizardPage1::OnSetActive()
{
    // First page - disable Back button
    ((CPropertySheet*)GetParent())->SetWizardButtons(
        PSWIZB_NEXT);  // Only Next button
    
    return CPropertyPage::OnSetActive();
}

LRESULT CWizardPage1::OnWizardNext()
{
    // Validate before moving to next page
    UpdateData(TRUE);
    
    if (m_name.IsEmpty())
    {
        AfxMessageBox(_T("Name is required"));
        return -1;  // Don't advance
    }
    
    return CPropertyPage::OnWizardNext();
}

class CWizardPage2 : public CPropertyPage
{
public:
    CWizardPage2() : CPropertyPage(IDD_WIZARD_PAGE2) {}
    
    enum { IDD = IDD_WIZARD_PAGE2 };
    
protected:
    virtual BOOL OnSetActive();
    virtual LRESULT OnWizardFinish();
    
    DECLARE_MESSAGE_MAP()
};

BOOL CWizardPage2::OnSetActive()
{
    // Last page - show Back and Finish buttons
    ((CPropertySheet*)GetParent())->SetWizardButtons(
        PSWIZB_BACK | PSWIZB_FINISH);
    
    // Change Finish button text
    ((CPropertySheet*)GetParent())->SetFinishText(_T("&Done"));
    
    return CPropertyPage::OnSetActive();
}

LRESULT CWizardPage2::OnWizardFinish()
{
    // Validate before finishing
    UpdateData(TRUE);
    
    // All validation passed
    return CPropertyPage::OnWizardFinish();
}

void ShowWizard()
{
    CPropertySheet wizard(_T("Setup Wizard"));
    wizard.SetWizardMode();
    
    CWizardPage1 page1;
    CWizardPage2 page2;
    
    wizard.AddPage(&page1);
    wizard.AddPage(&page2);
    
    if (wizard.DoModal() == ID_WIZFINISH)
    {
        // Wizard completed
    }
}

// ============================================================================
// 6. APPLY BUTTON
// ============================================================================

/*
The Apply button applies changes without closing the dialog.
Pages must call SetModified() to enable the Apply button.

PSH_NOAPPLYNOW - Hide Apply button
*/

void CGeneralPage::OnApplySettings()
{
    // Called when Apply is clicked
    UpdateData(TRUE);
    
    // Apply settings immediately
    // ...
    
    // Clear modified state
    SetModified(FALSE);
}

void CGeneralPage::OnSomethingChanged()
{
    // Enable Apply button when something changes
    SetModified(TRUE);
}

// ============================================================================
// 7. MODELESS PROPERTY SHEET
// ============================================================================

/*
Modeless property sheets stay open while user works elsewhere.
Use Create() instead of DoModal().
*/

void ShowModelessPropertySheet()
{
    CPropertySheet* pSheet = new CPropertySheet(_T("Modeless Settings"));
    pSheet->m_psh.dwFlags |= PSH_MODELESS;
    
    CGeneralPage* pPage1 = new CGeneralPage();
    CSettingsPage* pPage2 = new CSettingsPage();
    
    pSheet->AddPage(pPage1);
    pSheet->AddPage(pPage2);
    
    pSheet->Create();  // Modeless
}

// ============================================================================
// 8. BEST PRACTICES
// ============================================================================

/*
1. Use separate page classes for logical groups of settings
2. Validate data in OnKillActive (not in OnOK)
3. Use SetModified() to enable/disable Apply button
4. Use SetWizardButtons() to control wizard navigation
5. Use SetFinishText() for the last wizard page
6. Use PSH_NOAPPLYNOW if Apply is not needed
7. Use DDX/DDV for data exchange in pages
8. Override OnSetActive for page initialization
9. Use QuerySiblings() for cross-page communication
10. Clean up modeless property sheets in PostNcDestroy
*/

BEGIN_MESSAGE_MAP(CGeneralPage, CPropertyPage)
END_MESSAGE_MAP()

BEGIN_MESSAGE_MAP(CSettingsPage, CPropertyPage)
END_MESSAGE_MAP()

BEGIN_MESSAGE_MAP(CAdvancedPage, CPropertyPage)
END_MESSAGE_MAP()

BEGIN_MESSAGE_MAP(CMyPropertySheet, CPropertySheet)
END_MESSAGE_MAP()

BEGIN_MESSAGE_MAP(CWizardPage1, CPropertyPage)
END_MESSAGE_MAP()

BEGIN_MESSAGE_MAP(CWizardPage2, CPropertyPage)
END_MESSAGE_MAP()

#endif // _MFC_VER
