// ============================================================================
// MFC FEATURE PACK (MFC 9.0+)
// File: 17_feature_pack.cpp
// Covers: CMFCMenuBar, CMFCToolBar, CMFCStatusBar, ribbon, docking panes
// ============================================================================

#ifdef _MFC_VER

// ============================================================================
// 1. FEATURE PACK OVERVIEW
// ============================================================================

/*
MFC Feature Pack (Visual Studio 2008 SP1+) introduced modern UI elements:
- Ribbon bar (Office 2007 style)
- Dockable panes (Visual Studio style)
- Menu bar (replaces traditional menus)
- Toolbar customization
- Status bar with progress
- Color picker, font picker
- Property grid
- Shell list/tree controls
- Task dialog
- Auto-hide docking

Key classes:
- CMFCRibbonBar - Ribbon control
- CMFCMenuBar - Menu bar
- CMFCToolBar - Enhanced toolbar
- CMFCStatusBar - Enhanced status bar
- CDockablePane - Dockable pane
- CMFCPropertyGridCtrl - Property grid
- CMFCColorButton - Color picker
- CMFCFontComboBox - Font picker
- CMFCTaskDialog - Task dialog
- CMFCShellListCtrl / CMFCShellTreeCtrl - Shell controls
*/

// ============================================================================
// 2. CMFCMenuBar - MODERN MENU BAR
// ============================================================================

/*
CMFCMenuBar replaces the traditional menu with a modern look.

Key methods:
- Create() - Create menu bar
- SetMenu() - Set menu resource
- EnableMenuShadows() - Enable shadows
- GetMenu() - Get menu handle
- GetHMenu() - Get HMENU
- SetBarStyle() - Set bar style
*/

class CMainFrame : public CFrameWndEx
{
protected:
    CMFCMenuBar    m_wndMenuBar;
    CMFCToolBar    m_wndToolBar;
    CMFCStatusBar  m_wndStatusBar;
    
    virtual BOOL OnCreate(LPCREATESTRUCT lpcs);
    
    DECLARE_MESSAGE_MAP()
};

BOOL CMainFrame::OnCreate(LPCREATESTRUCT lpcs)
{
    if (CFrameWndEx::OnCreate(lpcs) == -1)
        return -1;
    
    // Create menu bar
    if (!m_wndMenuBar.Create(this))
    {
        TRACE0("Failed to create menubar\n");
        return -1;
    }
    
    m_wndMenuBar.SetMenu(AfxGetApp()->m_hMDIMenu);
    m_wndMenuBar.EnableMenuShadows(TRUE);
    
    // Create toolbar
    if (!m_wndToolBar.Create(this, AFX_DEFAULT_TOOLBAR_STYLE,
        IDR_MAINFRAME) ||
        !m_wndToolBar.LoadToolBar(IDR_MAINFRAME, 0, 0, TRUE))
    {
        TRACE0("Failed to create toolbar\n");
        return -1;
    }
    
    // Enable docking
    EnableDocking(CBRS_ALIGN_ANY);
    m_wndToolBar.EnableDocking(CBRS_ALIGN_ANY);
    DockPane(&m_wndToolBar);
    
    // Create status bar
    if (!m_wndStatusBar.Create(this))
    {
        TRACE0("Failed to create status bar\n");
        return -1;
    }
    
    return 0;
}

// ============================================================================
// 3. CMFCToolBar - ENHANCED TOOLBAR
// ============================================================================

/*
CMFCToolBar provides:
- Customizable buttons
- Large/small icons
- Toolbar customization dialog
- Keyboard shortcuts
- User-defined toolbars

Key methods:
- Create() - Create toolbar
- LoadToolBar() - Load from resource
- LoadBitmap() - Load button images
- SetSizes() - Set button sizes
- EnableCustomizeButton() - Enable customization
- EnableDocking() - Enable docking
- ResetAll() - Reset to default
- GetToolBarCtrl() - Get underlying control
- SetPaneStyle() - Set pane style
- AddButton() - Add button
- InsertButton() - Insert button
*/

void ToolbarCustomizationExample(CMFCToolBar* pToolbar)
{
    // Enable customization
    pToolbar->EnableCustomizeButton(TRUE, ID_VIEW_CUSTOMIZE, _T("Customize"));
    
    // Set button sizes
    pToolbar->SetSizes(CSize(32, 32), CSize(24, 24));
    
    // Enable large icons
    pToolbar->EnableLargeIcons(TRUE);
    
    // Enable docking
    pToolbar->EnableDocking(CBRS_ALIGN_ANY);
    
    // Set toolbar style
    pToolbar->SetPaneStyle(pToolbar->GetPaneStyle() |
        CBRS_TOOLTIPS | CBRS_FLYBY | CBRS_SIZE_DYNAMIC);
}

// ============================================================================
// 4. CMFCStatusBar - ENHANCED STATUS BAR
// ============================================================================

