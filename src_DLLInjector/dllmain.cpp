// Standard
#include <string>
#include <iostream>
#include <unordered_map>
#include <windows.h>

// DX9
#include <d3d9.h>
//#include <Psapi.h>
#pragma comment(lib, "d3d9.lib")
//#pragma comment(lib, "Psapi.lib")

// DX10
#include "include/kiero/kiero.h"
//#include <d3d10.h>

// DX11
//#include <d3d11.h>
//#include <d3dcompiler.h>
//#pragma comment(lib, "d3dcompiler.lib")
//#pragma comment(lib, "d3d11.lib")

// ImGUI
#include "include/imgui/imgui.h"
#include "include/imgui/backends/imgui_impl_win32.h"
#include "include/imgui/backends/imgui_impl_dx9.h"

// MinHook
#include "include/minhook/MinHook.h"
#pragma comment(lib, "libMinHook.x86.lib")

// Detours
#include <detours.h>
#pragma comment(lib, "detours.lib")

// Project
#include "stdafx.h"
#include "set.h"

// *********************************************** DLL stuff ***********************************************
DWORD WINAPI Main(LPVOID);
DWORD g_threadID;
HMODULE g_hModule;

static WNDPROC oWndProc = NULL;

extern IMGUI_IMPL_API LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);

LRESULT CALLBACK hkWindowProc(
	_In_ HWND   hwnd,
	_In_ UINT   uMsg,
	_In_ WPARAM wParam,
	_In_ LPARAM lParam
)
{
	if (ImGui_ImplWin32_WndProcHandler(hwnd, uMsg, wParam, lParam) > 0)
		return 1L;
	return ::CallWindowProcA(oWndProc, hwnd, uMsg, wParam, lParam);
}

void showExampleWindow(const char* comment)
{
	char buffer[128];
	::memset(buffer, 0, 128);
	::sprintf_s(buffer, "Kiero Dear ImGui Example (%s)", comment);

	ImGui::Begin(buffer);

	ImGui::Text("Hello");
	ImGui::Button("World!");

	ImGui::End();
}

typedef long(__stdcall* EndScene)(LPDIRECT3DDEVICE9);
static EndScene oEndScene = NULL;

long __stdcall hkEndScene(LPDIRECT3DDEVICE9 pDevice)
{
	static bool init = false;

	if (!init)
	{
		D3DDEVICE_CREATION_PARAMETERS params;
		pDevice->GetCreationParameters(&params);

		oWndProc = (WNDPROC)::SetWindowLongPtr((HWND)params.hFocusWindow, GWLP_WNDPROC, (LONG)hkWindowProc);

		ImGui::CreateContext();
		ImGui_ImplWin32_Init(params.hFocusWindow);
		ImGui_ImplDX9_Init(pDevice);

		init = true;
	}

	ImGui_ImplDX9_NewFrame();
	ImGui_ImplWin32_NewFrame();
	ImGui::NewFrame();

	showExampleWindow("D3D9");

	ImGui::EndFrame();
	ImGui::Render();
	ImGui_ImplDX9_RenderDrawData(ImGui::GetDrawData());

	return oEndScene(pDevice);
}


// *********************************************** d3d10 ***********************************************
//typedef long(__stdcall* Present)(IDXGISwapChain*, UINT, UINT);
//static Present OriginalD3D10Present = NULL;
//
//long __stdcall MyD3D10Present(IDXGISwapChain* pSwapChain, UINT SyncInterval, UINT Flags)
//{
//	return OriginalD3D10Present(pSwapChain, SyncInterval, Flags);
//}

