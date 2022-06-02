// pch.h: This is a precompiled header file.
// Files listed below are compiled only once, improving build performance for future builds.
// This also affects IntelliSense performance, including code completion and many code browsing features.
// However, files listed here are ALL re-compiled if any one of them is updated between builds.
// Do not add files here that you will be updating frequently as this negates the performance advantage.

#ifndef PCH_H
#define PCH_H

// Exclude rarely-used stuff from Windows headers
#define WIN32_LEAN_AND_MEAN            

// Standard header files don't change so we can pre-compile them
#include <wrl/client.h>
using Microsoft::WRL::ComPtr;

#include <exception>
#include <stdexcept>
#include <windows.h>

#include <d3d10_1.h>
#include <d3d10.h>
#pragma comment(lib, "d3d10.lib")

#include <d3d11.h>
#include <d3d11sdklayers.h>
#pragma comment(lib, "d3d11.lib")

// https://stackoverflow.com/questions/46789396/which-header-file-contains-throwiffailed-in-directx-12
namespace DX
{
    // Helper class for COM exceptions
    class com_exception : public std::exception
    {
    public:
        com_exception(HRESULT hr) : result(hr) {}

        virtual const char* what() const override
        {
            static char s_str[64] = {};
            sprintf_s(s_str, "Failure with HRESULT of %08X",
                static_cast<unsigned int>(result));
            return s_str;
        }

    private:
        HRESULT result;
    };

    // Helper utility converts D3D API failures into exceptions.
    inline void ThrowIfFailed(HRESULT hr)
    {
        if (FAILED(hr))
        {
            throw com_exception(hr);
        }
    }
}

// Currently we are not modifying ImGui so pre-compile it
#include <imgui/imgui.h>
#include <imgui/backends/imgui_impl_dx11.h>
#include <imgui/backends/imgui_impl_win32.h>

// Pre-compile logging library
#include <plog/Log.h>
#include <plog/Init.h>
#include <plog/Formatters/TxtFormatter.h>
#include <plog/Appenders/ColorConsoleAppender.h>
#include <plog/Appenders/RollingFileAppender.h>
#include <plog/Helpers/HexDump.h>
#define PLOG_EXPORT

#endif //PCH_H
