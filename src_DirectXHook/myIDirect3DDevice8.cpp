#include "myIDirect3DDevice8.h"
#include "hooks.h"

myIDirect3DDevice8::myIDirect3DDevice8(IDirect3DDevice8* pOriginal)
{
	pDevice = pOriginal; // store the pointer to original object
}

HRESULT __stdcall myIDirect3DDevice8::QueryInterface(REFIID riid, void** ppvObj)
{
	// check if original dll can provide an interface. then send *our* address
	*ppvObj = NULL;

	HRESULT hRes = pDevice->QueryInterface(riid, ppvObj);

	if (hRes == NOERROR)
	{
		*ppvObj = this;
	}

	return hRes;
}

ULONG   __stdcall myIDirect3DDevice8::AddRef(void)
{
	return (pDevice->AddRef());
}

ULONG   __stdcall myIDirect3DDevice8::Release(void)
{
	// ATTENTION: This is a booby-trap ! Watch out !
	// If we create our own sprites, surfaces, etc. (thus increasing the ref counter
	// by external action), we need to delete that objects before calling the original
	// Release function	

	// global var
	myIDirect3DDevice8* gl_pmyIDirect3DDevice8;

	// release/delete own objects
	// ... here if any ...

	// Calling original function now
	ULONG count = pDevice->Release();

	// now, the Original Object has deleted itself, so do we here
	gl_pmyIDirect3DDevice8 = NULL;
	delete(this);  // destructor will be called automatically

	return (count);
}

HRESULT __stdcall myIDirect3DDevice8::TestCooperativeLevel(void)
{
	return (pDevice->TestCooperativeLevel());
}

UINT    __stdcall myIDirect3DDevice8::GetAvailableTextureMem(void)
{
	return (pDevice->GetAvailableTextureMem());
}

HRESULT __stdcall myIDirect3DDevice8::ResourceManagerDiscardBytes(DWORD Bytes)
{
	return (pDevice->ResourceManagerDiscardBytes(Bytes));
}

HRESULT __stdcall myIDirect3DDevice8::GetDirect3D(IDirect3D8** ppD3D8)
{
	return (pDevice->GetDirect3D(ppD3D8));
}

HRESULT __stdcall myIDirect3DDevice8::GetDeviceCaps(D3DCAPS8* pCaps)
{
	return (pDevice->GetDeviceCaps(pCaps));
}

HRESULT __stdcall myIDirect3DDevice8::GetDisplayMode(D3DDISPLAYMODE* pMode)
{
	return (pDevice->GetDisplayMode(pMode));
}

HRESULT __stdcall myIDirect3DDevice8::GetCreationParameters(D3DDEVICE_CREATION_PARAMETERS *pParameters)
{
	return (pDevice->GetCreationParameters(pParameters));
}

HRESULT __stdcall myIDirect3DDevice8::SetCursorProperties(UINT XHotSpot, UINT YHotSpot, IDirect3DSurface8* pCursorBitmap)
{
	return (pDevice->SetCursorProperties(XHotSpot, YHotSpot, pCursorBitmap));
}

void    __stdcall myIDirect3DDevice8::SetCursorPosition(UINT XScreenSpace, UINT YScreenSpace, DWORD Flags)
{
	pDevice->SetCursorPosition(XScreenSpace, YScreenSpace, Flags);
}

BOOL    __stdcall myIDirect3DDevice8::ShowCursor(BOOL bShow)
{
	return (pDevice->ShowCursor(bShow));
}

HRESULT __stdcall myIDirect3DDevice8::CreateAdditionalSwapChain(D3DPRESENT_PARAMETERS* pPresentationParameters, IDirect3DSwapChain8** pSwapChain)
{
	return (pDevice->CreateAdditionalSwapChain(pPresentationParameters, pSwapChain));
}

HRESULT __stdcall myIDirect3DDevice8::Reset(D3DPRESENT_PARAMETERS* pPresentationParameters)
{
	return (pDevice->Reset(pPresentationParameters));
}