// *********************************************** d3d11 hooking ***********************************************
// https://niemand.com.ar/2019/01/01/how-to-hook-directx-11-imgui/
// https://www.mpgh.net/forum/showthread.php?t=1313252
//typedef HRESULT(__stdcall* D3D11PresentHook) (IDXGISwapChain* pSwapChain, UINT SyncInterval, UINT Flags);
//D3D11PresentHook OriginalSwapChainPresent = NULL;
//
//ID3D11Device* pDevice = NULL;
//ID3D11DeviceContext* pContext = NULL;
//
//DWORD_PTR* pSwapChainVtable = NULL;
//DWORD_PTR* pContextVTable = NULL;
//DWORD_PTR* pDeviceVTable = NULL;
//
//ID3D11Texture2D* RenderTargetTexture;
//ID3D11RenderTargetView* RenderTargetView = NULL;
//
//LRESULT CALLBACK DXGIMsgProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) { return DefWindowProc(hwnd, uMsg, wParam, lParam); }
//const int MultisampleCount = 1; // Set to 1 to disable multisampling
//// Definition of WndProc Hook. Its here to avoid dragging dependencies on <windows.h> types.
//extern LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);
//BOOL first_time = true;
//bool g_ShowMenu = false;
////static IDXGISwapChain* pSwapChain = NULL;
//static WNDPROC OriginalWndProcHandler = nullptr;
//HWND window = nullptr;
//
//
//LRESULT CALLBACK hWndProc(HWND hWnd, UINT uMsg, WPARAM wParam, LPARAM lParam)
//{
//	ImGuiIO& io = ImGui::GetIO();
//	POINT mPos;
//	GetCursorPos(&mPos);
//	ScreenToClient(window, &mPos);
//	ImGui::GetIO().MousePos.x = mPos.x;
//	ImGui::GetIO().MousePos.y = mPos.y;
//
//	if (uMsg == WM_KEYUP)
//	{
//		if (wParam == VK_DELETE)
//		{
//			g_ShowMenu = !g_ShowMenu;
//		}
//
//	}
//
//	if (g_ShowMenu)
//	{
//		ImGui_ImplWin32_WndProcHandler(hWnd, uMsg, wParam, lParam);
//		return true;
//	}
//
//	return CallWindowProc(OriginalWndProcHandler, hWnd, uMsg, wParam, lParam);
//}
//
//
//HRESULT __stdcall MyPresent(IDXGISwapChain* pSwapChain, UINT SyncInterval, UINT Flags)
//{
//	/*if (first_time) {
//		printf("Present hook set-up\n");
//		if (SUCCEEDED(pSwapChain->GetDevice(__uuidof(ID3D11Device), (void**)&pDevice)))
//		{
//			printf("Inside\n");
//			pSwapChain->GetDevice(__uuidof(pDevice), (void**)&pDevice);
//			pDevice->GetImmediateContext(&pContext);
//
//			// use the back buffer address to create the render target
//			//if (SUCCEEDED(pSwapChain->GetBuffer(0, __uuidof(ID3D11Texture2D), reinterpret_cast<LPVOID*>(&RenderTargetTexture))))
//			if (SUCCEEDED(pSwapChain->GetBuffer(0, __uuidof(ID3D11Texture2D), (LPVOID*)&RenderTargetTexture)))
//			{
//				printf("Target\n");
//				pDevice->CreateRenderTargetView(RenderTargetTexture, NULL, &RenderTargetView);
//				RenderTargetTexture->Release();
//			}
//
//			printf("Completed\n");
//		}
//		else {
//			printf("Failed?\n");
//		}
//		first_time = false;
//	}*/
//	
//	return OriginalSwapChainPresent(pSwapChain, SyncInterval, Flags);
//	//if (!g_bInitialised) {
//	//	
//
//	//	printf("swap1\n");
//	//	DXGI_SWAP_CHAIN_DESC sd;
//	//	pSwapChain->GetDesc(&sd);
//
//	//	printf("imgui1\n");
//	//	ImGui::CreateContext();
//	//	ImGuiIO& io = ImGui::GetIO(); (void)io;
//	//	io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard;
//	//	window = sd.OutputWindow;
//
//	//	printf("orig\n");
//	//	//Set OriginalWndProcHandler to the Address of the Original WndProc function
//	//	OriginalWndProcHandler = (WNDPROC)SetWindowLongPtr(window, GWLP_WNDPROC, (LONG_PTR)hWndProc);
//
//	//	printf("imgui2\n");
//	//	ImGui_ImplWin32_Init(window);
//	//	ImGui_ImplDX11_Init(pDevice, pContext);
//	//	ImGui::GetIO().ImeWindowHandle = window;
//
//	//	printf("buffer\n");
//	//	ID3D11Texture2D* pBackBuffer;
//	//	pSwapChain->GetBuffer(0, __uuidof(ID3D11Texture2D), (LPVOID*)&pBackBuffer);
//	//	pDevice->CreateRenderTargetView(pBackBuffer, NULL, &mainRenderTargetView);
//	//	pBackBuffer->Release();
//
//	//	g_bInitialised = true;
//	//}
//	//ImGui_ImplWin32_NewFrame();
//	//ImGui_ImplDX11_NewFrame();
//
//	//ImGui::NewFrame();
//	////Menu is displayed when g_ShowMenu is TRUE
//	//if (g_ShowMenu)
//	//{
//	//	bool bShow = true;
//	//	ImGui::ShowDemoWindow(&bShow);
//	//}
//	//ImGui::EndFrame();
//
//	//ImGui::Render();
//
//	//pContext->OMSetRenderTargets(1, &mainRenderTargetView, NULL);
//	//ImGui_ImplDX11_RenderDrawData(ImGui::GetDrawData());
//
//	//return OriginalSwapChainPresent(pSwapChain, SyncInterval, Flags);
//}
//
//
//int HookD3D11() {
//	printf("Hooking D3D11 \n");
//	HMODULE hDXGIDLL = 0;
//	do
//	{
//		hDXGIDLL = GetModuleHandleA("dxgi.dll");
//		Sleep(10);
//	} while (!hDXGIDLL);
//
//	IDXGISwapChain* pSwapChain;
//
//	WNDCLASSEXA wc = { sizeof(WNDCLASSEX), CS_CLASSDC, DXGIMsgProc, 0L, 0L, GetModuleHandleA(NULL), NULL, NULL, NULL, NULL, "DX", NULL };
//	RegisterClassExA(&wc);
//	HWND hWnd = CreateWindowA("DX", NULL, WS_OVERLAPPEDWINDOW, 100, 100, 300, 300, NULL, NULL, wc.hInstance, NULL);
//
//	D3D_FEATURE_LEVEL requestedLevels[] = { D3D_FEATURE_LEVEL_11_0, D3D_FEATURE_LEVEL_10_1 };
//	D3D_FEATURE_LEVEL obtainedLevel;
//	ID3D11Device* d3dDevice = nullptr;
//	ID3D11DeviceContext* d3dContext = nullptr;
//
//	DXGI_SWAP_CHAIN_DESC scd;
//	ZeroMemory(&scd, sizeof(scd));
//	scd.BufferCount = 1;
//	scd.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM;
//	scd.BufferDesc.Scaling = DXGI_MODE_SCALING_UNSPECIFIED;
//	scd.BufferDesc.ScanlineOrdering = DXGI_MODE_SCANLINE_ORDER_UNSPECIFIED;
//	scd.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;
//
//	scd.Flags = DXGI_SWAP_CHAIN_FLAG_ALLOW_MODE_SWITCH;
//	scd.OutputWindow = hWnd;
//	scd.SampleDesc.Count = MultisampleCount;
//	scd.SwapEffect = DXGI_SWAP_EFFECT_DISCARD;
//	scd.Windowed = ((GetWindowLongPtr(hWnd, GWL_STYLE) & WS_POPUP) != 0) ? false : true;
//
//	// LibOVR 0.4.3 requires that the width and height for the backbuffer is set even if
//	// you use windowed mode, despite being optional according to the D3D11 documentation.
//	scd.BufferDesc.Width = 1;
//	scd.BufferDesc.Height = 1;
//	scd.BufferDesc.RefreshRate.Numerator = 0;
//	scd.BufferDesc.RefreshRate.Denominator = 1;
//
//	UINT createFlags = 0;
//	// This flag gives you some quite wonderful debug text. Not wonderful for performance, though!
//	createFlags |= D3D11_CREATE_DEVICE_DEBUG;
//
//	printf("Creating swapchain\n");
//	IDXGISwapChain* d3dSwapChain = 0;
//	if (FAILED(D3D11CreateDeviceAndSwapChain(
//		nullptr,
//		D3D_DRIVER_TYPE_HARDWARE,
//		nullptr,
//		createFlags,
//		requestedLevels,
//		sizeof(requestedLevels) / sizeof(D3D_FEATURE_LEVEL),
//		D3D11_SDK_VERSION,
//		&scd,
//		&pSwapChain,
//		&pDevice,
//		&obtainedLevel,
//		&pContext)))
//	{
//		MessageBoxA(hWnd, "Failed to create directX device and swapchain!", "Error", MB_ICONERROR);
//		return 1;
//	}
//
//	pSwapChainVtable = (DWORD_PTR*)pSwapChain;
//	pSwapChainVtable = (DWORD_PTR*)pSwapChainVtable[0];
//
//	pContextVTable = (DWORD_PTR*)pContext;
//	pContextVTable = (DWORD_PTR*)pContextVTable[0];
//
//	pDeviceVTable = (DWORD_PTR*)pDevice;
//	pDeviceVTable = (DWORD_PTR*)pDeviceVTable[0];
//
//	/*OriginalSwapChainPresent = (DWORD_PTR*)pSwapChainVtable[8]; //(HRESULT(__stdcall*)(IDXGISwapChain*, UINT, UINT))pSwapChainVtable[8];
//
//	printf("Detouring... %x\n", (uintptr_t)pSwapChainVtable[8]);
//	DetourTransactionBegin();
//	DetourUpdateThread(GetCurrentThread());
//	DetourAttach(&(PVOID&)OriginalSwapChainPresent, MyPresent);
//	DetourTransactionCommit();*/
//
//	if (MH_Initialize() != MH_OK) { return 1; }
//	if (MH_CreateHook((DWORD_PTR*)pSwapChainVtable[8], MyPresent, reinterpret_cast<void**>(&OriginalSwapChainPresent)) != MH_OK) { return 1; }
//	if (MH_EnableHook((DWORD_PTR*)pSwapChainVtable[8]) != MH_OK) { return 1; }
//
//	printf("VirtualProtect\n");
//	DWORD dwOld;
//	//VirtualProtect(OriginalSwapChainPresent, 2, PAGE_EXECUTE_READWRITE, &dwOld);
//	return 0;
//}
//
//// *********************************************** d3d9 hooking ***********************************************
//// https://www.unknowncheats.me/forum/direct3d/336201-help-hooking-endscene.html
//signed int __stdcall hkEndScene(LPDIRECT3DDEVICE9 Device);
//typedef HRESULT(__stdcall* EndScene_t)(LPDIRECT3DDEVICE9);
//EndScene_t OrigEndScene;
//
//HRESULT __stdcall myEndScene(LPDIRECT3DDEVICE9 Device)
//{
//	/* endscene  here */
//	return OrigEndScene(Device);
//}
//
//
//bool bCompare(const BYTE* pData, const BYTE* bMask, const char* szMask)
//{
//	for (; *szMask; ++szMask, ++pData, ++bMask)
//		if (*szMask == 'x' && *pData != *bMask)
//			return false;
//
//	return (*szMask) == NULL;
//}
//
//DWORD FindPattern(DWORD dwAddress, DWORD dwLen, BYTE* bMask, const char* szMask)
//{
//	for (DWORD i = 0; i < dwLen; i++)
//		if (bCompare((BYTE*)(dwAddress + i), bMask, szMask))
//			return (DWORD)(dwAddress + i);
//
//	return 0;
//}
//
//void HookD3D9()
//{
//	DWORD* vtbl;
//
//	// wait for the d3dx dll
//	DWORD hD3D = 0;
//	do {
//		hD3D = (DWORD)GetModuleHandleA("d3d9.dll");
//		Sleep(10);
//	} while (!hD3D);
//	DWORD adre = FindPattern(hD3D, 0x128000, (PBYTE)"\xC7\x06\x00\x00\x00\x00\x89\x86\x00\x00\x00\x00\x89\x86", "xx????xx????xx");
//
//	if (adre)
//	{
//		memcpy(&vtbl, (void*)(adre + 2), 4);
//
//		//ms detours 1.5
//		//OrigEndScene = (EndScene_t)DetourFunction((BYTE*)vtbl[42], (BYTE*)myEndScene);
//
//		//ms detours 3.0
//		OrigEndScene = (HRESULT(__stdcall*)(LPDIRECT3DDEVICE9))vtbl[42];
//
//		DetourTransactionBegin();
//		DetourUpdateThread(GetCurrentThread());
//		DetourAttach(&(PVOID&)OrigEndScene, myEndScene);
//		DetourTransactionCommit();
//	}
//}

