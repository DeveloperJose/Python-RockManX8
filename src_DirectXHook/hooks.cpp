#include "stdafx.h"
#include "hooks.h"

void HookEndScene(IDirect3DDevice8 *pDevice) {
	//ID3DXFont *pFont = NULL;
	//HFONT font = CreateFont(48, 0, 0, 0, FW_NORMAL, FALSE, FALSE, FALSE, DEFAULT_CHARSET, OUT_DEFAULT_PRECIS, CLIP_DEFAULT_PRECIS, DEFAULT_QUALITY, FF_DONTCARE, "Comic Sans MS");
	//LOGFONT log_font = {
	//	32, //height
	//	0,  //width; 
	//	0,  // lfEscapement; 
	//	0,  //lfOrientation; 
	//	FW_BOLD, // lfWeight; 
	//	FALSE, // lfItalic; 
	//	FALSE, // lfUnderline; 
	//	FALSE, // lfStrikeOut; 
	//	DEFAULT_CHARSET, // lfCharSet; 
	//	OUT_DEFAULT_PRECIS, //lfOutPrecision; 
	//	CLIP_DEFAULT_PRECIS, // lfClipPrecision; 
	//	ANTIALIASED_QUALITY,// lfQuality; 
	//	DEFAULT_PITCH,// lfPitchAndFamily; 
	//	"Arial"// lfFaceName[LF_FACESIZE]; 
	//};

	//D3DXCreateFontIndirect(pDevice, &log_font, &pFont);

	//RECT rc = { 5, 5, 0, 0 };
	//pFont->Begin();
	//pFont->DrawText("Hello world", -1, &rc, DT_LEFT, D3DCOLOR_XRGB(220, 0, 0, 0));
	//pFont->End();
	D3DRECT backgroundRect = { 1, 1, 400 /*width*/, 80 /*height*/ };

	D3DRECT borderRect = { backgroundRect.x1 - 1,
						   backgroundRect.y1 - 1,
						   backgroundRect.x2 + 1,
						   backgroundRect.y2 + 1 };
	pDevice->Clear(1, &borderRect, D3DCLEAR_TARGET, D3DCOLOR_XRGB(255, 0, 0), 0, 0);
	pDevice->Clear(1, &backgroundRect, D3DCLEAR_TARGET, D3DCOLOR_XRGB(0, 0, 0), 0, 0);

	HRESULT r = 0;


	// Get a handle for the font to use
	const char* str = "Hello";
	HFONT hFont = (HFONT)GetStockObject(SYSTEM_FONT);
	LPD3DXFONT pFont = 0;

	// Create the D3DX Font
	r = D3DXCreateFont(pDevice, hFont, &pFont);

	if (FAILED(r)) {
		MessageBoxA(0, "Font failure", "Info", MB_ICONINFORMATION | MB_OK);
		return;
	}

	// Rectangle where the text will be located
	RECT TextRect = { 5,5,0,0 };

	// Inform font it is about to be used
	pFont->Begin();

	// Calculate the rectangle the text will occupy
	pFont->DrawText(str, -1, &TextRect, DT_CALCRECT, 0);

	// Output the text, left aligned
	pFont->DrawText(str, -1, &TextRect, DT_LEFT, D3DCOLOR_XRGB(255, 0, 0));

	// Finish up drawing
	pFont->End();


	// Release the font
	pFont->Release();
}
void HookCreateDevice(D3DPRESENT_PARAMETERS *pPresentParams) {

}
