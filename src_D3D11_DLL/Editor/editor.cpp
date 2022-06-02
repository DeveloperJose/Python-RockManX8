#include "pch.h"
#include "editor.h"
#include <tchar.h>

Editor::Editor() {
	// Open console for debugging
	AllocConsole();
	freopen_s((FILE**)stdout, "CONOUT$", "w", stdout);
	freopen_s((FILE**)stderr, "CONOUT$", "w", stderr);
	freopen_s((FILE**)stdin, "CONIN$", "r", stdin);

	// Load system d3d11 dll
	_d3d_module = LoadLibraryW(L"C:\\Windows\\SysWOW64\\d3d11.dll");
	if (_d3d_module == NULL)
		throw std::runtime_error("d3d11.dll not found in system. Do you not have DirectX 11 installed?");

	_is_imgui_initialized = false;

	PLOGD << "d3d11 dll loaded";
}

Editor::~Editor() {

}

extern IMGUI_IMPL_API LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);
WNDPROC oWndProc;
HWND window = NULL;
bool show_demo_window = true;

LRESULT WINAPI WndProc(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam) {

	if (ImGui_ImplWin32_WndProcHandler(hWnd, msg, wParam, lParam))
		return true;

	return ::DefWindowProc(hWnd, msg, wParam, lParam);
}


void Editor::Notify_Present(IDXGISwapChain* p_swap_chain, UINT sync_interval, UINT present_flags)
{
	ID3D11Device* p_device;
	DX::ThrowIfFailed(p_swap_chain->GetDevice(__uuidof(ID3D11Device), (void**)&p_device));

	//ID3D10Device* p_device;
	//DX::ThrowIfFailed(p_swap_chain->GetDevice(__uuidof(ID3D10Device), (void**)&p_device));
	
	ID3D11DeviceContext* p_context;
	p_device->GetImmediateContext(&p_context);
	if (p_context == nullptr)
		throw std::runtime_error("[Editor] Couldn't get immediate context");

	if ((uintptr_t)p_context == 0xcdcdcdcd)
		return;

	if (!_is_imgui_initialized) {
		//ID3D11Debug::ReportLiveDeviceObjects(D3D11_RLDO_SUMMARY);
		PLOGD.printf("device=%x, context=%x, swapchain=%x", p_device, p_context, p_swap_chain);

		p_device->GetImmediateContext(&p_context);
		DXGI_SWAP_CHAIN_DESC sd;
		p_swap_chain->GetDesc(&sd);
		window = sd.OutputWindow;

		/*WNDCLASSEX wc = { sizeof(WNDCLASSEX), CS_CLASSDC, WndProc, 0L, 0L, GetModuleHandle(NULL), NULL, NULL, NULL, NULL, _T("ImGui Example"), NULL };
		::RegisterClassEx(&wc);
		window = ::CreateWindow(wc.lpszClassName, _T("Dear ImGui DirectX11 Example"), WS_OVERLAPPEDWINDOW, 100, 100, 1280, 800, NULL, NULL, wc.hInstance, NULL);

		::ShowWindow(window, SW_SHOWDEFAULT);
		::UpdateWindow(window);*/
		//TCHAR WindowTitle[MAX_PATH];
		//HWND hwnd = GetForegroundWindow();
		//SendMessage(window, WM_GETTEXT, MAX_PATH, (LPARAM)WindowTitle);
		//PLOGD << "window=" << WindowTitle;

		//SendMessage(hwnd, WM_GETTEXT, MAX_PATH, (LPARAM)WindowTitle);
		//PLOGD << "window2=" << WindowTitle;

		ComPtr<ID3D11Texture2D> backBuffer;
		DX::ThrowIfFailed(p_swap_chain->GetBuffer(0, __uuidof(ID3D11Texture2D), &backBuffer));
		DX::ThrowIfFailed(p_device->CreateRenderTargetView(backBuffer.Get(), nullptr, &_render_target_view));
		PLOGD << "backbuffer";



		oWndProc = (WNDPROC)SetWindowLongPtr(window, GWLP_WNDPROC, (LONG_PTR)WndProc);

		ImGui::CreateContext();
		ImGuiIO& io = ImGui::GetIO(); (void)io;
		io.IniFilename = NULL;
		io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard;
		io.Fonts->AddFontDefault();
		PLOGD << "win32";
		ImGui_ImplWin32_Init(window);
		PLOGD << "dx11";
		ImGui_ImplDX11_Init(p_device, p_context);
		PLOGD << "init done";
		_is_imgui_initialized = true;
	}
	ImGui_ImplDX11_NewFrame();
	ImGui_ImplWin32_NewFrame();
	ImGui::NewFrame();

	//ImGui::ShowDemoWindow(&show_demo_window);

	ImGui::Begin("ImGui Window");
	ImGui::Text("This is some useful text.");
	ImGui::End();

	ImGui::Render();

	p_context->OMSetRenderTargets(1, _render_target_view.GetAddressOf(), nullptr);
	ImGui_ImplDX11_RenderDrawData(ImGui::GetDrawData());
	p_swap_chain->Present(1, 0);

	D3D11_VIEWPORT viewport;
	ZeroMemory(&viewport, sizeof(D3D11_VIEWPORT));

	viewport.TopLeftX = 0;
	viewport.TopLeftY = 0;
	viewport.Width = 100;
	viewport.Height = 100;

	p_context->RSSetViewports(1, &viewport);
}

HRESULT Editor::Hook_ResizeBuffers(IDXGISwapChain* p_swap_chain, UINT BufferCount, UINT Width, UINT Height, DXGI_FORMAT NewFormat, UINT SwapChainFlags)
{
	PLOGD << "ResizedBuffers";
	// https://stackoverflow.com/questions/34711294/cannot-release-direct3d-buffer-from-swap-chain-for-resize
	ID3D11Device* p_device;
	DX::ThrowIfFailed(p_swap_chain->GetDevice(__uuidof(ID3D11Device), (void**)&p_device));
	
	ID3D11DeviceContext* p_context;
	p_device->GetImmediateContext(&p_context);
	if (p_context == nullptr)
		throw std::runtime_error("[Editor] Couldn't get immediate context");

	PLOGD.printf("device=%x, context=%x", p_device, p_context);

	ID3D11RenderTargetView* nullViews[] = { nullptr };
	p_context->OMSetRenderTargets(_countof(nullViews), nullViews, nullptr);

	_render_target_view.Reset();
	p_context->Flush();

	HRESULT hr = p_swap_chain->ResizeBuffers(BufferCount, Width, Height, NewFormat, SwapChainFlags);
	if (hr == DXGI_ERROR_DEVICE_REMOVED || hr == DXGI_ERROR_DEVICE_RESET)
		throw std::logic_error("[Editor] Need to implement re-creation");
	DX::ThrowIfFailed(hr);

	ComPtr<ID3D11Texture2D> backBuffer;
	DX::ThrowIfFailed(p_swap_chain->GetBuffer(0, __uuidof(ID3D11Texture2D), &backBuffer));
	DX::ThrowIfFailed(p_device->CreateRenderTargetView(backBuffer.Get(), nullptr, &_render_target_view));

	p_context->OMSetRenderTargets(1, _render_target_view.GetAddressOf(), nullptr);
	return hr;
}
