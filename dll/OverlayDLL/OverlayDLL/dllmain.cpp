// dllmain.cpp : Defines the entry point for the DLL application.
#include "stdafx.h"
#include <windows.h>

DWORD WINAPI MyThread(LPVOID);
DWORD g_threadID;
HMODULE g_hModule;
WORD *w = (WORD *)0x46147B8;
typedef void (__thiscall *Load_MCB_File)(WORD *p46147B8, const char *pathMCB);
typedef void (__thiscall *Load_MCB_Format)(unsigned int);
typedef char(__thiscall *Cutscene_Gateway)(BYTE *p428E098);

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)
{
	switch (ul_reason_for_call)
	{
	case DLL_PROCESS_ATTACH:
		/* The DLL is being loaded for the first time by a given process.
		Perform per-process initialization here.  If the initialization
		is successful, return TRUE; if unsuccessful, return FALSE. */
		g_hModule = hModule;
		DisableThreadLibraryCalls(hModule);
		CreateThread(NULL, NULL, &MyThread, NULL, NULL, &g_threadID);
		break;
	}
	return TRUE;
}

DWORD WINAPI MyThread(LPVOID)
{
	Load_MCB_Format func = (Load_MCB_Format)0x008BB170;
	Load_MCB_File func2 = (Load_MCB_File)0x00404318;
	Cutscene_Gateway func3 = (Cutscene_Gateway)0x4F4770;

	BYTE *b = (BYTE *)0x428E098;
	*b = 4;

	while (true)
	{
		if (GetAsyncKeyState(VK_F3) & 1) //Set F3 as our hotkey
		{
			func3(b);
		}
		else if (GetAsyncKeyState(VK_F4) & 1)
			break;
		Sleep(100);
	}
	MessageBoxA(0, "DLL is being liberated", "DLL Bot", MB_ICONEXCLAMATION | MB_OK);
	FreeLibraryAndExitThread(g_hModule, 0);
	return 0;
}
