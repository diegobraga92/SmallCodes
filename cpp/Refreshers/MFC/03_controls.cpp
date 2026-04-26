// ============================================================================
// MFC BASIC CONTROLS
// File: 03_controls.cpp
// Covers: CButton, CEdit, CListBox, CComboBox, CStatic, CScrollBar
// ============================================================================

#ifdef _MFC_VER

// ============================================================================
// 1. CButton - BUTTON CONTROL
// ============================================================================

/*
CButton wraps the Windows button control. Supports:
- Push button (BS_PUSHBUTTON) - Default
- Check box (BS_CHECKBOX, BS_AUTOCHECKBOX)
- Radio button (BS_RADIOBUTTON, BS_AUTORADIOBUTTON)
- Group box (BS_GROUPBOX)
- Owner-draw button (BS_OWNERDRAW)

Key methods:
- Create() - Create the button
- SetWindowText() - Set button text
- GetWindowText() - Get button text
- SetCheck() - Set check state (BST_CHECKED/BST_UNCHECKED/BST_INDETERMINATE)
- GetCheck() - Get check state
- SetState() - Set button highlight state
- GetState() - Get button state
- SetButtonStyle() - Change button style
- GetButtonStyle() - Get button style
*/

class CButtonExample
{
public:
    // Creating buttons programmatically
    void CreateButtons(CWnd* pParent)
    {
        // Push button
        m_btnOk.Create(_T("&OK"),
            WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON,
            CRect(10, 10, 100, 35), pParent, IDOK);
        
        // Check box
        m_chkOption.Create(_T("&Enable Feature"),
            WS_CHILD | WS_VISIBLE | BS_AUTOCHECKBOX,
            CRect(10, 50, 200, 70), pParent, IDC_CHECK_OPTION);
        
        // Radio button (first in group)
        m_radio1.Create(_T("&Option A"),
            WS_CHILD | WS_VISIBLE | BS_AUTORADIOBUTTON | WS_GROUP,
            CRect(10, 90, 150, 110), pParent, IDC_RADIO_A);
        
        // Radio button (same group, no WS_GROUP)
        m_radio2.Create(_T("O&ption B"),
            WS_CHILD | WS_VISIBLE | BS_AUTORADIOBUTTON,
            CRect(10, 115, 150, 135), pParent, IDC_RADIO_B);
        
        // Group box
        m_group.Create(_T("Options"),
            WS_CHILD | WS_VISIBLE | BS_GROUPBOX,
            CRect(5, 75, 200, 150), pParent, IDC_GROUP_OPTIONS);
    }
    
    // Check box state
    void SetCheckBoxState(BOOL bChecked)
    {
        m_chkOption.SetCheck(bChecked ? BST_CHECKED : BST_UNCHECKED);
    }
    
    BOOL IsCheckBoxChecked()
    {
        return m_chkOption.GetCheck() == BST_CHECKED;
    }
    
    // Radio button selection
    void SelectRadio(int nIndex)
    {
        // CheckRadioButton handles radio group automatically
        CheckRadioButton(IDC_RADIO_A, IDC_RADIO_B,
            nIndex == 0 ? IDC_RADIO_A : IDC_RADIO_B);
    }
    
    int GetSelectedRadio()
    {
        int id = GetCheckedRadioButton(IDC_RADIO_A, IDC_RADIO_B);
        return (id == IDC_RADIO_A) ? 0 : 1;
    }
    
private:
    CButton m_btnOk;
    CButton m_chkOption;
    CButton m_radio1;
    CButton m_radio2;
    CButton m_group;
};

// ============================================================================
// 2. CEdit - EDIT CONTROL
// ============================================================================

/*
CEdit wraps the Windows edit control. Supports:
- Single-line (ES_AUTOHSCROLL)
- Multi-line (ES_MULTILINE | ES_AUTOVSCROLL | ES_WANTRETURN)
- Password (ES_PASSWORD)
- Read-only (ES_READONLY)
- Number-only (ES_NUMBER)
- Uppercase/Lowercase (ES_UPPERCASE/ES_LOWERCASE)

Key methods:
- Create() - Create the edit control
- SetWindowText() / GetWindowText() - Set/get text
- GetSel() / SetSel() - Get/set selection
- ReplaceSel() - Replace selected text
- GetLimitText() / SetLimitText() - Character limit
- CanUndo() / Undo() - Undo support
- Clear() - Clear selection
- Copy() / Cut() / Paste() - Clipboard operations
- SetReadOnly() - Toggle read-only
- GetLineCount() - Number of lines (multi-line)
- GetLine() - Get specific line (multi-line)
- LineScroll() - Scroll by lines
- LineFromChar() - Get line from character index
*/

