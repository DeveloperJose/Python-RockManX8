#include <string>
#include <iostream>
#include <windows.h>

#include "stdafx.h"
// #include "set.h"
// #include "detours.h"

DWORD WINAPI MyThread(LPVOID);
DWORD g_threadID;
HMODULE g_hModule;

// *********************************************** Editor ***********************************************
// SetFile* setFile = (SetFile*)(0x047E37B0);
bool isEditing = false;
vec3_t* camera = (vec3_t*)(baseAddr + 0x332C6C0);
float* other = (float*)(baseAddr + 0x332C6F0);

// *********************************************** Patches ***********************************************
void Patch(uintptr_t dstPtr, byte asmBytes[]) {
	DWORD oldProtect;

	VirtualProtect((LPVOID)dstPtr, sizeof(asmBytes), PAGE_EXECUTE_READWRITE, &oldProtect);
	memcpy((LPVOID)dstPtr, asmBytes, sizeof(asmBytes));
	VirtualProtect((LPVOID)dstPtr, sizeof(asmBytes), oldProtect, &oldProtect);
}
// *********************************************** Tab Patch ***********************************************
// BYTE nop[] = { 0x90, 0x90, 0x90, 0x90, 0x90, 0x90 };
byte tabPatchAsm[] = {0x5E, 0x5D, 0x33, 0xC0, 0x5B, 0xC2, 0x10, 0x00};
uintptr_t tabPatchPtr = (baseAddr + 0x19DBC13);
bool tabPatch = false;

// *********************************************** FreeCam Patch ***********************************************
byte camPatchAsm[] = { 0x90, 0x90, 0x90, 0x90, 0x90 };
uintptr_t camPatchXPtr = (baseAddr + 0x267A7BD);
uintptr_t camPatchYPtr = (baseAddr + 0x267A851);
uintptr_t camPatchZPtr = (baseAddr + 0x267A7C2);
bool camPatch = false;

// *********************************************** Main DLL Stuff ***********************************************
BOOL WINAPI DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)
{
	switch (ul_reason_for_call)
	{
	case DLL_PROCESS_ATTACH:
		g_hModule = hModule;
		DisableThreadLibraryCalls(hModule);
		CreateThread(NULL, NULL, &MyThread, NULL, NULL, &g_threadID);
		break;
	}
	return TRUE;
}

DWORD WINAPI MyThread(LPVOID lpParam)
{
	AllocConsole();
	freopen_s((FILE**)stdout, "CONOUT$", "w", stdout);
	freopen_s((FILE**)stdin, "CONIN$", "r", stdin);
	printf("== Starting up Injector DLL3 ==\n");
	printf("%x\n", baseAddr + tabPatchPtr);
	printf("%i\n", sizeof(tabPatchAsm));
	while (true)
	{
		if (GetAsyncKeyState(VK_F1) & 0x8000)
			break;
		else if (GetAsyncKeyState(VK_F5) & 0x8000) {
			if (!tabPatch) {
				Patch(tabPatchPtr, tabPatchAsm);
				tabPatch = true;
				printf("Tab Patch Applied\n");
			}
		}
		else if (GetAsyncKeyState(VK_F8) & 0x8000) {
			isEditing = !isEditing;
			printf("Editing Mode = %d\n", isEditing);
		}
		else if (GetAsyncKeyState(VK_F9) & 0x8000) {
			if (!camPatch) {
				Patch(camPatchXPtr, camPatchAsm);
				Patch(camPatchYPtr, camPatchAsm);
				Patch(camPatchZPtr, camPatchAsm);
				camPatch = true;
				printf("Cam Patch Applied\n");
			}
		}

		if (isEditing) {
			if (GetAsyncKeyState(VK_NUMPAD8))
				camera->y += 0.001f;
			if (GetAsyncKeyState(VK_NUMPAD6))
				camera->x += 0.001f;
			if (GetAsyncKeyState(VK_NUMPAD4))
				camera->x -= 0.001f;
			if (GetAsyncKeyState(VK_NUMPAD2))
				camera->y -= 0.001f;
			if (GetAsyncKeyState(VK_NUMPAD7))
				camera->z -= 0.001f;
			if (GetAsyncKeyState(VK_NUMPAD9))
				camera->z += 0.001f;
			if (GetAsyncKeyState(VK_NUMPAD1))
				*other -= 0.001f;
			if (GetAsyncKeyState(VK_NUMPAD3))
				*other += 0.001f;
		}
		// else if (GetAsyncKeyState(VK_F2) & 1) {
		// 	printf("Set file enemy count = %x\n", setFile->enemyCount);
		// 	printf("Set file enemy 1 x = %f\n", setFile->GetEnemy(0)->pos.x);
		// 	printf("Set file enemy 1 y = %f\n", setFile->GetEnemy(0)->pos.y);
		// }
		// else if (GetAsyncKeyState(VK_F3) & 1) {
		// 	printf("Set file enemy 1 name = %s\n", setFile->GetEnemy(0)->name);
		// }
		// else if (GetAsyncKeyState(VK_F4) & 1) {
		// 	int newX = -1;
		// 	int newY = -1;
		// 	char newName[32];
		// 	//printf("Set the new X\n");
		// 	//std::cin >> newX;

		// 	//printf("Set the new Y\n");
		// 	//std::cin >> newY;

		// 	printf("Set the new type\n");
		// 	std::cin >> newName;
		// 	strcpy_s(setFile->GetEnemy(0)->name, 8, newName);

		// 	printf("new x = %d, new y = %d, new type = %s\n", newX, newY, newName);
		// }
		Sleep(5);
	}
	
	printf("== Injector DLL has been liberated ==\n");
	FreeConsole();
	FreeLibraryAndExitThread(g_hModule, 0);
	return 0;
}
