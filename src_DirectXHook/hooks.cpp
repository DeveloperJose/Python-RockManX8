#include "stdafx.h"

#include "w_d3d9.h"
#include "hooks.h"

int playerPauseAddress = 0x0428DDB0;
int enemyPauseAddress = 0x0428DB88;
int coordBaseAddress = 0x045C284C;
int cordStructLength = 0x47C;

int* enemyPause = (int*)enemyPauseAddress;
int* playerPause = (int*)playerPauseAddress;

int currentObjectID = 0;
int editingMode = 0;
int debug = 0;

struct vec3_t {
	float x, y, z;
};

struct vec2 {
	float x, y;
};

struct vec4 {
	float x, y, z, w;
};

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

float* GetCurrObjectXPtr() {
	int xAddress = coordBaseAddress + (currentObjectID * cordStructLength);
	return (float *)(xAddress);
}

float* GetCurrObjectYPtr() {
	int xAddress = coordBaseAddress + (currentObjectID * cordStructLength);
	int yAddress = xAddress + 4;
	return (float *)(yAddress);
}

float * GetCurrObjectZPtr() {
	int xAddress = coordBaseAddress + (currentObjectID * cordStructLength);
	int yAddress = xAddress + 4;
	int zAddress = yAddress + 4;
	return (float *)(zAddress);
}

void ToggleEditingMode() {
	if (editingMode) {
		editingMode = 0;
		*enemyPause = 0;
	}
	else {
		editingMode = 1;
		*enemyPause = 1;
	}
}

void SyncPlayer() {
	if (currentObjectID > 1) {
		float* objectXPtr = GetCurrObjectXPtr();
		float* objectYPtr = GetCurrObjectYPtr();
		float* objectZPtr = GetCurrObjectZPtr();
		float x = *objectXPtr;
		float y = *objectYPtr;
		float z = *objectZPtr;
		int oldObjectID = currentObjectID;

		printf("Object: %f, %f, %f\n", x, y, z);

		*playerPause = 1;
		currentObjectID = 0;
		*(GetCurrObjectXPtr()) = x;
		*(GetCurrObjectYPtr()) = y;
		*(GetCurrObjectZPtr()) = z;

		currentObjectID = 1;
		*(GetCurrObjectXPtr()) = x;
		*(GetCurrObjectYPtr()) = y;
		*(GetCurrObjectZPtr()) = z;

		currentObjectID = oldObjectID;
	}
}

LRESULT CALLBACK SubclassWindowProc(HWND hWnd, UINT uMsg, WPARAM wParam, LPARAM lParam, UINT_PTR uIdSubclass, DWORD_PTR dwRefData)
{
	float xChange = 0;
	float yChange = 0;
	float zChange = 0;
	switch (uMsg) {
	case WM_KEYDOWN:
	{
		if (wParam == VK_NUMPAD7) {
			ToggleEditingMode();
		}

		if (editingMode) {
			if (wParam == VK_ADD) {
				currentObjectID++;
			}
			else if (wParam == VK_SUBTRACT) {
				currentObjectID--;
				if (currentObjectID < 0)
					currentObjectID = 0;
			}
			else if (wParam == VK_NUMPAD4)
				xChange = -0.5;
			else if (wParam == VK_NUMPAD6)
				xChange = 0.5;
			else if (wParam == VK_NUMPAD8)
				yChange = 0.5;
			else if (wParam == VK_NUMPAD2)
				yChange = -0.5;
			else if (wParam == VK_NUMPAD1)
				zChange = -0.5;
			else if (wParam == VK_NUMPAD3)
				zChange = 0.5;
		}
	}
	break;

	case WM_KEYUP:
	{
	}
	break;
	}

	if (xChange != 0) {
		*(GetCurrObjectXPtr()) += xChange;
		xChange = 0;
	}

	if (yChange != 0) {
		*(GetCurrObjectYPtr()) += yChange;
		yChange = 0;
	}

	if (zChange != 0) {
		*(GetCurrObjectZPtr()) += zChange;
		zChange = 0;
	}

	// Pass messages onto the main proc
	return DefSubclassProc(hWnd, uMsg, wParam, lParam);
}