// *********************************************** Detours ***********************************************
typedef int(__stdcall* Enemy_Load)(int32_t param1, int32_t param2, int32_t param3, int32_t param4, int32_t* param5, int32_t param6);
Enemy_Load TrueEnemyLoad = ((Enemy_Load)0x027e3d00);

//int(__cdecl* TrueEnemyLoad)(int param1, int param2, int param3, int param4, int param5, int param6);
int32_t dw_esi = 0;
std::unordered_map<SetEnemyParent*, CEnemy*> enemy_map;
int __stdcall Hooked_Enemy_Load_Fn(int32_t param1, int32_t param2, int32_t param3, int32_t param4, int32_t* param5, int32_t param6) {
	// Save ESI to dw_esi
	_asm {
		mov dw_esi, esi;
	}
	
	// Run original load function
	int caddr = TrueEnemyLoad(param1, param2, param3, param4, param5, param6);
	
	// Check if an enemy was loaded
	CEnemy* c_enemy = (CEnemy*)caddr;
	printf("ESI = %x and caddr = %x | c_enemy=%s\n", dw_esi, caddr, c_enemy->type); // p1=%x, p4=%x, p6=%x
	if (strcmp(c_enemy->type, "CEnemy") == 0 && dw_esi > (int32_t)base_addr) {
		// Map the SetEnemy parent to this CEnemy
		SetEnemyParent* set_enemy_parent = (SetEnemyParent*)dw_esi;
		enemy_map[set_enemy_parent] = c_enemy;
		
		// Debugging
		printf("CEnemy Loaded | %i enemies in map \n", enemy_map.size());
	}
	return caddr;
}

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

