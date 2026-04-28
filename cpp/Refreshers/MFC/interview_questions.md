# MFC Technical Interview Questions

> A comprehensive list of conversational technical interview questions covering MFC (Microsoft Foundation Classes) from junior to senior level. Based on the MFC refresher series covering 20 topics.

---

## 🟢 JUNIOR LEVEL — Fundamentals

### Application Architecture & Lifecycle

1. **What is the role of `CWinApp` in an MFC application, and what is the application lifecycle from startup to shutdown?**

   *Key points: Global CWinApp object constructed before WinMain, InitInstance() called to create main window, Run() enters message loop, ExitInstance() called on shutdown.*

2. **Explain the role of `InitInstance()` and `ExitInstance()`. What happens if `InitInstance()` returns `FALSE`?**

   *Key points: InitInstance creates main window and returns TRUE to continue; FALSE causes application to terminate. ExitInstance handles cleanup.*

3. **What is the purpose of `m_pMainWnd`, and why is it important to set it?**

   *Key points: Stores pointer to main frame window; used for proper shutdown, message routing, and identifying the application's main window.*

4. **How does MFC's internal `WinMain()` differ from a traditional Windows SDK `WinMain()`?**

   *Key points: MFC hides WinMain; it calls InitInstance, Run, ExitInstance automatically; handles message loop internally.*

5. **What is the difference between `Create()` and `LoadFrame()` for creating a frame window?**

   *Key points: Create() requires manual registration and parameters; LoadFrame() uses resource-defined settings (menu, icons, accelerators) — preferred for SDI/MDI apps.*

### Message Map System

6. **How do MFC message maps work internally? How do they differ from the traditional `switch` statement in `WndProc`?**

   *Key points: Message maps are static tables mapping messages to member functions; they support inheritance and routing; cleaner than giant switch statements.*

7. **What is the difference between `ON_COMMAND` and `ON_UPDATE_COMMAND_UI`? When would you use each?**

   *Key points: ON_COMMAND handles the action (click); ON_UPDATE_COMMAND_UI updates visual state (enabled/disabled, checked) when menus display or during idle.*

8. **How do you map a custom Windows message (e.g., `WM_APP + 100`) using MFC?**

   *Key points: Use `ON_MESSAGE(WM_APP + 100, handler)` in message map; handler signature is `afx_msg LRESULT handler(WPARAM, LPARAM)`.*

9. **What is the purpose of the `afx_msg` keyword in handler declarations?**

   *Key points: It's a documentation-only marker (maps to empty); indicates the function is a message handler; not enforced by compiler.*

10. **Explain the command routing order in an SDI application vs. an MDI application.**

    *Key points: SDI: View → Document → Document Template → Main Frame → App. MDI: Active Child Frame → View → Document → Doc Template → MDI Frame → App.*

### Dialog Basics

11. **What is the difference between a modal dialog and a modeless dialog? How do you create and manage each?**

    *Key points: Modal uses DoModal() (blocks); modeless uses Create() (non-blocking). Modeless must be heap-allocated with PostNcDestroy cleanup.*

12. **Explain how `DoDataExchange()` and `UpdateData()` work together. What happens when `UpdateData(TRUE)` vs. `UpdateData(FALSE)` is called?**

    *Key points: TRUE = controls → variables (read); FALSE = variables → controls (write). DoDataExchange handles the actual transfer via DDX/DDV macros.*

13. **What is the difference between `DDX` and `DDV`, and give examples of each?**

    *Key points: DDX transfers data (DDX_Text, DDX_Check); DDV validates data (DDV_MaxChars, DDV_MinMaxInt). DDV runs during save/validate.*

14. **Why must modeless dialogs be created on the heap, and what is the role of `PostNcDestroy()`?**

    *Key points: Modeless dialogs outlive the creating scope; PostNcDestroy deletes the C++ object after the window is destroyed to prevent memory leaks.*

15. **How do you handle a modeless dialog's `OnOK()` and `OnCancel()` differently from a modal dialog's?**

    *Key points: Modeless calls DestroyWindow() instead of EndDialog(); PostNcDestroy handles cleanup. Modal calls CDialog::OnOK/OnCancel which call EndDialog.*

### Basic Controls

16. **What is the difference between `BS_AUTOCHECKBOX` and `BS_CHECKBOX`? What about `BS_AUTORADIOBUTTON` vs. `BS_RADIOBUTTON`?**

    *Key points: Auto variants toggle state automatically on click; non-auto require manual SetCheck() calls.*

