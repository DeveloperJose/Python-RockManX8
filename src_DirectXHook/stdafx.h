#pragma once

#pragma comment (lib, "comctl32.lib")
#pragma comment(lib, "d3dx8.lib")
#include <d3d8.h>
#include <d3dx8.h>
#include <Windows.h>
#include <CommCtrl.h>
#include <iostream>

typedef IDirect3D8 *(WINAPI *Function_Direct3DCreate8)(UINT);