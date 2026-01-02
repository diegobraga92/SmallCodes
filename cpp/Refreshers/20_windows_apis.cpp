#ifdef _WIN32
#include <iostream>
#include <string>
#include <vector>
#include <windows.h>      // Windows API
#include <tchar.h>        // TCHAR support
#include <strsafe.h>      // Safe string functions
#include <direct.h>       // Directory operations
#include <io.h>           // File operations
#include <sys/stat.h>     // File status
#include <psapi.h>        // Process information

#pragma comment(lib, "psapi.lib")
#pragma comment(lib, "advapi32.lib")

void demonstrate_windows_apis() {
    std::cout << "\n=== WINDOWS APIs ===\n";
    
    // ============================================================================
    // 1. PROCESS INFORMATION
    // ============================================================================
    
    std::cout << "\n1. Process Information:\n";
    
    // Get current process ID
    DWORD pid = GetCurrentProcessId();
    std::cout << "Current PID: " << pid << "\n";
    
    // Get current thread ID
    DWORD tid = GetCurrentThreadId();
    std::cout << "Current Thread ID: " << tid << "\n";
    
    // Get process handle
    HANDLE hProcess = GetCurrentProcess();
    
    // Get process times
    FILETIME creation_time, exit_time, kernel_time, user_time;
    if (GetProcessTimes(hProcess, &creation_time, &exit_time, 
                        &kernel_time, &user_time)) {
        SYSTEMTIME sys_time;
        FileTimeToSystemTime(&creation_time, &sys_time);
        std::cout << "Process created: " 
                  << sys_time.wYear << "-" << sys_time.wMonth << "-" << sys_time.wDay << "\n";
    }
    
    // Get memory usage
    PROCESS_MEMORY_COUNTERS pmc;
    if (GetProcessMemoryInfo(hProcess, &pmc, sizeof(pmc))) {
        std::cout << "Working set size: " << pmc.WorkingSetSize / 1024 << " KB\n";
        std::cout << "Peak working set: " << pmc.PeakWorkingSetSize / 1024 << " KB\n";
        std::cout << "Page file usage: " << pmc.PagefileUsage / 1024 << " KB\n";
    }
    
    // ============================================================================
    // 2. FILE SYSTEM OPERATIONS
    // ============================================================================
    
    std::cout << "\n2. File System Operations:\n";
    
    // Create a directory
    if (CreateDirectory("test_dir_win", nullptr)) {
        std::cout << "Directory created: test_dir_win\n";
    } else if (GetLastError() == ERROR_ALREADY_EXISTS) {
        std::cout << "Directory already exists\n";
    }
    
    // Get current directory
    char current_dir[MAX_PATH];
    if (GetCurrentDirectory(MAX_PATH, current_dir)) {
        std::cout << "Current directory: " << current_dir << "\n";
    }
    
    // Change directory
    if (SetCurrentDirectory("test_dir_win")) {
        GetCurrentDirectory(MAX_PATH, current_dir);
        std::cout << "Changed to: " << current_dir << "\n";
        SetCurrentDirectory("..");  // Change back
    }
    
    // File operations with Windows API
    HANDLE hFile = CreateFile(
        "windows_example.txt",        // File name
        GENERIC_WRITE,                // Write access
        0,                            // No sharing
        nullptr,                      // Default security
        CREATE_ALWAYS,                // Create or overwrite
        FILE_ATTRIBUTE_NORMAL,        // Normal file
        nullptr                       // No template
    );
    
    if (hFile != INVALID_HANDLE_VALUE) {
        const char* data = "Hello from Windows API!\n";
        DWORD bytes_written;
        
        if (WriteFile(hFile, data, (DWORD)strlen(data), &bytes_written, nullptr)) {
            std::cout << "Wrote " << bytes_written << " bytes\n";
        }
        
        CloseHandle(hFile);
    }
    
    // Read file
    hFile = CreateFile(
        "windows_example.txt",
        GENERIC_READ,
        0,
        nullptr,
        OPEN_EXISTING,
        FILE_ATTRIBUTE_NORMAL,
        nullptr
    );
    
    if (hFile != INVALID_HANDLE_VALUE) {
        char buffer[256];
        DWORD bytes_read;
        
        if (ReadFile(hFile, buffer, sizeof(buffer) - 1, &bytes_read, nullptr)) {
            buffer[bytes_read] = '\0';
            std::cout << "Read: " << buffer;
        }
        
        CloseHandle(hFile);
    }
    
    // Get file information
    WIN32_FILE_ATTRIBUTE_DATA file_info;
    if (GetFileAttributesEx("windows_example.txt", GetFileExInfoStandard, &file_info)) {
        std::cout << "\nFile attributes:\n";
        std::cout << "File size: " << file_info.nFileSizeLow << " bytes\n";
        
        SYSTEMTIME sys_time;
        FileTimeToSystemTime(&file_info.ftLastWriteTime, &sys_time);
        std::cout << "Last modified: " << sys_time.wYear << "-" 
                  << sys_time.wMonth << "-" << sys_time.wDay << "\n";
    }
    
    // ============================================================================
    // 3. MEMORY MANAGEMENT
    // ============================================================================
    
    std::cout << "\n3. Memory Management:\n";
    
    // Allocate memory
    LPVOID memory = VirtualAlloc(
        nullptr,           // Let system choose address
        4096,              // 4KB
        MEM_COMMIT,        // Allocate committed memory
        PAGE_READWRITE     // Read/write access
    );
    
    if (memory) {
        std::cout << "Allocated 4KB at: " << memory << "\n";
        
        // Use the memory
        strcpy_s((char*)memory, 100, "Hello from allocated memory!");
        std::cout << "Memory contains: " << (char*)memory << "\n";
        
        // Free memory
        VirtualFree(memory, 0, MEM_RELEASE);
        std::cout << "Memory freed\n";
    }
    
    // Get system memory info
    MEMORYSTATUSEX mem_status;
    mem_status.dwLength = sizeof(mem_status);
    
    if (GlobalMemoryStatusEx(&mem_status)) {
        std::cout << "\nSystem Memory Status:\n";
        std::cout << "Total physical: " << mem_status.ullTotalPhys / (1024*1024) << " MB\n";
        std::cout << "Available physical: " << mem_status.ullAvailPhys / (1024*1024) << " MB\n";
        std::cout << "Total virtual: " << mem_status.ullTotalVirtual / (1024*1024) << " MB\n";
        std::cout << "Available virtual: " << mem_status.ullAvailVirtual / (1024*1024) << " MB\n";
        std::cout << "Memory load: " << mem_status.dwMemoryLoad << "%\n";
    }
    
    // ============================================================================
    // 4. REGISTRY OPERATIONS
    // ============================================================================
    
    std::cout << "\n4. Registry Operations:\n";
    
    HKEY hKey;
    LONG result;
    
    // Create/Open registry key
    result = RegCreateKeyEx(
        HKEY_CURRENT_USER,
        "Software\\MyApp",
        0,
        nullptr,
        REG_OPTION_NON_VOLATILE,
        KEY_ALL_ACCESS,
        nullptr,
        &hKey,
        nullptr
    );
    
    if (result == ERROR_SUCCESS) {
        std::cout << "Registry key created/opened\n";
        
        // Write value
        const char* value = "My Application Data";
        result = RegSetValueEx(
            hKey,
            "AppData",
            0,
            REG_SZ,
            (const BYTE*)value,
            (DWORD)strlen(value) + 1
        );
        
        if (result == ERROR_SUCCESS) {
            std::cout << "Registry value written\n";
        }
        
        // Read value
        char buffer[256];
        DWORD buffer_size = sizeof(buffer);
        DWORD type;
        
        result = RegQueryValueEx(
            hKey,
            "AppData",
            nullptr,
            &type,
            (LPBYTE)buffer,
            &buffer_size
        );
        
        if (result == ERROR_SUCCESS && type == REG_SZ) {
            std::cout << "Read from registry: " << buffer << "\n";
        }
        
        RegCloseKey(hKey);
    }
    
    // ============================================================================
    // 5. EVENT LOGGING
    // ============================================================================
    
    std::cout << "\n5. Event Logging:\n";
    
    HANDLE hEventLog = RegisterEventSource(nullptr, "MyApplication");
    
    if (hEventLog) {
        const char* messages[] = {"My Application started"};
        
        ReportEvent(
            hEventLog,                     // Event log handle
            EVENTLOG_INFORMATION_TYPE,     // Event type
            0,                             // Category
            0,                             // Event ID
            nullptr,                       // User SID
            1,                             // Number of strings
            0,                             // Binary data size
            (LPCSTR*)messages,             // String array
            nullptr                        // Binary data
        );
        
        std::cout << "Event logged to Windows Event Log\n";
        DeregisterEventSource(hEventLog);
    }
    
    // ============================================================================
    // 6. WINDOWS SERVICES (SERVICE CONTROL MANAGER)
    // ============================================================================
    
    std::cout << "\n6. Windows Service Interaction:\n";
    
    // Open Service Control Manager
    SC_HANDLE scm = OpenSCManager(
        nullptr,                    // Local computer
        nullptr,                    // SERVICES_ACTIVE_DATABASE
        SC_MANAGER_ALL_ACCESS      // Full access
    );
    
    if (scm) {
        // Query service status
        SC_HANDLE service = OpenService(
            scm,
            "EventLog",             // Event Log service
            SERVICE_QUERY_STATUS
        );
        
        if (service) {
            SERVICE_STATUS_PROCESS status;
            DWORD bytes_needed;
            
            if (QueryServiceStatusEx(
                service,
                SC_STATUS_PROCESS_INFO,
                (LPBYTE)&status,
                sizeof(status),
                &bytes_needed
            )) {
                std::cout << "EventLog service status: ";
                switch (status.dwCurrentState) {
                    case SERVICE_STOPPED: std::cout << "Stopped"; break;
                    case SERVICE_START_PENDING: std::cout << "Start Pending"; break;
                    case SERVICE_STOP_PENDING: std::cout << "Stop Pending"; break;
                    case SERVICE_RUNNING: std::cout << "Running"; break;
                    case SERVICE_CONTINUE_PENDING: std::cout << "Continue Pending"; break;
                    case SERVICE_PAUSE_PENDING: std::cout << "Pause Pending"; break;
                    case SERVICE_PAUSED: std::cout << "Paused"; break;
                    default: std::cout << "Unknown";
                }
                std::cout << "\n";
            }
            
            CloseServiceHandle(service);
        }
        
        CloseServiceHandle(scm);
    }
    
    // Clean up
    DeleteFile("windows_example.txt");
    RemoveDirectory("test_dir_win");
    RegDeleteKey(HKEY_CURRENT_USER, "Software\\MyApp");
}

#endif