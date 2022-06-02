// dllmain.cpp : Defines the entry point for the DLL application.
#include "pch.h"
BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved
                     )
{
    static plog::ColorConsoleAppender<plog::TxtFormatter> consoleAppender;
    static plog::RollingFileAppender<plog::TxtFormatter> fileAppender("x8_editor.txt", 8000, 3);
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
        plog::init(plog::debug, &consoleAppender).addAppender(&fileAppender);
        PLOGD << "************************************************************";
        break;
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}

