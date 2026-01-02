// map_network_drive_com.cpp
// Compile: cl /EHsc map_network_drive_com.cpp ole32.lib

#include <windows.h>
#include <iostream>
#include <comdef.h>     // _com_error
#include <oaidl.h>      // IDispatch, DISPPARAMS
#include <oleauto.h>    // SysAllocString, VariantInit

static void PrintHResultError(HRESULT hr, const char* msg) {
    _com_error err(hr);
    std::wcerr << L"[ERROR] " << msg << L" HRESULT=0x" << std::hex << hr
               << L" : " << err.ErrorMessage() << L"\n";
}

bool InvokeIDispatchMethod(IDispatch* pDisp, const wchar_t* methodName,
                           VARIANT* args, UINT argCount)
{
    if (!pDisp) return false;

    DISPID dispid;
    HRESULT hr = pDisp->GetIDsOfNames(IID_NULL, const_cast<LPOLESTR*>(&methodName), 1,
                                      LOCALE_USER_DEFAULT, &dispid);
    if (FAILED(hr)) {
        PrintHResultError(hr, "GetIDsOfNames failed");
        return false;
    }

    // Arguments must be in reverse order (right-to-left).
    DISPPARAMS dp = {};
    dp.cArgs = argCount;
    dp.rgvarg = args;
    dp.cNamedArgs = 0;
    dp.rgdispidNamedArgs = nullptr;

    VARIANT result;
    VariantInit(&result);

    hr = pDisp->Invoke(dispid, IID_NULL, LOCALE_USER_DEFAULT, DISPATCH_METHOD,
                       &dp, &result, nullptr, nullptr);
    if (FAILED(hr)) {
        PrintHResultError(hr, "Invoke failed");
        VariantClear(&result);
        return false;
    }

    VariantClear(&result);
    return true;
}

int wmain(int argc, wchar_t* argv[])
{
    HRESULT hr = CoInitializeEx(nullptr, COINIT_APARTMENTTHREADED);
    if (FAILED(hr)) {
        PrintHResultError(hr, "CoInitializeEx failed");
        return 1;
    }

    CLSID clsid;
    hr = CLSIDFromProgID(L"WScript.Network", &clsid);
    if (FAILED(hr)) {
        PrintHResultError(hr, "CLSIDFromProgID(WScript.Network) failed");
        CoUninitialize();
        return 1;
    }

    IDispatch* pNetwork = nullptr;
    hr = CoCreateInstance(clsid, nullptr, CLSCTX_INPROC_SERVER | CLSCTX_LOCAL_SERVER,
                          IID_IDispatch, (void**)&pNetwork);
    if (FAILED(hr) || !pNetwork) {
        PrintHResultError(hr, "CoCreateInstance(WScript.Network) failed");
        CoUninitialize();
        return 1;
    }

    // Example: Map drive Z: to \\server\share, not persistent, with optional credentials.
    // MapNetworkDrive(LocalName, NetworkName[, UpdateProfile[, UserName[, Password]]])
    // We'll provide LocalName and NetworkName; other args optional.

    // Parameters in reverse order for Invoke: last parameter first.
    VARIANT args[5];
    for (int i = 0; i < 5; ++i) VariantInit(&args[i]);

    // If you want to pass credentials, set username/password to BSTRs.
    // For this demo, we leave username/password empty (use current user credentials).
    // Order for VBScript call: MapNetworkDrive LocalName, NetworkName, UpdateProfile, UserName, Password
    // So reverse that for rgvarg: Password, UserName, UpdateProfile, NetworkName, LocalName

    // 5) Password (optional) - pass empty (VT_ERROR / VT_NULL) to use default
    VARIANT password; VariantInit(&password);
    V_VT(&password) = VT_ERROR;  // treat as missing optional parameter
    // 4) UserName (optional)
    VARIANT username; VariantInit(&username);
    V_VT(&username) = VT_ERROR;  // missing
    // 3) UpdateProfile (optional) - VARIANT_BOOL (TRUE to persist)
    VARIANT updateProfile; VariantInit(&updateProfile);
    V_VT(&updateProfile) = VT_BOOL;
    V_BOOL(&updateProfile) = VARIANT_FALSE; // set VARIANT_TRUE to persist in profile

    // 2) NetworkName (UNC path)
    VARIANT networkName; VariantInit(&networkName);
    V_VT(&networkName) = VT_BSTR;
    V_BSTR(&networkName) = SysAllocString(L"\\\\myserver\\shared"); // <-- change this

    // 1) LocalName (drive letter)
    VARIANT localName; VariantInit(&localName);
    V_VT(&localName) = VT_BSTR;
    V_BSTR(&localName) = SysAllocString(L"Z:"); // <-- change this (or "" for auto-pick via WScript? prefer "Z:")

    // Fill args in reverse order
    args[0] = password;       // last param
    args[1] = username;
    args[2] = updateProfile;
    args[3] = networkName;
    args[4] = localName;      // first param

    std::wcout << L"Mapping drive " << V_BSTR(&localName) << L" -> " << V_BSTR(&networkName) << L"\n";

    // Because we passed 5 VARIANT slots, tell Invoke about 5 arguments.
    if (!InvokeIDispatchMethod(pNetwork, L"MapNetworkDrive", args, 5)) {
        std::wcerr << L"MapNetworkDrive failed.\n";
        // cleanup before exit
        VariantClear(&localName);
        VariantClear(&networkName);
        VariantClear(&updateProfile);
        VariantClear(&username);
        VariantClear(&password);
        pNetwork->Release();
        CoUninitialize();
        return 1;
    }

    std::wcout << L"Drive mapped (if no exception/COM error was returned).\n";

    // Clean up the BSTRs/variants we allocated
    VariantClear(&localName);
    VariantClear(&networkName);
    VariantClear(&updateProfile);
    VariantClear(&username);
    VariantClear(&password);

    // Wait for user to press enter, then unmap
    std::wcout << L"Press Enter to remove the mapped drive...";
    std::wstring dummy;
    std::getline(std::wcin, dummy);

    // To remove: RemoveNetworkDrive(LocalName, [Force], [UpdateProfile])
    // We'll pass LocalName and Force=true, UpdateProfile=false.

    VARIANT remArgs[3];
    for (int i = 0; i < 3; ++i) VariantInit(&remArgs[i]);

    VARIANT remUpdate; VariantInit(&remUpdate);
    V_VT(&remUpdate) = VT_BOOL;
    V_BOOL(&remUpdate) = VARIANT_FALSE; // do not remove from profile

    VARIANT remForce; VariantInit(&remForce);
    V_VT(&remForce) = VT_BOOL;
    V_BOOL(&remForce) = VARIANT_TRUE; // force disconnect

    VARIANT remLocal; VariantInit(&remLocal);
    V_VT(&remLocal) = VT_BSTR;
    V_BSTR(&remLocal) = SysAllocString(L"Z:"); // same letter used above

    // reverse order: UpdateProfile, Force, LocalName
    remArgs[0] = remUpdate;
    remArgs[1] = remForce;
    remArgs[2] = remLocal;

    if (!InvokeIDispatchMethod(pNetwork, L"RemoveNetworkDrive", remArgs, 3)) {
        std::wcerr << L"RemoveNetworkDrive failed.\n";
    } else {
        std::wcout << L"RemoveNetworkDrive invoked.\n";
    }

    VariantClear(&remLocal);
    VariantClear(&remForce);
    VariantClear(&remUpdate);

    pNetwork->Release();
    CoUninitialize();
    return 0;
}
