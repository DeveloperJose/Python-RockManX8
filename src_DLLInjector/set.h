#pragma once
#include "stdafx.h"


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


// Disable warning about zero-sized arrays
#pragma warning( push )
#pragma warning( disable : 4200 )
class SetFile {
public:
	// We will be ignoring the regular header and starting at enemy_count in this in-memory version of the SetFile as the enemy count has an easier to find address
	int32_t enemy_count; //0x0000
	char pad_0004[60]; //0x0004
	class SetEnemy enemies[]; //0x0040

	SetEnemy* GetEnemy(int enemyID) {
		if (enemyID < 0 || enemyID > enemy_count)
			return NULL;
		return &enemies[enemyID];
	}
};
#pragma warning( pop )