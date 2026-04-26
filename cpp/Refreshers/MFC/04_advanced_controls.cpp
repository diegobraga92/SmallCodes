// ============================================================================
// MFC ADVANCED CONTROLS
// File: 04_advanced_controls.cpp
// Covers: CTreeCtrl, CListCtrl, CProgressCtrl, CSliderCtrl, CSpinButtonCtrl
// ============================================================================

#ifdef _MFC_VER

// ============================================================================
// 1. CTreeCtrl - TREE CONTROL
// ============================================================================

/*
CTreeCtrl wraps the Windows tree-view common control. Used for hierarchical
data display (file browsers, organization charts, etc.).

Key styles:
TVS_HASBUTTONS     - +/- buttons for expand/collapse
TVS_HASLINES       - Lines connecting parent to children
TVS_LINESATROOT    - Lines at root level
TVS_EDITLABELS     - Allow in-place editing
TVS_SHOWSELALWAYS  - Show selection even when control doesn't have focus
TVS_CHECKBOXES     - Check boxes next to items
TVS_FULLROWSELECT  - Full row selection highlight
TVS_INFOTIP        - Tooltip for items
TVS_TRACKSELECT    - Hot tracking

Key methods:
- InsertItem() - Add item (parent, text, image)
- DeleteItem() - Remove item
- DeleteAllItems() - Clear tree
- GetSelectedItem() / SelectItem() - Selection
- GetRootItem() - Get root item
- GetParentItem() / GetChildItem() - Navigation
- GetNextSiblingItem() / GetPrevSiblingItem() - Sibling navigation
- GetNextItem() - Generic navigation
- Expand() / ExpandAll() - Expand/collapse
- SetItemText() / GetItemText() - Item text
- SetItemData() / GetItemData() - Item data
- SetItemImage() / GetItemImage() - Item images
- SetCheck() / GetCheck() - Check state (with TVS_CHECKBOXES)
- EnsureVisible() - Scroll to make item visible
- SetBkColor() / SetTextColor() - Colors
*/

class CTreeCtrlExample
{
public:
    void CreateTree(CWnd* pParent)
    {
        m_tree.Create(
            WS_CHILD | WS_VISIBLE | WS_BORDER | WS_VSCROLL |
            TVS_HASBUTTONS | TVS_HASLINES | TVS_LINESATROOT |
            TVS_SHOWSELALWAYS | TVS_EDITLABELS,
            CRect(10, 10, 250, 300), pParent, IDC_TREE);
    }
    
    void PopulateTree()
    {
        // Clear existing items
        m_tree.DeleteAllItems();
        
        // Add root items
        HTREEITEM hRoot = m_tree.InsertItem(_T("Root"), TVI_ROOT);
        HTREEITEM hBranch1 = m_tree.InsertItem(_T("Branch 1"), hRoot);
        HTREEITEM hBranch2 = m_tree.InsertItem(_T("Branch 2"), hRoot);
        
        // Add child items
        m_tree.InsertItem(_T("Leaf 1.1"), hBranch1);
        m_tree.InsertItem(_T("Leaf 1.2"), hBranch1);
        m_tree.InsertItem(_T("Leaf 2.1"), hBranch2);
        m_tree.InsertItem(_T("Leaf 2.2"), hBranch2);
        
        // Expand root
        m_tree.Expand(hRoot, TVE_EXPAND);
        
        // Set item data (associate data with item)
        m_tree.SetItemData(hBranch1, (DWORD_PTR)100);
        m_tree.SetItemData(hBranch2, (DWORD_PTR)200);
    }
    
    void TreeOperations()
    {
        // Get selected item
        HTREEITEM hSel = m_tree.GetSelectedItem();
        if (hSel != nullptr)
        {
            CString text = m_tree.GetItemText(hSel);
            DWORD_PTR data = m_tree.GetItemData(hSel);
        }
        
        // Navigate tree
        HTREEITEM hRoot = m_tree.GetRootItem();
        HTREEITEM hChild = m_tree.GetChildItem(hRoot);
        
        while (hChild != nullptr)
        {
            // Process child
            hChild = m_tree.GetNextSiblingItem(hChild);
        }
        
        // Expand all
        ExpandAll(m_tree.GetRootItem());
        
        // Ensure visible
        m_tree.EnsureVisible(m_tree.GetRootItem());
    }
    
    void ExpandAll(HTREEITEM hItem)
    {
        if (hItem == nullptr) return;
        
        m_tree.Expand(hItem, TVE_EXPAND);
        
        HTREEITEM hChild = m_tree.GetChildItem(hItem);
        while (hChild != nullptr)
        {
            ExpandAll(hChild);
            hChild = m_tree.GetNextSiblingItem(hChild);
        }
    }
    
private:
    CTreeCtrl m_tree;
};