void HookEndScene(IDirect3DDevice9 *pDevice) {
	D3DRECT backgroundRect = { 1, 1, 400 /*width*/, 80 /*height*/ };

	D3DRECT borderRect = { backgroundRect.x1 - 1,
						   backgroundRect.y1 - 1,
						   backgroundRect.x2 + 1,
						   backgroundRect.y2 + 1 };
	//pDevice->Clear(1, &borderRect, D3DCLEAR_TARGET, D3DCOLOR_XRGB(255, 0, 0), 0, 0);
	//pDevice->Clear(1, &backgroundRect, D3DCLEAR_TARGET, D3DCOLOR_XRGB(0, 0, 0), 0, 0);

	HRESULT r = 0;

	// Create the D3DX Font
	ID3DXFont *pFont;
	r = D3DXCreateFont(pDevice, 36 /*Font size*/, 0 /*Font width*/, FW_BOLD, 1, FALSE, DEFAULT_CHARSET, OUT_DEFAULT_PRECIS, 0, DEFAULT_PITCH | FF_DONTCARE, "Comic Sans MS", &pFont);

	if (FAILED(r)) {
		MessageBoxA(0, "Font failure", "Info", MB_ICONINFORMATION | MB_OK);
		return;
	}

	// Rectangle where the text will be located
	RECT TextRect = { 15, 200, 0, 0 };

	// Calculate the rectangle the text will occupy
	if (editingMode) {
		char formatted_string[100];
		const char * entityName = NULL;
		if (currentObjectID == 0)
			entityName = "Player 1";
		else if (currentObjectID == 1)
			entityName = "Player 2";

		if (entityName == NULL)
			sprintf_s(formatted_string, "Entity: %d,X=%f,Y=%f,Z=%f,ptr=%u", currentObjectID, *GetCurrObjectXPtr(), *GetCurrObjectYPtr(), *GetCurrObjectZPtr(), coordBaseAddress + (currentObjectID * cordStructLength));
		else
			sprintf_s(formatted_string, "Entity: %s,X=%f,Y=%f,Z=%f,ptr=%u", entityName, *GetCurrObjectXPtr(), *GetCurrObjectYPtr(), *GetCurrObjectZPtr(), coordBaseAddress + (currentObjectID * cordStructLength));

		pFont->DrawText(NULL, formatted_string, -1, &TextRect, DT_LEFT | DT_NOCLIP, D3DCOLOR_XRGB(0, 158, 255));
	
		D3DXVECTOR3 pos = { *GetCurrObjectXPtr(), *GetCurrObjectYPtr(), *GetCurrObjectZPtr() };
		D3DXVECTOR3 screenPos;
		if (WorldToScreen(pDevice, &pos, &screenPos)) {
			//do stuff here
			//screenPos.x , screenPos.y
			RECT x = { screenPos.x, screenPos.y, screenPos.x + 5, screenPos.y + 5};
			pFont->DrawTextA(NULL, "YYY", -1, &x, DT_LEFT | DT_NOCLIP, D3DCOLOR_XRGB(0, 158, 255));
		}
	}

	// Release the font
	pFont->Release();
}
void HookPreCreateDevice(D3DPRESENT_PARAMETERS *pPresentParams) {
	//pPresentParams->BackBufferWidth = 1920;
	//pPresentParams->BackBufferHeight = 1080;
	//pPresentParams->BackBufferFormat = D3DFMT_X8R8G8B8;
	//pPresentParams->Windowed = TRUE;

	//SetWindowLongPtr(pPresentParams->hDeviceWindow, GWL_STYLE, WS_POPUP);
	//SetWindowPos(pPresentParams->hDeviceWindow, HWND_TOP, 0, 0, 1920, 1080, SWP_NOZORDER | SWP_SHOWWINDOW);

	if (pPresentParams->hDeviceWindow != NULL)
		SetWindowSubclass(pPresentParams->hDeviceWindow, SubclassWindowProc, (UINT_PTR)0, (DWORD_PTR)0);
}

void HookPostCreateDevice(IDirect3DDevice9 *pDevice) {

}