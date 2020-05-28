#include "stdafx.h"

#include "w_d3d9.h"
#include "hooks.h"

LRESULT CALLBACK SubclassWindowProc(HWND hWnd, UINT uMsg, WPARAM wParam, LPARAM lParam, UINT_PTR uIdSubclass, DWORD_PTR dwRefData)
{
	switch (uMsg) {

	case WM_KEYDOWN:
	{
		if (wParam == VK_NUMPAD0) {
			printf("numpad0");
			/*extern myIDirect3DDevice8* gl_pmyIDirect3DDevice8;
			
			RECT R = { 0, 0, 800, 600 };
			AdjustWindowRect(&R, WS_OVERLAPPEDWINDOW, false);
			D3DPRESENT_PARAMETERS pp;
			memset(&pp, 0, sizeof(D3DPRESENT_PARAMETERS));
			pp.BackBufferWidth = 800;
			pp.BackBufferHeight = 600;
			pp.BackBufferFormat = D3DFMT_A8R8G8B8;
			pp.BackBufferCount = 1;
			pp.MultiSampleType = D3DMULTISAMPLE_NONE;
			pp.Windowed = true;

			SetWindowLongPtr(hWnd, GWL_STYLE, WS_POPUP);
			SetWindowPos(hWnd, HWND_TOP, 0, 0, 800, 600, SWP_NOZORDER | SWP_SHOWWINDOW);
			HRESULT hr = gl_pmyIDirect3DDevice8->Reset(&pp);
			if (FAILED(hr)) {
				char pString[128];
				D3DXGetErrorString(hr, pString, 128);
				printf("Err? : %s - ", pString);
				printf("Device ptr: %d", gl_pmyIDirect3DDevice8);
			}

			D3DVIEWPORT8 viewData;
			memset(&viewData, 0, sizeof(D3DVIEWPORT8));
			viewData.X = 0;
			viewData.Y = 0;
			viewData.Width = 800;
			viewData.Height = 600;
			viewData.MinZ = 0.0f;
			viewData.MaxZ = 1.0f;
			hr = gl_pmyIDirect3DDevice8->SetViewport(&viewData);
			
			if (FAILED(hr)) {
				printf("Device ptr: %d", gl_pmyIDirect3DDevice8);
				printf("[SubclassWindowProc] Could not SetViewport: [%d]\n", hr);
			}*/
		}
	}
	break;

	case WM_KEYUP:
	{
	}
	break;
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
	pDevice->Clear(1, &borderRect, D3DCLEAR_TARGET, D3DCOLOR_XRGB(255, 0, 0), 0, 0);
	pDevice->Clear(1, &backgroundRect, D3DCLEAR_TARGET, D3DCOLOR_XRGB(0, 0, 0), 0, 0);

	HRESULT r = 0;

	// Create the D3DX Font
	ID3DXFont *pFont;
	r = D3DXCreateFont(pDevice, 72 /*Font size*/, 0 /*Font width*/, FW_BOLD, 1, FALSE, DEFAULT_CHARSET, OUT_DEFAULT_PRECIS, 0, DEFAULT_PITCH | FF_DONTCARE, "Comic Sans MS", &pFont);

	if (FAILED(r)) {
		MessageBoxA(0, "Font failure", "Info", MB_ICONINFORMATION | MB_OK);
		return;
	}

	// Rectangle where the text will be located
	RECT TextRect = { 15,15,0,0 };

	// Calculate the rectangle the text will occupy
	pFont->DrawText(NULL, "Hello World", -1, &TextRect, DT_LEFT|DT_NOCLIP, D3DCOLOR_XRGB(220, 0, 0));

	// Release the font
	pFont->Release();
}
void HookPreCreateDevice(D3DPRESENT_PARAMETERS *pPresentParams) {
	pPresentParams->BackBufferWidth = 1920;
	pPresentParams->BackBufferHeight = 1080;
	pPresentParams->BackBufferFormat = D3DFMT_X8R8G8B8;
	pPresentParams->Windowed = TRUE;

	SetWindowLongPtr(pPresentParams->hDeviceWindow, GWL_STYLE, WS_POPUP);
	SetWindowPos(pPresentParams->hDeviceWindow, HWND_TOP, 0, 0, 1920, 1080, SWP_NOZORDER | SWP_SHOWWINDOW);

	if (pPresentParams->hDeviceWindow != NULL)
		SetWindowSubclass(pPresentParams->hDeviceWindow, SubclassWindowProc, (UINT_PTR)0, (DWORD_PTR)0);
}

void HookPostCreateDevice(IDirect3DDevice9 *pDevice) {

}