// *********************************************** Move Enemies Patch
const BYTE move_enemies_patch_asm[] = { 0x90, 0x90, 0x90, 0x90, 0x90 };
const BYTE move_enemies_orig_asm[] = { 0xF3, 0x0F, 0x11, 0x40, 0x70 };
const uintptr_t move_enemies_patch_ptr = 0x2439989;

// *********************************************** Load Enemy Patch
const BYTE load_patch_asm[] = { 0x90, 0x90, 0x90, 0x90, 0x90 };
const BYTE load_orig_asm[] = { 0xE8, 0xC9, 0x9E, 0x12, 0x00 };
const uintptr_t load_patch_ptr = 0x23FF7B2;

// *********************************************** Entities
Entity* entities = (Entity*)(base_addr + 0x42E1820);
Entity* player1 = (Entity*)(base_addr + 0x42E21A0);
Entity* player2 = (Entity*)(base_addr + 0x42E1950);

// *********************************************** Camera
float* camera_x = (float*)(base_addr + 0x43767C0);
float* camera_y = (float*)(base_addr + 0x43767C4);
float* camera_z = (float*)(base_addr + 0x43767C8);
float* camera_xx = (float*)(base_addr + 0x43767E0);
float* camera_yy = (float*)(base_addr + 0x43767E4);
float* camera_zz = (float*)(base_addr + 0x43767E8);

