#include "stdafx.h"
#include "w_d3d9.h"
#include "hooks.h"

#pragma data_seg (".shared")
const char* example = "TEST";
//myIDirect3DDevice8* gl_pmyIDirect3DDevice8 = NULL;
//myIDirect3D8*       gl_pmyIDirect3D8;
//HINSTANCE           gl_hOriginalDll;
//HINSTANCE           gl_hThisInstance;
#pragma data_seg ()

Function_Direct3DCreate9 Original_Direct3DCreate9;

IDirect3D9* WINAPI Direct3DCreate9(UINT SDKVersion) {
	return new f_iD3D9(Original_Direct3DCreate9(SDKVersion));
}

void Startup(HINSTANCE hInstance)
{
	// MessageBoxA(0, "DirectX Hook Started!", "Information", MB_ICONINFORMATION | MB_OK);
	AllocConsole();
	freopen_s((FILE**)stdout, "CONOUT$", "w", stdout);
	printf("==Starting up DLL==\n");

	// Load original D3D8 if possible
	TCHAR szDllPath[MAX_PATH] = { 0 };
	GetSystemDirectory(szDllPath, MAX_PATH);

	// We have to specify the full path to avoid the search order
	lstrcat(szDllPath, "\\d3d9.dll");
	HMODULE hDll = LoadLibrary(szDllPath);

	if (hDll == NULL)
		return;

	// Pointer to the original function
	Original_Direct3DCreate9 = (Function_Direct3DCreate9)GetProcAddress(hDll, "Direct3DCreate9");

	if (Original_Direct3DCreate9 == NULL)
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
