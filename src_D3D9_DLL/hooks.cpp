/*
	TODO:
		-Virtual pausing is incomplete, not everything is paused
		-Sync with SET files
		-Make player model invisible
		-Only allow set editor when a level is loaded
		-Integrate with C# WinForms for easier GUI?
*/
#include "stdafx.h"

#include "set.h"
#include "w_d3d9.h"
#include "hooks.h"

//// POINTERS
//uintptr_t pBase = (uintptr_t)GetModuleHandle(TEXT("NOCD.EXE"));
//uintptr_t pCoordinatesBase = 0x045C284C;
//unsigned int coordinatesLength = 0x47C;
//
//bool* noCollision = (bool*)0x45A619C;
//
//float* p1ScreenPercent = (float*)0x44D28A4;
//int* setFileEnemyCount = (int*)0x047E37C6;
//
//bool* enemyPause = (bool*)0x0428DB88;
//bool* playerPause = (bool*)0x0428DDB0;
//
//int currentObjectID = 0;
//bool editingMode = false;
//bool debug = false;
//
//vec3_t* p1Position = (vec3_t*)(pBase + 0x41A61F8);
//vec3_t* p2Position = (vec3_t*)(pBase + 0x3FFDF58 + 0x70);


bool WorldToScreen(LPDIRECT3DDEVICE9 pDevice, D3DXVECTOR3* pos, D3DXVECTOR3* out) {
	D3DVIEWPORT9 viewPort;
	D3DXMATRIX view, projection, world;

	pDevice->GetViewport(&viewPort);
	pDevice->GetTransform(D3DTS_VIEW, &view);
	pDevice->GetTransform(D3DTS_PROJECTION, &projection);
	D3DXMatrixIdentity(&world);

	D3DXVec3Project(out, pos, &viewPort, &projection, &view, &world);
	if (out->z < 1) {
		return true;
	}
	return false;
}

void DrawBone(IDirect3DDevice9 *pDevice, ID3DXFont *pFont, int ptr, char * name) {
	float* x = (float*)ptr;
	float* y = (float*)(ptr + 4);
	float* z = (float*)(ptr + 8);

	D3DXVECTOR3 boneVector = { *x, *y, *z };
	D3DXVECTOR3 boneScreenPos;

	// printf("[DrawBone] X=%f, Y=%f, Z=%f\n", *x, *y, *z);

	if (WorldToScreen(pDevice, &boneVector, &boneScreenPos)) {
		RECT x = { boneScreenPos.x, boneScreenPos.y, boneScreenPos.x + 0.1, boneScreenPos.y + 0.1 };
		pFont->DrawText(NULL, name, -1, &x, DT_LEFT | DT_NOCLIP, D3DCOLOR_XRGB(0, 158, 255));
	}
}

bool IsValidVec3(int ptr) {
	float* xptr = (float*)ptr;
	float* yptr = (float*)(ptr + 4);
	float* zptr = (float*)(ptr + 8);

	float x = *xptr;
	float y = *yptr;
	float z = *zptr;

	return x + y + z > 1;
}

//vec3_t* GetCoordinatesForObject(int objectNumber) {
//	return (vec3_t*)(pCoordinatesBase + (objectNumber * coordinatesLength));
//}
//
//void SetGravity(bool gravity) {
//	if (gravity) {
//		DWORD oldProtect;
//		BYTE orig[] = { 0xD9, 0x9E, 0xD4, 0x60, 0x5A, 0x04 };
//		VirtualProtect((LPVOID)(pBase + 0xA1A80), sizeof(orig), PAGE_EXECUTE_READWRITE, &oldProtect);
//		memcpy((LPVOID)(pBase + 0xA1A80), orig, sizeof(orig));
//		VirtualProtect((LPVOID)(pBase + 0xA1A80), sizeof(orig), oldProtect, &oldProtect);
//	}
//	else {
//		BYTE nop[] = { 0x90, 0x90, 0x90, 0x90, 0x90, 0x90 };
//		DWORD oldProtect;
//		VirtualProtect((LPVOID)(pBase + 0xA1A80), sizeof(nop), PAGE_EXECUTE_READWRITE, &oldProtect);
//		memset((LPVOID)(pBase + 0xA1A80), 0x90, sizeof(nop));
//		VirtualProtect((LPVOID)(pBase + 0xA1A80), sizeof(nop), oldProtect, &oldProtect);
//	}
//}
//
//void ToggleEditingMode() {
//	printf("Engine located at %X\n", pBase);
//	if (editingMode) {
//		// Disable editing mode
//		editingMode = false;
//		*enemyPause = false;
//		*noCollision = false;
//		SetGravity(true);
//	}
//	else {
//		// Enable editing mode
//		editingMode = true;
//		*enemyPause = true;
//		*noCollision = true;
//		SetGravity(false);
//	}
//}
//
//void SyncPlayer() {
//	if (currentObjectID > 1) {
//		vec3_t* objectCoords = GetCoordinatesForObject(currentObjectID);
//		p1Position->x = objectCoords->x;
//		p1Position->y = objectCoords->y;
//		p1Position->z = objectCoords->z;
//		
//	}
//}

