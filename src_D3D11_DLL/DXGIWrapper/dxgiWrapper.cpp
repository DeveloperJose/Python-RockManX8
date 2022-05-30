#include "dxgiWrapper.h"
#include "stdafx.h"
#include "utils.h"

DXGIWrapper::DXGIWrapper(): d3d_module(nullptr), m_swapchain(nullptr), is_dll_valid(false)
{
	Event = std::ofstream("DXGI.log");
	Event << this << std::endl;
}

DXGIWrapper::~DXGIWrapper()
{
}

bool DXGIWrapper::LoadDLL()
{
	// Initialise wrapper
	//Event << LOG("Loading DLL") << std::endl;

	HMODULE hD3D = nullptr;
	if (IsWow64())
	{
		//Event << LOG("Running on SysWOW64") << std::endl;
		hD3D = LoadLibrary(L"C:\\Windows\\SysWOW64\\dxgi.dll");
	}
	else
	{
		hD3D = LoadLibrary(L"C:\\Windows\\System32\\dxgi.dll");
	}

	if (hD3D == NULL)
	{
		//Event << LOGERR("Unable to load DLL") << std::endl;
		return false;
	}

	this->d3d_module = hD3D;
	this->is_dll_valid = true;
	//Event << LOG("Loaded DLL") << std::endl;
	return true;
}

HMODULE DXGIWrapper::GetDLL()
{
	std::lock_guard<std::mutex> lock(MutLoader);
	if (!is_dll_valid) this->LoadDLL();
	return d3d_module;
}

void DXGIWrapper::setSwapChain(IDXGISwapChain* swapchain)
{
	m_swapchain = swapchain;
}
