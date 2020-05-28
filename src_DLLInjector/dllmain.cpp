// dllmain.cpp : Defines the entry point for the DLL application.
#include "stdafx.h"
#include <string>
#include <iostream>
#include <windows.h>

#include "detours.h";

using namespace std;

DWORD WINAPI MyThread(LPVOID);
DWORD g_threadID;
HMODULE g_hModule;
WORD *w = (WORD *)0x46147B8;
FLOAT *x = (FLOAT *)0x045A61F8;
FLOAT *y = (FLOAT *)0x045A61FC;
WORD *p428E098 = (WORD *)0x428E098;
//typedef void (__thiscall *Load_MCB_File)(WORD *p46147B8, const char *pathMCB);
typedef void (__thiscall *Load_MCB_Format)(unsigned int);
typedef char(__thiscall *Cutscene_Gateway)(WORD *p428E098);
typedef __int16(__thiscall *Load_MCB_File2)(WORD* p, const char *a2);
typedef __int16(__thiscall *sub_4071f3)(WORD *w, const char *a2, int a3, int a4);
typedef int(__cdecl *sub40A628)(int a1);

// cutscene
DWORD *dword4478F90 = (DWORD *)0x4478F90;
typedef int(__thiscall *sub4148F8)(DWORD *dword);
typedef int(__stdcall *sub40D670)(int a1);
typedef int(__cdecl *sub40D7A6)(int a1, int a2);
typedef int(__cdecl *sub4140F6)(int a1);
typedef signed int(__cdecl *sub409444)(int a1, const char* a2, int a3, int a4);

// Debugging function, currently only prints VER 0119 and SPA
typedef int(__cdecl *debug_print1)(int a1, int a2, int a3, int a4, const char * a5, char a6);
debug_print1 j_true_print1 = ((debug_print1)0x40D571);
debug_print1 true_print1 = ((debug_print1)0x47A920);

// Parameter test
typedef int(__thiscall *parameter_test)(char *th, unsigned __int8 a2);
parameter_test true_parameter_test = ((parameter_test)0x875D20);

// Detour prints
typedef int(__cdecl *null_print)(const char* c);
null_print true_null_print1 = ((null_print)0x409660);
null_print true_null_print2 = ((null_print)0x41194B);
null_print true_null_print3 = ((null_print)0x004078AB);

void(__stdcall *True_OutputDebugStringA)(LPCSTR) = OutputDebugStringA;
void(__stdcall *True_OoutputDebugStringW)(LPCWSTR) = OutputDebugStringW;
void(__stdcall *True_OutputDebugString)(LPCWSTR) = OutputDebugString;

void __stdcall HookedOutputDebugStringA(LPCSTR s) {
	printf("OutputA: %s\n", s);
}

void __stdcall HookedOutputDebugString(LPCWSTR s) {
	printf("OutputW: %ls\n", s);
}

int __cdecl HookedPrint(const char* c) {
	printf("HP %s\n", c);
	return 0;
}

// Detour
int __cdecl Hooked(int a1, int a2, int a3, int a4, const char * a5, char a6) {
	printf("Hook: A1=%d, A2=%d, A3=%d, A4=%d, Format=%s, Char=%c\n", a1, a2, a3, a4, a5, a6);
	return 0;
}

// Detour MCB (my area of expertise)
typedef void(__thiscall *Load_MCB_File)(void*, WORD*, const char *);
Load_MCB_File true_load_mcb_file = ((Load_MCB_File)0x00527A40);

void __fastcall HookedLoadMCBFile(void* pthis, WORD* w, const char *path) {
	printf("Load: %s\n", path);
	printf("Addr: %d, Content: %x\n", &w, w);
}

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

FLOAT prevX = 0;
FLOAT prevY = 0;