17. **How do you create a group of radio buttons and determine which one is selected?**

    *Key points: Use WS_GROUP on the first radio; use CheckRadioButton() to select; use GetCheckedRadioButton() to query.*

18. **What styles would you use to create a multi-line edit control with scroll bars?**

    *Key points: ES_MULTILINE | ES_AUTOVSCROLL | ES_AUTOHSCROLL | WS_VSCROLL | WS_HSCROLL | ES_WANTRETURN.*

19. **What is the difference between `CBS_DROPDOWN`, `CBS_DROPDOWNLIST`, and `CBS_SIMPLE` for combo boxes?**

    *Key points: DROPDOWN = editable + dropdown list; DROPDOWNLIST = static + dropdown list; SIMPLE = editable + always-visible list.*

20. **How do you associate extra data with a list box or combo box item?**

    *Key points: Use SetItemData() for DWORD_PTR values; use SetItemDataPtr() for pointers.*

### Menus, Toolbars, and Status Bars

21. **How do you create a right-click context menu in MFC?**

    *Key points: Load menu resource, get submenu with GetSubMenu(0), call TrackPopupMenu() with TPM_LEFTALIGN | TPM_RIGHTBUTTON.*

22. **How do `ON_UPDATE_COMMAND_UI` handlers work to enable/disable menu items and toolbar buttons?**

    *Key points: Called when menu displays or during idle; CCmdUI provides Enable(), SetCheck(), SetRadio(), SetText() methods.*

23. **How do you create a toolbar with docking support?**

    *Key points: Create toolbar with CBRS_* styles, call EnableDocking(CBRS_ALIGN_ANY) on toolbar, call EnableDocking on parent frame, then DockControlBar().*

### GDI Drawing Basics

24. **What is the difference between `CPaintDC`, `CClientDC`, and `CWindowDC`? When should each be used?**

    *Key points: CPaintDC only in OnPaint() (auto BeginPaint/EndPaint); CClientDC for client area outside WM_PAINT; CWindowDC for entire window including non-client.*

25. **Explain how you would use double buffering to eliminate flicker in custom drawing.**

    *Key points: Create compatible memory DC and bitmap, draw to memory DC, BitBlt to screen DC in one operation.*

26. **What is the importance of saving and restoring GDI objects when using `SelectObject()`?**

    *Key points: SelectObject returns previous object; must restore it to prevent GDI resource leaks; GDI objects are limited system resources.*

---

## 🟡 MID-LEVEL — Intermediate

### Document/View Architecture

27. **Explain the Document/View architecture. What are the benefits of separating data from presentation?**

    *Key points: CDocument stores data, CView displays it. Benefits: multiple views of same data, simplified serialization, clean separation of concerns, automatic command routing.*

28. **Describe the flow from `OnNewDocument()` through `Serialize()` when a user creates a new file.**

    *Key points: OnNewDocument initializes data, DeleteContents clears old data, Serialize called on save/open. Document template manages the lifecycle.*

29. **What is the purpose of `UpdateAllViews()` and how can you use hints (`lHint`, `pHint`) for efficient updates?**

    *Key points: Notifies all views (except sender) of data changes. Hints allow views to update only what changed rather than redrawing everything.*

30. **Compare `CScrollView`, `CFormView`, `CEditView`, `CListView`, and `CTreeView`. When would you choose each?**

    *Key points: CScrollView for large/zoomable documents; CFormView for data-entry forms; CEditView for text editing; CListView/CTreeView for structured data display.*

31. **How does `CFormView` combine dialog-based data entry with document/view architecture?**

    *Key points: Uses dialog resource template, supports DDX/DDV like CDialog, integrates with document via GetDocument(), can be used in splitter windows.*

### SDI vs MDI

32. **What are the key differences between SDI and MDI applications? When would you choose one over the other?**

    *Key points: SDI = one document at a time (simpler, less resources); MDI = multiple documents (complex, needs Window menu). Choose SDI for simple tools, MDI for IDEs/comparison apps.*

33. **How do you register multiple document types in a single MDI application?**

    *Key points: Create multiple CMultiDocTemplate objects with different resource IDs, document/view/frame classes, and file extensions; add each with AddDocTemplate().*

34. **How do you handle the Window menu in an MDI application (Cascade, Tile, Arrange Icons)?**

    *Key points: Use MDICascade(), MDITile(), MDIIconArrange(). MFC automatically adds open document list to Window menu.*

