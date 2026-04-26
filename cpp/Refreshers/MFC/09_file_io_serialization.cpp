// ============================================================================
// MFC FILE I/O AND SERIALIZATION
// File: 09_file_io_serialization.cpp
// Covers: CFile, CArchive, CStdioFile, Serialize, versioning, binary vs text
// ============================================================================

#ifdef _MFC_VER

// ============================================================================
// 1. CFile - LOW-LEVEL FILE OPERATIONS
// ============================================================================

/*
CFile is the base class for MFC file operations. Provides binary I/O.

Key methods:
- Open() / Close() - Open/close file
- Read() / Write() - Read/write data
- Seek() / SeekToBegin() / SeekToEnd() - Position
- GetLength() / SetLength() - File size
- GetPosition() - Current position
- Flush() - Flush buffers
- GetStatus() / SetStatus() - File status
- Rename() / Remove() - File operations (static)
- GetFileName() / GetFilePath() - Path info

Open flags:
CFile::modeCreate      - Create new file (overwrite if exists)
CFile::modeRead        - Read-only
CFile::modeWrite       - Write-only
CFile::modeReadWrite   - Read/write
CFile::modeNoTruncate  - Don't truncate existing file
CFile::modeNoInherit   - Don't inherit to child processes
CFile::shareDenyNone   - Allow sharing
CFile::shareDenyRead   - Deny read sharing
CFile::shareDenyWrite  - Deny write sharing
CFile::shareExclusive  - Exclusive access
CFile::typeText        - Text mode (CR/LF translation)
CFile::typeBinary      - Binary mode (no translation)
*/

void CFileExample()
{
    CFile file;
    CFileException ex;
    
    // Open file for writing
    if (!file.Open(_T("data.bin"), CFile::modeCreate | CFile::modeWrite, &ex))
    {
        // Handle error
        TCHAR errorMsg[256];
        ex.GetErrorMessage(errorMsg, 256);
        AfxMessageBox(errorMsg);
        return;
    }
    
    // Write data
    int value = 42;
    double pi = 3.14159;
    char buffer[] = "Hello";
    
    file.Write(&value, sizeof(value));
    file.Write(&pi, sizeof(pi));
    file.Write(buffer, sizeof(buffer));
    
    file.Close();
    
    // Open file for reading
    if (!file.Open(_T("data.bin"), CFile::modeRead))
    {
        AfxMessageBox(_T("Failed to open file"));
        return;
    }
    
    // Get file size
    ULONGLONG size = file.GetLength();
    
    // Read data
    int readValue;
    double readPi;
    char readBuffer[256];
    
    file.Read(&readValue, sizeof(readValue));
    file.Read(&readPi, sizeof(readPi));
    file.Read(readBuffer, sizeof(readBuffer));
    
    // Seek operations
    file.Seek(0, CFile::begin);     // Seek to beginning
    file.Seek(10, CFile::current);  // Seek forward 10 bytes
    file.Seek(-5, CFile::end);      // Seek to 5 bytes before end
    
    file.Close();
    
    // Static file operations
    if (CFile::Exists(_T("data.bin")))
    {
        CFile::Remove(_T("data.bin"));  // Delete file
    }
    
    // File status
    CFileStatus status;
    if (CFile::GetStatus(_T("data.bin"), status))
    {
        CTime creationTime = status.m_ctime;
        CTime modificationTime = status.m_mtime;
        ULONGLONG fileSize = status.m_size;
        BOOL readOnly = status.m_attribute & CFile::readOnly;
    }
}

// ============================================================================
// 2. CMemFile - MEMORY FILE
// ============================================================================

/*
CMemFile stores data in memory (RAM) instead of disk.
Useful for temporary data, buffers, or testing.

Key methods:
- Same as CFile
- Detach() - Detach memory buffer
- Attach() - Attach memory buffer
*/

void CMemFileExample()
{
    CMemFile memFile;
    
    // Write to memory
    int data[] = { 1, 2, 3, 4, 5 };
    memFile.Write(data, sizeof(data));
    
    // Read from memory
    memFile.SeekToBegin();
    int readData[5];
    memFile.Read(readData, sizeof(readData));
    
    // Get memory pointer
    BYTE* pBuffer = memFile.Detach();  // Caller must free with free()
    // Use buffer...
    free(pBuffer);
}

