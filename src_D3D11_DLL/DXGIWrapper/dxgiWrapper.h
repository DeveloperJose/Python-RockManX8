#pragma once
#include <dxgi.h>
#include <dxgi1_6.h>
#include <fstream>
#include <mutex>

class DXGIWrapper
{
protected:
	HMODULE d3d_module;
	IDXGISwapChain* m_swapchain;
	std::mutex MutLoader;
	bool is_dll_valid;

public:
	std::ofstream Event;

public:
	DXGIWrapper();
	~DXGIWrapper();

	/// Public functions
	bool LoadDLL();

	// Getters
	HMODULE GetDLL();

	// Setters
	void setSwapChain(IDXGISwapChain* swapchain);
};
