# MFC (Microsoft Foundation Classes) Refreshers

## Overview

This directory contains comprehensive refresher files for MFC (Microsoft Foundation Classes), covering topics from junior to upper mid-level concepts. Each file focuses on a specific area of MFC development with detailed comments and practical code examples.

## Prerequisites

- Visual Studio (any edition with C++ MFC components)
- Windows SDK
- MFC libraries (install via Visual Studio Installer → Individual Components → "C++ MFC for latest v143 build tools")

## Structure

| File | Topic | Level |
|------|-------|-------|
| `00_mfc_architecture.cpp` | Application architecture, CWinApp, CFrameWnd, WinMain | Junior |
| `01_message_map_system.cpp` | Message maps, command routing, ON_WM_*, ON_COMMAND | Junior |
| `02_dialog_basics.cpp` | CDialog, modal/modeless, DDX/DDV, common dialogs | Junior |
| `03_controls.cpp` | Basic controls: CButton, CEdit, CListBox, CComboBox | Junior |
| `04_advanced_controls.cpp` | CTreeCtrl, CListCtrl, CProgressCtrl, CSliderCtrl | Junior-Mid |
| `05_document_view.cpp` | CDocument, CView, CScrollView, Serialize | Mid |
| `06_sdi_mdi_apps.cpp` | SDI vs MDI, document templates, multiple views | Mid |
| `07_menus_toolbars_status.cpp` | CMenu, CToolBar, CStatusBar, command UI handlers | Mid |
| `08_gdi_drawing.cpp` | CDC, CPaintDC, CPen, CBrush, CFont, CRect | Mid |
| `09_file_io_serialization.cpp` | CFile, CArchive, CStdioFile, Serialize versioning | Mid |
| `10_collections.cpp` | CArray, CList, CMap, CStringArray, type-safe templates | Mid |
| `11_threading.cpp` | CWinThread, AfxBeginThread, synchronization primitives | Mid |
| `12_property_sheets.cpp` | CPropertySheet, CPropertyPage, wizard dialogs | Mid |
| `13_splitter_views.cpp` | CSplitterWnd, multiple panes, CFormView | Mid-Upper |
| `14_activex_ole.cpp` | ActiveX controls, OLE drag-drop, OLE containers | Upper Mid |
| `15_database_odbc.cpp` | CDatabase, CRecordset, ODBC, CRecordView | Upper Mid |
| `16_networking_sockets.cpp` | CSocket, CAsyncSocket, CInternetSession | Upper Mid |
| `17_feature_pack.cpp` | CMFCRibbonBar, CMFCStatusBar, docking panes | Upper Mid |
| `18_debugging_error_handling.cpp` | ASSERT, VERIFY, TRACE, CException | Upper Mid |
| `19_custom_controls.cpp` | Subclassing, owner-draw, custom drawing | Upper Mid |
| `20_windows_common_controls.cpp` | Shell tree, rebar, animation, TaskDialog | Upper Mid |
| `_mfc_review.cpp` | Comprehensive review tying all concepts together | All |

## How to Use

Each file is self-contained with commented code examples. To compile and run:

1. Create a new MFC project in Visual Studio
2. Copy relevant sections into your project
3. Or use the code as reference for your own MFC applications

## Notes

- All code assumes MFC is available (Windows-only)
- Code examples use `#ifdef _MFC_VER` guards where appropriate
- Modern MFC (Feature Pack) examples require Visual Studio 2008+ with MFC Feature Pack
