cmake_minimum_required(VERSION 3.12) # 3.12 allows linking object libs
project(Karma C CXX)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(PROJECT_NAME "Karma")
set(PROJECT_VERSION_MAJOR "1")
set(PROJECT_VERSION_MINOR "0")
set(PROJECT_VERSION_PATCH "0")
set(PROJECT_VERSION "${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}.${PROJECT_VERSION_PATCH}")

set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -fPIC -O0 -Wall -pedantic -Wextra")
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -fPIC -Wall -pedantic -Wextra")
set(CMAKE_CXX_FLAGS_RELWITHDEBINFO "${CMAKE_CXX_FLAGS_RELWITHDEBINFO} -fPIC -O3 -g -rdynamic -Wall -pedantic -Wextra")

set(CMAKE_BUILD_TYPE RelWithDebInfo)

add_library(libkarma STATIC src/karma_allocator.cpp src/bheap.cpp)
set_target_properties(libfunnel PROPERTIES PREFIX "")
target_include_directories(libkarma PUBLIC include)

add_executable(example example/example.cpp)
target_include_directories(example PUBLIC include)
target_link_libraries(example PRIVATE libkarma)