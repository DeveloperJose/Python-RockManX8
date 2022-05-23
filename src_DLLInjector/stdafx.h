#pragma once
#include <Windows.h>
#include <CommCtrl.h>
#include <iostream>

#define base_addr (DWORD)GetModuleHandle(0)

struct vec3_t {
	float x, y, z;
};

struct vec2 {
	float x, y;
};

struct vec4 {
	float x, y, z, w;
};

class Entity
{
public:
	class Entity* Prev; //0x0000
	class Entity* Next; //0x0004
	char pad_0008[12]; //0x0008
	int32_t NoCollision; //0x0014
	int32_t ID; //0x0018
	void* Animations1; //0x001C
	char pad_0020[4]; //0x0020
	void* Animations1_Dupe; //0x0024
	char pad_0028[72]; //0x0028
	float X; //0x0070
	float Y; //0x0074
	float Z; //0x0078
	float UNF_7C; //0x007C
	float X_Dupe; //0x0080
	float Y_Dupe; //0x0084
	float Z_Dupe; //0x0088
	float N0000040F; //0x008C
	float Angle1; //0x0090
	float Angle2; //0x0094
	float Angle3; //0x0098
	float Angle4; //0x009C
	float Angle5; //0x00A0
	float N00000414; //0x00A4
	float N00000415; //0x00A8
	float N00000416; //0x00AC
	float N00000417; //0x00B0
	float N00000418; //0x00B4
	float N00000419; //0x00B8
	float Angle_BC; //0x00BC
	float N0000041B; //0x00C0
	float N0000041C; //0x00C4
	float N0000041D; //0x00C8
	float VisibleModel; //0x00CC
	float N0000041F; //0x00D0
	float Height; //0x00D4
	float Width; //0x00D8
	float N00000422; //0x00DC
	float N00000423; //0x00E0
	float N00000424; //0x00E4
	float N00000425; //0x00E8
	float N00000426; //0x00EC
	char pad_00F0[64]; //0x00F0

}; //Size: 0x0130

// Disable warning about zero-sized arrays
#pragma warning( push )
#pragma warning( disable : 4200 )
class EntityList {
public:
	class Entity entities[];
};
#pragma warning( pop )