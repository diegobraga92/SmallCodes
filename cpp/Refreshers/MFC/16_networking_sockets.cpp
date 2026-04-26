// ============================================================================
// MFC NETWORKING AND SOCKETS
// File: 16_networking_sockets.cpp
// Covers: CAsyncSocket, CSocket, CSocketFile, CArchive with sockets
// ============================================================================

#ifdef _MFC_VER

// ============================================================================
// 1. SOCKET OVERVIEW
// ============================================================================

/*
MFC provides two socket classes:
1. CAsyncSocket - Low-level, asynchronous socket wrapper
2. CSocket - Higher-level, synchronous, works with CArchive

Key classes:
- CAsyncSocket - Wraps Windows Sockets API
- CSocket - Derived from CAsyncSocket, blocking operations
- CSocketFile - CFile interface for sockets
- CArchive - Serialization over sockets

Socket types:
- SOCK_STREAM - TCP (reliable, connection-oriented)
- SOCK_DGRAM - UDP (unreliable, connectionless)
- SOCK_RAW - Raw protocol access
*/

// ============================================================================
// 2. CAsyncSocket - ASYNCHRONOUS SOCKETS
// ============================================================================

/*
CAsyncSocket provides event-driven socket communication.

Key methods:
- Create() - Create socket
- Bind() - Bind to address
- Listen() - Listen for connections
- Accept() - Accept connection
- Connect() - Connect to server
- Send() / SendTo() - Send data
- Receive() / ReceiveFrom() - Receive data
- Close() - Close socket
- ShutDown() - Disable send/receive
- GetPeerName() / GetSockName() - Address info
- SetSockOpt() / GetSockOpt() - Socket options
- AsyncSelect() - Select events to monitor
- LoadSocketCounts() - Load socket counts

Event notifications (override these):
- OnConnect() - Connection established
- OnAccept() - Connection available to accept
- OnSend() - Ready to send
- OnReceive() - Data available to read
- OnClose() - Connection closed
- OnOutOfBandData() - Out-of-band data
*/

class CMyAsyncSocket : public CAsyncSocket
{
public:
    virtual void OnConnect(int nErrorCode);
    virtual void OnAccept(int nErrorCode);
    virtual void OnReceive(int nErrorCode);
    virtual void OnSend(int nErrorCode);
    virtual void OnClose(int nErrorCode);
};

void CMyAsyncSocket::OnConnect(int nErrorCode)
{
    if (nErrorCode == 0)
    {
        // Connected successfully
        TRACE(_T("Connected\n"));
    }
    else
    {
        // Connection failed
        TRACE(_T("Connection failed: %d\n"), nErrorCode);
    }
}

void CMyAsyncSocket::OnAccept(int nErrorCode)
{
    if (nErrorCode == 0)
    {
        CMyAsyncSocket* pSocket = new CMyAsyncSocket();
        if (Accept(*pSocket))
        {
            // New connection accepted
            TRACE(_T("Accepted connection\n"));
        }
        else
        {
            delete pSocket;
        }
    }
}

void CMyAsyncSocket::OnReceive(int nErrorCode)
{
    if (nErrorCode == 0)
    {
        char buffer[1024];
        int nRead = Receive(buffer, sizeof(buffer));
        
        if (nRead > 0)
        {
            // Process received data
            buffer[nRead] = '\0';
            TRACE(_T("Received: %s\n"), buffer);
        }
    }
}

void CMyAsyncSocket::OnSend(int nErrorCode)
{
    if (nErrorCode == 0)
    {
        // Ready to send more data
        TRACE(_T("Ready to send\n"));
    }
}

void CMyAsyncSocket::OnClose(int nErrorCode)
{
    // Connection closed
    TRACE(_T("Connection closed\n"));
    Close();
}

// ============================================================================
// 3. TCP SERVER EXAMPLE
// ============================================================================

class CTCPServerSocket : public CAsyncSocket
{
public:
    BOOL StartServer(int nPort)
    {
        // Create socket
        if (!Create(nPort, SOCK_STREAM, FD_ACCEPT))
        {
            TRACE(_T("Failed to create server socket\n"));
            return FALSE;
        }
        
        // Listen for connections
        if (!Listen())
        {
            TRACE(_T("Failed to listen\n"));
            return FALSE;
        }
        
        TRACE(_T("Server listening on port %d\n"), nPort);
        return TRUE;
    }
    
    virtual void OnAccept(int nErrorCode)
    {
        if (nErrorCode == 0)
        {
            CAsyncSocket* pClient = new CAsyncSocket();
            if (Accept(*pClient))
            {
                // Handle client connection
                m_clients.Add(pClient);
            }
            else
            {
                delete pClient;
            }
        }
    }
    
private:
    CObArray m_clients;  // Array of client sockets
};

// ============================================================================
// 4. TCP CLIENT EXAMPLE
// ============================================================================