35. **What is the purpose of `FWS_ADDTOTITLE` in MDI child windows?**

    *Key points: Adds document title to child window title bar. Combined with FWS_PREFIXTITLE gives "Document - Application" format.*

### Advanced Controls

36. **Explain the difference between `TVS_HASLINES`, `TVS_LINESATROOT`, and `TVS_HASBUTTONS` in a tree control.**

    *Key points: HASLINES = connecting lines between items; LINESATROOT = lines at root level; HASBUTTONS = +/- expand/collapse buttons.*

37. **How do you implement virtual mode for a list control (`LVS_OWNERDATA`) and what are its benefits?**

    *Key points: Control requests item data via LVN_GETDISPINFO; benefits: handle millions of items without storing them all in the control, lower memory usage.*

38. **How do you enable checkboxes, full row selection, and grid lines in a `CListCtrl`?**

    *Key points: Use SetExtendedStyle() with LVS_EX_CHECKBOXES, LVS_EX_FULLROWSELECT, LVS_EX_GRIDLINES after Create().*

39. **How do you use `SetItemData()` and `GetItemData()` with tree and list controls?**

    *Key points: Associates DWORD_PTR value with each item; useful for storing IDs, indices, or pointers to associated data structures.*

40. **Explain how `NM_CUSTOMDRAW` works for customizing the appearance of list and tree controls.**

    *Key points: Notification sent during drawing; stages: CDDS_PREPAINT, CDDS_ITEMPREPAINT, CDDS_SUBITEM; return CDRF_NOTIFYITEMDRAW/CDRF_NOTIFYSUBITEMDRAW to chain notifications.*

### Property Sheets and Wizards

41. **What is the difference between a property sheet and a wizard? How do you enable wizard mode?**

    *Key points: Property sheet has tabs; wizard has Next/Back/Finish buttons. Enable with SetWizardMode() on the CPropertySheet.*

42. **How do you enable and use the Apply button in a property sheet?**

    *Key points: Call SetModified(TRUE) on a page to enable Apply; handle changes in OnApply(); use PSH_NOAPPLYNOW to hide Apply button.*

43. **Explain the `OnSetActive()`, `OnKillActive()`, `OnWizardNext()`, and `OnWizardFinish()` lifecycle methods.**

    *Key points: OnSetActive when page becomes active; OnKillActive when leaving (validate here); OnWizardNext/Finish for wizard navigation (return -1 to block).*

44. **How would you validate data when the user navigates between wizard pages?**

    *Key points: Override OnKillActive() or OnWizardNext(); call UpdateData(TRUE); return FALSE or -1 if validation fails.*

### File I/O and Serialization

45. **Compare `CFile`, `CStdioFile`, and `CMemFile`. When would you use each?**

    *Key points: CFile for binary I/O; CStdioFile for text with ReadString/WriteString; CMemFile for in-memory data (buffers, testing).*

46. **What does `CArchive` provide over raw `CFile::Read()/Write()` operations?**

    *Key points: Type-safe serialization with << and >> operators; handles complex MFC types (CString, CPoint, collections); manages object versioning.*

47. **How do you implement version support in `Serialize()` to handle different file format versions?**

    *Key points: Read/write a version number first; use switch on version to handle different formats; use VERSIONABLE_SCHEMA in IMPLEMENT_SERIAL.*

48. **What macros are required for a class to be serializable through `CArchive`?**

    *Key points: DECLARE_SERIAL in header, IMPLEMENT_SERIAL in .cpp (with class name, base class, schema number). Class needs default constructor and Serialize() override.*

49. **How would you serialize an entire `CArray` or `CList` using `CArchive`?**

    *Key points: Call the collection's Serialize(ar) method; or iterate and serialize each element individually with << / >> operators.*

### Collections

50. **Compare `CArray`, `CList`, and `CMap` in terms of performance characteristics and when to use each.**

    *Key points: CArray: O(1) index access, O(n) insert/remove; CList: O(1) insert/remove at known position, O(n) access; CMap: O(1) key lookup. Choose based on access pattern.*

51. **What is a `POSITION` variable, and how is it used with `CList` and `CMap`?**

    *Key points: POSITION is an opaque iterator; used with GetNext()/GetPrev() for lists and GetNextAssoc() for maps. Not a pointer — don't dereference it.*

