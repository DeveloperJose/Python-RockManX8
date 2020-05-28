#include "stdafx.h"
#include "myIDirect3D8.h"
#include "myIDirect3DDevice8.h"
#include "hooks.h"

typedef IDirect3D8 *(WINAPI *FND3DC8)(UINT);
FND3DC8 Direct3DCreate8_out;


IDirect3D8* WINAPI Direct3DCreate8(UINT SDKVersion) {
	return new myIDirect3D8(Direct3DCreate8_out(SDKVersion));
}

void Startup(HINSTANCE hInstance)
{
	MessageBoxA(0, "DirectX Hook Started!", "Information", MB_ICONINFORMATION | MB_OK);
	TCHAR szDllPath[MAX_PATH] = { 0 };

	GetSystemDirectory(szDllPath, MAX_PATH);

	// We have to specify the full path to avoid the search order
	lstrcat(szDllPath, "\\d3d8.dll");
	HMODULE hDll = LoadLibrary(szDllPath);

	if (hDll == NULL)
		return;

	// Pointer to the original function
	Direct3DCreate8_out = (FND3DC8)GetProcAddress(hDll, "Direct3DCreate8");

	if (Direct3DCreate8_out == NULL)
	{
		FreeLibrary(hDll);
		return;
	}

}

void Shutdown(HINSTANCE hInstance)
{

}

bool WINAPI DllMain(HINSTANCE hInstance, DWORD dwReason, LPVOID p)
{
	switch (dwReason) {
	case DLL_PROCESS_ATTACH:
		Startup(hInstance);
		break;

	case DLL_PROCESS_DETACH:
		Shutdown(hInstance);
		break;
	}
	return TRUE;
}