class CEditExample
{
public:
    void CreateEdits(CWnd* pParent)
    {
        // Single-line edit
        m_editName.Create(
            WS_CHILD | WS_VISIBLE | WS_BORDER | ES_AUTOHSCROLL,
            CRect(10, 10, 200, 30), pParent, IDC_NAME_EDIT);
        
        // Password edit
        m_editPassword.Create(
            WS_CHILD | WS_VISIBLE | WS_BORDER | ES_PASSWORD | ES_AUTOHSCROLL,
            CRect(10, 40, 200, 60), pParent, IDC_PASSWORD_EDIT);
        
        // Multi-line edit with scroll bars
        m_editMulti.Create(
            WS_CHILD | WS_VISIBLE | WS_BORDER | WS_VSCROLL | WS_HSCROLL |
            ES_MULTILINE | ES_AUTOVSCROLL | ES_AUTOHSCROLL | ES_WANTRETURN,
            CRect(10, 70, 300, 200), pParent, IDC_MULTI_EDIT);
        
        // Read-only edit
        m_editReadOnly.Create(
            WS_CHILD | WS_VISIBLE | WS_BORDER | ES_READONLY | ES_AUTOHSCROLL,
            CRect(10, 210, 300, 230), pParent, IDC_READONLY_EDIT);
        
        // Number-only edit
        m_editNumber.Create(
            WS_CHILD | WS_VISIBLE | WS_BORDER | ES_NUMBER | ES_AUTOHSCROLL,
            CRect(10, 240, 100, 260), pParent, IDC_NUMBER_EDIT);
    }
    
    void EditOperations()
    {
        CString text;
        
        // Get text
        m_editName.GetWindowText(text);
        
        // Set text
        m_editName.SetWindowText(_T("John Doe"));
        
        // Set character limit
        m_editName.SetLimitText(50);
        
        // Select all text
        m_editName.SetSel(0, -1);
        
        // Replace selection
        m_editName.ReplaceSel(_T("New Text"));
        
        // Get selection
        int start, end;
        m_editName.GetSel(start, end);
        
        // Multi-line operations
        int lineCount = m_editMulti.GetLineCount();
        
        // Get specific line
        TCHAR buffer[256];
        int len = m_editMulti.GetLine(0, buffer, 255);
        buffer[len] = _T('\0');
        
        // Scroll to specific line
        m_editMulti.LineScroll(0, 5);  // Scroll down 5 lines
    }
    
private:
    CEdit m_editName;
    CEdit m_editPassword;
    CEdit m_editMulti;
    CEdit m_editReadOnly;
    CEdit m_editNumber;
};

// ============================================================================
// 3. CListBox - LIST BOX CONTROL
// ============================================================================

/*
CListBox wraps the Windows list box control. Supports:
- Single selection (LBS_STANDARD)
- Multiple selection (LBS_MULTIPLESEL)
- Extended selection (LBS_EXTENDEDSEL)
- Owner-draw (LBS_OWNERDRAWFIXED, LBS_OWNERDRAWVARIABLE)
- Sort (LBS_SORT) or no sort (LBS_NOSORT)
- Multi-column (LBS_MULTICOLUMN)
- No data (LBS_NODATA) - virtual list box

Key methods:
- AddString() / InsertString() - Add items
- DeleteString() - Remove item
- ResetContent() - Clear all items
- GetCount() - Number of items
- GetText() - Get item text
- GetCurSel() / SetCurSel() - Single selection
- GetSelCount() / GetSelItems() - Multiple selection
- SelItemRange() - Select range (multiple)
- FindString() / SelectString() - Find item
- SetItemData() / GetItemData() - Attach 32-bit data to item
- SetItemDataPtr() / GetItemDataPtr() - Attach pointer to item
- SetTopIndex() / GetTopIndex() - Scrolling
- SetColumnWidth() - Multi-column width
*/