class CTCPClientSocket : public CAsyncSocket
{
public:
    BOOL ConnectToServer(LPCTSTR lpszHost, int nPort)
    {
        // Create socket
        if (!Create())
        {
            TRACE(_T("Failed to create client socket\n"));
            return FALSE;
        }
        
        // Connect to server
        if (!Connect(lpszHost, nPort))
        {
            int nError = GetLastError();
            if (nError != WSAEWOULDBLOCK)
            {
                TRACE(_T("Failed to connect\n"));
                return FALSE;
            }
        }
        
        return TRUE;
    }
    
    BOOL SendData(const CString& data)
    {
        int nSent = Send(data, data.GetLength());
        return nSent == data.GetLength();
    }
    
    virtual void OnReceive(int nErrorCode)
    {
        if (nErrorCode == 0)
        {
            TCHAR buffer[4096];
            int nRead = Receive(buffer, sizeof(buffer) - 1);
            
            if (nRead > 0)
            {
                buffer[nRead] = '\0';
                // Process received data
            }
        }
    }
};

// ============================================================================
// 5. CSocket - SYNCHRONOUS SOCKETS
// ============================================================================

/*
CSocket provides blocking operations, useful with CArchive.
Works with CSocketFile for serialization.

Key differences from CAsyncSocket:
- Operations block until complete
- Works with CSocketFile and CArchive
- Simpler programming model
- Automatic event handling
*/

void CSocketExample()
{
    CSocket socket;
    
    // Create socket
    if (!socket.Create())
    {
        AfxMessageBox(_T("Failed to create socket"));
        return;
    }
    
    // Connect (blocks until connected or timeout)
    if (!socket.Connect(_T("127.0.0.1"), 8080))
    {
        AfxMessageBox(_T("Failed to connect"));
        return;
    }
    
    // Send data
    CString data = _T("Hello Server");
    socket.Send(data, data.GetLength() * sizeof(TCHAR));
    
    // Receive data
    TCHAR buffer[4096];
    int nRead = socket.Receive(buffer, sizeof(buffer) - 1);
    if (nRead > 0)
    {
        buffer[nRead / sizeof(TCHAR)] = '\0';
    }
    
    socket.Close();
}

// ============================================================================
// 6. CSocketFile AND CArchive WITH SOCKETS
// ============================================================================

/*
CSocketFile provides a CFile interface to a CSocket.
CArchive can then serialize data over the socket.

Pattern:
CSocket -> CSocketFile -> CArchive
*/

void SocketArchiveExample()
{
    CSocket socket;
    socket.Create();
    socket.Connect(_T("127.0.0.1"), 8080);
    
    // Create file and archive
    CSocketFile file(&socket);
    CArchive ar(&file, CArchive::store);  // Sending
    
    // Serialize data
    ar << (int)42;
    ar << CString(_T("Hello"));
    ar << (double)3.14;
    
    ar.Close();  // Flushes data
    socket.Close();
}

void SocketArchiveReceiveExample()
{
    CSocket socket;
    socket.Create();
    socket.Connect(_T("127.0.0.1"), 8080);
    
    // Create file and archive
    CSocketFile file(&socket);
    CArchive ar(&file, CArchive::load);  // Receiving
    
    // Deserialize data
    int value;
    CString text;
    double pi;
    
    ar >> value;
    ar >> text;
    ar >> pi;
    
    ar.Close();
    socket.Close();
}

// ============================================================================
// 7. UDP SOCKETS
// ============================================================================

/*
UDP is connectionless. Use SendTo/ReceiveFrom instead of Send/Receive.
*/

void UDPSocketExample()
{
    CAsyncSocket udpSocket;
    
    // Create UDP socket
    if (!udpSocket.Create(0, SOCK_DGRAM))
    {
        AfxMessageBox(_T("Failed to create UDP socket"));
        return;
    }
    
    // Send to specific address
    CString data = _T("Hello UDP");
    udpSocket.SendTo(data, data.GetLength() * sizeof(TCHAR),
        8080, _T("127.0.0.1"));
    
    // Receive from any address
    char buffer[1024];
    CString fromAddress;
    UINT fromPort;
    
    int nRead = udpSocket.ReceiveFrom(buffer, sizeof(buffer),
        fromAddress, fromPort);
    
    if (nRead > 0)
    {
        buffer[nRead] = '\0';
        TRACE(_T("Received from %s:%d: %s\n"),
            fromAddress, fromPort, buffer);
    }
    
    udpSocket.Close();
}

// ============================================================================
// 8. BEST PRACTICES
// ============================================================================

/*
1. Use CAsyncSocket for event-driven applications
2. Use CSocket with CArchive for simpler serialization
3. Always check return values from socket operations
4. Handle WSAEWOULDBLOCK for non-blocking operations
5. Use FD_* flags with AsyncSelect for event monitoring
6. Clean up socket objects properly
7. Use CSocketFile for archive-based communication
8. Set socket timeouts for blocking operations
9. Use UDP for broadcast/multicast scenarios
10. Handle OnClose for graceful disconnection
*/

#endif // _MFC_VER
