#pragma once
#include "stdafx.h"

void HookEndScene(IDirect3DDevice9 *pDevice);
void HookPreCreateDevice(D3DPRESENT_PARAMETERS *pPresentParams);
void HookPostCreateDevice(IDirect3DDevice9 *pDevice);