// ============================================================================
// 2. CListCtrl - LIST CONTROL
// ============================================================================

/*
CListCtrl wraps the Windows list-view common control. Supports four views:
1. Icon view (LVS_ICON) - Large icons
2. Small icon view (LVS_SMALLICON) - Small icons
3. List view (LVS_LIST) - Simple list
4. Report view (LVS_REPORT) - Columns (most common)

Key styles:
LVS_REPORT         - Report view with columns
LVS_SINGLESEL      - Single selection only
LVS_SHOWSELALWAYS  - Show selection without focus
LVS_EDITLABELS     - Allow in-place editing
LVS_NOSORTHEADER   - No sort on column click
LVS_OWNERDATA      - Virtual list (for large data sets)
LVS_EX_CHECKBOXES  - Check boxes
LVS_EX_FULLROWSELECT - Full row select
LVS_EX_GRIDLINES   - Grid lines
LVS_EX_TRACKSELECT - Hot tracking
LVS_EX_DOUBLEBUFFER - Double buffered (reduces flicker)

Key methods:
- InsertColumn() - Add column (report view)
- InsertItem() - Add item
- SetItemText() / GetItemText() - Item text
- SetItemData() / GetItemData() - Item data
- SetItemState() / GetItemState() - Item state
- DeleteItem() / DeleteAllItems() - Remove items
- DeleteColumn() - Remove column
- GetSelectedCount() / GetNextItem() - Selection
- SetColumnWidth() - Column width
- GetColumnWidth() - Get column width
- SortItems() - Custom sort
- SetView() - Change view (LVS_ICON, LVS_REPORT, etc.)
- SetExtendedStyle() - Extended styles
- EnsureVisible() - Scroll to item
*/

class CListCtrlExample
{
public:
    void CreateList(CWnd* pParent)
    {
        m_list.Create(
            WS_CHILD | WS_VISIBLE | WS_BORDER | WS_VSCROLL | WS_HSCROLL |
            LVS_REPORT | LVS_SINGLESEL | LVS_SHOWSELALWAYS,
            CRect(10, 10, 500, 300), pParent, IDC_LIST);
        
        // Set extended styles
        m_list.SetExtendedStyle(
            m_list.GetExtendedStyle() |
            LVS_EX_FULLROWSELECT |
            LVS_EX_GRIDLINES |
            LVS_EX_DOUBLEBUFFER);
    }
    
    void PopulateList()
    {
        // Add columns
        m_list.InsertColumn(0, _T("Name"), LVCFMT_LEFT, 150);
        m_list.InsertColumn(1, _T("Type"), LVCFMT_LEFT, 100);
        m_list.InsertColumn(2, _T("Size"), LVCFMT_RIGHT, 80);
        m_list.InsertColumn(3, _T("Modified"), LVCFMT_LEFT, 150);
        
        // Add items
        int index = m_list.InsertItem(0, _T("Document.txt"));
        m_list.SetItemText(index, 1, _T("Text File"));
        m_list.SetItemText(index, 2, _T("1.2 KB"));
        m_list.SetItemText(index, 3, _T("2024-01-15 10:30"));
        m_list.SetItemData(index, (DWORD_PTR)100);  // User data
        
        index = m_list.InsertItem(1, _T("Image.png"));
        m_list.SetItemText(index, 1, _T("PNG Image"));
        m_list.SetItemText(index, 2, _T("256 KB"));
        m_list.SetItemText(index, 3, _T("2024-01-14 15:45"));
        m_list.SetItemData(index, (DWORD_PTR)200);
        
        // Auto-size columns
        for (int i = 0; i < 4; i++)
        {
            m_list.SetColumnWidth(i, LVSCW_AUTOSIZE_USEHEADER);
        }
    }
    
    void ListOperations()
    {
        // Get selection
        POSITION pos = m_list.GetFirstSelectedItemPosition();
        if (pos != nullptr)
        {
            int nItem = m_list.GetNextSelectedItem(pos);
            CString text = m_list.GetItemText(nItem, 0);
            DWORD_PTR data = m_list.GetItemData(nItem);
        }
        
        // Get item count
        int count = m_list.GetItemCount();
        
        // Delete item
        m_list.DeleteItem(0);
        
        // Delete all
        m_list.DeleteAllItems();
        
        // Sort (custom callback)
        // m_list.SortItems(CompareFunc, (LPARAM)this);
        
        // Ensure visible
        m_list.EnsureVisible(0, FALSE);
    }
    
