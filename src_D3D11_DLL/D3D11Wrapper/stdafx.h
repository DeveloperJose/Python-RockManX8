// stdafx.h : include file for standard system include files,
// or project specific include files that are used frequently, but
// are changed infrequently
//

#pragma once
#include <Windows.h>
#include <CommCtrl.h>
#pragma comment (lib, "comctl32.lib")

#include "targetver.h"

#ifndef NDEBUG
#define DEBUG_ONLY_PRINT(x) std::cout << x << std::endl
#define DEBUG_LOGLINE(x, msg) x << msg << std::endl

#define DEBUG_LINE(x, msg) \
	std::cout << "[" << std::to_string(uint64_t(this)) << "] " << msg << std::endl; \
	DEBUG_LOGLINE(x, msg)

#else
#define DEBUG_ONLY_PRINT(x)
#define DEBUG_LOGLINE(x, msg)
#define DEBUG_LINE(x, msg)
#endif


#include <cstdint>
#define LOG(x) "[INFO] " << x
#define LOGWRT(x) "[WRTE] " << x
#define LOGERR(x) "[ERRO] " << x
#define LOGWARN(x) "[WARN] " << x