LRESULT CALLBACK SubclassWindowProc(HWND hWnd, UINT uMsg, WPARAM wParam, LPARAM lParam, UINT_PTR uIdSubclass, DWORD_PTR dwRefData)
{
	//float xChange = 0;
	//float yChange = 0;
	//float zChange = 0;
	//switch (uMsg) {
	//case WM_KEYDOWN:
	//{
	//	if (wParam == VK_NUMPAD7) {
	//		ToggleEditingMode();
	//	}

	//	if (editingMode) {
	//		if (wParam == VK_ADD) {
	//			currentObjectID++;
	//			SyncPlayer();
	//		}
	//		else if (wParam == VK_SUBTRACT) {
	//			currentObjectID--;
	//			if (currentObjectID < 0)
	//				currentObjectID = 0;

	//			SyncPlayer();
	//		}
	//		else if (wParam == VK_NUMPAD4)
	//			xChange = -0.5;
	//		else if (wParam == VK_NUMPAD6)
	//			xChange = 0.5;
	//		else if (wParam == VK_NUMPAD8)
	//			yChange = 0.5;
	//		else if (wParam == VK_NUMPAD2)
	//			yChange = -0.5;
	//		else if (wParam == VK_NUMPAD1)
	//			zChange = -0.5;
	//		else if (wParam == VK_NUMPAD3)
	//			zChange = 0.5;
	//	}
	//	else
	//	{
	//		/*if (wParam == VK_NUMPAD9) {
	//			int validCount = 0;
	//			for (int i = 0; i < *setFileEnemyCount; i++) {
	//				uintptr_t coord_ptr = pCoordinatesBase + (i * coordinatesLength);
	//				if (IsValidVec3(coord_ptr))
	//					validCount++;
	//			}
	//			printf("The set file has %d enemies, in memory %d enemies have valid coordinates\n", *setFileEnemyCount, validCount);
	//		}
	//		else if (wParam == VK_NUMPAD4) {
	//			p1Position->x = 1000;
	//			p1Position->y = 1000;

	//			p1Position->x = 5;
	//			p1Position->y = 5;
	//		}
	//		else if (wParam == VK_NUMPAD6) {
	//			p1Position->x = 5;
	//			p1Position->y = 5;
	//		}
	//		else if (wParam == VK_NUMPAD0) {
	//			printf("P1 Position: x=%f\n", p1Position->x);
	//			printf("P1 Ptr at %x\n", pBase + 0x41A61F8);
	//		}*/
	//	}
	//}
	//break;

	//case WM_KEYUP:
	//{
	//}
	//break;
	//}

	//vec3_t* objectCoords;
	//if (currentObjectID == 0)
	//	objectCoords = p1Position;
	//else if (currentObjectID == 1)
	//	objectCoords = p2Position;
	//else
	//	objectCoords = GetCoordinatesForObject(currentObjectID);

	//if (xChange != 0) {
	//	objectCoords->x += xChange;
	//	xChange = 0;
	//}

	//if (yChange != 0) {
	//	objectCoords->y += yChange;
	//	yChange = 0;
	//}

	//if (zChange != 0) {
	//	objectCoords->z += zChange;
	//	zChange = 0;
	//}

	// Pass messages onto the main proc
	return DefSubclassProc(hWnd, uMsg, wParam, lParam);
}