    // Custom sort callback
    static int CALLBACK CompareFunc(LPARAM lParam1, LPARAM lParam2, LPARAM lParamSort)
    {
        // Compare items by data
        if (lParam1 < lParam2) return -1;
        if (lParam1 > lParam2) return 1;
        return 0;
    }
    
private:
    CListCtrl m_list;
};

// ============================================================================
// 3. CProgressCtrl - PROGRESS CONTROL
// ============================================================================

/*
CProgressCtrl wraps the Windows progress bar control.

Key styles:
PBS_VERTICAL       - Vertical progress bar
PBS_SMOOTH         - Smooth (not blocky) appearance
PBS_MARQUEE        - Marquee style (indeterminate progress)
PBS_SMOOTHREVERSE  - Smooth reverse

Key methods:
- Create() - Create the progress bar
- SetRange() / GetRange() - Min/max values
- SetPos() / GetPos() - Current position
- OffsetPos() - Increment position
- SetStep() / StepIt() - Step increment
- SetMarquee() - Enable/disable marquee mode
- SetBarColor() / SetBkColor() - Colors
*/

void CreateProgressControl(CWnd* pParent)
{
    CProgressCtrl progress;
    
    // Standard progress bar
    progress.Create(
        WS_CHILD | WS_VISIBLE | PBS_SMOOTH,
        CRect(10, 10, 300, 30), pParent, IDC_PROGRESS);
    
    // Set range (0 to 100)
    progress.SetRange(0, 100);
    
    // Set position
    progress.SetPos(50);
    
    // Increment
    progress.OffsetPos(10);  // Now at 60
    
    // Step increment
    progress.SetStep(5);
    progress.StepIt();  // Now at 65
    
    // Marquee mode (indeterminate)
    // progress.SetMarquee(TRUE, 30);  // 30ms update rate
    
    // Vertical progress bar
    CProgressCtrl progressVert;
    progressVert.Create(
        WS_CHILD | WS_VISIBLE | PBS_VERTICAL | PBS_SMOOTH,
        CRect(10, 10, 30, 200), pParent, IDC_PROGRESS_VERT);
    progressVert.SetRange(0, 100);
    progressVert.SetPos(75);
}

// ============================================================================
// 4. CSliderCtrl - SLIDER CONTROL
// ============================================================================

/*
CSliderCtrl wraps the Windows trackbar control.

Key styles:
TBS_AUTOTICKS      - Auto tick marks
TBS_VERT           - Vertical slider
TBS_HORZ           - Horizontal slider
TBS_BOTH           - Ticks on both sides
TBS_NOTICKS        - No ticks
TBS_ENABLESELRANGE - Selection range highlighting
TBS_TOOLTIPS       - Tooltip showing value

Key methods:
- Create() - Create the slider
- SetRange() / GetRange() - Min/max values
- SetPos() / GetPos() - Current position
- SetTicFreq() - Tick mark frequency
- SetLineSize() / GetLineSize() - Arrow key increment
- SetPageSize() / GetPageSize() - Page up/down increment
- SetSelection() / ClearSel() - Selection range
- GetNumTics() - Number of tick marks
- SetBuddy() - Buddy control (e.g., edit showing value)
*/

void CreateSliderControl(CWnd* pParent)
{
    CSliderCtrl slider;
    
    slider.Create(
        WS_CHILD | WS_VISIBLE | TBS_HORZ | TBS_AUTOTICKS | TBS_TOOLTIPS,
        CRect(10, 10, 300, 40), pParent, IDC_SLIDER);
    
    // Set range (0 to 100)
    slider.SetRange(0, 100, TRUE);  // TRUE = redraw
    
    // Set position
    slider.SetPos(50);
    
    // Tick frequency (every 10 units)
    slider.SetTicFreq(10);
    
    // Line size (arrow keys)
    slider.SetLineSize(1);
    
    // Page size (Page Up/Down)
    slider.SetPageSize(10);
    
    // Selection range (highlighted area)
    slider.SetSelection(20, 80);
    
    // Get position
    int pos = slider.GetPos();
}

// ============================================================================
// 5. CSpinButtonCtrl - SPIN BUTTON CONTROL
// ============================================================================

/*
CSpinButtonCtrl wraps the Windows up-down control.
Usually paired with an edit control (buddy window).

Key styles:
UDS_ALIGNLEFT      - Spin button on left of buddy
UDS_ALIGNRIGHT     - Spin button on right of buddy
UDS_AUTOBUDDY      - Auto-select buddy window
UDS_ARROWKEYS      - Arrow keys change value
UDS_HORZ           - Horizontal orientation
UDS_NOTHOUSANDS    - No thousands separator
UDS_SETBUDDYINT    - Auto-update buddy text
UDS_WRAP           - Wrap around at min/max

Key methods:
- Create() - Create the spin button
- SetRange() / GetRange() - Min/max values
- SetPos() / GetPos() - Current position
- SetBase() - Base (10 or 16)
- SetBuddy() / GetBuddy() - Buddy control
- SetAccel() - Acceleration table
*/

