// ============================================================================
// MFC COLLECTIONS
// File: 10_collections.cpp
// Covers: CArray, CList, CMap, CStringArray, CPtrList, type-safe templates
// ============================================================================

#ifdef _MFC_VER

// ============================================================================
// 1. COLLECTION OVERVIEW
// ============================================================================

/*
MFC provides three main collection types:
1. Arrays - Ordered, index-based (CArray, CByteArray, CStringArray, etc.)
2. Lists - Doubly-linked lists (CList, CPtrList, CObList, etc.)
3. Maps - Key-value pairs (CMap, CMapStringToString, etc.)

Collection categories:
- Template-based: Type-safe, flexible (CArray<T>, CList<T>, CMap<K,V>)
- Non-template: Specific types (CStringArray, CPtrList, CObList)
- Pointer-based: Store void* or CObject* (CPtrList, CObList)
- Value-based: Store actual values (CArray<int>, CList<CString>)

All MFC collections support serialization via Serialize().
*/

// ============================================================================
// 2. CArray - DYNAMIC ARRAY
// ============================================================================

/*
CArray is a template-based dynamic array. Elements are stored contiguously.

Template: CArray<STORED_TYPE, ARG_TYPE>
- STORED_TYPE: Type stored in array
- ARG_TYPE: Type used for function arguments (usually const STORED_TYPE&)

Key methods:
- Add() - Add element at end
- InsertAt() - Insert at position
- SetAt() / SetAtGrow() - Set element
- GetAt() / operator[] - Get element
- RemoveAt() - Remove at position
- RemoveAll() - Clear array
- GetSize() / GetCount() - Number of elements
- GetUpperBound() - Last valid index
- SetSize() - Pre-allocate memory
- FreeExtra() - Free unused memory
- GetData() - Get raw pointer to data
- Append() - Append another array
- Copy() - Copy from another array
*/

void CArrayExample()
{
    // Integer array
    CArray<int, int> intArray;
    
    // Pre-allocate for performance
    intArray.SetSize(0, 10);  // Grow by 10 elements
    
    // Add elements
    intArray.Add(10);
    intArray.Add(20);
    intArray.Add(30);
    
    // Insert at position
    intArray.InsertAt(1, 15);  // {10, 15, 20, 30}
    
    // Access elements
    int first = intArray[0];       // operator[]
    int second = intArray.GetAt(1);
    
    // Set element
    intArray[0] = 100;
    intArray.SetAt(1, 200);
    
    // Set with auto-grow
    intArray.SetAtGrow(10, 500);  // Array grows to accommodate
    
    // Iterate
    for (int i = 0; i < intArray.GetSize(); i++)
    {
        int value = intArray[i];
    }
    
    // Remove
    intArray.RemoveAt(0);       // Remove first
    intArray.RemoveAt(0, 2);    // Remove 2 elements starting at 0
    intArray.RemoveAll();       // Clear all
    
    // CString array
    CArray<CString, CString&> strArray;
    strArray.Add(_T("Hello"));
    strArray.Add(_T("World"));
    
    // Get raw data
    CString* pData = strArray.GetData();
}

// ============================================================================
// 3. SPECIFIC ARRAY TYPES
// ============================================================================

/*
MFC provides non-template array classes for common types:

CByteArray - Array of BYTE
CWordArray - Array of WORD
CDWordArray - Array of DWORD
CUIntArray - Array of UINT
CStringArray - Array of CString
CPtrArray - Array of void*
CObArray - Array of CObject*
*/

void SpecificArrayExample()
{
    // CByteArray
    CByteArray byteArray;
    byteArray.Add(0xFF);
    byteArray.Add(0x00);
    BYTE b = byteArray[0];
    
    // CStringArray
    CStringArray strArray;
    strArray.Add(_T("Item 1"));
    strArray.Add(_T("Item 2"));
    
    // Sort strings
    // Note: MFC doesn't provide Sort, but you can implement it
    for (int i = 0; i < strArray.GetSize() - 1; i++)
    {
        for (int j = i + 1; j < strArray.GetSize(); j++)
        {
            if (strArray[i] > strArray[j])
            {
                CString temp = strArray[i];
                strArray[i] = strArray[j];
                strArray[j] = temp;
            }
        }
    }
    
    // CPtrArray (stores void*)
    CPtrArray ptrArray;
    int value = 42;
    ptrArray.Add(&value);
    int* pValue = (int*)ptrArray[0];
    
    // CObArray (stores CObject*)
    CObArray objArray;
    // objArray.Add(new CMyData(1, _T("Test")));
    // CMyData* pData = (CMyData*)objArray[0];
    // delete pData;
    // objArray.RemoveAll();
}