HRESULT __stdcall myIDirect3DDevice8::Present(CONST RECT* pSourceRect, CONST RECT* pDestRect, HWND hDestWindowOverride, CONST RGNDATA* pDirtyRegion)
{
	return (pDevice->Present(pSourceRect, pDestRect, hDestWindowOverride, pDirtyRegion));
}

HRESULT __stdcall myIDirect3DDevice8::GetBackBuffer(UINT BackBuffer, D3DBACKBUFFER_TYPE Type, IDirect3DSurface8** ppBackBuffer)
{
	return (pDevice->GetBackBuffer(BackBuffer, Type, ppBackBuffer));
}

HRESULT __stdcall myIDirect3DDevice8::GetRasterStatus(D3DRASTER_STATUS* pRasterStatus)
{
	return (pDevice->GetRasterStatus(pRasterStatus));
}

void    __stdcall myIDirect3DDevice8::SetGammaRamp(DWORD Flags, CONST D3DGAMMARAMP* pRamp)
{
	pDevice->SetGammaRamp(Flags, pRamp);
}

void    __stdcall myIDirect3DDevice8::GetGammaRamp(D3DGAMMARAMP* pRamp)
{
	pDevice->GetGammaRamp(pRamp);
}

HRESULT __stdcall myIDirect3DDevice8::CreateTexture(UINT Width, UINT Height, UINT Levels, DWORD Usage, D3DFORMAT Format, D3DPOOL Pool, IDirect3DTexture8** ppTexture)
{
	return (pDevice->CreateTexture(Width, Height, Levels, Usage, Format, Pool, ppTexture));
}

HRESULT __stdcall myIDirect3DDevice8::CreateVolumeTexture(UINT Width, UINT Height, UINT Depth, UINT Levels, DWORD Usage, D3DFORMAT Format, D3DPOOL Pool, IDirect3DVolumeTexture8** ppVolumeTexture)
{
	return (pDevice->CreateVolumeTexture(Width, Height, Depth, Levels, Usage, Format, Pool, ppVolumeTexture));
}

HRESULT __stdcall myIDirect3DDevice8::CreateCubeTexture(UINT EdgeLength, UINT Levels, DWORD Usage, D3DFORMAT Format, D3DPOOL Pool, IDirect3DCubeTexture8** ppCubeTexture)
{
	return (pDevice->CreateCubeTexture(EdgeLength, Levels, Usage, Format, Pool, ppCubeTexture));
}

HRESULT __stdcall myIDirect3DDevice8::CreateVertexBuffer(UINT Length, DWORD Usage, DWORD FVF, D3DPOOL Pool, IDirect3DVertexBuffer8** ppVertexBuffer)
{
	return (pDevice->CreateVertexBuffer(Length, Usage, FVF, Pool, ppVertexBuffer));
}

HRESULT __stdcall myIDirect3DDevice8::CreateIndexBuffer(UINT Length, DWORD Usage, D3DFORMAT Format, D3DPOOL Pool, IDirect3DIndexBuffer8** ppIndexBuffer)
{
	return (pDevice->CreateIndexBuffer(Length, Usage, Format, Pool, ppIndexBuffer));
}

HRESULT __stdcall myIDirect3DDevice8::CreateRenderTarget(UINT Width, UINT Height, D3DFORMAT Format, D3DMULTISAMPLE_TYPE MultiSample, BOOL Lockable, IDirect3DSurface8** ppSurface)
{
	return (pDevice->CreateRenderTarget(Width, Height, Format, MultiSample, Lockable, ppSurface));
}

HRESULT __stdcall myIDirect3DDevice8::CreateDepthStencilSurface(UINT Width, UINT Height, D3DFORMAT Format, D3DMULTISAMPLE_TYPE MultiSample, IDirect3DSurface8** ppSurface)
{
	return (pDevice->CreateDepthStencilSurface(Width, Height, Format, MultiSample, ppSurface));
}

HRESULT __stdcall myIDirect3DDevice8::CreateImageSurface(UINT Width, UINT Height, D3DFORMAT Format, IDirect3DSurface8** ppSurface)
{
	return (pDevice->CreateImageSurface(Width, Height, Format, ppSurface));
}