/*
CMFCStatusBar supports:
- Multiple panes
- Progress bar in pane
- Animation
- Icons
- Timer

Key methods:
- Create() - Create status bar
- SetIndicators() - Set pane indicators
- SetPaneText() - Set text
- SetPaneIcon() - Set icon
- SetPaneProgress() - Set progress
- SetPaneAnimation() - Set animation
- EnablePaneProgressBar() - Enable progress
- GetPaneText() - Get text
*/

void StatusBarExample(CMFCStatusBar* pStatusBar)
{
    // Set pane text
    pStatusBar->SetPaneText(0, _T("Ready"));
    
    // Set pane icon
    pStatusBar->SetPaneIcon(1, AfxGetApp()->LoadIcon(IDI_STATUS_ICON));
    
    // Enable progress bar in pane
    pStatusBar->EnablePaneProgressBar(2, 100);
    pStatusBar->SetPaneProgress(2, 50);  // 50%
    
    // Set pane width
    pStatusBar->SetPaneWidth(0, 300);
}

// ============================================================================
// 5. CDockablePane - DOCKING PANES
// ============================================================================

/*
CDockablePane provides Visual Studio-style docking panes.
Can contain any CWnd-derived control.

Key methods:
- Create() - Create pane
- EnableDocking() - Enable docking
- DockToFrameWindow() - Dock to frame
- DockToPane() - Dock to another pane
- SetAutoHideMode() - Enable auto-hide
- SetMiniFrameRTC() - Set mini-frame class
- AdjustLayout() - Recalculate layout
- GetCaption() - Get caption text
- SetCaption() - Set caption text
- CanBeClosed() - Can be closed
- CanBeResized() - Can be resized
*/

class COutputPane : public CDockablePane
{
public:
    virtual void OnUpdateCmdUI(CFrameWnd* pTarget, BOOL bDisableIfNoHndler);
    
protected:
    CEdit m_wndOutput;
    
    virtual BOOL OnCreate(LPCREATESTRUCT lpcs);
    
    DECLARE_MESSAGE_MAP()
};

BOOL COutputPane::OnCreate(LPCREATESTRUCT lpcs)
{
    if (!CDockablePane::OnCreate(lpcs))
        return FALSE;
    
    // Create output edit control
    CRect rect;
    GetClientRect(rect);
    
    m_wndOutput.Create(ES_MULTILINE | ES_READONLY | WS_VSCROLL |
        WS_VISIBLE | WS_CHILD, rect, this, IDC_OUTPUT_EDIT);
    
    // Set font
    m_wndOutput.SetFont(&afxGlobalData.fontRegular);
    
    return TRUE;
}

void CreateDockingPane(CMainFrame* pFrame)
{
    // Create output pane
    COutputPane* pPane = new COutputPane();
    
    if (!pPane->Create(_T("Output"),
        pFrame, CRect(0, 0, 300, 200),
        TRUE, ID_VIEW_OUTPUT,
        WS_CHILD | WS_VISIBLE | CBRS_BOTTOM |
        CBRS_FLOAT_MULTI))
    {
        TRACE0("Failed to create output pane\n");
        delete pPane;
        return;
    }
    
    // Enable docking
    pPane->EnableDocking(CBRS_ALIGN_ANY);
    pPane->DockToFrameWindow(CBRS_BOTTOM);
    
    // Enable auto-hide
    pPane->SetAutoHideMode(TRUE, CBRS_BOTTOM);
}

// ============================================================================
// 6. CMFCRibbonBar - RIBBON INTERFACE
// ============================================================================

/*
CMFCRibbonBar implements the Office 2007+ ribbon interface.

Key classes:
- CMFCRibbonBar - Ribbon container
- CMFCRibbonCategory - Tab category
- CMFCRibbonPanel - Panel within category
- CMFCRibbonButton - Button
- CMFCRibbonCheckBox - Checkbox
- CMFCRibbonComboBox - Combobox
- CMFCRibbonEdit - Edit control
- CMFCRibbonGallery - Gallery
- CMFCRibbonProgressBar - Progress bar
- CMFCRibbonSlider - Slider
- CMFCRibbonSeparator - Separator
- CMFCRibbonLabel - Label
- CMFCRibbonColorButton - Color button
- CMFCRibbonLinkCtrl - Hyperlink
- CMFCRibbonButtonsGroup - Button group
- CMFCRibbonUndoButton - Undo button
*/

