// ============================================================================
// MFC MENUS, TOOLBARS, AND STATUS BARS
// File: 07_menus_toolbars_status.cpp
// Covers: CMenu, CToolBar, CStatusBar, command UI handlers, docking
// ============================================================================

#ifdef _MFC_VER

// ============================================================================
// 1. CMenu - MENU HANDLING
// ============================================================================

/*
CMenu wraps the Windows HMENU. Menus are typically defined in resources
(.rc file) but can also be created programmatically.

Key methods:
- LoadMenu() - Load menu from resource
- CreateMenu() - Create empty menu
- CreatePopupMenu() - Create popup menu
- TrackPopupMenu() - Show context menu
- AppendMenu() / InsertMenu() - Add items
- DeleteMenu() - Remove item
- ModifyMenu() - Change item
- EnableMenuItem() - Enable/disable
- CheckMenuItem() - Check/uncheck
- SetDefaultItem() - Set default (bold) item
- GetMenuString() - Get item text
- GetMenuItemCount() - Number of items
- GetSubMenu() - Get popup submenu
- DestroyMenu() - Cleanup
*/

class CMenuExample
{
public:
    // Loading menu from resource
    void LoadMenuFromResource()
    {
        m_menu.LoadMenu(IDR_MAINFRAME);
        
        // Get submenu (File menu is at index 0)
        CMenu* pFileMenu = m_menu.GetSubMenu(0);
        
        // Modify menu item
        pFileMenu->ModifyMenu(ID_FILE_OPEN, MF_BYCOMMAND, ID_FILE_OPEN, _T("&Open...\tCtrl+O"));
    }
    
    // Creating menu programmatically
    void CreateMenuProgrammatically()
    {
        // Create popup menu
        CMenu popupMenu;
        popupMenu.CreatePopupMenu();
        
        // Add items
        popupMenu.AppendMenu(MF_STRING, ID_EDIT_COPY, _T("&Copy\tCtrl+C"));
        popupMenu.AppendMenu(MF_STRING, ID_EDIT_CUT, _T("Cu&t\tCtrl+X"));
        popupMenu.AppendMenu(MF_STRING, ID_EDIT_PASTE, _T("&Paste\tCtrl+V"));
        
        // Separator
        popupMenu.AppendMenu(MF_SEPARATOR);
        
        // Checked item
        popupMenu.AppendMenu(MF_STRING | MF_CHECKED, ID_VIEW_TOOLBAR, _T("&Toolbar"));
        
        // Radio items
        popupMenu.AppendMenu(MF_STRING | MF_RADIOCHECK, ID_VIEW_LARGE, _T("&Large Icons"));
        popupMenu.AppendMenu(MF_STRING | MF_RADIOCHECK, ID_VIEW_SMALL, _T("&Small Icons"));
        
        // Submenu
        CMenu sortMenu;
        sortMenu.CreatePopupMenu();
        sortMenu.AppendMenu(MF_STRING, ID_SORT_NAME, _T("By &Name"));
        sortMenu.AppendMenu(MF_STRING, ID_SORT_DATE, _T("By &Date"));
        sortMenu.AppendMenu(MF_STRING, ID_SORT_SIZE, _T("By Si&ze"));
        popupMenu.AppendMenu(MF_POPUP, (UINT_PTR)sortMenu.m_hMenu, _T("&Sort"));
        sortMenu.Detach();  // Detach so it's not destroyed
    }
    
    // Context menu (right-click)
    void ShowContextMenu(CWnd* pParent, CPoint point)
    {
        CMenu contextMenu;
        contextMenu.LoadMenu(IDR_CONTEXT_MENU);
        
        CMenu* pPopup = contextMenu.GetSubMenu(0);
        ASSERT(pPopup != nullptr);
        
        // Display context menu
        pPopup->TrackPopupMenu(
            TPM_LEFTALIGN | TPM_RIGHTBUTTON,
            point.x, point.y,
            pParent);
    }
    