HRESULT __stdcall myIDirect3DDevice8::CopyRects(IDirect3DSurface8* pSourceSurface, CONST RECT* pSourceRectsArray, UINT cRects, IDirect3DSurface8* pDestinationSurface, CONST POINT* pDestPointsArray)
{
	return (pDevice->CopyRects(pSourceSurface, pSourceRectsArray, cRects, pDestinationSurface, pDestPointsArray));
}

HRESULT __stdcall myIDirect3DDevice8::UpdateTexture(IDirect3DBaseTexture8* pSourceTexture, IDirect3DBaseTexture8* pDestinationTexture)
{
	return (pDevice->UpdateTexture(pSourceTexture, pDestinationTexture));
}

HRESULT __stdcall myIDirect3DDevice8::GetFrontBuffer(IDirect3DSurface8* pDestSurface)
{
	return (pDevice->GetFrontBuffer(pDestSurface));
}

HRESULT __stdcall myIDirect3DDevice8::SetRenderTarget(IDirect3DSurface8* pRenderTarget, IDirect3DSurface8* pNewZStencil)
{
	return (pDevice->SetRenderTarget(pRenderTarget, pNewZStencil));
}

HRESULT __stdcall myIDirect3DDevice8::GetRenderTarget(IDirect3DSurface8** ppRenderTarget)
{
	return (pDevice->GetRenderTarget(ppRenderTarget));
}

HRESULT __stdcall myIDirect3DDevice8::GetDepthStencilSurface(IDirect3DSurface8** ppZStencilSurface)
{
	return (pDevice->GetDepthStencilSurface(ppZStencilSurface));
}

HRESULT __stdcall myIDirect3DDevice8::BeginScene(void)
{
	return (pDevice->BeginScene());
}

HRESULT __stdcall myIDirect3DDevice8::EndScene(void)
{
	HookEndScene(pDevice);
	return (pDevice->EndScene());
}

HRESULT __stdcall myIDirect3DDevice8::Clear(DWORD Count, CONST D3DRECT* pRects, DWORD Flags, D3DCOLOR Color, float Z, DWORD Stencil)
{
	return (pDevice->Clear(Count, pRects, Flags, Color, Z, Stencil));
}

HRESULT __stdcall myIDirect3DDevice8::SetTransform(D3DTRANSFORMSTATETYPE State, CONST D3DMATRIX* pMatrix)
{
	return (pDevice->SetTransform(State, pMatrix));
}

HRESULT __stdcall myIDirect3DDevice8::GetTransform(D3DTRANSFORMSTATETYPE State, D3DMATRIX* pMatrix)
{
	return (pDevice->GetTransform(State, pMatrix));
}

HRESULT __stdcall myIDirect3DDevice8::MultiplyTransform(D3DTRANSFORMSTATETYPE State, CONST D3DMATRIX* pMatrix)
{
	return (pDevice->MultiplyTransform(State, pMatrix));
}

HRESULT __stdcall myIDirect3DDevice8::SetViewport(CONST D3DVIEWPORT8* pViewport)
{
	return (pDevice->SetViewport(pViewport));
}

HRESULT __stdcall myIDirect3DDevice8::GetViewport(D3DVIEWPORT8* pViewport)
{
	return (pDevice->GetViewport(pViewport));
}

HRESULT __stdcall myIDirect3DDevice8::SetMaterial(CONST D3DMATERIAL8* pMaterial)
{
	return (pDevice->SetMaterial(pMaterial));
}

HRESULT __stdcall myIDirect3DDevice8::GetMaterial(D3DMATERIAL8* pMaterial)
{
	return (pDevice->GetMaterial(pMaterial));
}

HRESULT __stdcall myIDirect3DDevice8::SetLight(DWORD Index, CONST D3DLIGHT8* pLight)
{
	return (pDevice->SetLight(Index, pLight));
}

HRESULT __stdcall myIDirect3DDevice8::GetLight(DWORD Index, D3DLIGHT8* pLight)
{
	return (pDevice->GetLight(Index, pLight));
}

