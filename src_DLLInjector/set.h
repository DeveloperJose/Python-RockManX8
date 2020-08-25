#pragma once
#include "stdafx.h"

class SetEnemy {
public:
	union {
		DEFINE_MEMBER_N(vec3_t pos, 0x10);
		DEFINE_MEMBER_N(char name[8], 0x28);
	};
};

class SetFile {
public:
	union {
		DEFINE_MEMBER_0(int enemyCount, 0x00);
	};

	SetEnemy* GetEnemy(int enemyID) {
		if (enemyID < 0 || enemyID > enemyCount)
			return NULL;
		return (SetEnemy*)(this + 16 + (enemyID * 20));
	}
};