52. **How do you iterate through all key-value pairs in a `CMap`?**

    *Key points: Use GetStartPosition() + GetNextAssoc() in a while loop: POSITION pos = map.GetStartPosition(); while(pos) { map.GetNextAssoc(pos, key, value); }*

### Threading

53. **What is the difference between a worker thread and a UI thread in MFC?**

    *Key points: Worker thread has no message pump (background computation); UI thread has its own message pump (can create windows). Use AfxBeginThread with function vs. runtime class.*

54. **Explain the MFC synchronization primitives: `CCriticalSection`, `CMutex`, `CSemaphore`, `CEvent`. When would you use each?**

    *Key points: CCriticalSection (fast, same process); CMutex (cross-process); CSemaphore (resource counting); CEvent (signaling between threads).*

55. **How do you use `CSingleLock` and `CMultiLock` for RAII-style locking?**

    *Key points: Constructor takes sync object and auto-lock flag; Lock()/Unlock() methods; destructor auto-unlocks. CMultiLock can wait on multiple objects.*

56. **How do you safely communicate between a worker thread and a UI thread?**

    *Key points: Use PostMessage/PostThreadMessage for async communication; never directly access MFC UI objects from worker threads; use shared data with synchronization.*

57. **Why shouldn't you directly access MFC objects from another thread? What is the safe alternative?**

    *Key points: MFC objects are not thread-safe; use PostMessage to the UI thread's window handle; use synchronization primitives for shared data.*

### Splitter Windows

58. **What is the difference between a static splitter and a dynamic splitter?**

    *Key points: Static splitter has fixed number of panes (CreateStatic); dynamic splitter allows user to split/unsplit (Create with max rows/cols).*

59. **How do you create a nested splitter (e.g., top/bottom with the bottom pane split left/right)?**

    *Key points: Create outer splitter, then create inner splitter in one of its panes using the pane's ID from IdFromRowCol().*

60. **How do views in different splitter panes communicate with each other?**

    *Key points: Through the shared document using UpdateAllViews()/OnUpdate(); or by accessing the other pane via GetPane() and casting.*

---

## 🔴 UPPER-MID TO SENIOR LEVEL

### Custom Controls, Subclassing & Owner-Draw

61. **What is the difference between subclassing a control and creating a custom control from scratch? When would you use each approach?**

    *Key points: Subclassing modifies existing control behavior (SubclassDlgItem); custom control from scratch (derive from CWnd, register class) for completely new UI elements.*

62. **Explain the owner-draw mechanism. What is `DrawItem()` and what information does `DRAWITEMSTRUCT` provide?**

    *Key points: Control sends WM_DRAWITEM; DrawItem() override receives DRAWITEMSTRUCT with CtlType, itemID, itemState, hDC, rcItem, itemData. Used for BS_OWNERDRAW buttons, etc.*

63. **Explain the custom draw (`NM_CUSTOMDRAW`) notification stages: `CDDS_PREPAINT`, `CDDS_ITEMPREPAINT`, `CDDS_SUBITEM | CDDS_ITEMPREPAINT`. How do you chain these notifications?**

    *Key points: Return CDRF_NOTIFYITEMDRAW from PREPAINT to get ITEMPREPAINT; return CDRF_NOTIFYSUBITEMDRAW from ITEMPREPAINT to get subitem notifications.*

64. **What is the purpose of `PreSubclassWindow()` and when should it be used?**

    *Key points: Called before the window is subclassed; use it to modify styles or perform initialization that must happen before the window procedure is attached.*

65. **How do you register a custom window class with `AfxRegisterWndClass()`?**

    *Key points: Pass style flags, cursor, background brush, and icon; returns class name string; use with CWnd::Create(). Must be called before creating the window.*

### ActiveX, OLE & Drag-and-Drop

66. **Explain the difference between embedding and linking in OLE compound documents.**

    *Key points: Embedding stores the object data inside the document; linking stores a reference to an external file. Embedded objects travel with the document; linked objects update from source.*

67. **How do you implement drag-and-drop using `COleDropTarget`? What events do you need to handle?**

    *Key points: Register with Register() in OnInitialUpdate(); override OnDragEnter, OnDragOver, OnDrop. Check data availability with IsDataAvailable().*

68. **How do you copy data to the clipboard using `COleDataSource` and check for available formats on paste?**

    *Key points: Cache data with CacheGlobalData(), call SetClipboard(). On paste, use COleDataObject::AttachClipboard() and IsDataAvailable() to check formats.*

