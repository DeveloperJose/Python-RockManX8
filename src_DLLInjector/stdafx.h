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
	char pad_0028[52]; //0x0028
	int32_t N00000403; //0x005C
	int32_t N00000404; //0x0060
	char pad_0064[12]; //0x0064
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


class EntityExtra
{
public:
	char pad_0000[8]; //0x0000
	void* NextPlayerPtr; //0x0008
	void* UnkPtr1; //0x000C
	int32_t ID; //0x0010
	void* NextPlayerPtr_Dupe; //0x0014
	void* UnkPtr1_Dupe; //0x0018
	void* UnkPtr2; //0x001C
	void* UnkPtr2_Dupe; //0x0020
	void* UnkPtr3; //0x0024
	char pad_0028[8]; //0x0028
	void* UnkPtr3_Dupe; //0x0030
	char pad_0034[8]; //0x0034
	bool Vulnerable; //0x003C
	char pad_003D[3]; //0x003D
	int32_t HP; //0x0040
	int32_t MaxHP; //0x0044
	int32_t N000008CF; //0x0048
	int32_t N000008D0; //0x004C
	int32_t N000008D1; //0x0050
	int32_t InvTimer; //0x0054
	int32_t N000008D3; //0x0058
	int32_t N000008D4; //0x005C
	int32_t N000008D5; //0x0060
	int32_t N000008D6; //0x0064
	int32_t InvTimer2; //0x0068
	int32_t N000008D8; //0x006C
	int32_t N000008D9; //0x0070
	char pad_0074[512]; //0x0074
}; //Size: 0x0274

class SetEnemyParent
{
public:
	char pad_0000[4]; //0x0000
	int32_t idx; //0x0004
	class SetEnemy* set_enemy; //0x0008
	int16_t is_active; //0x000C
	int16_t N00000CF4; //0x000E
	int32_t N00000CAF; //0x0010
	char pad_0014[188]; //0x0014
}; //Size: 0x00D0

class CEnemy
{
public:
	void* N00000CF7; //0x0000
	char type[8]; //0x0004
	char pad_000C[24]; //0x000C
	int32_t unk1; //0x0024
	int32_t activated; //0x0028
	int32_t keep_loaded; //0x002C
	char pad_0030[12]; //0x0030
	class CEnemy* prev; //0x003C
	class CEnemy* next; //0x0040
	char pad_0044[140]; //0x0044
	int32_t entity_idx; //0x00D0
	int32_t unknown_idx; //0x00D4
	int16_t entity_extra_idx; //0x00D8
	char pad_00DA[1110]; //0x00DA
}; //Size: 0x0530