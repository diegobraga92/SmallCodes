// ServiceBase.h
#pragma once
#include <windows.h>
#include <string>
#include <atomic>
#include <thread>
#include <memory>
#include <vector>

class ServiceBase {
public:
    ServiceBase(const std::wstring& serviceName, 
                const std::wstring& displayName,
                DWORD serviceType = SERVICE_WIN32_OWN_PROCESS,
                DWORD startType = SERVICE_DEMAND_START,
                DWORD errorControl = SERVICE_ERROR_NORMAL,
                const std::wstring& dependencies = L"",
                const std::wstring& account = L"NT AUTHORITY\\LocalService",
                const std::wstring& password = L"");
    
    virtual ~ServiceBase();
    
    // Main service entry point (called by ServiceMain)
    static VOID WINAPI ServiceMain(DWORD argc, LPWSTR* argv);
    
    // Control handler entry point
    static DWORD WINAPI ServiceCtrlHandler(DWORD ctrlCode, DWORD eventType, 
                                          LPVOID eventData, LPVOID context);
    
    // Public interface
    bool Run();
    void Stop();
    void Pause();
    void Continue();
    
    // Status reporting
    void ReportStatus(DWORD currentState, DWORD exitCode = NO_ERROR,
                     DWORD waitHint = 3000);
    
    // Service properties
    std::wstring GetServiceName() const { return serviceName; }
    std::wstring GetDisplayName() const { return displayName; }
    DWORD GetCurrentState() const { return currentState; }
    
protected:
    // Override these in derived class
    virtual bool OnStart(int argc, wchar_t* argv[]) = 0;
    virtual void OnStop() = 0;
    virtual void OnPause() = 0;
    virtual void OnContinue() = 0;
    virtual void OnShutdown() = 0;
    virtual void OnSessionChange(DWORD eventType, WTSSESSION_NOTIFICATION* notification) {}
    virtual void OnPowerEvent(DWORD eventType, POWERBROADCAST_SETTING* setting) {}
    virtual void OnDeviceEvent(DWORD eventType, DEV_BROADCAST_HDR* deviceData) {}
    
    // Utility functions
    void SetAcceptControls(DWORD controls);
    void SetServiceDescription(const std::wstring& description);
    
    // Worker thread management
    void StartWorkerThread(std::function<void()> worker);
    void StopWorkerThreads();
    
private:
    std::wstring serviceName;
    std::wstring displayName;
    
    // Service status
    SERVICE_STATUS_HANDLE serviceStatusHandle{nullptr};
    SERVICE_STATUS serviceStatus;
    std::atomic<DWORD> currentState{SERVICE_STOPPED};
    
    // Control handler
    static ServiceBase* instance;
    
    // Worker threads
    std::vector<std::thread> workerThreads;
    std::atomic<bool> stopRequested{false};
    
    // Internal methods
    void InitializeServiceStatus();
    void MainServiceLoop();
    void HandleControlCode(DWORD ctrlCode);
    
    // Performance monitoring
    void UpdatePerformanceCounters();
    
    // Prevent copying
    ServiceBase(const ServiceBase&) = delete;
    ServiceBase& operator=(const ServiceBase&) = delete;
};

// MyService.cpp — minimal illustrative Windows Service in C++ (Win32)
#include <windows.h>
#include <string>
#include <thread>
#include <atomic>

static SERVICE_STATUS_HANDLE g_statusHandle = nullptr;
static SERVICE_STATUS g_serviceStatus = {};
static HANDLE g_stopEvent = nullptr;
static std::thread g_worker;
static std::atomic<bool> g_running{false};

void SetServiceState(DWORD currentState, DWORD win32ExitCode = NO_ERROR, DWORD waitHint = 0) {
    g_serviceStatus.dwCurrentState = currentState;
    g_serviceStatus.dwWin32ExitCode = win32ExitCode;
    g_serviceStatus.dwWaitHint = waitHint;
    if (currentState == SERVICE_START_PENDING) g_serviceStatus.dwControlsAccepted = 0;
    else g_serviceStatus.dwControlsAccepted = SERVICE_ACCEPT_STOP | SERVICE_ACCEPT_SHUTDOWN;
    SetServiceStatus(g_statusHandle, &g_serviceStatus);
}

DWORD WINAPI ServiceCtrlHandler(DWORD ctrl, DWORD eventType, LPVOID, LPVOID) {
    switch (ctrl) {
    case SERVICE_CONTROL_STOP:
    case SERVICE_CONTROL_SHUTDOWN:
        SetServiceState(SERVICE_STOP_PENDING, NO_ERROR, 30000);
        if (g_stopEvent) SetEvent(g_stopEvent);
        return NO_ERROR;
    case SERVICE_CONTROL_INTERROGATE:
        SetServiceStatus(g_statusHandle, &g_serviceStatus);
        return NO_ERROR;
    default:
        return ERROR_CALL_NOT_IMPLEMENTED;
    }
}