    // Dynamic menu modification
    void UpdateRecentFilesMenu(CMenu* pFileMenu, const CStringArray& recentFiles)
    {
        // Find "Recent Files" separator
        for (int i = pFileMenu->GetMenuItemCount() - 1; i >= 0; i--)
        {
            CString text;
            pFileMenu->GetMenuString(i, text, MF_BYPOSITION);
            if (text.IsEmpty())  // Separator
            {
                // Remove old recent files
                while (pFileMenu->GetMenuItemCount() > i + 1)
                {
                    pFileMenu->DeleteMenu(i + 1, MF_BYPOSITION);
                }
                
                // Add recent files
                for (int j = 0; j < recentFiles.GetSize() && j < 4; j++)
                {
                    CString menuText;
                    menuText.Format(_T("&%d %s"), j + 1, recentFiles[j]);
                    pFileMenu->AppendMenu(MF_STRING, ID_FILE_MRU_FILE1 + j, menuText);
                }
                break;
            }
        }
    }
    
private:
    CMenu m_menu;
};

// ============================================================================
// 2. CToolBar - TOOLBAR CONTROL
// ============================================================================

/*
CToolBar wraps the Windows toolbar common control.

Key methods:
- Create() / CreateEx() - Create toolbar
- LoadToolBar() - Load from resource
- LoadBitmap() - Load button images
- SetButtons() - Set button IDs
- SetSizes() - Set button and image sizes
- SetHeight() - Set toolbar height
- CommandToIndex() - Get button index from ID
- GetItemID() - Get ID from index
- GetToolBarCtrl() - Access underlying CToolBarCtrl
- EnableDocking() - Enable docking
- SetBarStyle() - Set toolbar style

Toolbar styles:
CBRS_TOP           - Dock at top
CBRS_BOTTOM        - Dock at bottom
CBRS_LEFT          - Dock at left
CBRS_RIGHT         - Dock at right
CBRS_FLOATING      - Floating toolbar
CBRS_TOOLTIPS      - Show tooltips
CBRS_FLYBY         - Show flyby status text
CBRS_HIDE_INPLACE  - Hide when inactive
CBRS_SIZE_DYNAMIC  - Resizable when floating
CBRS_GRIPPER       - Show gripper
CBRS_BORDER_ANY    - Border on any side
*/

class CToolBarExample
{
public:
    BOOL CreateToolbar(CWnd* pParentWnd)
    {
        // Create toolbar with extended styles
        if (!m_wndToolBar.CreateEx(pParentWnd,
            TBSTYLE_FLAT,                     // Flat toolbar
            WS_CHILD | WS_VISIBLE | CBRS_TOP |
            CBRS_GRIPPER | CBRS_TOOLTIPS |
            CBRS_FLYBY | CBRS_SIZE_DYNAMIC) ||
            !m_wndToolBar.LoadToolBar(IDR_MAINFRAME))
        {
            TRACE0("Failed to create toolbar\n");
            return FALSE;
        }
        
        // Set toolbar sizes
        m_wndToolBar.SetSizes(CSize(32, 32), CSize(24, 24));
        
        // Make toolbar dockable
        m_wndToolBar.EnableDocking(CBRS_ALIGN_ANY);
        pParentWnd->EnableDocking(CBRS_ALIGN_ANY);
        pParentWnd->DockControlBar(&m_wndToolBar);
        
        return TRUE;
    }
    