// ============================================================================
// 3. CStdioFile - TEXT FILE OPERATIONS
// ============================================================================

/*
CStdioFile provides text-mode file operations with line-by-line reading.

Key methods:
- ReadString() - Read line (CString or char buffer)
- WriteString() - Write string
- Read() / Write() - Binary operations (inherited)
*/

void CStdioFileExample()
{
    CStdioFile file;
    
    // Write text file
    if (file.Open(_T("data.txt"),
        CFile::modeCreate | CFile::modeWrite | CFile::typeText))
    {
        file.WriteString(_T("Line 1\n"));
        file.WriteString(_T("Line 2\n"));
        file.WriteString(_T("Line 3\n"));
        file.Close();
    }
    
    // Read text file
    if (file.Open(_T("data.txt"),
        CFile::modeRead | CFile::typeText))
    {
        CString line;
        while (file.ReadString(line))
        {
            // Process each line
            AfxMessageBox(line);
        }
        file.Close();
    }
    
    // Read with char buffer
    if (file.Open(_T("data.txt"),
        CFile::modeRead | CFile::typeText))
    {
        TCHAR buffer[1024];
        while (file.ReadString(buffer, 1024))
        {
            // Process line
        }
        file.Close();
    }
}

// ============================================================================
// 4. CArchive - SERIALIZATION
// ============================================================================

/*
CArchive provides type-safe serialization for MFC objects.
Works with CFile to read/write data.

CArchive modes:
CArchive::store - Writing data
CArchive::load - Reading data

Serialization operators:
<< - Store data (ar << value)
>> - Load data (ar >> value)

Serializable types:
- All MFC collections
- CString, CPoint, CRect, CSize
- CTime, COleDateTime, COleCurrency
- CObject-derived classes with DECLARE_SERIAL/DECLARE_DYNCREATE
- Standard types (int, double, BYTE, WORD, DWORD, etc.)
*/

void CArchiveExample()
{
    // Writing with archive
    CFile file;
    if (file.Open(_T("archive.dat"),
        CFile::modeCreate | CFile::modeWrite))
    {
        CArchive ar(&file, CArchive::store);
        
        // Write data
        ar << (int)42;
        ar << (double)3.14159;
        ar << CString(_T("Hello"));
        ar << CPoint(10, 20);
        ar << CRect(0, 0, 100, 100);
        
        // Close archive (flushes data)
        ar.Close();
        file.Close();
    }
    
    // Reading with archive
    if (file.Open(_T("archive.dat"), CFile::modeRead))
    {
        CArchive ar(&file, CArchive::load);
        
        // Read data (must match write order)
        int value;
        double pi;
        CString text;
        CPoint pt;
        CRect rect;
        
        ar >> value;
        ar >> pi;
        ar >> text;
        ar >> pt;
        ar >> rect;
        
        ar.Close();
        file.Close();
    }
}

// ============================================================================
// 5. SERIALIZATION WITH VERSION SUPPORT
// ============================================================================

/*
Version support allows reading files created by older versions.

Schema:
VERSIONABLE_SCHEMA - Allow reading older versions
2nd param in Serialize: version number

Example:
IMPLEMENT_SERIAL(CMyDocument, CDocument, VERSIONABLE_SCHEMA | 2)

void CMyDocument::Serialize(CArchive& ar)
{
    if (ar.IsStoring())
    {
        ar << (WORD)2;  // Write version
        ar << m_name;
        ar << m_value;
    }
    else
    {
        WORD version;
        ar >> version;  // Read version first
        
        switch (version)
        {
        case 1:
            // Old format
            ar >> m_name;
            m_value = 0;  // Default for new field
            break;
        case 2:
            // Current format
            ar >> m_name;
            ar >> m_value;
            break;
        default:
            AfxThrowArchiveException(CArchiveException::badSchema);
        }
    }
}
*/

// ============================================================================
// 6. COBJECT SERIALIZATION
// ============================================================================

/*
CObject-derived classes can be serialized using DECLARE_SERIAL/
IMPLEMENT_SERIAL macros.

DECLARE_SERIAL(class_name) - In header
IMPLEMENT_SERIAL(class_name, base_class_name, schema) - In .cpp

The class must have:
- Default constructor
- Serialize() override
- DECLARE_MESSAGE_MAP() (optional)
*/

