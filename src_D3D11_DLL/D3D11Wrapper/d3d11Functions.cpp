#include "stdafx.h"
#include "d3d11ObjectManager.h"
#include "d3d11Device.h"
#include "d3d11DeviceContext.h"

#include <DXGIWrapper/dxgiSwapchain2.h>

#include <editor/editor.h>

#include <processenv.h>

// Global Class
//D3DObjectManager *GlOM = new D3DObjectManager();
Editor* GlOM = new Editor();


// TODO: Handling


typedef HRESULT(WINAPI* PFN_D3D11_CREATE_DEVICE)(__in_opt IDXGIAdapter*,
	D3D_DRIVER_TYPE, HMODULE, UINT,
	__in_ecount_opt(FeatureLevels) CONST D3D_FEATURE_LEVEL*,
	UINT FeatureLevels, UINT, __out_opt ID3D11Device**,
	__out_opt D3D_FEATURE_LEVEL*, __out_opt ID3D11DeviceContext**);


HRESULT WINAPI D3D11CreateDevice(
	__in_opt IDXGIAdapter* pAdapter,
	D3D_DRIVER_TYPE DriverType,
	HMODULE Software,
	UINT Flags,
	__in_ecount_opt(FeatureLevels) CONST D3D_FEATURE_LEVEL* pFeatureLevels,
	UINT FeatureLevels,
	UINT SDKVersion,
	__out_opt ID3D11Device** ppDevice,
	__out_opt D3D_FEATURE_LEVEL* pFeatureLevel,
	__out_opt ID3D11DeviceContext** ppImmediateContext)
{
	// Log
	//DEBUG_LOGLINE(GlOM->Event, LOG("D3D11CreateDevice intercepted"));
	printf("D3D11CreateDevice intercepted\n");
	PFN_D3D11_CREATE_DEVICE createDev = (PFN_D3D11_CREATE_DEVICE)GetProcAddress(GlOM->_d3d_module, "D3D11CreateDevice");
	if (createDev == nullptr)
	{
		//DEBUG_LOGLINE(GlOM->Event, LOGERR("Cannot find function D3D11CreateDevice in DLL"));
		return NULL;
	}

	// Use the real DLL's function
	HRESULT out = createDev(pAdapter, DriverType, Software, Flags, pFeatureLevels, FeatureLevels, SDKVersion, ppDevice, pFeatureLevel, ppImmediateContext);
	if (ppDevice)
	{
		//DEBUG_LOGLINE(GlOM->Event, LOG("Device Created. Registering."));
		//d3dw->setDevice(*ppDevice);

		const auto temp = new D3D11CustomDevice(*ppDevice, GlOM);
		*ppDevice = temp;

		// Check if the optional immediate is being used
		if (ppImmediateContext)
		{
			//DEBUG_LOGLINE(GlOM->Event, LOG("Caught Immediate Context"));
			ID3D11DeviceContext* tempCtx = new D3D11CustomContext(*ppImmediateContext, temp, GlOM);
			*ppImmediateContext = tempCtx;
		}
	} 
	else
	{
		//DEBUG_LOGLINE(GlOM->Event, LOGWARN("Failed to get device from D3D11"));
	}

	return out;
}

typedef HRESULT(WINAPI* PFN_D3D11ON12_CREATE_DEVICE)(_In_ IUnknown*, UINT,
	_In_reads_opt_(FeatureLevels) CONST D3D_FEATURE_LEVEL*, UINT FeatureLevels,
	_In_reads_opt_(NumQueues) IUnknown* CONST*, UINT NumQueues,
	UINT, _COM_Outptr_opt_ ID3D11Device**, _COM_Outptr_opt_ ID3D11DeviceContext**,
	_Out_opt_ D3D_FEATURE_LEVEL*);