    void ModifyToolbar()
    {
        // Get toolbar control
        CToolBarCtrl& tbCtrl = m_wndToolBar.GetToolBarCtrl();
        
        // Add new button
        TBBUTTON tb = { 0 };
        tb.iBitmap = 5;           // Image index
        tb.idCommand = ID_MY_BUTTON;
        tb.fsState = TBSTATE_ENABLED;
        tb.fsStyle = TBSTYLE_BUTTON;
        tb.iString = (INT_PTR)_T("My Button");
        tbCtrl.AddButtons(1, &tb);
        
        // Add separator
        tb.fsStyle = TBSTYLE_SEP;
        tbCtrl.AddButtons(1, &tb);
        
        // Remove button
        int index = m_wndToolBar.CommandToIndex(ID_OLD_BUTTON);
        if (index >= 0)
        {
            m_wndToolBar.GetToolBarCtrl().DeleteButton(index);
        }
        
        // Hide/show button
        m_wndToolBar.GetToolBarCtrl().HideButton(ID_MY_BUTTON, TRUE);
    }
    
    // Toolbar customization
    void AllowCustomization()
    {
        // Enable toolbar customization dialog
        m_wndToolBar.EnableCustomization(TRUE);
    }
    
private:
    CToolBar m_wndToolBar;
};

// ============================================================================
// 3. CStatusBar - STATUS BAR
// ============================================================================

/*
CStatusBar displays status information at the bottom of a frame window.

Key methods:
- Create() - Create status bar
- SetIndicators() - Set pane indicators
- SetPaneText() - Set pane text
- GetPaneText() - Get pane text
- SetPaneInfo() - Set pane style, width, ID
- GetPaneInfo() - Get pane info
- SetPaneStyle() - Set pane style
- CommandToIndex() - Get pane index from ID
- GetItemID() - Get ID from index
- SetSizes() - Set pane sizes

Status bar panes are defined by an array of indicator IDs:
static UINT indicators[] =
{
    ID_SEPARATOR,           // Status line indicator
    ID_INDICATOR_CAPS,      // Caps Lock
    ID_INDICATOR_NUM,       // Num Lock
    ID_INDICATOR_SCRL,      // Scroll Lock
};
*/

class CStatusBarExample
{
public:
    BOOL CreateStatusBar(CWnd* pParentWnd)
    {
        // Define status bar panes
        static UINT indicators[] =
        {
            ID_SEPARATOR,           // Main status text (stretches)
            ID_INDICATOR_CAPS,      // Caps Lock
            ID_INDICATOR_NUM,       // Num Lock
            ID_INDICATOR_SCRL,      // Scroll Lock
            ID_INDICATOR_OVR,       // Overtype
            ID_SEPARATOR,           // Custom pane (line/col)
        };
        
        if (!m_wndStatusBar.Create(pParentWnd) ||
            !m_wndStatusBar.SetIndicators(indicators,
                sizeof(indicators) / sizeof(UINT)))
        {
            TRACE0("Failed to create status bar\n");
            return FALSE;
        }
        
        // Set pane widths
        m_wndStatusBar.SetPaneInfo(0, ID_SEPARATOR, SBPS_STRETCH, 100);
        m_wndStatusBar.SetPaneInfo(1, ID_INDICATOR_CAPS, SBPS_NORMAL, 50);
        m_wndStatusBar.SetPaneInfo(2, ID_INDICATOR_NUM, SBPS_NORMAL, 50);
        m_wndStatusBar.SetPaneInfo(3, ID_INDICATOR_SCRL, SBPS_NORMAL, 50);
        m_wndStatusBar.SetPaneInfo(4, ID_INDICATOR_OVR, SBPS_NORMAL, 50);
        m_wndStatusBar.SetPaneInfo(5, ID_SEPARATOR, SBPS_NORMAL, 100);
        
        return TRUE;
    }
    
    void UpdateStatusBar()
    {
        // Set main status text
        m_wndStatusBar.SetPaneText(0, _T("Ready"));
        
        // Set custom pane text
        CString text;
        text.Format(_T("Line: %d  Col: %d"), line, col);
        m_wndStatusBar.SetPaneText(5, text);
    }
    
    // Command UI handler for status bar panes
    void OnUpdateCapsLock(CCmdUI* pCmdUI)
    {
        pCmdUI->Enable(::GetKeyState(VK_CAPITAL) & 0x0001);
    }
    