// ============================================================================
// 4. CList - DOUBLY-LINKED LIST
// ============================================================================

/*
CList is a template-based doubly-linked list.

Template: CList<STORED_TYPE, ARG_TYPE>

Key methods:
- AddHead() / AddTail() - Add at beginning/end
- RemoveHead() / RemoveTail() - Remove from beginning/end
- GetHead() / GetTail() - Get first/last element
- InsertBefore() / InsertAfter() - Insert at position
- Find() - Find element
- GetNext() / GetPrev() - Iterate
- GetHeadPosition() / GetTailPosition() - Get position
- RemoveAt() - Remove at position
- RemoveAll() - Clear list
- GetCount() - Number of elements
- IsEmpty() - Check if empty
*/

void CListExample()
{
    // String list
    CList<CString, CString&> strList;
    
    // Add elements
    strList.AddTail(_T("Third"));
    strList.AddHead(_T("First"));
    strList.InsertAfter(strList.GetHeadPosition(), _T("Second"));
    // List: First -> Second -> Third
    
    // Get elements
    CString first = strList.GetHead();    // "First"
    CString last = strList.GetTail();     // "Third"
    
    // Remove elements
    strList.RemoveHead();  // Remove "First"
    strList.RemoveTail();  // Remove "Third"
    
    // Iterate forward
    POSITION pos = strList.GetHeadPosition();
    while (pos != nullptr)
    {
        CString& str = strList.GetNext(pos);
        // Process str
    }
    
    // Iterate backward
    pos = strList.GetTailPosition();
    while (pos != nullptr)
    {
        CString& str = strList.GetPrev(pos);
        // Process str
    }
    
    // Find element
    pos = strList.Find(_T("Second"));
    if (pos != nullptr)
    {
        // Found
        strList.RemoveAt(pos);
    }
    
    // Integer list
    CList<int, int> intList;
    intList.AddTail(10);
    intList.AddTail(20);
    intList.AddTail(30);
    
    // Check if empty
    if (!intList.IsEmpty())
    {
        int count = intList.GetCount();
    }
}

// ============================================================================
// 5. SPECIFIC LIST TYPES
// ============================================================================

/*
MFC provides non-template list classes:

CStringList - List of CString
CPtrList - List of void*
CObList - List of CObject*
*/

void SpecificListExample()
{
    // CStringList
    CStringList strList;
    strList.AddTail(_T("Apple"));
    strList.AddTail(_T("Banana"));
    strList.AddTail(_T("Cherry"));
    
    // Iterate
    POSITION pos = strList.GetHeadPosition();
    while (pos != nullptr)
    {
        CString fruit = strList.GetNext(pos);
    }
    
    // CPtrList
    CPtrList ptrList;
    int a = 1, b = 2;
    ptrList.AddTail(&a);
    ptrList.AddTail(&b);
    
    // CObList
    CObList objList;
    // objList.AddTail(new CMyData(1, _T("Data")));
    // Cleanup required
}

// ============================================================================
// 6. CMap - KEY-VALUE MAP
// ============================================================================

/*
CMap is a template-based hash map (dictionary).

Template: CMap<KEY_TYPE, ARG_KEY_TYPE, VALUE_TYPE, ARG_VALUE_TYPE>

Key methods:
- SetAt() / operator[] - Add/update key-value pair
- Lookup() - Find value by key
- RemoveKey() - Remove by key
- RemoveAll() - Clear map
- GetStartPosition() - Start iteration
- GetNextAssoc() - Get next key-value pair
- GetCount() - Number of entries
- IsEmpty() - Check if empty
- InitHashTable() - Set hash table size
*/