HRESULT __stdcall myIDirect3DDevice8::LightEnable(DWORD Index, BOOL Enable)
{
	return (pDevice->LightEnable(Index, Enable));
}

HRESULT __stdcall myIDirect3DDevice8::GetLightEnable(DWORD Index, BOOL* pEnable)
{
	return (pDevice->GetLightEnable(Index, pEnable));
}

HRESULT __stdcall myIDirect3DDevice8::SetClipPlane(DWORD Index, CONST float* pPlane)
{
	return (pDevice->SetClipPlane(Index, pPlane));
}

HRESULT __stdcall myIDirect3DDevice8::GetClipPlane(DWORD Index, float* pPlane)
{
	return (pDevice->GetClipPlane(Index, pPlane));
}

HRESULT __stdcall myIDirect3DDevice8::SetRenderState(D3DRENDERSTATETYPE State, DWORD Value)
{
	return (pDevice->SetRenderState(State, Value));
}

HRESULT __stdcall myIDirect3DDevice8::GetRenderState(D3DRENDERSTATETYPE State, DWORD* pValue)
{
	return (pDevice->GetRenderState(State, pValue));
}

HRESULT __stdcall myIDirect3DDevice8::BeginStateBlock(void)
{
	return (pDevice->BeginStateBlock());
}

HRESULT __stdcall myIDirect3DDevice8::EndStateBlock(DWORD* pToken)
{
	return (pDevice->EndStateBlock(pToken));
}

HRESULT __stdcall myIDirect3DDevice8::ApplyStateBlock(DWORD Token)
{
	return (pDevice->ApplyStateBlock(Token));
}

HRESULT __stdcall myIDirect3DDevice8::CaptureStateBlock(DWORD Token)
{
	return (pDevice->CaptureStateBlock(Token));
}

HRESULT __stdcall myIDirect3DDevice8::DeleteStateBlock(DWORD Token)
{
	return (pDevice->DeleteStateBlock(Token));
}

HRESULT __stdcall myIDirect3DDevice8::CreateStateBlock(D3DSTATEBLOCKTYPE Type, DWORD* pToken)
{
	return (pDevice->CreateStateBlock(Type, pToken));
}

HRESULT __stdcall myIDirect3DDevice8::SetClipStatus(CONST D3DCLIPSTATUS8* pClipStatus)
{
	return (pDevice->SetClipStatus(pClipStatus));
}

HRESULT __stdcall myIDirect3DDevice8::GetClipStatus(D3DCLIPSTATUS8* pClipStatus)
{
	return (pDevice->GetClipStatus(pClipStatus));
}

HRESULT __stdcall myIDirect3DDevice8::GetTexture(DWORD Stage, IDirect3DBaseTexture8** ppTexture)
{
	return (pDevice->GetTexture(Stage, ppTexture));
}

HRESULT __stdcall myIDirect3DDevice8::SetTexture(DWORD Stage, IDirect3DBaseTexture8* pTexture)
{
	return (pDevice->SetTexture(Stage, pTexture));
}

HRESULT __stdcall myIDirect3DDevice8::GetTextureStageState(DWORD Stage, D3DTEXTURESTAGESTATETYPE Type, DWORD* pValue)
{
	return (pDevice->GetTextureStageState(Stage, Type, pValue));
}

HRESULT __stdcall myIDirect3DDevice8::SetTextureStageState(DWORD Stage, D3DTEXTURESTAGESTATETYPE Type, DWORD Value)
{
	return (pDevice->SetTextureStageState(Stage, Type, Value));
}

HRESULT __stdcall myIDirect3DDevice8::ValidateDevice(DWORD* pNumPasses)
{
	return (pDevice->ValidateDevice(pNumPasses));
}

HRESULT __stdcall myIDirect3DDevice8::GetInfo(DWORD DevInfoID, void* pDevInfoStruct, DWORD DevInfoStructSize)
{
	return (pDevice->GetInfo(DevInfoID, pDevInfoStruct, DevInfoStructSize));
}

