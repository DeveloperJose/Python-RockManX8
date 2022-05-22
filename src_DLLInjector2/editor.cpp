// #include <string>
// #include <iostream>
#include <windows.h>

// #include "stdafx.h"
// #include "set.h"
// #include "detours.h"

// DWORD WINAPI MyThread(LPVOID);
// DWORD g_threadID;
// HMODULE g_hModule;

// *********************************************** Editor ***********************************************
// SetFile* setFile = (SetFile*)(0x047E37B0);


// *********************************************** Main DLL Stuff ***********************************************
BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD ul_reason_for_call, LPVOID lpReserved)
{
	switch (ul_reason_for_call)
	{
	case DLL_PROCESS_ATTACH:
		// g_hModule = hModule;
		// DisableThreadLibraryCalls(hModule);
		// CreateThread(NULL, 0, &MyThread, NULL, 0, &g_threadID);
        MessageBoxA(NULL, "Loaded", "Title", 0);
		break;
	}
	return TRUE;
}

// DWORD WINAPI MyThread(LPVOID lpParam)
// {
// 	AllocConsole();
// 	freopen_s((FILE**)stdout, "CONOUT$", "w", stdout);
// 	freopen_s((FILE**)stdin, "CONIN$", "r", stdin);
// 	printf("== Starting up Injector DLL3 ==\n");

// 	while (true)
// 	{
// 		if (GetAsyncKeyState(VK_F1) & 1)
// 			break;
// 		// else if (GetAsyncKeyState(VK_F2) & 1) {
// 		// 	printf("Set file enemy count = %x\n", setFile->enemyCount);
// 		// 	printf("Set file enemy 1 x = %f\n", setFile->GetEnemy(0)->pos.x);
// 		// 	printf("Set file enemy 1 y = %f\n", setFile->GetEnemy(0)->pos.y);
// 		// }
// 		// else if (GetAsyncKeyState(VK_F3) & 1) {
// 		// 	printf("Set file enemy 1 name = %s\n", setFile->GetEnemy(0)->name);
// 		// }
// 		// else if (GetAsyncKeyState(VK_F4) & 1) {
// 		// 	int newX = -1;
// 		// 	int newY = -1;
// 		// 	char newName[32];
// 		// 	//printf("Set the new X\n");
// 		// 	//std::cin >> newX;

// 		// 	//printf("Set the new Y\n");
// 		// 	//std::cin >> newY;

// 		// 	printf("Set the new type\n");
// 		// 	std::cin >> newName;
// 		// 	strcpy_s(setFile->GetEnemy(0)->name, 8, newName);

// 		// 	printf("new x = %d, new y = %d, new type = %s\n", newX, newY, newName);
// 		// }
// 		Sleep(5);
// 	}
// 	printf("== Injector DLL is being liberated ==\n");
// 	FreeLibraryAndExitThread(g_hModule, 0);
// 	return 0;
// }
