# CMakeList.txt : CMake project
# https://guidedhacking.com/threads/anyone-used-vscode-and-compiled-manually-in-c.11916/
cmake_minimum_required (VERSION 3.8)

project(editor)

# # set C++ to 17
set(CMAKE_CXX_STANDARD 17)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
# add_definitions(-D_WIN32_WINNT=0x0502)
# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -m32")
# SET(CMAKE_EXE_LINKER_FLAGS  "${CMAKE_EXE_LINKER_FLAGS} -m32")

# get all header files
# file(GLOB_RECURSE header_files *.h)

# # get all source files
# file(GLOB_RECURSE source_files *.cpp)

# # get all lib files in lib/
# file(GLOB lib_files lib/*.lib)

# # include our includes in "inc" folder
# include_directories(inc)

# Add source to this project's executable.
# add_library(editor SHARED ${source_files} ${lib_files} ${header_files})

set(source_files editor.cpp)
add_library(editor SHARED ${source_files})

# # And add lib files
# target_link_libraries(editor ${lib_files})