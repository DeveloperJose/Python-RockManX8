//#include <sstream>
//#include <iostream>
//#include <d3dcompiler.h>
//
//#include "d3d11ObjectManager.h"
//#include "stdafx.h"
//#include "utils.h"
//
//#include <imgui.h>
//#include "imgui/backends/imgui_impl_dx11.h"
//#include "imgui/backends/imgui_impl_win32.h"
//
//#include <set>
//
//D3DObjectManager::D3DObjectManager(HMODULE _hD3D) :
//	d3d_module(_hD3D),
//	is_dll_valid(true)
//{
//	//Event = std::ofstream("d3d.txt");
//}
//
//D3DObjectManager::D3DObjectManager()
//	: d3d_module(nullptr),
//	is_dll_valid(false)
//{
//	AllocConsole();
//	freopen_s((FILE**)stdout, "CONOUT$", "w", stdout);
//
//
//#ifndef NDEBUG
//	DEBUG_LOGLINE(Event, LOG("Initialising"));
//	Event.open("d3d11_editor.log");
//
//
//	std::cout << "DLL initialised" << std::endl;
//
//	LPSTR lls = GetCommandLineA();
//	DEBUG_LOGLINE(Event, "[ARGS] " << lls);
//#endif
//
//	LoadDLL();
//}
//
//D3DObjectManager::~D3DObjectManager()
//{
//#ifndef NDEBUG
//	Event.close();
//#endif
//}
//
//bool D3DObjectManager::LoadDLL()
//{
//	DEBUG_LOGLINE(Event, LOG("Loading DLL"));
//
//	HMODULE d3d_module = nullptr;
//	if (IsWow64())
//	{
//		Event << LOG("Running on SysWOW64 (x86)") << std::endl;
//		d3d_module = LoadLibrary(L"C:\\Windows\\SysWOW64\\d3d11.dll");
//	}
//	else
//	{
//		d3d_module = LoadLibrary(L"C:\\Windows\\System32\\d3d11.dll");
//	}
//
//	if (d3d_module == NULL)
//	{
//		DEBUG_LOGLINE(Event, LOGERR("Unable to load DLL"));
//		return false;
//	}
//
//	this->d3d_module = d3d_module;
//	this->is_dll_valid = true;
//	DEBUG_LOGLINE(Event, LOG("Loaded DLL"));
//	return true;
//}
//
//HMODULE D3DObjectManager::GetDLL()
//{
//	if (!is_dll_valid) this->LoadDLL();
//	return d3d_module;
//}
//
//extern LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);
////ID3D11Device* pDevice = NULL;
////ID3D11DeviceContext* pContext = NULL;
////
////DWORD_PTR* pSwapChainVtable = NULL;
////DWORD_PTR* pContextVTable = NULL;
////DWORD_PTR* pDeviceVTable = NULL;
////
////ID3D11Texture2D* RenderTargetTexture;
//ID3D11RenderTargetView* RenderTargetView = NULL;
////
////LRESULT CALLBACK DXGIMsgProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) { return DefWindowProc(hwnd, uMsg, wParam, lParam); }
////const int MultisampleCount = 1; // Set to 1 to disable multisampling
////// Definition of WndProc Hook. Its here to avoid dragging dependencies on <windows.h> types.
////extern LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);
////BOOL first_time = true;
////bool g_ShowMenu = false;
//////static IDXGISwapChain* pSwapChain = NULL;
//static WNDPROC OriginalWndProcHandler = nullptr;
//HWND window = nullptr;
//
//bool is_imgui_initialized = false;
//bool is_d3d_initialized = false;
//bool g_ShowMenu = true;
//
//std::ofstream EEvent = std::ofstream("d3d2.txt");
//
//
//LRESULT __stdcall WndProc(const HWND hWnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
//	if (ImGui_ImplWin32_WndProcHandler(hWnd, uMsg, wParam, lParam)) {
//		return true;
//	}
//	return CallWindowProc(OriginalWndProcHandler, hWnd, uMsg, wParam, lParam);
//	////DEBUG_LOGLINE(EEvent, LOGERR("1"));
//	//ImGuiIO& io = ImGui::GetIO();
//	//POINT mPos;
//	//GetCursorPos(&mPos);
//	//ScreenToClient(window, &mPos);
//	//ImGui::GetIO().MousePos.x = mPos.x;
//	//ImGui::GetIO().MousePos.y = mPos.y;
//	////DEBUG_LOGLINE(EEvent, LOGERR("2"));
//
//
//	//if (uMsg == WM_KEYUP)
//	//{
//	//	DEBUG_LOGLINE(EEvent, LOG("KeyUp"));
//	//	if (wParam == VK_DELETE)
//	//	{
//	//		g_ShowMenu = !g_ShowMenu;
//	//	}
//
//	//}
//	////DEBUG_LOGLINE(EEvent, LOGERR("3"));
//	//if (g_ShowMenu)
//	//{
//	//	ImGui_ImplWin32_WndProcHandler(hWnd, uMsg, wParam, lParam);
//	//	return true;
//	//}
//	////DEBUG_LOGLINE(EEvent, LOGERR("4"));
//	//return CallWindowProc(OriginalWndProcHandler, hWnd, uMsg, wParam, lParam);
//}
//
////std::set<UINT> messages;
////LRESULT CALLBACK D3DObjectManager::SubclassWindowProc(HWND hWnd, UINT uMsg, WPARAM wParam, LPARAM lParam, UINT_PTR uIdSubclass, DWORD_PTR dwRefData)
////{
////	messages.insert(uMsg);
////	for (auto el : messages)
////	{
////		std::cout << el << ',';
////	}
////	printf("\n");
////	return DefSubclassProc(hWnd, uMsg, wParam, lParam);
////}
//
//void D3DObjectManager::Clear() {
//	pDevice2->GetImmediateContext(&pContext2);
//	pContext2->ClearState();
//
//	RenderTargetView->Release();
//	is_d3d_initialized = false;
//}
//
//void D3DObjectManager::Notify_Present(IDXGISwapChain4* p_swap_chain, UINT sync_interval, UINT present_flags, const DXGI_PRESENT_PARAMETERS* p_present_params, ID3D11DeviceContext* pContextasdasd)
//{
//	//DEBUG_LOGLINE(Event, LOGERR("Called Notify"));
//
//		//DEBUG_LOGLINE(Event, LOGERR("0 Context"));
//		//char cBuf[128];
//		//sprintf_s(cBuf, "device=%x, context=%x, context2=%x", (uintptr_t)pDevice2, (uintptr_t)pContext2, (uintptr_t)&pContext2);
//		//DEBUG_LOGLINE(Event, LOGERR(cBuf));
//
//	if (!is_d3d_initialized) {
//		DEBUG_LOGLINE(Event, LOG("[Notify_Present] Trying to initialize d3d device"));
//		//if (SUCCEEDED(p_swap_chain->GetDevice(__uuidof(ID3D11Device), (void**)&pDevice2)))
//		//{
//			DEBUG_LOGLINE(Event, LOG("[Notify_Present] Trying to acquire ImmediateContext"));
//			pDevice2->GetImmediateContext(&pContext2);
//			if (pContext2 == nullptr || (uintptr_t)pContext2 == 0xcdcdcdcd) {
//				DEBUG_LOGLINE(Event, LOGERR("[Notify_Present] Could not acquire ImmediateContext"));
//				return;
//			}
//			char cBuf[256];
//			sprintf_s(cBuf, "device=%x, context=%x", (uintptr_t)pDevice2, (uintptr_t)pContext2);
//			DEBUG_LOGLINE(Event, LOG(cBuf));
//
//			DEBUG_LOGLINE(Event, LOG("[Notify_Present] Acquiring swap chain description"));
//			DXGI_SWAP_CHAIN_DESC sd;
//			p_swap_chain->GetDesc(&sd);
//			window = sd.OutputWindow;
//
//			char wnd_title[256];
//			GetWindowText(window, (LPWSTR)wnd_title, sizeof(wnd_title));
//			sprintf_s(cBuf, "window title = %s", wnd_title);
//			DEBUG_LOGLINE(Event, LOG(cBuf));
//
//			ID3D11Texture2D* pBackBuffer = nullptr;
//			p_swap_chain->GetBuffer(0, __uuidof(ID3D11Texture2D), (LPVOID*)&pBackBuffer);
//			if (pBackBuffer == nullptr) {
//				DEBUG_LOGLINE(Event, LOGERR("[Notify_Present] Couldn't get buffer"));
//				return;
//			}
//			pDevice2->CreateRenderTargetView(pBackBuffer, NULL, &RenderTargetView);
//			pBackBuffer->Release();
//			if (RenderTargetView == nullptr) {
//				DEBUG_LOGLINE(Event, LOGERR("[Notify_Present] Couldn't get RenderTargetView"));
//				return;
//			}
//
//			DEBUG_LOGLINE(Event, LOG("[Notify_Present] Preparing wndproc"));
//			OriginalWndProcHandler = (WNDPROC)SetWindowLongPtr(window, GWLP_WNDPROC, (LONG_PTR)WndProc);
//
//			if (!is_imgui_initialized) {
//				DEBUG_LOGLINE(Event, LOG("[Notify_Present] Initializing imgui context"));
//				ImGui::CreateContext();
//				ImGuiIO& io = ImGui::GetIO();
//				io.ConfigFlags = ImGuiConfigFlags_NoMouseCursorChange;
//
//				DEBUG_LOGLINE(Event, LOG("[Notify_Present] Initializing imgui win32"));
//				ImGui_ImplWin32_Init(window);
//
//				DEBUG_LOGLINE(Event, LOG("[Notify_Present] Initializing imgui dx11"));
//				ImGui_ImplDX11_Init(pDevice2, pContext2);
//
//				DEBUG_LOGLINE(Event, LOG("[Notify_Present] Successfully initialized imgui"));
//				is_imgui_initialized = true;
//			}
//			DEBUG_LOGLINE(Event, LOG("[Notify_Present] Successfully initialized d3d"));
//			is_d3d_initialized = true;
//		//}
//	}
//
//	ImGui_ImplDX11_NewFrame();
//	ImGui_ImplWin32_NewFrame();
//	ImGui::NewFrame();
//
//	ImGui::Begin("ImGui Window");
//	ImGui::End();
//
//	ImGui::Render();
//
//	pContext2->OMSetRenderTargets(1, &RenderTargetView, NULL);
//	ImGui_ImplDX11_RenderDrawData(ImGui::GetDrawData());
//
//}