// ============================================================================
// MFC DATABASE (ODBC)
// File: 15_database_odbc.cpp
// Covers: CDatabase, CRecordset, CRecordView, ODBC, DAO
// ============================================================================

#ifdef _MFC_VER

// ============================================================================
// 1. DATABASE OVERVIEW
// ============================================================================

/*
MFC provides two database technologies:
1. ODBC (Open Database Connectivity) - Cross-platform database access
2. DAO (Data Access Objects) - Access to Jet/ACE engine (legacy)

Key classes (ODBC):
- CDatabase - Connection to data source
- CRecordset - Set of records from data source
- CRecordView - Form view bound to recordset
- CFieldExchange - Field exchange mechanism (RFX)
- CDBException - Database exception
- CLongBinary - Large binary data

Key classes (DAO):
- CDaoDatabase - DAO database connection
- CDaoRecordset - DAO recordset
- CDaoRecordView - DAO form view
- CDaoFieldExchange - DAO field exchange
- CDaoException - DAO exception
*/

// ============================================================================
// 2. CDatabase - DATABASE CONNECTION
// ============================================================================

/*
CDatabase manages a connection to a data source.

Key methods:
- Open() / OpenEx() - Open connection
- Close() - Close connection
- ExecuteSQL() - Execute SQL statement
- BeginTrans() / CommitTrans() / Rollback() - Transactions
- CanTransact() - Check transaction support
- GetDatabaseName() - Get database name
- GetConnect() - Get connection string
- IsOpen() - Check if open
- SetLoginTimeout() - Set login timeout
- SetQueryTimeout() - Set query timeout
*/

void CDatabaseExample()
{
    CDatabase db;
    CDBException dbEx;
    
    // Method 1: Open with DSN
    if (!db.Open(_T("MyDSN"), FALSE, FALSE, _T("ODBC;UID=user;PWD=pass")))
    {
        AfxMessageBox(_T("Failed to connect"));
        return;
    }
    
    // Method 2: OpenEx with connection string
    if (!db.OpenEx(_T("DSN=MyDSN;UID=user;PWD=pass;"),
        CDatabase::noOdbcDialog))
    {
        AfxMessageBox(_T("Failed to connect"));
        return;
    }
    
    // Execute SQL directly
    try
    {
        db.ExecuteSQL(_T("CREATE TABLE Test (ID INT, Name TEXT)"));
        db.ExecuteSQL(_T("INSERT INTO Test VALUES (1, 'Hello')"));
    }
    catch (CDBException* e)
    {
        e->ReportError();
        e->Delete();
    }
    
    // Transactions
    if (db.CanTransact())
    {
        db.BeginTrans();
        try
        {
            db.ExecuteSQL(_T("UPDATE Test SET Name='World' WHERE ID=1"));
            db.CommitTrans();
        }
        catch (CDBException* e)
        {
            db.Rollback();
            e->Delete();
        }
    }
    
    db.Close();
}

// ============================================================================
// 3. CRecordset - RECORD SETS
// ============================================================================

/*
CRecordset represents a set of records from a data source.

Types:
- CRecordset::dynaset - Dynamic set (reflects changes)
- CRecordset::snapshot - Static snapshot
- CRecordset::forwardOnly - Forward-only cursor
- CRecordset::dynamic - Dynamic (ODBC level 2)

Key methods:
- Open() - Open recordset
- Close() - Close recordset
- Move() / MoveNext() / MovePrev() / MoveFirst() / MoveLast() - Navigation
- AddNew() - Add new record
- Edit() - Edit current record
- Update() - Save changes
- Delete() - Delete current record
- CanAppend() / CanUpdate() - Check capabilities
- GetDefaultSQL() - Default SQL
- DoFieldExchange() - Field exchange
- IsEOF() / IsBOF() - Position checks
- Requery() - Re-execute query
*/

class CMyRecordset : public CRecordset
{
public:
    CMyRecordset(CDatabase* pDatabase = nullptr);
    
    // Field data members
    long    m_id;
    CString m_name;
    CString m_address;
    double  m_salary;
    
    // Field exchange
    virtual void DoFieldExchange(CFieldExchange* pFX);
    
