#pragma once
#include <Windows.h>
#include <CommCtrl.h>
#include <iostream>

#define baseAddr (DWORD)GetModuleHandle(NULL)

#define STR_MERGE_IMPL(x, y)				x##y
#define STR_MERGE(x,y)						STR_MERGE_IMPL(x,y)
#define MAKE_PAD(size)						BYTE STR_MERGE(pad_, __COUNTER__) [ size ]

#define DEFINE_MEMBER_0(x, y)				x
#define DEFINE_MEMBER_N(x,offset)			struct { MAKE_PAD(offset); x; }

struct vec3_t {
	float x, y, z;
};

struct vec2 {
	float x, y;
};

struct vec4 {
	float x, y, z, w;
};

class SetEnemy
{
public:
	char pad_0000[4]; //0x0000
	float Rotation; //0x0004
	char pad_0008[8]; //0x0008
	float X; //0x0010
	float Y; //0x0014
	float Z; //0x0018
	float Fvar2; //0x001C
	char SS1[4]; //0x0020
	char pad_0024[4]; //0x0024
	char PrmType[8]; //0x0028
	char pad_0030[32]; //0x0030
}; //Size: 0x0050
