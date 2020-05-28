#include "myIDirect3D8.h"
#include "myIDirect3DDevice8.h"
#include "hooks.h"

myIDirect3D8::myIDirect3D8(IDirect3D8 *pOriginal)
{
	pD3D = pOriginal;
}

HRESULT __stdcall myIDirect3D8::CreateDevice(UINT Adapter, D3DDEVTYPE DeviceType, HWND hFocusWindow, DWORD BehaviorFlags, D3DPRESENT_PARAMETERS* pPresentationParameters, IDirect3DDevice8** ppReturnedDeviceInterface)
{
	extern myIDirect3DDevice8* gl_pmyIDirect3DDevice8;
	HookCreateDevice(pPresentationParameters);

	// we intercept this call and provide our own "fake" Device Object
	HRESULT hres = pD3D->CreateDevice(Adapter, DeviceType, hFocusWindow, BehaviorFlags, pPresentationParameters, ppReturnedDeviceInterface);

	// Create our own Device object and strore it in global pointer
	// note: the object will delete itself once Ref count is zero (similar to COM objects)
	gl_pmyIDirect3DDevice8 = new myIDirect3DDevice8(*ppReturnedDeviceInterface);

	// store our pointer (the fake one) for returning it to the calling progam
	*ppReturnedDeviceInterface = gl_pmyIDirect3DDevice8;

	return(hres);
}

HRESULT __stdcall myIDirect3D8::QueryInterface(REFIID riid, void** ppvObj)
{
	*ppvObj = NULL;

	// call this to increase AddRef at original object
	// and to check if such an interface is there

	HRESULT hRes = pD3D->QueryInterface(riid, ppvObj);

	if (hRes == NOERROR) // if OK, send our "fake" address
	{
		*ppvObj = this;
	}

	return hRes;
}

ULONG __stdcall myIDirect3D8::AddRef()
{
	return(pD3D->AddRef());
}

ULONG __stdcall myIDirect3D8::Release()
{
	myIDirect3D8* gl_pIDirect3D8_Wrapper;

	// call original routine
	ULONG count = pD3D->Release();

	// in case no further Ref is there, the Original Object has deleted itself
	// so do we here
	if (count == 0)
	{
		gl_pIDirect3D8_Wrapper = NULL;
		delete(this);
	}

	return(count);
}

HRESULT __stdcall myIDirect3D8::RegisterSoftwareDevice(void* pInitializeFunction)
{
	return(pD3D->RegisterSoftwareDevice(pInitializeFunction));
}

UINT __stdcall myIDirect3D8::GetAdapterCount()
{
	return(pD3D->GetAdapterCount());
}

HRESULT __stdcall myIDirect3D8::GetAdapterIdentifier(UINT Adapter, DWORD Flags, D3DADAPTER_IDENTIFIER8* pIdentifier)
{
	return(pD3D->GetAdapterIdentifier(Adapter, Flags, pIdentifier));
}

UINT __stdcall myIDirect3D8::GetAdapterModeCount(UINT Adapter)
{
	return(pD3D->GetAdapterModeCount(Adapter));
}

HRESULT __stdcall myIDirect3D8::EnumAdapterModes(UINT Adapter, UINT Mode, D3DDISPLAYMODE* pMode)
{
	return(pD3D->EnumAdapterModes(Adapter, Mode, pMode));
}

HRESULT __stdcall myIDirect3D8::GetAdapterDisplayMode(UINT Adapter, D3DDISPLAYMODE* pMode)
{
	return(pD3D->GetAdapterDisplayMode(Adapter, pMode));
}

HRESULT __stdcall myIDirect3D8::CheckDeviceType(UINT Adapter, D3DDEVTYPE CheckType, D3DFORMAT DisplayFormat, D3DFORMAT BackBufferFormat, BOOL Windowed)
{
	return(pD3D->CheckDeviceType(Adapter, CheckType, DisplayFormat, BackBufferFormat, Windowed));
}

HRESULT __stdcall myIDirect3D8::CheckDeviceFormat(UINT Adapter, D3DDEVTYPE DeviceType, D3DFORMAT AdapterFormat, DWORD Usage, D3DRESOURCETYPE RType, D3DFORMAT CheckFormat)
{
	return(pD3D->CheckDeviceFormat(Adapter, DeviceType, AdapterFormat, Usage, RType, CheckFormat));
}

HRESULT __stdcall myIDirect3D8::CheckDeviceMultiSampleType(UINT Adapter, D3DDEVTYPE DeviceType, D3DFORMAT SurfaceFormat, BOOL Windowed, D3DMULTISAMPLE_TYPE MultiSampleType)
{
	return(pD3D->CheckDeviceMultiSampleType(Adapter, DeviceType, SurfaceFormat, Windowed, MultiSampleType));
}

HRESULT __stdcall myIDirect3D8::CheckDepthStencilMatch(UINT Adapter, D3DDEVTYPE DeviceType, D3DFORMAT AdapterFormat, D3DFORMAT RenderTargetFormat, D3DFORMAT DepthStencilFormat)
{
	return(pD3D->CheckDepthStencilMatch(Adapter, DeviceType, AdapterFormat, RenderTargetFormat, DepthStencilFormat));
}

HRESULT __stdcall myIDirect3D8::GetDeviceCaps(UINT Adapter, D3DDEVTYPE DeviceType, D3DCAPS8* pCaps)
{
	return(pD3D->GetDeviceCaps(Adapter, DeviceType, pCaps));
}

HMONITOR __stdcall myIDirect3D8::GetAdapterMonitor(UINT Adapter)
{
	return(pD3D->GetAdapterMonitor(Adapter));
}