    // Default SQL
    virtual CString GetDefaultSQL();
    
protected:
    virtual CString GetDefaultConnect();
};

CMyRecordset::CMyRecordset(CDatabase* pDatabase /*= nullptr*/)
    : CRecordset(pDatabase)
{
    m_id = 0;
    m_name = _T("");
    m_address = _T("");
    m_salary = 0.0;
    m_nFields = 4;  // Number of field data members
}

CString CMyRecordset::GetDefaultConnect()
{
    return _T("DSN=MyDSN;UID=user;PWD=pass;");
}

CString CMyRecordset::GetDefaultSQL()
{
    return _T("SELECT ID, Name, Address, Salary FROM Employees");
}

void CMyRecordset::DoFieldExchange(CFieldExchange* pFX)
{
    pFX->SetFieldType(CFieldExchange::outputColumn);
    
    RFX_Long(pFX, _T("ID"), m_id);
    RFX_Text(pFX, _T("Name"), m_name);
    RFX_Text(pFX, _T("Address"), m_address);
    RFX_Double(pFX, _T("Salary"), m_salary);
}

// ============================================================================
// 4. USING RECORDSETS
// ============================================================================

void RecordsetUsageExample()
{
    CDatabase db;
    db.OpenEx(_T("DSN=MyDSN;UID=user;PWD=pass;"));
    
    CMyRecordset rs(&db);
    
    // Open recordset
    rs.Open(CRecordset::snapshot, _T("SELECT * FROM Employees WHERE Salary > 50000"));
    
    // Navigate records
    while (!rs.IsEOF())
    {
        // Access field values
        long id = rs.m_id;
        CString name = rs.m_name;
        double salary = rs.m_salary;
        
        rs.MoveNext();
    }
    
    // Add new record
    rs.AddNew();
    rs.m_id = 100;
    rs.m_name = _T("John Doe");
    rs.m_address = _T("123 Main St");
    rs.m_salary = 75000.0;
    rs.Update();
    
    // Edit record
    rs.MoveFirst();
    rs.Edit();
    rs.m_salary = 80000.0;
    rs.Update();
    
    // Delete record
    rs.MoveFirst();
    rs.Delete();
    
    // Requery
    rs.Requery();
    
    rs.Close();
    db.Close();
}

// ============================================================================
// 5. CRecordView - FORM VIEW WITH RECORDSET
// ============================================================================

/*
CRecordView is a form view connected to a recordset.
Provides automatic navigation and field updates.

Key methods:
- OnMove() - Move to next/prev record
- OnGetRecordset() - Get associated recordset
- IsOnFirstRecord() / IsOnLastRecord() - Position checks
- OnMoveNext() / OnMovePrev() / OnMoveFirst() / OnMoveLast()
*/

class CMyRecordView : public CRecordView
{
public:
    CMyRecordView();
    
    enum { IDD = IDD_MY_FORM };
    
    CMyRecordset* m_pSet;
    
    virtual CRecordset* OnGetRecordset();
    virtual void DoDataExchange(CDataExchange* pDX);
    
    DECLARE_DYNCREATE(CMyRecordView)
    DECLARE_MESSAGE_MAP()
};

IMPLEMENT_DYNCREATE(CMyRecordView, CRecordView)

CMyRecordView::CMyRecordView()
    : CRecordView(IDD_MY_FORM)
{
    m_pSet = nullptr;
}

CRecordset* CMyRecordView::OnGetRecordset()
{
    if (m_pSet == nullptr)
    {
        m_pSet = new CMyRecordset();
        m_pSet->Open();
    }
    
    return m_pSet;
}

void CMyRecordView::DoDataExchange(CDataExchange* pDX)
{
    CRecordView::DoDataExchange(pDX);
    
    // DDX with recordset fields
    DDX_FieldText(pDX, IDC_ID_EDIT, m_pSet->m_id, m_pSet);
    DDX_FieldText(pDX, IDC_NAME_EDIT, m_pSet->m_name, m_pSet);
    DDX_FieldText(pDX, IDC_ADDRESS_EDIT, m_pSet->m_address, m_pSet);
    DDX_FieldText(pDX, IDC_SALARY_EDIT, m_pSet->m_salary, m_pSet);
}