int CountActiveEntities() {
	int active = 0;
	for (int i = 0; i <= 200; ++i) {
		if (entities[i].Animations1 != 0)
			++active;
	}
	return active;
}

int FindClosestEntity(SetEnemy* enemy) {
	double best_distance = 1e10;
	int best_id = 0;
	//printf("Curr Enemy | X=%f\n", enemy->X);
	for (int i = 0; i <= 200; i++) {
		if (entities[i].Animations1 == 0 || &entities[i] == player1 || &entities[i] == player2)
			continue;

		double xdiff = (entities[i].X - enemy->x);
		double ydiff = (entities[i].Y - enemy->y);
		double zdiff = (entities[i].Z - enemy->z);
		double xx = xdiff * xdiff;
		double yy = ydiff * ydiff;
		double zz = zdiff * zdiff;
		double distance = xx + yy + zz;
		if (distance < best_distance) {
			best_distance = distance;
			//printf("Curr Best Entity | X=%f\n", entities[i].X);
			best_id = entities[i].ID;
		}
	}
	return best_id;
}
// *********************************************** Editor ***********************************************
SetFile* set_file = (SetFile*)(base_addr + 0x323F940);
SetEnemyParent* set_parents = (SetEnemyParent*)(base_addr + 0x322B030);
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
int selected_set_enemy_idx = 0;

CEnemy* selected_c_enemy = 0;
int selected_entity_idx = 0;

void MovePlayerToSetEnemy() {
	// Move player close to the coordinates the SetEnemy is supposed to be at
	SetEnemyParent* set_enemy_parent = &set_parents[selected_set_enemy_idx];
	SetEnemy* set_enemy = set_enemy_parent->set_enemy;
	for (int i = 0; i < 5; i++) {
		player1->X = set_enemy->x;
		player1->Y = set_enemy->y;
		player1->Z = set_enemy->z;
	}
	if (set_enemy_parent->is_active != 1) {
		printf("Trying to move player to an inactive enemy\n");
		return;
	}
	// Get the CEnemy that was last loaded
	selected_c_enemy = enemy_map[set_enemy_parent];
	selected_entity_idx = selected_c_enemy->entity_idx;
	//Sleep(250);

	// Hopefully by now the enemy has been loaded as an Entity. Let's look for it
	//selected_entity_idx = FindClosestEntity(set_enemy);
	// Entity* entity = &entities[selected_entity_idx];

	// Let's sync them a few times
	/*for (int i = 0; i < 10; i++) {
		player1->X = entities[selected_entity_idx].X;
		player1->Y = entities[selected_entity_idx].Y;
		player1->Z = entities[selected_entity_idx].Z;
		player1->Angle1 = entities[selected_entity_idx].Angle1;
		player1->Angle2 = entities[selected_entity_idx].Angle2;
		player1->Angle3 = entities[selected_entity_idx].Angle3;
		player1->Angle4 = entities[selected_entity_idx].Angle4;
		player1->Angle5 = entities[selected_entity_idx].Angle5;
		Sleep(5);
		//player1->Angle_BC = entities[selected_entity_idx].Angle_BC;
	}

	Sleep(5);*/
	printf("Current Entity = %x with ID = %i and coords (X=%f, Y=%f, Z=%f) | SetEnemy %s with IDX = %i and coords (X=%f, Y=%f, Z=%f, Angle=%f) | Player with coords (X=%f, Y=%f, Z=%f) | SetEnemyParent = %x, CEnemy = %x\n",
		(uintptr_t)(&entities[selected_entity_idx]), entities[selected_entity_idx].ID, entities[selected_entity_idx].X, entities[selected_entity_idx].Y, entities[selected_entity_idx].Z,
		set_enemy->prm_type, selected_set_enemy_idx, set_enemy->x, set_enemy->y, set_enemy->z, set_enemy->angle,
		player1->X, player1->Y, player1->Z,
		(uintptr_t)(&set_enemy_parent), (uintptr_t)(&selected_c_enemy)
	);
}

