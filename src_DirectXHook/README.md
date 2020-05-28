# Visual Studio 2017 DirectX8 Hooking
This project creates a DirectX8 dll to place in the game directory to hook DirectX calls. Usually you would need to use an older version of Visual Studio but this set-up solution works for VS2017.

Since I spent several hours setting this up, here are the steps.
* Get a copy of the DirectX8 headers and libraries (I got mine from Microsoft's NuGet repo: https://www.nuget.org/packages/DirectX8/1.0.0)
* Add the headers and libraries to the Project Settings->VC++ Directories (they have to be the last ones)
* Ignore libci in your Project Settings->Linker->Input->Ignore Specific Default Libraries
* Add legacy_stdio_definitions.lib to your Project Settings->Linker->Input->Additional Dependencies