    void OnUpdateNumLock(CCmdUI* pCmdUI)
    {
        pCmdUI->Enable(::GetKeyState(VK_NUMLOCK) & 0x0001);
    }
    
    void OnUpdateScrollLock(CCmdUI* pCmdUI)
    {
        pCmdUI->Enable(::GetKeyState(VK_SCROLL) & 0x0001);
    }
    
private:
    CStatusBar m_wndStatusBar;
};

// ============================================================================
// 4. REBAR CONTROL
// ============================================================================

/*
CReBar (Rebar) is a container that holds multiple toolbars/groups.
Each group has a gripper and can be rearranged by the user.

Key methods:
- Create() - Create rebar
- AddBar() - Add toolbar or dialog bar
- GetReBarCtrl() - Access underlying CReBarCtrl
*/

class CReBarExample
{
public:
    BOOL CreateReBar(CWnd* pParentWnd)
    {
        if (!m_wndReBar.Create(pParentWnd) ||
            !m_wndReBar.AddBar(&m_wndToolBar))
        {
            TRACE0("Failed to create rebar\n");
            return FALSE;
        }
        
        return TRUE;
    }
    
private:
    CReBar m_wndReBar;
    CToolBar m_wndToolBar;
};

// ============================================================================
// 5. DIALOG BAR
// ============================================================================

/*
CDialogBar is a modeless dialog that can be docked in a frame window.
Useful for tool windows with controls (e.g., color palette, font selector).

Key methods:
- Create() - Create dialog bar
- SetBarStyle() - Set bar style
*/

class CDialogBarExample
{
public:
    BOOL CreateDialogBar(CWnd* pParentWnd)
    {
        if (!m_wndDialogBar.Create(pParentWnd, IDD_DIALOGBAR,
            CBRS_LEFT | CBRS_TOOLTIPS | CBRS_FLYBY | CBRS_HIDE_INPLACE,
            IDD_DIALOGBAR))
        {
            TRACE0("Failed to create dialog bar\n");
            return FALSE;
        }
        
        m_wndDialogBar.EnableDocking(CBRS_ALIGN_ANY);
        pParentWnd->DockControlBar(&m_wndDialogBar);
        
        return TRUE;
    }
    
private:
    CDialogBar m_wndDialogBar;
};

// ============================================================================
// 6. COMMAND UI HANDLERS
// ============================================================================

/*
Command UI handlers update the state of menu items, toolbar buttons,
and status bar panes. They are called when the menu is displayed or
during idle processing.

CCmdUI methods:
- Enable(BOOL) - Enable/disable
- SetCheck(int) - Check/uncheck
- SetRadio(BOOL) - Radio button
- SetText(LPCTSTR) - Change text
- ContinueRouting() - Route to next target
*/

void OnUpdateViewToolbar(CCmdUI* pCmdUI)
{
    // Check/uncheck toolbar menu item based on visibility
    pCmdUI->SetCheck(m_wndToolBar.IsWindowVisible());
}

void OnUpdateViewStatusBar(CCmdUI* pCmdUI)
{
    pCmdUI->SetCheck(m_wndStatusBar.IsWindowVisible());
}

// ============================================================================
// 7. BEST PRACTICES
// ============================================================================

/*
1. Use CBRS_TOOLTIPS | CBRS_FLYBY for better user experience
2. Use CBRS_SIZE_DYNAMIC for floating toolbars
3. Enable docking for all control bars
4. Use command UI handlers for enabling/disabling
5. Use ID_SEPARATOR for stretchable status bar panes
6. Use indicator IDs for keyboard state panes
7. Use TrackPopupMenu for context menus
8. Use ModifyMenu for dynamic menu changes
9. Use SetPaneInfo for custom pane widths
10. Use GetToolBarCtrl() for advanced toolbar operations
*/

#endif // _MFC_VER
