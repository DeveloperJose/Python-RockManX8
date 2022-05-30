#include <sstream>
#include <iostream>
#include <d3dcompiler.h>

#include "d3d11ObjectManager.h"
#include "stdafx.h"
#include "utils.h"

#include "imgui/imgui.h"
#include "imgui/backends/imgui_impl_dx11.h"
#include "imgui/backends/imgui_impl_win32.h"

#include <set>

D3DObjectManager::D3DObjectManager(HMODULE _hD3D) :
	d3d_module(_hD3D),
	is_dll_valid(true)
{
	//Event = std::ofstream("d3d.txt");
}

D3DObjectManager::D3DObjectManager()
	: d3d_module(nullptr),
	is_dll_valid(false)
{
	AllocConsole();
	freopen_s((FILE**)stdout, "CONOUT$", "w", stdout);


#ifndef NDEBUG
	DEBUG_LOGLINE(Event, LOG("Initialising"));
	Event.open("d3d11_editor.log");


	std::cout << "DLL initialised" << std::endl;

	LPSTR lls = GetCommandLineA();
	DEBUG_LOGLINE(Event, "[ARGS] " << lls);
#endif

	LoadDLL();
}

D3DObjectManager::~D3DObjectManager()
{
#ifndef NDEBUG
	Event.close();
#endif
}

bool D3DObjectManager::LoadDLL()
{
	DEBUG_LOGLINE(Event, LOG("Loading DLL"));

	HMODULE d3d_module = nullptr;
	if (IsWow64())
	{
		Event << LOG("Running on SysWOW64 (x86)") << std::endl;
		d3d_module = LoadLibrary(L"C:\\Windows\\SysWOW64\\d3d11.dll");
	}
	else
	{
		d3d_module = LoadLibrary(L"C:\\Windows\\System32\\d3d11.dll");
	}

	if (d3d_module == NULL)
	{
		DEBUG_LOGLINE(Event, LOGERR("Unable to load DLL"));
		return false;
	}

	this->d3d_module = d3d_module;
	this->is_dll_valid = true;
	DEBUG_LOGLINE(Event, LOG("Loaded DLL"));
	return true;
}

HMODULE D3DObjectManager::GetDLL()
{
	if (!is_dll_valid) this->LoadDLL();
	return d3d_module;
}

extern LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);
ID3D11Device* pDevice = NULL;
//ID3D11DeviceContext* pContext = NULL;
//
//DWORD_PTR* pSwapChainVtable = NULL;
//DWORD_PTR* pContextVTable = NULL;
//DWORD_PTR* pDeviceVTable = NULL;
//
ID3D11Texture2D* RenderTargetTexture;
ID3D11RenderTargetView* RenderTargetView = NULL;
//
//LRESULT CALLBACK DXGIMsgProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) { return DefWindowProc(hwnd, uMsg, wParam, lParam); }
//const int MultisampleCount = 1; // Set to 1 to disable multisampling
//// Definition of WndProc Hook. Its here to avoid dragging dependencies on <windows.h> types.
//extern LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);
//BOOL first_time = true;
//bool g_ShowMenu = false;
////static IDXGISwapChain* pSwapChain = NULL;
static WNDPROC OriginalWndProcHandler = nullptr;
HWND window = nullptr;

bool is_first_time = true;
bool is_clear = true;
bool g_ShowMenu = true;

std::ofstream EEvent = std::ofstream("d3d2.txt");


LRESULT CALLBACK hWndProc(HWND hWnd, UINT uMsg, WPARAM wParam, LPARAM lParam)
{
	//DEBUG_LOGLINE(EEvent, LOGERR("1"));
	ImGuiIO& io = ImGui::GetIO();
	POINT mPos;
	GetCursorPos(&mPos);
	ScreenToClient(window, &mPos);
	ImGui::GetIO().MousePos.x = mPos.x;
	ImGui::GetIO().MousePos.y = mPos.y;
	//DEBUG_LOGLINE(EEvent, LOGERR("2"));


	if (uMsg == WM_KEYUP)
	{
		DEBUG_LOGLINE(EEvent, LOG("KeyUp"));
		if (wParam == VK_DELETE)
		{
			g_ShowMenu = !g_ShowMenu;
		}

	}
	//DEBUG_LOGLINE(EEvent, LOGERR("3"));
	if (g_ShowMenu)
	{
		ImGui_ImplWin32_WndProcHandler(hWnd, uMsg, wParam, lParam);
		return true;
	}
	//DEBUG_LOGLINE(EEvent, LOGERR("4"));
	return CallWindowProc(OriginalWndProcHandler, hWnd, uMsg, wParam, lParam);
}