HRESULT __stdcall myIDirect3DDevice8::SetPaletteEntries(UINT PaletteNumber, CONST PALETTEENTRY* pEntries)
{
	return (pDevice->SetPaletteEntries(PaletteNumber, pEntries));
}

HRESULT __stdcall myIDirect3DDevice8::GetPaletteEntries(UINT PaletteNumber, PALETTEENTRY* pEntries)
{
	return (pDevice->GetPaletteEntries(PaletteNumber, pEntries));
}

HRESULT __stdcall myIDirect3DDevice8::SetCurrentTexturePalette(UINT PaletteNumber)
{
	return (pDevice->SetCurrentTexturePalette(PaletteNumber));
}

HRESULT __stdcall myIDirect3DDevice8::GetCurrentTexturePalette(UINT *PaletteNumber)
{
	return (pDevice->GetCurrentTexturePalette(PaletteNumber));
}

HRESULT __stdcall myIDirect3DDevice8::DrawPrimitive(D3DPRIMITIVETYPE PrimitiveType, UINT StartVertex, UINT PrimitiveCount)
{
	return (pDevice->DrawPrimitive(PrimitiveType, StartVertex, PrimitiveCount));
}

HRESULT __stdcall myIDirect3DDevice8::DrawIndexedPrimitive(D3DPRIMITIVETYPE Type, UINT minIndex, UINT NumVertices, UINT startIndex, UINT primCount)
{
	return (pDevice->DrawIndexedPrimitive(Type, minIndex, NumVertices, startIndex, primCount));
}

HRESULT __stdcall myIDirect3DDevice8::DrawPrimitiveUP(D3DPRIMITIVETYPE PrimitiveType, UINT PrimitiveCount, CONST void* pVertexStreamZeroData, UINT VertexStreamZeroStride)
{
	return (pDevice->DrawPrimitiveUP(PrimitiveType, PrimitiveCount, pVertexStreamZeroData, VertexStreamZeroStride));
}

HRESULT __stdcall myIDirect3DDevice8::DrawIndexedPrimitiveUP(D3DPRIMITIVETYPE PrimitiveType, UINT MinVertexIndex, UINT NumVertexIndices, UINT PrimitiveCount, CONST void* pIndexData, D3DFORMAT IndexDataFormat, CONST void* pVertexStreamZeroData, UINT VertexStreamZeroStride)
{
	return (pDevice->DrawIndexedPrimitiveUP(PrimitiveType, MinVertexIndex, NumVertexIndices, PrimitiveCount, pIndexData, IndexDataFormat, pVertexStreamZeroData, VertexStreamZeroStride));
}

HRESULT __stdcall myIDirect3DDevice8::ProcessVertices(UINT SrcStartIndex, UINT DestIndex, UINT VertexCount, IDirect3DVertexBuffer8* pDestBuffer, DWORD Flags)
{
	return (pDevice->ProcessVertices(SrcStartIndex, DestIndex, VertexCount, pDestBuffer, Flags));
}

HRESULT __stdcall myIDirect3DDevice8::CreateVertexShader(CONST DWORD* pDeclaration, CONST DWORD* pFunction, DWORD* pHandle, DWORD Usage)
{
	return (pDevice->CreateVertexShader(pDeclaration, pFunction, pHandle, Usage));
}

HRESULT __stdcall myIDirect3DDevice8::SetVertexShader(DWORD Handle)
{
	return (pDevice->SetVertexShader(Handle));
}

HRESULT __stdcall myIDirect3DDevice8::GetVertexShader(DWORD* pHandle)
{
	return (pDevice->GetVertexShader(pHandle));
}

HRESULT __stdcall myIDirect3DDevice8::DeleteVertexShader(DWORD Handle)
{
	return (pDevice->DeleteVertexShader(Handle));
}

HRESULT __stdcall myIDirect3DDevice8::SetVertexShaderConstant(DWORD Register, CONST void* pConstantData, DWORD ConstantCount)
{
	return (pDevice->SetVertexShaderConstant(Register, pConstantData, ConstantCount));
}