void CMapExample()
{
    // Map string to int
    CMap<CString, LPCTSTR, int, int> scoreMap;
    
    // Add entries
    scoreMap.SetAt(_T("Alice"), 95);
    scoreMap.SetAt(_T("Bob"), 87);
    scoreMap.SetAt(_T("Charlie"), 92);
    
    // Using operator[]
    scoreMap[_T("Diana")] = 88;
    
    // Lookup
    int score;
    if (scoreMap.Lookup(_T("Alice"), score))
    {
        // score = 95
    }
    
    // Check if key exists
    BOOL exists = scoreMap.Lookup(_T("Eve"), score);
    
    // Remove
    scoreMap.RemoveKey(_T("Bob"));
    
    // Iterate all entries
    CString name;
    int value;
    POSITION pos = scoreMap.GetStartPosition();
    while (pos != nullptr)
    {
        scoreMap.GetNextAssoc(pos, name, value);
        // Process name and value
    }
    
    // Get count
    int count = scoreMap.GetCount();
    
    // Clear
    scoreMap.RemoveAll();
    
    // Map int to CString
    CMap<int, int, CString, CString&> idMap;
    idMap.SetAt(1, _T("One"));
    idMap.SetAt(2, _T("Two"));
    
    CString str;
    if (idMap.Lookup(1, str))
    {
        // str = "One"
    }
}

// ============================================================================
// 7. SPECIFIC MAP TYPES
// ============================================================================

/*
MFC provides non-template map classes:

CMapWordToPtr - WORD to void*
CMapWordToOb - WORD to CObject*
CMapPtrToWord - void* to WORD
CMapPtrToPtr - void* to void*
CMapStringToPtr - CString to void*
CMapStringToOb - CString to CObject*
CMapStringToString - CString to CString
*/

void SpecificMapExample()
{
    // CMapStringToString
    CMapStringToString translationMap;
    translationMap.SetAt(_T("Hello"), _T("Bonjour"));
    translationMap.SetAt(_T("Goodbye"), _T("Au revoir"));
    
    CString translation;
    if (translationMap.Lookup(_T("Hello"), translation))
    {
        // translation = "Bonjour"
    }
    
    // Iterate
    CString english, french;
    POSITION pos = translationMap.GetStartPosition();
    while (pos != nullptr)
    {
        translationMap.GetNextAssoc(pos, english, french);
    }
}

// ============================================================================
// 8. COLLECTION SERIALIZATION
// ============================================================================

/*
All MFC collections support serialization:

void SerializeCollection(CArchive& ar)
{
    CStringArray names;
    CArray<int, int> scores;
    
    if (ar.IsStoring())
    {
        names.Serialize(ar);
        scores.Serialize(ar);
    }
    else
    {
        names.Serialize(ar);
        scores.Serialize(ar);
    }
}
*/

// ============================================================================
// 9. PERFORMANCE CONSIDERATIONS
// ============================================================================

/*
Collection Performance:

Operation          | CArray | CList | CMap
-------------------|--------|-------|-------
Add at end         | O(1)*  | O(1)  | O(1)
Insert at position | O(n)   | O(1)**| N/A
Remove at position | O(n)   | O(1)**| O(1)
Find by value      | O(n)   | O(n)  | O(1)
Find by key        | N/A    | N/A   | O(1)
Access by index    | O(1)   | O(n)  | N/A
Memory overhead    | Low    | High  | Medium

* May require reallocation
** If position is known

When to use each:
- CArray: Random access, small to medium collections
- CList: Frequent insert/remove, sequential access
- CMap: Key-based lookup, unique keys
*/

// ============================================================================
// 10. BEST PRACTICES
// ============================================================================

/*
1. Use template-based collections for type safety
2. Pre-allocate CArray with SetSize() for performance
3. Use POSITION for efficient list operations
4. Use Lookup() instead of operator[] for map existence checks
5. Use InitHashTable() for large maps (prime number size)
6. Use CStringArray for string collections
7. Use CPtrList/CObList for polymorphic collections
8. Serialize collections with their Serialize() method
9. Clean up pointer collections manually
10. Use STL containers for cross-platform code
*/

#endif // _MFC_VER