void CreateRibbonBar(CMainFrame* pFrame)
{
    CMFCRibbonBar* pRibbon = &pFrame->m_wndRibbonBar;
    
    // Create ribbon bar
    if (!pRibbon->Create(pFrame))
    {
        TRACE0("Failed to create ribbon bar\n");
        return;
    }
    
    // Set ribbon panel min size
    pRibbon->SetPanelMinSize(ID_CATEGORY_HOME, CSize(100, 100));
    
    // Add Home category
    CMFCRibbonCategory* pCategory = pRibbon->AddCategory(
        _T("&Home"), IDB_HOME_IMAGES, IDB_HOME_IMAGES_SMALL);
    
    // Add Clipboard panel
    CMFCRibbonPanel* pPanel = pCategory->AddPanel(
        _T("Clipboard"));
    
    // Add buttons
    pPanel->Add(new CMFCRibbonButton(ID_EDIT_PASTE,
        _T("Paste"), 0, 0));
    
    // Add button group
    CMFCRibbonButtonsGroup* pGroup = new CMFCRibbonButtonsGroup();
    pGroup->AddButton(new CMFCRibbonButton(ID_EDIT_CUT,
        _T("Cut"), 1, 1));
    pGroup->AddButton(new CMFCRibbonButton(ID_EDIT_COPY,
        _T("Copy"), 2, 2));
    pPanel->Add(pGroup);
    
    // Add Font panel
    CMFCRibbonPanel* pFontPanel = pCategory->AddPanel(
        _T("Font"));
    
    // Add combobox
    CMFCRibbonComboBox* pFontCombo = new CMFCRibbonComboBox(
        ID_FONT_COMBO, TRUE, -1, 0, -1, 200);
    pFontCombo->AddItem(_T("Arial"));
    pFontCombo->AddItem(_T("Times New Roman"));
    pFontCombo->AddItem(_T("Courier New"));
    pFontPanel->Add(pFontCombo);
    
    // Add checkbox
    pFontPanel->Add(new CMFCRibbonCheckBox(ID_FONT_BOLD,
        _T("Bold")));
    
    // Add View category
    CMFCRibbonCategory* pViewCategory = pRibbon->AddCategory(
        _T("&View"), IDB_VIEW_IMAGES, IDB_VIEW_IMAGES_SMALL);
    
    CMFCRibbonPanel* pShowPanel = pViewCategory->AddPanel(
        _T("Show/Hide"));
    
    // Add checkboxes for panes
    pShowPanel->Add(new CMFCRibbonCheckBox(ID_VIEW_OUTPUT,
        _T("Output")));
    pShowPanel->Add(new CMFCRibbonCheckBox(ID_VIEW_PROPERTIES,
        _T("Properties")));
}

// ============================================================================
// 7. CMFCPropertyGridCtrl - PROPERTY GRID
// ============================================================================

/*
CMFCPropertyGridCtrl provides a Visual Studio-style property grid.

Key classes:
- CMFCPropertyGridCtrl - Property grid control
- CMFCPropertyGridProperty - Property item
- CMFCPropertyGridColorProperty - Color property
- CMFCPropertyGridFileProperty - File property
- CMFCPropertyGridFontProperty - Font property
*/

void CreatePropertyGrid(CWnd* pParent)
{
    CMFCPropertyGridCtrl* pGrid = new CMFCPropertyGridCtrl();
    
    pGrid->Create(WS_CHILD | WS_VISIBLE | WS_BORDER,
        CRect(0, 0, 300, 400), pParent, IDC_PROPERTY_GRID);
    
    // Enable description area
    pGrid->EnableDescriptionArea(TRUE);
    
    // Enable header
    pGrid->EnableHeaderCtrl(TRUE);
    
    // Set colors
    pGrid->SetCustomColors(RGB(255, 255, 255), RGB(0, 0, 0),
        RGB(240, 240, 240), RGB(0, 0, 0),
        RGB(255, 255, 255), RGB(0, 0, 0));
    
    // Add categories and properties
    CMFCPropertyGridProperty* pAppearance = new CMFCPropertyGridProperty(
        _T("Appearance"));
    
    pAppearance->AddSubItem(new CMFCPropertyGridProperty(
        _T("Caption"), (COleVariant)_T("Default")));
    
    pAppearance->AddSubItem(new CMFCPropertyGridProperty(
        _T("Visible"), (COleVariant)TRUE));
    
    pGrid->AddProperty(pAppearance);
    
    CMFCPropertyGridProperty* pPosition = new CMFCPropertyGridProperty(
        _T("Position"));
    
    pPosition->AddSubItem(new CMFCPropertyGridProperty(
        _T("Left"), (COleVariant)0L, _T("X position")));
    
    pPosition->AddSubItem(new CMFCPropertyGridProperty(
        _T("Top"), (COleVariant)0L, _T("Y position")));
    
    pGrid->AddProperty(pPosition);
}

// ============================================================================
// 8. BEST PRACTICES
// ============================================================================

/*
1. Use CFrameWndEx instead of CFrameWnd for feature pack support
2. Use CMFCMenuBar for modern menu appearance
3. Use CDockablePane for tool windows
4. Use CMFCPropertyGridCtrl for property editing
5. Use CMFCRibbonBar for Office-style UI
6. Enable customization for toolbars
7. Use auto-hide for frequently used panes
8. Use CMFCStatusBar for enhanced status display
9. Use CMFCTaskDialog for modern message boxes
10. Use afxGlobalData for consistent theming
*/

#endif // _MFC_VER