69. **What is the `COleInsertDialog` and how is it used to embed OLE objects?**

    *Key points: Standard dialog for Insert Object; call DoModal(), then CreateItem() to create the COleClientItem from the dialog's selection.*

### Database (ODBC)

70. **Explain the relationship between `CDatabase`, `CRecordset`, and `CRecordView`.**

    *Key points: CDatabase manages the connection; CRecordset represents query results; CRecordView is a form view bound to a recordset with automatic navigation.*

71. **What is the difference between a dynaset and a snapshot recordset? When would you use each?**

    *Key points: Dynaset reflects changes made by other users (live data); snapshot is a static copy (consistent view). Use dynaset for interactive editing, snapshot for reporting.*

72. **How do you implement parameterized queries using MFC's RFX mechanism?**

    *Key points: Add parameter member variables, set m_nParams, use RFX_* with CFieldExchange::param in DoFieldExchange, set parameter values before Open()/Requery().*

73. **How do you handle transactions (`BeginTrans`, `CommitTrans`, `Rollback`) with `CDatabase`?**

    *Key points: Check CanTransact(), call BeginTrans(), execute SQL, call CommitTrans() on success or Rollback() on exception.*

74. **What are the RFX macros for mapping long, text, double, and date fields?**

    *Key points: RFX_Long(), RFX_Text(), RFX_Double(), RFX_Date(). Each takes CFieldExchange pointer, column name, and variable reference.*

### Networking & Sockets

75. **Compare `CAsyncSocket` and `CSocket`. When would you choose one over the other?**

    *Key points: CAsyncSocket is low-level and event-driven (override OnReceive, etc.); CSocket is higher-level, blocking, works with CArchive/CSocketFile for serialization.*

76. **How do you use `CSocketFile` with `CArchive` for serialized socket communication?**

    *Key points: Create CSocket → CSocketFile(socket) → CArchive(&file, store/load). Use << and >> operators to serialize data over the network.*

77. **Explain the event notifications in `CAsyncSocket` (`OnConnect`, `OnAccept`, `OnReceive`, `OnSend`, `OnClose`) and how they work.**

    *Key points: Override these to handle asynchronous socket events; called by MFC when the corresponding FD_* event occurs (registered via AsyncSelect).*

78. **What is the difference between TCP (`SOCK_STREAM`) and UDP (`SOCK_DGRAM`) socket communication in MFC?**

    *Key points: TCP is connection-oriented, reliable, uses Send()/Receive(); UDP is connectionless, unreliable, uses SendTo()/ReceiveFrom().*

### Feature Pack (Modern MFC)

79. **What is the MFC Feature Pack, and what modern UI elements did it introduce?**

    *Key points: Introduced in VS 2008 SP1+; includes ribbon bar, dockable panes, modern menu/toolbar/status bar, property grid, task dialogs, color/font pickers.*

80. **How do you create a ribbon bar using `CMFCRibbonBar`? Explain the hierarchy: Category → Panel → Button.**

    *Key points: Create ribbon bar, add categories (tabs), add panels to categories, add controls (buttons, combos, checkboxes) to panels.*

81. **How do you implement a dockable pane with auto-hide support using `CDockablePane`?**

    *Key points: Create CDockablePane, enable docking, dock to frame, call SetAutoHideMode(TRUE, CBRS_ALIGN_*) to enable auto-hide (pin/unpin behavior).*

82. **What is `CMFCPropertyGridCtrl`, and how do you add categories and properties to it?**

    *Key points: Property grid control (VS Properties window style). Create CMFCPropertyGridProperty objects for categories, add sub-items for properties, add to grid with AddProperty().*

83. **How do `CMFCMenuBar` and `CMFCToolBar` compare with the traditional `CMenu` and `CToolBar`?**

    *Key points: Feature Pack versions support Office/VS-style appearance, customization dialogs, large/small icons, keyboard shortcuts, user-defined toolbars.*

84. **Explain how `CMFCStatusBar` supports progress bars in panes.**

    *Key points: EnablePaneProgressBar() enables progress in a pane; SetPaneProgress() sets the value; useful for showing operation progress in the status bar.*

### Debugging & Error Handling

85. **What is the difference between `ASSERT`, `VERIFY`, and `ENSURE`? When should each be used?**

    *Key points: ASSERT = debug-only check; VERIFY = evaluates in both debug and release (asserts in debug); ENSURE = checks and throws exception if failed.*