class CMyData : public CObject
{
    DECLARE_SERIAL(CMyData)
    
public:
    CMyData() : m_id(0), m_name(_T("")) {}
    CMyData(int id, const CString& name)
        : m_id(id), m_name(name) {}
    
    virtual void Serialize(CArchive& ar);
    
    int m_id;
    CString m_name;
};

IMPLEMENT_SERIAL(CMyData, CObject, 1)

void CMyData::Serialize(CArchive& ar)
{
    CObject::Serialize(ar);  // Call base class
    
    if (ar.IsStoring())
    {
        ar << m_id;
        ar << m_name;
    }
    else
    {
        ar >> m_id;
        ar >> m_name;
    }
}

// Using serializable objects
void SerializableObjectExample()
{
    CFile file;
    
    // Write objects
    if (file.Open(_T("objects.dat"),
        CFile::modeCreate | CFile::modeWrite))
    {
        CArchive ar(&file, CArchive::store);
        
        CMyData data1(1, _T("First"));
        CMyData data2(2, _T("Second"));
        
        // Serialize objects
        ar << &data1;
        ar << &data2;
        
        ar.Close();
        file.Close();
    }
    
    // Read objects
    if (file.Open(_T("objects.dat"), CFile::modeRead))
    {
        CArchive ar(&file, CArchive::load);
        
        CMyData* pData1 = nullptr;
        CMyData* pData2 = nullptr;
        
        // Deserialize (objects are created on heap)
        ar >> pData1;
        ar >> pData2;
        
        // Use objects
        if (pData1 != nullptr)
        {
            // pData1->m_id, pData1->m_name
            delete pData1;
        }
        if (pData2 != nullptr)
        {
            delete pData2;
        }
        
        ar.Close();
        file.Close();
    }
}

// ============================================================================
// 7. FILE DIALOGS
// ============================================================================

/*
CFileDialog provides standard Open/Save dialogs.

Constructor:
CFileDialog(
    BOOL bOpenFileDialog,  // TRUE=Open, FALSE=Save
    LPCTSTR lpszDefExt,    // Default extension
    LPCTSTR lpszFileName,  // Default filename
    DWORD dwFlags,         // Flags
    LPCTSTR lpszFilter,    // File filter
    CWnd* pParentWnd       // Parent window
);
*/

void FileDialogExample()
{
    // Open file dialog
    CFileDialog openDlg(TRUE, _T("txt"), _T("*.txt"),
        OFN_HIDEREADONLY | OFN_FILEMUSTEXIST | OFN_ALLOWMULTISELECT,
        _T("Text Files (*.txt)|*.txt|")
        _T("All Files (*.*)|*.*||"));
    
    if (openDlg.DoModal() == IDOK)
    {
        // Single file
        CString pathName = openDlg.GetPathName();
        CString fileName = openDlg.GetFileName();
        
        // Multiple files
        POSITION pos = openDlg.GetStartPosition();
        while (pos != nullptr)
        {
            CString filePath = openDlg.GetNextPathName(pos);
            // Process each file
        }
    }
    
    // Save file dialog
    CFileDialog saveDlg(FALSE, _T("dat"), _T("data.dat"),
        OFN_HIDEREADONLY | OFN_OVERWRITEPROMPT,
        _T("Data Files (*.dat)|*.dat|")
        _T("All Files (*.*)|*.*||"));
    
    if (saveDlg.DoModal() == IDOK)
    {
        CString pathName = saveDlg.GetPathName();
        // Save to file
    }
}

// ============================================================================
// 8. BEST PRACTICES
// ============================================================================

/*
1. Always check CFile::Open() return value
2. Use CFileException for detailed error handling
3. Use CArchive for complex data (not raw CFile::Read/Write)
4. Implement version support in Serialize() for forward compatibility
5. Use CStdioFile for text files, CFile for binary
6. Use CMemFile for temporary data
7. Always call ar.Close() before file.Close()
8. Use DECLARE_SERIAL/IMPLEMENT_SERIAL for serializable objects
9. Use CFileDialog for standard file open/save
10. Handle CArchiveException and CFileException properly
*/

#endif // _MFC_VER
