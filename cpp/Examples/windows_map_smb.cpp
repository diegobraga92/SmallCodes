// map_smb_drive.cpp
// Compile with: cl /EHsc map_smb_drive.cpp Mpr.lib
// or add Mpr.lib to your Visual Studio Linker -> Input.

#include <windows.h>
#include <winnetwk.h>
#include <iostream>
#include <string>
#include <sstream>

#pragma comment(lib, "Mpr.lib")

std::wstring GetLastErrorMessage(DWORD err) {
    if (err == NO_ERROR) return L"No error.";

    LPWSTR msgBuf = nullptr;
    DWORD size = FormatMessageW(
        FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS,
        nullptr, err, MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
        (LPWSTR)&msgBuf, 0, nullptr);

    std::wstring msg = (size && msgBuf) ? msgBuf : L"Unknown error";
    if (msgBuf) LocalFree(msgBuf);
    return msg;
}

bool MapNetworkDrive(
    const std::wstring& driveLetter,          // e.g. L"Z:"
    const std::wstring& uncPath,              // e.g. L"\\\\server\\share"
    const std::wstring& username = L"",       // e.g. L"DOMAIN\\username" or L"username"
    const std::wstring& password = L"",       // password (empty if using current user's credentials)
    bool persistent = false,                  // true -> reconnect at logon (writes to user profile)
    DWORD& outWinError = *(new DWORD(0)))
{
    NETRESOURCEW nr = {};
    nr.dwType = RESOURCETYPE_DISK;
    nr.lpLocalName = const_cast<LPWSTR>(driveLetter.c_str());
    nr.lpRemoteName = const_cast<LPWSTR>(uncPath.c_str());
    nr.lpProvider = nullptr;

    DWORD flags = 0;
    if (persistent) flags |= CONNECT_UPDATE_PROFILE; // write mapping to profile

    // If driveLetter is an empty string, Windows will choose a drive letter (lpLocalName = NULL).
    LPWSTR user = username.empty() ? nullptr : const_cast<LPWSTR>(username.c_str());
    LPWSTR pass = password.empty() ? nullptr : const_cast<LPWSTR>(password.c_str());

    DWORD result = WNetAddConnection2W(&nr, pass, user, flags);
    outWinError = result;

    if (result == NO_ERROR) {
        return true;
    } else {
        std::wcerr << L"WNetAddConnection2 failed: " << result << L" - " << GetLastErrorMessage(result) << L"\n";
        return false;
    }
}

bool UnmapNetworkDrive(
    const std::wstring& driveOrRemote, // e.g. L"Z:" or L"\\\\server\\share"
    bool force = false,                // true -> force the disconnect (close open files)
    bool persistent = false,           // true -> remove from profile if present
    DWORD& outWinError = *(new DWORD(0)))
{
    DWORD flags = 0;
    if (persistent) flags |= CONNECT_UPDATE_PROFILE;
    DWORD result = WNetCancelConnection2W(driveOrRemote.c_str(), flags, force ? TRUE : FALSE);
    outWinError = result;
    if (result == NO_ERROR) {
        return true;
    } else {
        std::wcerr << L"WNetCancelConnection2 failed: " << result << L" - " << GetLastErrorMessage(result) << L"\n";
        return false;
    }
}

int wmain(int argc, wchar_t* argv[])
{
    // Example usage:
    // 1) Map Z: to \\server\share using explicit credentials, persistent
    // 2) Unmap Z:
    //
    // WARNING: Passing credentials on the command line can expose them to other users on the machine.
    //          Prefer secure credential storage or prompting at runtime for production.

    std::wstring drive = L"Z:";                          // desired local drive letter
    std::wstring unc = L"\\\\myfileserver\\shared";     // UNC path to the SMB share
    std::wstring user = L"DOMAIN\\myuser";              // or just L"myuser" for local account
    std::wstring pass = L"SuperSecretPassword";         // be careful with plaintext passwords
    bool persistent = false;                            // set to true to reconnect at logon

    DWORD err;
    std::wcout << L"Mapping " << drive << L" -> " << unc << L"\n";
    if (MapNetworkDrive(drive, unc, user, pass, persistent, err)) {
        std::wcout << L"Drive mapped successfully.\n";
    } else {
        std::wcout << L"Failed to map drive. Error " << err << L": " << GetLastErrorMessage(err) << L"\n";
    }

    // If you want to unmap later:
    std::wcout << L"Press Enter to unmap the drive...";
    std::wstring dummy;
    std::getline(std::wcin, dummy);

    if (UnmapNetworkDrive(drive, /*force=*/true, persistent, err)) {
        std::wcout << L"Drive unmapped successfully.\n";
    } else {
        std::wcout << L"Failed to unmap drive. Error " << err << L": " << GetLastErrorMessage(err) << L"\n";
    }

    return 0;
}