class CListBoxExample
{
public:
    void CreateListBox(CWnd* pParent)
    {
        // Standard list box with sort
        m_listBox.Create(
            WS_CHILD | WS_VISIBLE | WS_BORDER | WS_VSCROLL |
            LBS_STANDARD,  // LBS_NOTIFY | LBS_SORT | WS_VSCROLL | WS_BORDER
            CRect(10, 10, 200, 200), pParent, IDC_LISTBOX);
        
        // Multiple selection list box
        m_listBoxMulti.Create(
            WS_CHILD | WS_VISIBLE | WS_BORDER | WS_VSCROLL |
            LBS_MULTIPLESEL | LBS_NOSORT,
            CRect(220, 10, 420, 200), pParent, IDC_LISTBOX_MULTI);
    }
    
    void ListBoxOperations()
    {
        // Add items
        m_listBox.AddString(_T("Item 1"));
        m_listBox.AddString(_T("Item 2"));
        m_listBox.AddString(_T("Item 3"));
        
        // Insert at specific position
        m_listBox.InsertString(1, _T("Inserted Item"));
        
        // Attach data to items
        m_listBox.SetItemData(0, (DWORD_PTR)100);  // User data
        m_listBox.SetItemData(1, (DWORD_PTR)200);
        
        // Get item data
        DWORD_PTR data = m_listBox.GetItemData(0);
        
        // Single selection
        int sel = m_listBox.GetCurSel();
        if (sel != LB_ERR)
        {
            CString text;
            m_listBox.GetText(sel, text);
        }
        
        // Multiple selection
        int selCount = m_listBoxMulti.GetSelCount();
        if (selCount > 0)
        {
            int* selections = new int[selCount];
            m_listBoxMulti.GetSelItems(selCount, selections);
            // Process selections
            delete[] selections;
        }
        
        // Find string
        int index = m_listBox.FindString(-1, _T("Item 2"));
        
        // Select string
        m_listBox.SelectString(-1, _T("Item 2"));
        
        // Delete item
        m_listBox.DeleteString(0);
        
        // Clear all
        m_listBox.ResetContent();
        
        // Get count
        int count = m_listBox.GetCount();
    }
    
private:
    CListBox m_listBox;
    CListBox m_listBoxMulti;
};

// ============================================================================
// 4. CComboBox - COMBO BOX CONTROL
// ============================================================================

/*
CComboBox wraps the Windows combo box control. Supports:
- Simple (CBS_SIMPLE) - Edit + always-visible list
- Dropdown (CBS_DROPDOWN) - Edit + dropdown list
- Drop List (CBS_DROPDOWNLIST) - Static text + dropdown list
- Owner-draw (CBS_OWNERDRAWFIXED, CBS_OWNERDRAWVARIABLE)
- Auto sort (CBS_SORT) or no sort (CBS_NOSORT)

Key methods:
- AddString() / InsertString() - Add items
- DeleteString() / ResetContent() - Remove items
- GetCount() - Number of items
- GetLBText() / GetLBTextLen() - Get item text
- GetCurSel() / SetCurSel() - Get/set selection
- SelectString() / FindString() - Find item
- SetItemData() / GetItemData() - Attach data
- GetEditSel() / SetEditSel() - Edit portion selection
- SetDroppedWidth() / GetDroppedWidth() - Dropdown width
- ShowDropDown() - Show/hide dropdown
- GetDroppedState() - Is dropdown visible?
- GetDroppedControlRect() - Dropdown rectangle
- LimitText() - Max text length in edit portion
*/

class CComboBoxExample
{
public:
    void CreateComboBoxes(CWnd* pParent)
    {
        // Dropdown combo box (editable)
        m_comboDropDown.Create(
            WS_CHILD | WS_VISIBLE | WS_BORDER | WS_VSCROLL |
            CBS_DROPDOWN | CBS_SORT,
            CRect(10, 10, 200, 150), pParent, IDC_COMBO_DROPDOWN);
        
        // Drop list combo box (not editable)
        m_comboDropList.Create(
            WS_CHILD | WS_VISIBLE | WS_BORDER | WS_VSCROLL |
            CBS_DROPDOWNLIST | CBS_SORT,
            CRect(10, 60, 200, 200), pParent, IDC_COMBO_DROPLIST);
        
        // Simple combo box (always visible list)
        m_comboSimple.Create(
            WS_CHILD | WS_VISIBLE | WS_BORDER | WS_VSCROLL |
            CBS_SIMPLE | CBS_SORT,
            CRect(10, 110, 200, 300), pParent, IDC_COMBO_SIMPLE);
    }
    