DWORD WINAPI MyThread(LPVOID)
{
	AllocConsole();
	freopen_s((FILE**)stdout, "CONOUT$", "w", stdout);
	cout << "==Starting up DLL==\n";
	//Load_MCB_Format func = (Load_MCB_Format)0x008BB170;
	//Load_MCB_File loadmcbfile = (Load_MCB_File)0x00404318;
	//Cutscene_Gateway func3 = (Cutscene_Gateway)0x4F4770;
	//Load_MCB_File2 loadmcbfile2 = (Load_MCB_File2)0x00527EE0;

	//BYTE *b = (BYTE *)0x428E098;
	//*b = 4;

	prevX = *x;
	prevY = *y;

	// Detours
	LONG lError;
	
	//DetourTransactionBegin();
	//DetourUpdateThread(GetCurrentThread());
	//DetourAttach(&(PVOID&)true_print1, Hooked);
	//lError = DetourTransactionCommit();
	//if (lError != NO_ERROR) {
	//	MessageBox(HWND_DESKTOP, L"Failed to detour1", L"timb3r", MB_OK);
	//	return FALSE;
	//}

	DetourTransactionBegin();
	DetourUpdateThread(GetCurrentThread());
	DetourAttach(&(PVOID&)true_null_print1, HookedPrint);
	lError = DetourTransactionCommit();
	if (lError != NO_ERROR) {
		MessageBox(HWND_DESKTOP, L"Failed to detour2", L"timb3r", MB_OK);
		return FALSE;
	}

	DetourTransactionBegin();
	DetourUpdateThread(GetCurrentThread());
	DetourAttach(&(PVOID&)true_null_print2, HookedPrint);
	lError = DetourTransactionCommit();
	if (lError != NO_ERROR) {
		MessageBox(HWND_DESKTOP, L"Failed to detour3", L"timb3r", MB_OK);
		return FALSE;
	}

	DetourTransactionBegin();
	DetourUpdateThread(GetCurrentThread());
	DetourAttach(&(PVOID&)true_null_print3, HookedPrint);
	lError = DetourTransactionCommit();
	if (lError != NO_ERROR) {
		MessageBox(HWND_DESKTOP, L"Failed to detour4", L"timb3r", MB_OK);
		return FALSE;
	}

	DetourTransactionBegin();
	DetourUpdateThread(GetCurrentThread());
	DetourAttach(&(PVOID&)True_OutputDebugStringA, HookedOutputDebugStringA);
	lError = DetourTransactionCommit();
	if (lError != NO_ERROR) {
		MessageBox(HWND_DESKTOP, L"Failed to detour5", L"timb3r", MB_OK);
		return FALSE;
	}


	DetourTransactionBegin();
	DetourUpdateThread(GetCurrentThread());
	DetourAttach(&(PVOID&)True_OoutputDebugStringW, HookedOutputDebugString);
	lError = DetourTransactionCommit();
	if (lError != NO_ERROR) {
		MessageBox(HWND_DESKTOP, L"Failed to detour6", L"timb3r", MB_OK);
		return FALSE;
	}


	DetourTransactionBegin();
	DetourUpdateThread(GetCurrentThread());
	DetourAttach(&(PVOID&)True_OutputDebugString, HookedOutputDebugString);
	lError = DetourTransactionCommit();
	if (lError != NO_ERROR) {
		MessageBox(HWND_DESKTOP, L"Failed to detour7", L"timb3r", MB_OK);
		return FALSE;
	}

	DetourTransactionBegin();
	DetourUpdateThread(GetCurrentThread());
	DetourAttach(&(PVOID&)true_load_mcb_file, HookedLoadMCBFile);
	lError = DetourTransactionCommit();
	if (lError != NO_ERROR) {
		MessageBox(HWND_DESKTOP, L"Failed to detour MCB Load", L"timb3r", MB_OK);
		return FALSE;
	}

	
	while (true)
	{
		*x = prevX;
		*y = prevY;
		if (GetAsyncKeyState(VK_LEFT) & 1) //Set F3 as our hotkey
		{
			prevX -= 0.5;
		}
		else if (GetAsyncKeyState(VK_RIGHT) & 1)
			prevX += 0.5;
		else if (GetAsyncKeyState(VK_UP) & 1)
			prevY -= 0.5;
		else if (GetAsyncKeyState(VK_DOWN) & 1)
			prevY += 0.5;
		else if (GetAsyncKeyState(VK_F1) & 1)
			break;
		else if (GetAsyncKeyState(VK_NUMPAD0) & 1)
		{
			//func4(w, "mes/OPT_TIT.mcb");
			//func2(w, "mes/LAB_TXT.mcb");
			//((sub_4071f3)0x4071f3)(w, "HB_DEMO19*", 1, 1); // Seems to close dialog with first integer being 1, the other integer's effect is unknown
			
		/*	loadmcbfile2(w, "mes/HB_TIT.mcb");
			loadmcbfile2(w, "mes/SAVE_TIT.mcb");
			loadmcbfile2(w, "mes/LABO_TIT.mcb");
			loadmcbfile2(w, "mes/OPT_TIT.mcb");
			loadmcbfile(w, "mes/OPT_TXT.mcb");
			loadmcbfile(w, "mes/HB_IM.mcb");
			loadmcbfile(w, "mes/LABO_TXT.mcb");*/
			((sub40A628)0x40A628)(23);
			
		}
		else if (GetAsyncKeyState(VK_NUMPAD1) & 1) {
			int d_2A = -1;
			d_2A = ((sub4148F8)0x4148F8)(dword4478F90);
			printf("d_2A=%d\n", d_2A);
			int r1 = ((sub40D670)0x40D670)(d_2A);
			int r2 = ((sub40D7A6)0x40D7A6)(d_2A, 65526);
			int r3 = ((sub4140F6)0x4140F6)(d_2A);
			int v3 = ((sub409444)0x409444)(d_2A, "ID_HB_013", 0, -1);
			printf("r1=%d, r2=%d, r3=%d, v3=%d\n", r1, r2, r3, v3);
		}
		else if (GetAsyncKeyState(VK_NUMPAD2) & 1) {
			printf("Numpad2\n");
			// ((Cutscene_Gateway)0x40769E)(p428E098);
			((debug_print1)0x40D571)(54, 38, 50, 34, "Message", 'C');
		}
		else if (GetAsyncKeyState(VK_NUMPAD3) & 1) {
			printf("Numpad3\n");
			char test = 't';
			true_parameter_test(&test, 1);
		}
		Sleep(5);
	}
	MessageBoxA(0, "DLL is being liberated", "DLL Bot", MB_ICONEXCLAMATION | MB_OK);
	FreeLibraryAndExitThread(g_hModule, 0);
	FreeConsole();

	//DetourTransactionBegin();
	//DetourUpdateThread(GetCurrentThread());
	//DetourDetach(&(PVOID&)truesub, Hooked);
	//lError = DetourTransactionCommit();
	//if (lError != NO_ERROR) {
	//	MessageBox(HWND_DESKTOP, L"Failed to detour", L"timb3r", MB_OK);
	//	return FALSE;
	//}

	return 0;
}