HRESULT __stdcall myIDirect3DDevice8::GetVertexShaderConstant(DWORD Register, void* pConstantData, DWORD ConstantCount)
{
	return (pDevice->GetVertexShaderConstant(Register, pConstantData, ConstantCount));
}

HRESULT __stdcall myIDirect3DDevice8::GetVertexShaderDeclaration(DWORD Handle, void* pData, DWORD* pSizeOfData)
{
	return (pDevice->GetVertexShaderDeclaration(Handle, pData, pSizeOfData));
}

HRESULT __stdcall myIDirect3DDevice8::GetVertexShaderFunction(DWORD Handle, void* pData, DWORD* pSizeOfData)
{
	return (pDevice->GetVertexShaderFunction(Handle, pData, pSizeOfData));
}

HRESULT __stdcall myIDirect3DDevice8::SetStreamSource(UINT StreamNumber, IDirect3DVertexBuffer8* pStreamData, UINT Stride)
{
	return (pDevice->SetStreamSource(StreamNumber, pStreamData, Stride));
}

HRESULT __stdcall myIDirect3DDevice8::GetStreamSource(UINT StreamNumber, IDirect3DVertexBuffer8** ppStreamData, UINT* pStride)
{
	return (pDevice->GetStreamSource(StreamNumber, ppStreamData, pStride));
}

HRESULT __stdcall myIDirect3DDevice8::SetIndices(IDirect3DIndexBuffer8* pIndexData, UINT BaseVertexIndex)
{
	return (pDevice->SetIndices(pIndexData, BaseVertexIndex));
}

HRESULT __stdcall myIDirect3DDevice8::GetIndices(IDirect3DIndexBuffer8** ppIndexData, UINT* pBaseVertexIndex)
{
	return (pDevice->GetIndices(ppIndexData, pBaseVertexIndex));
}

HRESULT __stdcall myIDirect3DDevice8::CreatePixelShader(CONST DWORD* pFunction, DWORD* pHandle)
{
	return (pDevice->CreatePixelShader(pFunction, pHandle));
}

HRESULT __stdcall myIDirect3DDevice8::SetPixelShader(DWORD Handle)
{
	return (pDevice->SetPixelShader(Handle));
}

HRESULT __stdcall myIDirect3DDevice8::GetPixelShader(DWORD* pHandle)
{
	return (pDevice->GetPixelShader(pHandle));
}

HRESULT __stdcall myIDirect3DDevice8::DeletePixelShader(DWORD Handle)
{
	return (pDevice->DeletePixelShader(Handle));
}

HRESULT __stdcall myIDirect3DDevice8::SetPixelShaderConstant(DWORD Register, CONST void* pConstantData, DWORD ConstantCount)
{
	return (pDevice->SetPixelShaderConstant(Register, pConstantData, ConstantCount));
}

HRESULT __stdcall myIDirect3DDevice8::GetPixelShaderConstant(DWORD Register, void* pConstantData, DWORD ConstantCount)
{
	return (pDevice->GetPixelShaderConstant(Register, pConstantData, ConstantCount));
}

HRESULT __stdcall myIDirect3DDevice8::GetPixelShaderFunction(DWORD Handle, void* pData, DWORD* pSizeOfData)
{
	return (pDevice->GetPixelShaderFunction(Handle, pData, pSizeOfData));
}

HRESULT __stdcall myIDirect3DDevice8::DrawRectPatch(UINT Handle, CONST float* pNumSegs, CONST D3DRECTPATCH_INFO* pRectPatchInfo)
{
	return (pDevice->DrawRectPatch(Handle, pNumSegs, pRectPatchInfo));
}

HRESULT __stdcall myIDirect3DDevice8::DrawTriPatch(UINT Handle, CONST float* pNumSegs, CONST D3DTRIPATCH_INFO* pTriPatchInfo)
{
	return (pDevice->DrawTriPatch(Handle, pNumSegs, pTriPatchInfo));
}

HRESULT __stdcall myIDirect3DDevice8::DeletePatch(UINT Handle)
{
	return (pDevice->DeletePatch(Handle));
}

