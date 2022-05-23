#include <string>
#include <iostream>
#include <windows.h>

#include "stdafx.h"
#include "set.h"
// #include "detours.h"

// *********************************************** DLL Stuff ***********************************************
DWORD WINAPI MyThread(LPVOID);
DWORD g_threadID;
HMODULE g_hModule;

// *********************************************** Patches ***********************************************
void Patch(uintptr_t dst_ptr, const BYTE asm_bytes[], size_t size) {
	DWORD oldProtect;
	LPVOID dst = (LPVOID)(base_addr + dst_ptr);

	VirtualProtect(dst, size, PAGE_EXECUTE_READWRITE, &oldProtect);
	memcpy(dst, asm_bytes, size);
	VirtualProtect(dst, size, oldProtect, &oldProtect);
}
// *********************************************** Tab Patch
const BYTE tab_patch_asm[] = { 0x5E, 0x5D, 0x33, 0xC0, 0x5B, 0xC2, 0x10, 0x00 };
const uintptr_t tab_patch_ptr = 0x19DBC13;
bool has_tab_patch = false;

// *********************************************** FreeCam Patch
const BYTE cam_patch_asm[] = { 0x90, 0x90, 0x90, 0x90, 0x90 };
const uintptr_t cam_patch_x_ptr = 0x267A7BD;
const uintptr_t cam_patch_y_ptr = 0x267A851;
const uintptr_t cam_patch_z_ptr = 0x267A7C2;
bool has_cam_patch = false;

// *********************************************** NoGrav Patch
const BYTE no_grav_patch_asm[] = { 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, };
const BYTE no_grav_original_asm[] = { 0xF3, 0x0F, 0x11, 0x87, 0x94, 0x18, 0x6E, 0x04 };
const uintptr_t no_grav_patch_ptr = 0x244E08D;
bool has_nograv_patch = false;

// *********************************************** Editor ***********************************************
Entity* player1 = (Entity*)(base_addr + 0x42E21A0);
SetFile* set_file = (SetFile*)(base_addr + 0x323F940);
//vec3_t* camera = (vec3_t*)(base_addr + 0x332C6C0);
//float* other = (float*)(base_addr + 0x332C6F0);
//bool* invisible = (bool*)(base_addr + 0x42E21AC);

int32_t* pause_enemies = (int32_t*)(base_addr + 0x420A888);
int32_t* pause_exploding_boxes = (int32_t*)(base_addr + 0x420A978);
int32_t* pause_anims_and_interacts1 = (int32_t*)(base_addr + 0x420A8E8);
int32_t* pause_anims_and_interacts2 = (int32_t*)(base_addr + 0x420A8D0);
int32_t* pause_metals = (int32_t*)(base_addr + 0x420A8C4);
int32_t* pause_fog = (int32_t*)(base_addr + 0x420A8AC);
int32_t* hide_fog = (int32_t*)(base_addr + 0x420B6B4);
int32_t* hide_hp_ui = (int32_t*)(base_addr + 0x420BE4C);

bool is_editing = false;
int selected_enemy_idx = 0;

void MovePlayerToSelectedEnemy() {
	player1->X = set_file->enemies[selected_enemy_idx].X;
	player1->Y = set_file->enemies[selected_enemy_idx].Y;
	player1->Z = set_file->enemies[selected_enemy_idx].Z;
}

void RefreshChanges() {
	float old_x = player1->X;
	float old_y = player1->Y;
	float old_z = player1->Z;

	player1->X -= 1000;
	player1->Y -= 1000;
	player1->Z -= 1000;

	MovePlayerToSelectedEnemy();
}