HRESULT WINAPI D3D11On12CreateDevice(
	_In_ IUnknown* pDevice,
	UINT Flags,
	_In_reads_opt_(FeatureLevels) CONST D3D_FEATURE_LEVEL* pFeatureLevels,
	UINT FeatureLevels,
	_In_reads_opt_(NumQueues) IUnknown* CONST* ppCommandQueues,
	UINT NumQueues,
	UINT NodeMask,
	_COM_Outptr_opt_ ID3D11Device** ppDevice,
	_COM_Outptr_opt_ ID3D11DeviceContext** ppImmediateContext,
	_Out_opt_ D3D_FEATURE_LEVEL* pChosenFeatureLevel)
{
	printf("Intercepted D3D11On12CreateDevice call\n");
	auto createDev = (PFN_D3D11ON12_CREATE_DEVICE)GetProcAddress(GlOM->_d3d_module, "D3D11On12CreateDevice");
	if (!createDev)
	{
		//DEBUG_LOGLINE(GlOM->Event, LOGERR("Cannot find function D3D11On12CreateDevice in DLL"));
		return NULL;
	}

	HRESULT out = createDev(pDevice, Flags, pFeatureLevels, FeatureLevels, ppCommandQueues, NumQueues, NodeMask, ppDevice, ppImmediateContext, pChosenFeatureLevel);
	if (ppDevice != nullptr)
	{
		//d3dw->setDevice(*ppDevice);
	}
	else
	{
		//DEBUG_LOGLINE(GlOM->Event, LOGWARN("Failed to get device from D3D11"));
	}
	return out;
}

HRESULT WINAPI D3D11CreateDeviceForD3D12() { return NULL; }

LRESULT CALLBACK DXGIMsgProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
	return DefWindowProc(hwnd, uMsg, wParam, lParam);
}

inline bool SdkLayersAvailable()
{
	PFN_D3D11_CREATE_DEVICE createDev = (PFN_D3D11_CREATE_DEVICE)GetProcAddress(GlOM->_d3d_module, "D3D11CreateDevice");
	HRESULT hr = createDev(
		nullptr,
		D3D_DRIVER_TYPE_NULL,       // There is no need to create a real hardware device.
		0,
		D3D11_CREATE_DEVICE_DEBUG,  // Check for the SDK layers.
		nullptr,                    // Any feature level will do.
		0,
		D3D11_SDK_VERSION,
		nullptr,                    // No need to keep the D3D device reference.
		nullptr,                    // No need to know the feature level.
		nullptr                     // No need to keep the D3D device context reference.
	);

	return SUCCEEDED(hr);
}

typedef HRESULT(WINAPI* PFN_D3D11_CREATE_DEVICE_AND_SWAP_CHAIN)(__in_opt IDXGIAdapter*,
	D3D_DRIVER_TYPE, HMODULE, UINT,
	__in_ecount_opt(FeatureLevels) CONST D3D_FEATURE_LEVEL*,
	UINT FeatureLevels, UINT, __in_opt CONST DXGI_SWAP_CHAIN_DESC*,
	__out_opt IDXGISwapChain**, __out_opt ID3D11Device**,
	__out_opt D3D_FEATURE_LEVEL*, __out_opt ID3D11DeviceContext**);