    void ComboBoxOperations()
    {
        // Add items
        m_comboDropDown.AddString(_T("Option 1"));
        m_comboDropDown.AddString(_T("Option 2"));
        m_comboDropDown.AddString(_T("Option 3"));
        
        // Insert at position
        m_comboDropDown.InsertString(0, _T("First Option"));
        
        // Set selection
        m_comboDropDown.SetCurSel(0);
        
        // Get selection
        int sel = m_comboDropDown.GetCurSel();
        if (sel != CB_ERR)
        {
            CString text;
            m_comboDropDown.GetLBText(sel, text);
        }
        
        // Find string
        int index = m_comboDropDown.FindString(-1, _T("Option 2"));
        
        // Select by string
        m_comboDropDown.SelectString(-1, _T("Option 2"));
        
        // Set dropdown width (wider than control)
        m_comboDropDown.SetDroppedWidth(300);
        
        // Limit text in edit portion
        m_comboDropDown.LimitText(50);
        
        // Clear all
        m_comboDropDown.ResetContent();
    }
    
private:
    CComboBox m_comboDropDown;
    CComboBox m_comboDropList;
    CComboBox m_comboSimple;
};

// ============================================================================
// 5. CStatic - STATIC CONTROL
// ============================================================================

/*
CStatic wraps the Windows static control. Supports:
- Text label (SS_LEFT, SS_CENTER, SS_RIGHT)
- Image (SS_BITMAP, SS_ICON, SS_ENHMETAFILE)
- Owner-draw (SS_OWNERDRAW)
- Notify (SS_NOTIFY) - Enable click notifications
- Sunken/Elevated border (SS_SUNKEN, SS_ETCHED*)
- Black/Gray/White frame and rect

Key methods:
- Create() - Create the static control
- SetBitmap() / GetBitmap() - Bitmap image
- SetIcon() / GetIcon() - Icon image
- SetEnhMetaFile() / GetEnhMetaFile() - Enhanced metafile
- SetWindowText() / GetWindowText() - Text
*/

void CreateStaticControls(CWnd* pParent)
{
    CStatic* pStatic;
    
    // Text label
    pStatic = new CStatic();
    pStatic->Create(_T("Name:"),
        WS_CHILD | WS_VISIBLE | SS_RIGHT,
        CRect(10, 10, 80, 30), pParent);
    
    // Centered text
    pStatic = new CStatic();
    pStatic->Create(_T("Important Notice"),
        WS_CHILD | WS_VISIBLE | SS_CENTER | SS_SUNKEN,
        CRect(10, 40, 200, 60), pParent);
    
    // Icon
    pStatic = new CStatic();
    HICON hIcon = ::LoadIcon(nullptr, IDI_INFORMATION);
    pStatic->Create(_T(""),
        WS_CHILD | WS_VISIBLE | SS_ICON,
        CRect(10, 70, 50, 100), pParent);
    pStatic->SetIcon(hIcon);
}

// ============================================================================
// 6. CScrollBar - SCROLL BAR CONTROL
// ============================================================================

/*
CScrollBar wraps the Windows scroll bar control.
Can be horizontal (SBS_HORZ) or vertical (SBS_VERT).

Key methods:
- Create() - Create the scroll bar
- SetScrollRange() / GetScrollRange() - Min/max values
- SetScrollPos() / GetScrollPos() - Current position
- SetScrollInfo() / GetScrollInfo() - Extended info (page size, etc.)
- ShowScrollBar() - Show/hide
- EnableScrollBar() - Enable/disable arrows
*/