void ToggleEditMode() {
	is_editing = !is_editing;

	*pause_enemies = is_editing;
	pause_exploding_boxes = is_editing;
	pause_anims_and_interacts1 = is_editing;
	pause_anims_and_interacts2 = is_editing;
	pause_metals = is_editing;
	*pause_fog = 1;
	hide_fog = is_editing;
	hide_hp_ui = is_editing;

	Patch(no_grav_patch_ptr, is_editing ? no_grav_patch_asm : no_grav_original_asm, is_editing ? sizeof(no_grav_patch_asm) : sizeof(no_grav_original_asm));
}

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
	printf("Base Addr: %x\n", base_addr);

	printf("HotKeys:\n");
	printf("F1 - Exit\n");
	printf("F4 - Set Debug\n");
	printf("F5 - Apply Tab Patch\n");
	printf("F6 - Find starting ptr\n");
	printf("F7 - Apply NoGrav Patch\n");
	printf("F8 - Editing Mode\n");
	printf("F9 - Apply Cam Patch\n");

	while (true)
	{
		if (GetAsyncKeyState(VK_F1) & 1)
			break;
		else if (GetAsyncKeyState(VK_F4) & 1) {
			
			printf("Enemies = %i\n", set_file->enemy_count);
			printf("E1 = %s\n", set_file->enemies[0].PrmType);
		}
		else if (GetAsyncKeyState(VK_F5) & 1) {
			if (!has_tab_patch) {
				Patch(tab_patch_ptr, tab_patch_asm, sizeof(tab_patch_asm));
				has_tab_patch = true;
				printf("Tab Patch Applied\n");
			}
		}
		else if (GetAsyncKeyState(VK_F7) & 1) {
			if (!has_nograv_patch) {
				printf("size before %i\n", sizeof(no_grav_patch_asm));
				Patch(no_grav_patch_ptr, no_grav_patch_asm, sizeof(no_grav_patch_asm));
				has_nograv_patch = true;
				printf("NoGrav Patch Applied\n");
			}
		}
		else if (GetAsyncKeyState(VK_F8) & 1) {
			ToggleEditMode();
			printf("Edit Mode = %d\n", is_editing);
		}
		else if (GetAsyncKeyState(VK_F9) & 1) {
			if (!has_cam_patch) {
				Patch(cam_patch_x_ptr, cam_patch_asm, sizeof(cam_patch_asm));
				Patch(cam_patch_y_ptr, cam_patch_asm, sizeof(cam_patch_asm));
				Patch(cam_patch_z_ptr, cam_patch_asm, sizeof(cam_patch_asm));
				has_cam_patch = true;
				printf("Cam Patch Applied\n");
			}
		}
		else if (GetAsyncKeyState(VK_F6) & 1) {
			Entity* player2_ptr = (Entity*)0x046E1950;

			// Look for prev
			Entity* prev = player2_ptr->Prev;
			Entity* prev_cpy = prev;
			printf("1st Prev Addr = %x\n", (uintptr_t)prev);
			int prev_count = 0;
			while ((uintptr_t)prev > 0) {
				prev_cpy = prev;
				prev = prev->Prev;
				++prev_count;

				if (prev_count > 300) {
					printf("Counted more than 300 prevs, stopping just in case.\n");
					break;
				}
			}

			// Look for next
			Entity* next = player2_ptr->Next;
			Entity* next_cpy = next;
			printf("1st Next Addr = %x\n", (uintptr_t)next);
			int next_count = 0;
			while ((uintptr_t)next > 0) {
				next_cpy = next;
				next = next->Next;
				++next_count;

				if (next_count > 300) {
					printf("Counted more than 300 prevs, stopping just in case.\n");
					break;
				}
			}

			printf("Prev Addr: %x | Total Prev Count = %i\n", (uintptr_t)prev, prev_count);
			printf("Next Addr: %x | Total Next Count = %i\n", (uintptr_t)next, next_count);
			printf("First Addr: %x | Last Addr: %x\n", (uintptr_t)prev_cpy, (uintptr_t)next_cpy);
		}

		if (is_editing) {
			if (GetAsyncKeyState(VK_ADD) & 1) {
				if (++selected_enemy_idx > set_file->enemy_count)
					selected_enemy_idx = set_file->enemy_count;
				MovePlayerToSelectedEnemy();
			}
			else if (GetAsyncKeyState(VK_SUBTRACT) & 1) {
				if (--selected_enemy_idx < 0)
					selected_enemy_idx = 0;
				MovePlayerToSelectedEnemy();
			}
			if (GetAsyncKeyState(VK_NUMPAD8) & 0x8000) {
				set_file->enemies[selected_enemy_idx].Y += 0.001f;
				RefreshChanges();
			}
			if (GetAsyncKeyState(VK_NUMPAD6) & 0x8000) {
				set_file->enemies[selected_enemy_idx].X += 0.001f;
				RefreshChanges();
			}
			if (GetAsyncKeyState(VK_NUMPAD4) & 0x8000) {
				set_file->enemies[selected_enemy_idx].X -= 0.001f;
				RefreshChanges();
			}
			if (GetAsyncKeyState(VK_NUMPAD2) & 0x8000) {
				set_file->enemies[selected_enemy_idx].Y -= 0.001f;
				RefreshChanges();
			}
			if (GetAsyncKeyState(VK_NUMPAD7) & 0x8000) {
				set_file->enemies[selected_enemy_idx].Z -= 0.001f;
				RefreshChanges();
			}
			if (GetAsyncKeyState(VK_NUMPAD9) & 0x8000) {
				set_file->enemies[selected_enemy_idx].Z += 0.001f;
				RefreshChanges();
			}
			if (GetAsyncKeyState(VK_NUMPAD1) & 0x8000) {
				set_file->enemies[selected_enemy_idx].Rotation -= 0.001f;
				RefreshChanges();
			}
			if (GetAsyncKeyState(VK_NUMPAD3) & 0x8000) {
				set_file->enemies[selected_enemy_idx].Rotation += 0.001f;
				RefreshChanges();
			}
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