void CreateSpinControl(CWnd* pParent)
{
    CSpinButtonCtrl spin;
    
    // Create spin button with auto-buddy
    spin.Create(
        WS_CHILD | WS_VISIBLE |
        UDS_AUTOBUDDY | UDS_SETBUDDYINT | UDS_ARROWKEYS | UDS_ALIGNRIGHT,
        CRect(0, 0, 0, 0), pParent, IDC_SPIN);
    
    // Set range
    spin.SetRange(0, 100);
    
    // Set position
    spin.SetPos(50);
    
    // Get position
    int pos = spin.GetPos();
    
    // Set acceleration (how fast value changes when held)
    UDACCEL accel[3] = {
        { 0, 1 },    // No delay, increment 1
        { 2, 5 },    // After 2 seconds, increment 5
        { 5, 10 }    // After 5 seconds, increment 10
    };
    spin.SetAccel(3, accel);
}

// ============================================================================
// 6. CAnimateCtrl - ANIMATION CONTROL
// ============================================================================

/*
CAnimateCtrl wraps the Windows animation control (AVI files).

Key styles:
ACS_CENTER         - Center animation in control
ACS_TRANSPARENT    - Transparent background
ACS_AUTOPLAY       - Auto-play on open
ACS_TIMER          - Use timer instead of separate thread

Key methods:
- Create() - Create the animation control
- Open() - Open AVI file or resource
- Play() / Stop() - Play/stop animation
- Close() - Close AVI
- Seek() - Seek to specific frame
*/

void CreateAnimationControl(CWnd* pParent)
{
    CAnimateCtrl anim;
    
    anim.Create(
        WS_CHILD | WS_VISIBLE | ACS_CENTER | ACS_AUTOPLAY,
        CRect(10, 10, 200, 200), pParent, IDC_ANIMATION);
    
    // Open from resource
    // anim.Open(IDR_AVI_ANIMATION);
    
    // Play (from frame 0 to end, loop indefinitely)
    // anim.Play(0, -1, -1);  // -1 = all frames, -1 = loop forever
}

// ============================================================================
// 7. COMMON CONTROL NOTIFICATIONS
// ============================================================================

/*
Tree control notifications (NM_* / TVN_*):
TVN_SELCHANGED     - Selection changed
TVN_ITEMEXPANDED   - Item expanded/collapsed
TVN_BEGINLABELEDIT - Start label editing
TVN_ENDLABELEDIT   - End label editing
TVN_DELETEITEM     - Item being deleted
TVN_GETDISPINFO    - Request item info (virtual tree)
NM_DBLCLK          - Double-click
NM_RCLICK          - Right-click
NM_CUSTOMDRAW      - Custom drawing

List control notifications (NM_* / LVN_*):
LVN_ITEMCHANGED    - Item state changed
LVN_COLUMNCLICK    - Column header clicked
LVN_BEGINLABELEDIT - Start label editing
LVN_ENDLABELEDIT   - End label editing
LVN_DELETEITEM     - Item being deleted
LVN_GETDISPINFO    - Request item info (virtual list)
LVN_ODFINDITEM     - Find item (virtual list)
NM_DBLCLK          - Double-click
NM_RCLICK          - Right-click
NM_CUSTOMDRAW      - Custom drawing

Slider notifications:
NM_CUSTOMDRAW      - Custom drawing
NM_RELEASEDCAPTURE - User released slider

Spin notifications:
UDN_DELTAPOS       - Position is changing
*/

// ============================================================================
// 8. BEST PRACTICES
// ============================================================================

/*
1. Use TVS_EDITLABELS with caution - handle TVN_ENDLABELEDIT
2. For large tree/list data, use virtual mode (TVS_NODATA / LVS_OWNERDATA)
3. Use LVS_EX_DOUBLEBUFFER to reduce flicker in list controls
4. Set extended styles after Create() for list controls
5. Use SetItemData to associate data with tree/list items
6. Use NM_CUSTOMDRAW for custom coloring of items
7. Always set buddy for spin controls (or use UDS_AUTOBUDDY)
8. Use PBS_MARQUEE for indeterminate progress
9. Use SetTicFreq for readable slider tick marks
10. Handle NM_RELEASEDCAPTURE for slider (not continuous updates)
*/

#endif // _MFC_VER