// ============================================================================
// 6. PARAMETERIZED QUERIES
// ============================================================================

/*
Parameterized queries use RFX for parameter exchange.
Parameters are prefixed with ? in SQL.

Steps:
1. Add parameter data members
2. Set m_nParams
3. Set m_strFilter with ?
4. Set parameter values before Open()/Requery()
*/

class CParamRecordset : public CRecordset
{
public:
    CParamRecordset(CDatabase* pDatabase = nullptr);
    
    // Field data members
    CString m_name;
    double  m_salary;
    
    // Parameter data members
    double m_minSalary;
    CString m_deptName;
    
    virtual void DoFieldExchange(CFieldExchange* pFX);
    virtual CString GetDefaultSQL();
};

CParamRecordset::CParamRecordset(CDatabase* pDatabase /*= nullptr*/)
    : CRecordset(pDatabase)
{
    m_name = _T("");
    m_salary = 0.0;
    m_minSalary = 0.0;
    m_deptName = _T("");
    m_nFields = 2;
    m_nParams = 2;  // Two parameters
}

CString CParamRecordset::GetDefaultSQL()
{
    return _T("{CALL GetEmployeesByDeptAndSalary(?, ?)}");
}

void CParamRecordset::DoFieldExchange(CFieldExchange* pFX)
{
    pFX->SetFieldType(CFieldExchange::outputColumn);
    RFX_Text(pFX, _T("Name"), m_name);
    RFX_Double(pFX, _T("Salary"), m_salary);
    
    pFX->SetFieldType(CFieldExchange::param);
    RFX_Double(pFX, _T("MinSalary"), m_minSalary);
    RFX_Text(pFX, _T("DeptName"), m_deptName);
}

void ParameterizedQueryExample()
{
    CDatabase db;
    db.OpenEx(_T("DSN=MyDSN;"));
    
    CParamRecordset rs(&db);
    
    // Set parameters
    rs.m_minSalary = 50000.0;
    rs.m_deptName = _T("Engineering");
    
    // Open with filter
    rs.m_strFilter = _T("Salary >= ? AND Department = ?");
    rs.Open();
    
    while (!rs.IsEOF())
    {
        // Process record
        rs.MoveNext();
    }
    
    rs.Close();
    db.Close();
}

// ============================================================================
// 7. JOINED QUERIES
// ============================================================================

/*
For joined queries, map fields from multiple tables.
Use RFX for each field regardless of source table.
*/

class CJoinedRecordset : public CRecordset
{
public:
    CJoinedRecordset(CDatabase* pDatabase = nullptr);
    
    long    m_empId;
    CString m_empName;
    CString m_deptName;
    CString m_deptLocation;
    
    virtual void DoFieldExchange(CFieldExchange* pFX);
    virtual CString GetDefaultSQL();
};

CJoinedRecordset::CJoinedRecordset(CDatabase* pDatabase /*= nullptr*/)
    : CRecordset(pDatabase)
{
    m_nFields = 4;
}

CString CJoinedRecordset::GetDefaultSQL()
{
    return _T("SELECT Employees.ID, Employees.Name, "
              _T("Departments.Name, Departments.Location ")
              _T("FROM Employees INNER JOIN Departments ")
              _T("ON Employees.DeptID = Departments.ID"));
}

void CJoinedRecordset::DoFieldExchange(CFieldExchange* pFX)
{
    pFX->SetFieldType(CFieldExchange::outputColumn);
    RFX_Long(pFX, _T("ID"), m_empId);
    RFX_Text(pFX, _T("Name"), m_empName);
    RFX_Text(pFX, _T("DeptName"), m_deptName);
    RFX_Text(pFX, _T("Location"), m_deptLocation);
}

// ============================================================================
// 8. BEST PRACTICES
// ============================================================================

/*
1. Use OpenEx() instead of Open() for more control
2. Use try/catch for database exceptions
3. Use transactions for multiple related operations
4. Use parameterized queries to prevent SQL injection
5. Use dynaset for live data, snapshot for reporting
6. Close recordsets before closing database
7. Use RFX_* macros for field exchange
8. Set m_nFields and m_nParams correctly
9. Use CRecordView for simple data entry forms
10. Handle CDBException properly
*/

#endif // _MFC_VER