void ToggleEditMode() {
	is_editing = !is_editing;

	*pause_enemies = is_editing;
	*pause_exploding_boxes = is_editing;
	*pause_anims_and_interacts1 = is_editing;
	*pause_anims_and_interacts2 = is_editing;
	*pause_metals = is_editing;
	*pause_fog = is_editing;
	*hide_fog = is_editing;
	*hide_hp_ui = is_editing;

	Patch(no_grav_patch_ptr, is_editing ? no_grav_patch_asm : no_grav_original_asm, is_editing ? sizeof(no_grav_patch_asm) : sizeof(no_grav_original_asm));
	Patch(move_enemies_patch_ptr, is_editing ? move_enemies_patch_asm : move_enemies_orig_asm, is_editing ? sizeof(move_enemies_patch_asm) : sizeof(move_enemies_orig_asm));
}

void RefreshChanges() {
	/*player1->Y = 1000000000000.0f;
	ToggleEditMode();
	Sleep(15);
	ToggleEditMode();
	MovePlayerToSetEnemy();*/
	//Patch(load_patch_ptr, load_patch_asm, sizeof(load_patch_asm));
	/*SetEnemy* set_enemy = &set_file->enemies[selected_set_enemy_idx];
	selected_entity_idx = FindClosestEntity(set_enemy);
	Entity* entity = &entities[selected_entity_idx];
	entity->X = -1e10f;
	entity->Y = -1e10f;
	entity->Z = -1e10f;
	entity->NoCollision = 1;
	Sleep(10);*/
	//Patch(load_patch_ptr, load_orig_asm, sizeof(load_orig_asm));
}

// *********************************************** Main DLL Stuff ***********************************************
BOOL WINAPI DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)
{
	switch (ul_reason_for_call)
	{
	case DLL_PROCESS_ATTACH:
		g_hModule = hModule;
		DisableThreadLibraryCalls(hModule);
		CreateThread(NULL, NULL, &Main, NULL, NULL, &g_threadID);
		break;
	}
	return TRUE;
}