void CreateScrollBar(CWnd* pParent)
{
    CScrollBar scrollBar;
    
    scrollBar.Create(
        WS_CHILD | WS_VISIBLE | SBS_HORZ,
        CRect(10, 10, 300, 30), pParent, IDC_SCROLLBAR);
    
    // Set range (0 to 100)
    scrollBar.SetScrollRange(0, 100);
    
    // Set position
    scrollBar.SetScrollPos(50);
    
    // Extended info with page size
    SCROLLINFO si = { sizeof(SCROLLINFO) };
    si.fMask = SIF_ALL;
    si.nMin = 0;
    si.nMax = 100;
    si.nPage = 10;   // Thumb size proportional to page
    si.nPos = 50;
    scrollBar.SetScrollInfo(&si);
}

// ============================================================================
// 7. CONTROL STYLES REFERENCE
// ============================================================================

/*
Common Control Styles:

Button Styles:
BS_PUSHBUTTON      - Standard push button
BS_DEFPUSHBUTTON   - Default push button (bolder border)
BS_CHECKBOX        - Check box
BS_AUTOCHECKBOX    - Auto check box (toggles on click)
BS_RADIOBUTTON     - Radio button
BS_AUTORADIOBUTTON - Auto radio button
BS_GROUPBOX        - Group box
BS_OWNERDRAW       - Owner-draw button
BS_BITMAP          - Button displays bitmap
BS_ICON            - Button displays icon
BS_FLAT            - Flat button
BS_MULTILINE       - Multi-line button text

Edit Styles:
ES_LEFT            - Left align text
ES_CENTER          - Center align text
ES_RIGHT           - Right align text
ES_MULTILINE       - Multi-line edit
ES_UPPERCASE       - Convert to uppercase
ES_LOWERCASE       - Convert to lowercase
ES_PASSWORD        - Password field
ES_AUTOVSCROLL     - Auto vertical scroll
ES_AUTOHSCROLL     - Auto horizontal scroll
ES_NUMBER          - Numbers only
ES_READONLY        - Read-only
ES_WANTRETURN      - Enter inserts newline (multi-line)

List Box Styles:
LBS_STANDARD       - Standard (notify | sort | vscroll | border)
LBS_SORT           - Alphabetical sort
LBS_NOSORT         - No sort
LBS_NOTIFY         - Parent receives notifications
LBS_MULTIPLESEL    - Multiple selection
LBS_EXTENDEDSEL    - Extended selection (Shift+Click, Ctrl+Click)
LBS_MULTICOLUMN    - Multi-column
LBS_NODATA         - Virtual list box (no strings stored)
LBS_OWNERDRAWFIXED - Owner-draw, fixed height
LBS_OWNERDRAWVARIABLE - Owner-draw, variable height
LBS_HASSTRINGS     - Items have strings (with owner-draw)
LBS_USETABSTOPS    - Tab stops in items
LBS_NOINTEGRALHEIGHT - Exact height (not multiple of item height)

Combo Box Styles:
CBS_SIMPLE         - Edit + always-visible list
CBS_DROPDOWN       - Edit + dropdown list
CBS_DROPDOWNLIST   - Static + dropdown list
CBS_OWNERDRAWFIXED - Owner-draw fixed height
CBS_OWNERDRAWVARIABLE - Owner-draw variable height
CBS_AUTOHSCROLL    - Auto horizontal scroll in edit
CBS_SORT           - Alphabetical sort
CBS_HASSTRINGS     - Items have strings
CBS_NOINTEGRALHEIGHT - Exact height
CBS_DISABLENOSCROLL - Always show scroll bar
*/

// ============================================================================
// 8. BEST PRACTICES
// ============================================================================

/*
1. Use DDX_Control to attach member variables to controls in DoDataExchange
2. Create controls in OnCreate or OnInitDialog, not in constructor
3. Use WS_CHILD | WS_VISIBLE for all child controls
4. Set control limits (SetLimitText, LimitText) to prevent buffer overflow
5. Use SetItemData/GetItemData to associate data with list/combo items
6. Use CheckRadioButton for radio button groups (not manual SetCheck)
7. Use BS_AUTOCHECKBOX and BS_AUTORADIOBUTTON for auto-toggle behavior
8. Always check return values from Create()
9. Use resource IDs (IDC_*) for control identification
10. Clean up dynamically created controls in destructor
*/

#endif // _MFC_VER