HRESULT WINAPI D3D11CreateDeviceAndSwapChain(
	__in_opt IDXGIAdapter* pAdapter,
	D3D_DRIVER_TYPE DriverType,
	HMODULE Software,
	UINT Flags,
	__in_ecount_opt(FeatureLevels) CONST D3D_FEATURE_LEVEL* pFeatureLevels,
	UINT FeatureLevels,
	UINT SDKVersion,
	__in_opt CONST DXGI_SWAP_CHAIN_DESC* pSwapChainDesc,
	__out_opt IDXGISwapChain** ppSwapChain,
	__out_opt ID3D11Device** ppDevice,
	__out_opt D3D_FEATURE_LEVEL* pFeatureLevel,
	__out_opt ID3D11DeviceContext** ppImmediateContext)
{

	printf("D3D11CreateDeviceAndSwapChain intercepted\n");
	//DEBUG_LOGLINE(GlOM->Event, LOG("D3D11CreateDeviceAndSwapChain intercepted"));
	// 
	//MessageBox(NULL, L"Creating Device and SwapChain", L"D3D9Wrapper", MB_OK);
	PFN_D3D11_CREATE_DEVICE_AND_SWAP_CHAIN createDev = (PFN_D3D11_CREATE_DEVICE_AND_SWAP_CHAIN)GetProcAddress(GlOM->_d3d_module, "D3D11CreateDeviceAndSwapChain");
	if (!createDev) return NULL;

	// https://docs.microsoft.com/en-us/windows/win32/direct3d11/overviews-direct3d-11-devices-initialize
	//WNDCLASSEXA wc = { sizeof(WNDCLASSEX), CS_CLASSDC, DXGIMsgProc, 0L, 0L, GetModuleHandleA(NULL), NULL, NULL, NULL, NULL, "DX", NULL };
	//RegisterClassExA(&wc);
	//HWND hWnd = CreateWindowA("DX", NULL, WS_OVERLAPPEDWINDOW, 100, 100, 300, 300, NULL, NULL, wc.hInstance, NULL);

	//DXGI_SWAP_CHAIN_DESC scd;
	//ZeroMemory(&scd, sizeof(scd));
	//scd.BufferCount = 1;
	//scd.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM;
	//scd.BufferDesc.Scaling = DXGI_MODE_SCALING_UNSPECIFIED;
	//scd.BufferDesc.ScanlineOrdering = DXGI_MODE_SCANLINE_ORDER_UNSPECIFIED;
	//scd.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;
	//scd.Flags = DXGI_SWAP_CHAIN_FLAG_ALLOW_MODE_SWITCH;
	//scd.OutputWindow = hWnd;
	//scd.SampleDesc.Count = 1;
	//scd.SwapEffect = DXGI_SWAP_EFFECT_DISCARD;
	//scd.Windowed = ((GetWindowLongPtr(hWnd, GWL_STYLE) & WS_POPUP) != 0) ? false : true;
	//// LibOVR 0.4.3 requires that the width and height for the backbuffer is set even if
	//// you use windowed mode, despite being optional according to the D3D11 documentation.
	//scd.BufferDesc.Width = 1;
	//scd.BufferDesc.Height = 1;
	//scd.BufferDesc.RefreshRate.Numerator = 0;
	//scd.BufferDesc.RefreshRate.Denominator = 1;

	//UINT createFlags = 0;

	//D3D_FEATURE_LEVEL requestedLevels[] = { D3D_FEATURE_LEVEL_11_0, D3D_FEATURE_LEVEL_10_1 };

	//if (SdkLayersAvailable())
	//Flags = D3D11_CREATE_DEVICE_DEBUG;
	
	HRESULT out = createDev(pAdapter, DriverType, Software, Flags, pFeatureLevels, FeatureLevels, SDKVersion, pSwapChainDesc, ppSwapChain, ppDevice, pFeatureLevel, ppImmediateContext);
	//HRESULT out = createDev(nullptr, D3D_DRIVER_TYPE_HARDWARE, nullptr, createFlags, requestedLevels, sizeof(requestedLevels) / sizeof(D3D_FEATURE_LEVEL), D3D11_SDK_VERSION, &scd, ppSwapChain, ppDevice, pFeatureLevel, ppImmediateContext);
	if (out == S_OK)
	{
		//DEBUG_LOGLINE(GlOM->Event, LOG("CDSC Success"));
		//GlOM->pDevice2 = *ppDevice;

		//char cBuf[64];
		//sprintf_s(cBuf, "context=%x\n", (uintptr_t)ppImmediateContext);
		//DEBUG_LOGLINE(GlOM->Event, LOGERR(cBuf));
		printf("new device %x\n", *ppDevice);

		if (ppDevice)
		{
			//DEBUG_LOGLINE(GlOM->Event, LOG("CDSC Has Device"));
			const auto temp = new D3D11CustomDevice(*ppDevice, GlOM);
			*ppDevice = temp;

			if (ppImmediateContext)
			{
				//DEBUG_LOGLINE(GlOM->Event, LOG("CDSC Device + IM"));
				ID3D11DeviceContext* tempCtx = new D3D11CustomContext(*ppImmediateContext, temp, GlOM);
				*ppImmediateContext = tempCtx;
			}

			if (ppSwapChain)
			{
				//DEBUG_LOGLINE(GlOM->Event, LOG("CDSC Device + SC"));

				const auto tempSc = new DXGICustomSwapChain(*ppSwapChain, temp, GlOM);
				*ppSwapChain = tempSc;
				/*HWND pH;
				tempSc->GetHwnd(&pH);
				SetWindowSubclass(pH, GlOM->SubclassWindowProc, (UINT_PTR)0, (DWORD_PTR)0);*/
			}
		}
		else
		{
			if (ppImmediateContext)
			{
				//DEBUG_LOGLINE(GlOM->Event, LOG("CDSC IM"));
				ID3D11DeviceContext* tempCtx = new D3D11CustomContext(*ppImmediateContext, GlOM);
				*ppImmediateContext = tempCtx;
			}

			if (ppSwapChain)
			{
				//DEBUG_LOGLINE(GlOM->Event, LOG("CDSC SC"));
				const auto tempSc = new DXGICustomSwapChain(*ppSwapChain, nullptr, GlOM);
				*ppSwapChain = tempSc;
			}
		}
	}

	return out;
}