86. **How do you override `AssertValid()` and `Dump()` in a custom `CObject`-derived class for diagnostic support?**

    *Key points: Override inside #ifdef _DEBUG; AssertValid() validates member invariants with ASSERT; Dump() outputs member values to CDumpContext (afxDump).*

87. **What MFC exception classes exist, and how do you properly handle and cleanup after an MFC exception?**

    *Key points: CFileException, CArchiveException, CDBException, CMemoryException, COleException, etc. Catch by pointer, call ReportError() or GetErrorMessage(), then Delete().*

88. **How does `DEBUG_NEW` help with memory leak detection?**

    *Key points: When #define new DEBUG_NEW, it tracks file/line of allocations; at program exit, unreleased allocations are reported in the Output window.*

### Design & Architecture

89. **Explain the complete command routing chain in MFC. How does a menu command reach the appropriate handler?**

    *Key points: Active child → View → Document → Doc Template → Main Frame → App. If no handler found, the command is automatically disabled.*

90. **How would you implement multiple views of the same document (e.g., a form view and a list view sharing data)?**

    *Key points: Use a splitter window with two panes; both views share the same CDocument; use UpdateAllViews() with hints for synchronization.*

91. **What is the purpose of `CCmdUI`, and how does MFC automatically disable commands that have no handler?**

    *Key points: CCmdUI provides Enable/SetCheck/SetRadio. MFC routes commands through the chain; if no handler found, the command UI is automatically disabled.*

92. **Describe how you would architect a large MFC application using the Document/View pattern with splitter windows, ribbon UI, docking panes, and a property grid.**

    *Key points: Use CFrameWndEx, CMFCRibbonBar, CDockablePane for tool windows, CSplitterWnd for main workspace, CMFCPropertyGridCtrl for properties, all sharing data through CDocument.*

93. **What considerations should guide your choice between using the classic MFC controls, custom-draw, or the Feature Pack classes?**

    *Key points: Classic for simplicity/standard look; custom-draw for unique branding/requirements; Feature Pack for modern Office/VS-style UI with less custom code.*

---

## 💡 BONUS: Behavioral & Problem-Solving Questions

94. **Describe a time you had to debug a memory leak in an MFC application. What tools and techniques did you use?**

    *Key points: DEBUG_NEW, CRT debug heap, _CrtDumpMemoryLeaks(), Visual Studio diagnostic tools, checking GDI object counts, ensuring SelectObject restore pairs.*

95. **How would you approach modernizing a legacy MFC application? What would you keep, rewrite, or wrap?**

    *Key points: Incremental approach — keep business logic, modernize UI with Feature Pack classes, consider wrapping MFC in COM/.NET interop, or gradually migrating to WPF/Qt.*

96. **Have you worked with both MFC and a modern UI framework (WPF, Qt, web). What are the trade-offs you've observed?**

    *Key points: MFC: native performance, deep Windows integration, but verbose and dated. Modern frameworks: better separation, data binding, but higher overhead and learning curve.*

97. **How would you design a thread-safe data processing pipeline using MFC threading primitives?**

    *Key points: Worker threads for processing, CEvent for signaling, CCriticalSection for shared data access, PostMessage to UI thread for progress updates.*

98. **Explain how you would implement undo/redo support in an MFC document/view application.**

    *Key points: Command pattern — store actions as CObject-derived command objects in two stacks (undo/redo); each command has Do()/Undo() methods; document calls UpdateAllViews after each operation.*

99. **How would you handle a scenario where a user edits data in a `CFormView`, and you need to update the document and all other views?**

    *Key points: Call UpdateData(TRUE) to read controls, update document members, call SetModifiedFlag(), then UpdateAllViews(this) with appropriate hints. Other views handle OnUpdate().*

100. **What strategies would you use to reduce flicker during complex custom drawing operations?**

     *Key points: Double buffering (memory DC + BitBlt), override OnEraseBkgnd to return TRUE (prevent erasing), use InvalidateRect with specific region instead of Invalidate(), use LVS_EX_DOUBLEBUFFER for list controls.*

---

*Generated from the MFC Refreshers series covering 20 topics: architecture, message maps, dialogs, controls, document/view, SDI/MDI, menus/toolbars, GDI, file I/O, collections, threading, property sheets, splitters, OLE/ActiveX, ODBC, networking, Feature Pack, debugging, custom controls, and common controls.*