std::set<UINT> messages;
LRESULT CALLBACK D3DObjectManager::SubclassWindowProc(HWND hWnd, UINT uMsg, WPARAM wParam, LPARAM lParam, UINT_PTR uIdSubclass, DWORD_PTR dwRefData)
{
	messages.insert(uMsg);
	for (auto el : messages)
	{
		std::cout << el << ',';
	}
	printf("\n");
	return DefSubclassProc(hWnd, uMsg, wParam, lParam);
}

void D3DObjectManager::Clear() {
	pDevice2->GetImmediateContext(&pContext2);
	pContext2->ClearState();

	RenderTargetView->Release();
	is_clear = true;
}

void D3DObjectManager::Notify_Present(IDXGISwapChain4* p_swap_chain, UINT sync_interval, UINT present_flags, const DXGI_PRESENT_PARAMETERS* p_present_params, ID3D11DeviceContext* pContextasdasd)
{
	//DEBUG_LOGLINE(Event, LOGERR("Called Notify"));
	pDevice2->GetImmediateContext(&pContext2);
	if (pContext2 == nullptr) {
		return;
		//DEBUG_LOGLINE(Event, LOGERR("0 Context"));
	}
	else {
		//char cBuf[128];
		//sprintf_s(cBuf, "device=%x, context=%x, context2=%x", (uintptr_t)pDevice2, (uintptr_t)pContext2, (uintptr_t)&pContext2);
		//DEBUG_LOGLINE(Event, LOGERR(cBuf));

		if (is_clear) {
			/*HWND pH;
			p_swap_chain->GetHwnd(&pH);
			SetWindowSubclass(pH, SubclassWindowProc, (UINT_PTR)0, (DWORD_PTR)0);*/
			/*if (SUCCEEDED(p_swap_chain->GetDevice(__uuidof(ID3D11Device), (void**)&pDevice)))
			{
				DEBUG_LOGLINE(Event, LOGERR("Got device"));
				p_swap_chain->GetDevice(__uuidof(pDevice), (void**)&pDevice);
			}*/

			if (SUCCEEDED(p_swap_chain->GetBuffer(0, __uuidof(ID3D11Texture2D), (LPVOID*)&RenderTargetTexture)))
			{
				DEBUG_LOGLINE(Event, LOGERR("Got buffer"));
				pDevice2->CreateRenderTargetView(RenderTargetTexture, NULL, &RenderTargetView);
				RenderTargetTexture->Release();
			}
			is_clear = false;
		}

		if (is_first_time) {
			DXGI_SWAP_CHAIN_DESC sd;
			p_swap_chain->GetDesc(&sd);
			//DEBUG_LOGLINE(Event, LOGERR("Got ChainDesc"));

			ImGui::CreateContext();
			ImGuiIO& io = ImGui::GetIO(); (void)io;
			io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard;
			window = sd.OutputWindow;
			//DEBUG_LOGLINE(Event, LOGERR("Created ImGUI context"));

			//OriginalWndProcHandler = (WNDPROC)SetWindowLongPtr(window, GWLP_WNDPROC, (LONG_PTR)hWndProc);
			DEBUG_LOGLINE(Event, LOGERR("Got WndProc"));/*

			DEBUG_LOGLINE(Event, LOGERR("ImGUI Init1"));*/
			ImGui_ImplWin32_Init(window);

			//DEBUG_LOGLINE(Event, LOGERR("ImGUI Init2"));
			ImGui_ImplDX11_Init(pDevice2, pContext2);

			//DEBUG_LOGLINE(Event, LOGERR("ImGUI Init3"));
			ImGui::GetIO().ImeWindowHandle = window;

			//DEBUG_LOGLINE(Event, LOGERR("ImGUI Init4"));

			is_first_time = false;
		}
		ImGui_ImplWin32_NewFrame();
		ImGui_ImplDX11_NewFrame();
		ImGui::NewFrame();
		//DEBUG_LOGLINE(Event, LOGERR("ImGUI frames"));
		if (g_ShowMenu) {
			DEBUG_LOGLINE(Event, LOGERR("show menu"));
			bool bShow = true;
			ImGui::ShowDemoWindow(&bShow);
		}
		ImGui::EndFrame();
		//DEBUG_LOGLINE(Event, LOGERR("End frames"));

		//DEBUG_LOGLINE(Event, LOGERR("Render"));
		ImGui::Render();

		//DEBUG_LOGLINE(Event, LOGERR("SetRender"));
		pContext2->OMSetRenderTargets(1, &RenderTargetView, NULL);

		//DEBUG_LOGLINE(Event, LOGERR("Render2"));
		ImGui_ImplDX11_RenderDrawData(ImGui::GetDrawData());

		//DEBUG_LOGLINE(Event, LOGERR("DrawData"));
	}
	
}
