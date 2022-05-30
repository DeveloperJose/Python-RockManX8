#pragma once

#ifndef SCOPED_LOCK
/**
 * Scoped Lock in C++17
 *
 * Fall back to LockGuard in C++14
 */
#if __cplusplus >= 201703L
#define SCOPED_LOCK(x) std::scoped_lock lock_ ## x (x)
#define SCOPED_LOCK_XY(x,y) std::scoped_lock lock_ ## x ## y (x,y)
#else
#define SCOPED_LOCK(x) std::lock_guard<std::mutex> lock_ ## x (x)
#define SCOPED_LOCK_XY(x,y) std::lock(x, y); \
            std::lock_guard<std::mutex> lock_ ## x (x, std::adopt_lock); \
            std::lock_guard<std::mutex> lock_ ## y (y, std::adopt_lock)
#endif
#endif


bool IsWow64();

/// Convert the specified single precision float number to a half precision float number.
static uint16_t FloatToHalfFloat(float floatValue);

/// Convert the specified half float number to a single precision float number.
float HalfFloatToFloat(uint16_t halfFloat);