typedef HRESULT(WINAPI *DXGIFAC)(REFIID, void **);
HRESULT WINAPI CreateDXGIFactory(REFIID riid, void **ppFactory)
{
	//MessageBox(NULL, L"FactoryCreate", L"D3D9Wrapper", MB_OK);
	printf("CreateDXGIFactory intercepted\n");
	DXGIFAC pCreateFactory = (DXGIFAC)GetProcAddress(GlOM->_d3d_module, "CreateDXGIFactory");
	if (!pCreateFactory)
	{
		//g_Globals.ErrorFile() << "coud not find Direct3DCreate9 in d3d9.dll\n";
		return NULL;
	}

	HRESULT pD3D = pCreateFactory(riid, ppFactory);
	if (pD3D == NULL)
	{
		return NULL;
	}

	return pD3D;
}

HRESULT WINAPI CreateDXGIFactory1(REFIID riid, void **ppFactory)
{
	//DEBUG_LOGLINE(GlOM->Event, LOG("CreateDXGIFactory1 intercepted"));
	printf("CreateDXGIFactory1 intercepted\n");
	DXGIFAC pCreateFactory = (DXGIFAC)GetProcAddress(GlOM->_d3d_module, "CreateDXGIFactory1");
	if (!pCreateFactory)
	{
		//g_Globals.ErrorFile() << "coud not find Direct3DCreate9 in d3d9.dll\n";
		return NULL;
	}

	HRESULT pD3D = pCreateFactory(riid, ppFactory);
	if (pD3D == NULL)
	{
		return NULL;
	}

	return pD3D;
}

HRESULT WINAPI CreateDXGIFactory2(REFIID riid, void **ppFactory)
{
	//MessageBox(NULL, L"FactoryCreate2", L"D3D9Wrapper", MB_OK);
	//DEBUG_LOGLINE(GlOM->Event, LOG("CreateDXGIFactory2 intercepted"));
	printf("CreateDXGIFactory2 intercepted\n");
	DXGIFAC pCreateFactory = (DXGIFAC)GetProcAddress(GlOM->_d3d_module, "CreateDXGIFactory2");
	if (!pCreateFactory)
	{
		//g_Globals.ErrorFile() << "coud not find Direct3DCreate9 in d3d9.dll\n";
		return NULL;
	}

	HRESULT pD3D = pCreateFactory(riid, ppFactory);
	if (pD3D == NULL)
	{
		return NULL;
	}

	return pD3D;
}

int WINAPI D3DPerformance_BeginEvent(DWORD col, LPCWSTR wszName)
{
	return 0;
}

int WINAPI D3DPerformance_EndEvent()
{
	return 0;
}

DWORD WINAPI D3DPerformance_GetStatus()
{
	//MessageBox(NULL, L"D3DPERF_GetStatus", L"D3D9Wrapper", MB_OK);
	return 0;
}

void WINAPI D3DPerformance_SetMarker()
{
	//MessageBox(NULL, L"D3DPERF_SetMarker", L"D3D9Wrapper", MB_OK);
}
