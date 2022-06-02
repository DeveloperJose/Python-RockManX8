#pragma once

#if defined(EDITOR_EXPORTS)
	#define DLL_SHARED __declspec(dllexport)
#else
	#define DLL_SHARED __declspec(dllimport)
	#pragma comment(lib, "Editor.lib")
#endif

#include "pch.h"
class DLL_SHARED Editor
{
public:
	Editor();
	~Editor();

	HMODULE _d3d_module;

	// d3d11 hooks
	void Notify_Present(IDXGISwapChain* p_swap_chain, UINT sync_interval, UINT present_flags);
	HRESULT Hook_ResizeBuffers(IDXGISwapChain* p_swap_chain, UINT BufferCount, UINT Width, UINT Height, DXGI_FORMAT NewFormat, UINT SwapChainFlags);

protected:
	ComPtr<ID3D11RenderTargetView> _render_target_view;
	bool _is_imgui_initialized;
};