void WorkerThread() {
    // Example: do work until stop signaled
    while (g_running.load()) {
        // Wait for stopEvent for 1s or do periodic work
        DWORD wait = WaitForSingleObject(g_stopEvent, 1000);
        if (wait == WAIT_OBJECT_0) break;
        // Do actual work here (IO, DB, processing...). Break large tasks into cancellable chunks.
    }
}

void WINAPI ServiceMain(DWORD, LPWSTR*) {
    g_statusHandle = RegisterServiceCtrlHandlerExW(L"MyService", (LPHANDLER_FUNCTION_EX)ServiceCtrlHandler, nullptr);
    if (!g_statusHandle) return;

    ZeroMemory(&g_serviceStatus, sizeof(g_serviceStatus));
    g_serviceStatus.dwServiceType = SERVICE_WIN32_OWN_PROCESS;
    g_serviceStatus.dwServiceSpecificExitCode = 0;

    SetServiceState(SERVICE_START_PENDING, NO_ERROR, 30000);

    // create synchronization object for shutdown
    g_stopEvent = CreateEvent(nullptr, TRUE, FALSE, nullptr);
    if (!g_stopEvent) {
        SetServiceState(SERVICE_STOPPED, GetLastError(), 0);
        return;
    }

    // Start worker thread
    g_running.store(true);
    try {
        g_worker = std::thread(WorkerThread);
    } catch (...) {
        SetServiceState(SERVICE_STOPPED, ERROR_EXCEPTION_IN_SERVICE, 0);
        return;
    }

    // Now report running
    SetServiceState(SERVICE_RUNNING, NO_ERROR, 0);

    // Wait for worker to exit (or for stopEvent)
    WaitForSingleObject(g_stopEvent, INFINITE);

    // Signal cancellation and join worker
    g_running.store(false);
    if (g_worker.joinable()) g_worker.join();

    SetServiceState(SERVICE_STOPPED, NO_ERROR, 0);

    CloseHandle(g_stopEvent);
    g_stopEvent = nullptr;
}

// Simple install / uninstall helpers
bool InstallService(const std::wstring& exePath) {
    SC_HANDLE scm = OpenSCManager(nullptr, nullptr, SC_MANAGER_CREATE_SERVICE);
    if (!scm) return false;
    SC_HANDLE svc = CreateServiceW(
        scm, L"MyService", L"MyService DisplayName",
        SERVICE_ALL_ACCESS,
        SERVICE_WIN32_OWN_PROCESS,
        SERVICE_AUTO_START,
        SERVICE_ERROR_NORMAL,
        exePath.c_str(),
        nullptr, nullptr, nullptr, nullptr, nullptr);
    if (svc) CloseServiceHandle(svc);
    CloseServiceHandle(scm);
    return svc != nullptr;
}
bool UninstallService() {
    SC_HANDLE scm = OpenSCManager(nullptr, nullptr, SC_MANAGER_CONNECT);
    if (!scm) return false;
    SC_HANDLE svc = OpenServiceW(scm, L"MyService", SERVICE_STOP | DELETE | SERVICE_QUERY_STATUS);
    if (!svc) { CloseServiceHandle(scm); return false; }
    SERVICE_STATUS status;
    ControlService(svc, SERVICE_CONTROL_STOP, &status);
    bool ok = DeleteService(svc) == TRUE;
    CloseServiceHandle(svc);
    CloseServiceHandle(scm);
    return ok;
}

int wmain(int argc, wchar_t* argv[]) {
    if (argc > 1) {
        std::wstring cmd = argv[1];
        if (cmd == L"--install") {
            wchar_t path[MAX_PATH]; GetModuleFileNameW(nullptr, path, MAX_PATH);
            if (InstallService(path)) return 0;
            return 1;
        } else if (cmd == L"--uninstall") {
            return UninstallService() ? 0 : 1;
        } else if (cmd == L"--console") {
            // run as console for dev/debug
            g_stopEvent = CreateEvent(nullptr, TRUE, FALSE, nullptr);
            g_running.store(true);
            g_worker = std::thread(WorkerThread);
            printf("Running as console. Press Enter to stop...\n");
            getchar();
            SetEvent(g_stopEvent);
            g_running.store(false);
            g_worker.join();
            CloseHandle(g_stopEvent);
            return 0;
        }
    }

    // Normal service start
    SERVICE_TABLE_ENTRYW table[] = { { (LPWSTR)L"MyService", (LPSERVICE_MAIN_FUNCTIONW)ServiceMain }, { nullptr, nullptr } };
    if (!StartServiceCtrlDispatcherW(table)) {
        // If fails, consider logging the error
        return 1;
    }
    return 0;
}

