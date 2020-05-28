#pragma once

#pragma comment (lib, "comctl32.lib")
#pragma comment(lib, "d3dx9.lib")
#include <d3d9.h>
#include <d3dx9.h>
#include <Windows.h>
#include <CommCtrl.h>
#include <iostream>

typedef IDirect3D9 *(WINAPI *Function_Direct3DCreate9)(UINT);