void HookEndScene(IDirect3DDevice9 *pDevice) {
	printf("EndScence\n");
	//D3DRECT backgroundRect = { 1, 1, 400 /*width*/, 80 /*height*/ };

	//D3DRECT borderRect = { backgroundRect.x1 - 1,
	//					   backgroundRect.y1 - 1,
	//					   backgroundRect.x2 + 1,
	//					   backgroundRect.y2 + 1 };
	////pDevice->Clear(1, &borderRect, D3DCLEAR_TARGET, D3DCOLOR_XRGB(255, 0, 0), 0, 0);
	////pDevice->Clear(1, &backgroundRect, D3DCLEAR_TARGET, D3DCOLOR_XRGB(0, 0, 0), 0, 0);

	//HRESULT r = 0;

	//// Create the D3DX Font
	//ID3DXFont *pFont;
	//r = D3DXCreateFont(pDevice, 24 /*Font size*/, 0 /*Font width*/, FW_BOLD, 1, FALSE, DEFAULT_CHARSET, OUT_DEFAULT_PRECIS, 0, DEFAULT_PITCH | FF_DONTCARE, "Comic Sans MS", &pFont);

	//if (FAILED(r)) {
	//	MessageBoxA(0, "Font failure", "Info", MB_ICONINFORMATION | MB_OK);
	//	return;
	//}

	//// Rectangle where the text will be located
	//RECT TextRect = { 15, 200, 0, 0 };

	// Calculate the rectangle the text will occupy
	//if (editingMode) {
	//	vec3_t* objectCoords = GetCoordinatesForObject(currentObjectID);

	//	char formatted_string[100];
	//	const char * entityName = NULL;
	//	if (currentObjectID == 0)
	//		entityName = "Player 1";
	//	else if (currentObjectID == 1)
	//		entityName = "Player 2";

	//	if (entityName == NULL)
	//		sprintf_s(formatted_string, "Entity: %d,X=%f,Y=%f,Z=%f,ptr=%X", currentObjectID, objectCoords->x, objectCoords->y, objectCoords->z, pCoordinatesBase + (currentObjectID * coordinatesLength));
	//	else
	//		sprintf_s(formatted_string, "Entity: %s,X=%f,Y=%f,Z=%f,ptr=%X", entityName, objectCoords->x, objectCoords->y, objectCoords->z, pCoordinatesBase + (currentObjectID * coordinatesLength));

	//	pFont->DrawText(NULL, formatted_string, -1, &TextRect, DT_LEFT | DT_NOCLIP, D3DCOLOR_XRGB(0, 0, 0));
	//
	//	D3DXVECTOR3 pos = { objectCoords->x, objectCoords->y, objectCoords->z };
	//	D3DXVECTOR3 screenPos;
	//	if (WorldToScreen(pDevice, &pos, &screenPos)) {
	//		RECT x = { screenPos.x, screenPos.y, screenPos.x + 0.1, screenPos.y + 0.1};
	//		pFont->DrawText(NULL, "Entity", -1, &x, DT_LEFT | DT_NOCLIP, D3DCOLOR_XRGB(0, 0, 0));
	//	}

	//	int baseAddress = 0x04408D84;
	//	int size = 0xB8;
	//	for (int i = 0; i < 32; i++) {
	//		int addr = (baseAddress)+(i * size);
	//		if (IsValidVec3(addr)) {
	//			float* x = (float*)addr;
	//			float* y = (float*)(addr + 4);
	//			float* z = (float*)(addr + 8);
	//			char bone_name[100];
	//			sprintf_s(bone_name, "B%d,X=%f,Y=%f,Z=%f", i, *x, *y, *z);
	//			DrawBone(pDevice, pFont, addr, bone_name);
	//		}
	//	}
	//}

	//// Release the font
	//pFont->Release();
}

void HookPreCreateDevice(D3DPRESENT_PARAMETERS *pPresentParams) {
	printf("PreCreateDevice\n");
	//pPresentParams->BackBufferWidth = 1920;
	//pPresentParams->BackBufferHeight = 1080;
	//pPresentParams->BackBufferFormat = D3DFMT_X8R8G8B8;
	//pPresentParams->Windowed = TRUE;

	//SetWindowLongPtr(pPresentParams->hDeviceWindow, GWL_STYLE, WS_POPUP);
	//SetWindowPos(pPresentParams->hDeviceWindow, HWND_TOP, 0, 0, 1920, 1080, SWP_NOZORDER | SWP_SHOWWINDOW);

	//if (pPresentParams->hDeviceWindow != NULL)
		//SetWindowSubclass(pPresentParams->hDeviceWindow, SubclassWindowProc, (UINT_PTR)0, (DWORD_PTR)0);
}

void HookPostCreateDevice(IDirect3DDevice9 *pDevice) {

}