DWORD WINAPI Main(LPVOID lpParam)
{
	AllocConsole();
	freopen_s((FILE**)stdout, "CONOUT$", "w", stdout);
	freopen_s((FILE**)stdin, "CONIN$", "r", stdin);

	kiero::Status::Enum kiero_status = kiero::init(kiero::RenderType::D3D10);
	if (kiero_status == kiero::Status::Success) {
		printf("<Main> [Info] kiero was succesfully initialized, hooking\n");
		//assert(kiero::bind(8, (void**)&oPresent, hkPresent10) == kiero::Status::Success);
		assert(kiero::bind(42, (void**)&oEndScene, hkEndScene) == kiero::Status::Success);
	}
	else {
		printf("<Main> [Error] kiero could not initialize, error code = %i\n", kiero_status);
		return EXIT_FAILURE;
	}

	//int r = HookD3D11();

	// Menu
	printf("== Starting up Injector DLL3 ==\n");
	printf("Base Addr: %x\n", base_addr);

	printf("HotKeys:\n");
	printf("F1 - Exit\n");

	// Apply NoTab patch
	Patch(tab_patch_ptr, tab_patch_asm, sizeof(tab_patch_asm));
	has_tab_patch = true;
	printf("NoTab patch applied\n");

	// Detour enemy loading function
	LONG lError;
	DetourTransactionBegin();
	DetourUpdateThread(GetCurrentThread());
	DetourAttach(&(PVOID&)TrueEnemyLoad, Hooked_Enemy_Load_Fn);
	lError = DetourTransactionCommit();

	// Detour DX11
	/*DWORD_PTR hDxgi = (DWORD_PTR)GetModuleHandle((LPCWSTR)"dxgi.dll");
	fnIDXGISwapChainPresent = (IDXGISwapChainPresent)((DWORD_PTR)hDxgi + 0x5070);
	std::cout << "[+] Present Addr: " << std::hex << fnIDXGISwapChainPresent << std::endl;
	DetourTransactionBegin();
	DetourUpdateThread(GetCurrentThread());
	// Detours the original fnIDXGISwapChainPresent with our Present
	DetourAttach(&(LPVOID&)fnIDXGISwapChainPresent, (PBYTE)Present);
	DetourTransactionCommit();*/

	if (lError != NO_ERROR) {
		MessageBox(HWND_DESKTOP, L"Failed to detour enemy_load_fn", L"Error", MB_OK);
		return FALSE;
	}

	while (true)
	{
		if (GetAsyncKeyState(VK_F1) & 1)
			break;
		else if (GetAsyncKeyState(VK_F4) & 1) {
			/*printf("Enemies = %i\n", set_file->enemy_count);
			printf("E1 = %s\n", set_file->enemies[0].prm_type);
			printf("Entity0 = %i\n", entities[0].ID);
			printf("Entity5 = %i\n", entities[5].ID);
			printf("There are %i active entities\n", CountActiveEntities());*/

			SetEnemyParent* set_enemy_parent = &set_parents[selected_set_enemy_idx];
			char part[5];
			memcpy(part, set_enemy_parent->set_enemy->prm_type + 3, 4);
			part[4] = 0; // string terminator
			printf("%s", part);

			/*SetEnemy* current_enemy = &set_file->enemies[selected_enemy_idx];
			int entity_idx = FindClosestEntity(current_enemy);
			printf("Closest Entity = %x\n", entities[entity_idx]);*/
			//Entity* closest_entity = FindClosestEntity(current_enemy);
			//printf("Closest Entity = %x \n", &closest_entity);
			//printf("Closest Entity = %i | Set(X=%f, Y=%f, Z=%f) | Entity(X=%f, Y=%f, Z=%f)\n", closest_entity->ID, current_enemy->X, current_enemy->Y, current_enemy->Z, closest_entity->X, closest_entity->Y, closest_entity->Z);
			/*for (int i = 0; i <= 200; i++) {
				printf("(%i|an=%x|prev=%x|next=%x)\n", entities[i].ID, entities[i].Animations1, entities[i].Prev, entities[i].Next);
			}*/
		}
		else if (GetAsyncKeyState(VK_F5) & 1) {
			char newName[8];
			printf("Set the new prm_type\n");
			std::cin >> newName;
			SetEnemyParent* set_enemy_parent = &set_parents[selected_set_enemy_idx];
			strcpy_s(set_enemy_parent->set_enemy->prm_type, 8, newName);
		}
		else if (GetAsyncKeyState(VK_F7) & 1) {
			// Deactivate enemy entity
			selected_c_enemy->activated = 5;
			
			// Reload SetEnemy to create a new entity
			SetEnemyParent* set_enemy_parent = &set_parents[selected_set_enemy_idx];
			set_enemy_parent->is_active = 0;

			// Move player to re-create pointers when the enemy is re-loaded
			// TODO: Timer to avoid infinite loop
			while (set_enemy_parent->is_active != 1) {
				Sleep(5);
			}
			printf("Enemy finally re-loaded xd\n");
			MovePlayerToSetEnemy();
		}
		else if (GetAsyncKeyState(VK_F8) & 1) {
			ToggleEditMode();
			printf("Edit Mode = %d\n", is_editing);
		}
		else if (GetAsyncKeyState(VK_F9) & 1) {
			
		}
		else if (GetAsyncKeyState(VK_F6) & 1) {
			
		}

		if (is_editing) {
			if (GetAsyncKeyState(VK_ADD) & 1) {
				if (++selected_set_enemy_idx > set_file->enemy_count)
					selected_set_enemy_idx = set_file->enemy_count;

				MovePlayerToSetEnemy();
			}
			else if (GetAsyncKeyState(VK_SUBTRACT) & 1) {
				if (--selected_set_enemy_idx < 0)
					selected_set_enemy_idx = 0;

				MovePlayerToSetEnemy();
			}

			float delta = 0.01f;

			if (GetAsyncKeyState(VK_NUMPAD8) & 0x8000) {
				entities[selected_entity_idx].Y += delta;
				RefreshChanges();
			}
			if (GetAsyncKeyState(VK_NUMPAD6) & 0x8000) {
				entities[selected_entity_idx].X += delta;
				RefreshChanges();
			}
			if (GetAsyncKeyState(VK_NUMPAD4) & 0x8000) {
				entities[selected_entity_idx].X -= delta;
				RefreshChanges();
			}
			if (GetAsyncKeyState(VK_NUMPAD2) & 0x8000) {
				entities[selected_entity_idx].Y -= delta;
				RefreshChanges();
			}
			if (GetAsyncKeyState(VK_NUMPAD7) & 0x8000) {
				entities[selected_entity_idx].Z -= delta;
				RefreshChanges();
			}
			if (GetAsyncKeyState(VK_NUMPAD9) & 0x8000) {
				entities[selected_entity_idx].Z += delta;
				RefreshChanges();
			}
			if (GetAsyncKeyState(VK_NUMPAD1) & 0x8000) {
				//set_file->enemies[selected_set_enemy_idx].x -= delta;
				RefreshChanges();
			}
			if (GetAsyncKeyState(VK_NUMPAD3) & 0x8000) {
				//set_file->enemies[selected_set_enemy_idx].x += delta;
				RefreshChanges();
			}
		}
		else {
			float delta = 0.01f;
			if (GetAsyncKeyState(VK_NUMPAD8) & 0x8000) {
				*camera_y += delta;
			}
			if (GetAsyncKeyState(VK_NUMPAD6) & 0x8000) {
				*camera_x += delta;
			}
			if (GetAsyncKeyState(VK_NUMPAD4) & 0x8000) {
				*camera_x -= delta;
			}
			if (GetAsyncKeyState(VK_NUMPAD2) & 0x8000) {
				*camera_y -= delta;
			}
			if (GetAsyncKeyState(VK_NUMPAD7) & 0x8000) {
				*camera_z -= delta;
			}
			if (GetAsyncKeyState(VK_NUMPAD9) & 0x8000) {
				*camera_z += delta;
			}
			if (GetAsyncKeyState(VK_NUMPAD1) & 0x8000) {
				*camera_xx -= delta;
			}
			if (GetAsyncKeyState(VK_NUMPAD3) & 0x8000) {
				*camera_xx += delta;
			}
			if (GetAsyncKeyState(VK_OEM_4) & 0x8000) {
				*camera_yy -= delta;
			}
			if (GetAsyncKeyState(VK_OEM_6) & 0x8000) {
				*camera_yy += delta;
			}
			if (GetAsyncKeyState(VK_OEM_1) & 0x8000) {
				*camera_zz -= delta;
			}
			if (GetAsyncKeyState(VK_OEM_7) & 0x8000) {
				*camera_zz += delta;
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

		/*if (!has_cam_patch) {
				Patch(cam_patch_x_ptr, cam_patch_asm, sizeof(cam_patch_asm));
				Patch(cam_patch_y_ptr, cam_patch_asm, sizeof(cam_patch_asm));
				Patch(cam_patch_z_ptr, cam_patch_asm, sizeof(cam_patch_asm));
				has_cam_patch = true;
				printf("Cam Patch Applied\n");
			}*/
			
		//Entity* player2_ptr = (Entity*)0x046E1950;

		//// Look for prev
		//Entity* prev = player2_ptr->Prev;
		//Entity* prev_cpy = prev;
		//printf("1st Prev Addr = %x\n", (uintptr_t)prev);
		//int prev_count = 0;
		//while ((uintptr_t)prev > 0) {
		//	prev_cpy = prev;
		//	prev = prev->Prev;
		//	++prev_count;

		//	if (prev_count > 300) {
		//		printf("Counted more than 300 prevs, stopping just in case.\n");
		//		break;
		//	}
		//}

		//// Look for next
		//Entity* next = player2_ptr->Next;
		//Entity* next_cpy = next;
		//printf("1st Next Addr = %x\n", (uintptr_t)next);
		//int next_count = 0;
		//while ((uintptr_t)next > 0) {
		//	next_cpy = next;
		//	next = next->Next;
		//	++next_count;

		//	if (next_count > 300) {
		//		printf("Counted more than 300 prevs, stopping just in case.\n");
		//		break;
		//	}
		//}

		//printf("Prev Addr: %x | Total Prev Count = %i\n", (uintptr_t)prev, prev_count);
		//printf("Next Addr: %x | Total Next Count = %i\n", (uintptr_t)next, next_count);
		//printf("First Addr: %x | Last Addr: %x\n", (uintptr_t)prev_cpy, (uintptr_t)next_cpy);
		Sleep(5);
	}

	DetourTransactionBegin();
	DetourUpdateThread(GetCurrentThread());
	DetourDetach(&(PVOID&)TrueEnemyLoad, Hooked_Enemy_Load_Fn);
	lError = DetourTransactionCommit();

	if (lError != NO_ERROR) {
		MessageBox(HWND_DESKTOP, L"Failed to detach enemy_load_fn", L"Error", MB_OK);
		return FALSE;
	}

	printf("== Injector DLL has been liberated ==\n");

	FreeConsole();
	FreeLibraryAndExitThread(g_hModule, 0);
	return 0;
}
