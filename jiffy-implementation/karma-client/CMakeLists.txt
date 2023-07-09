if (NOT APPLE AND UNIX)
  set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -Wl,--no-as-needed -ldl")
endif ()

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../libjiffy/src
        ${CMAKE_CURRENT_SOURCE_DIR}/../karma-client
        ${Boost_INCLUDE_DIRS})

add_executable(test_client src/test_client.cpp)
add_dependencies(test_client boost_ep jemalloc_ep)

target_link_libraries(test_client jiffy_client ${JEMALLOC_LIBRARY} ${Boost_PROGRAM_OPTIONS_LIBRARY})

install(TARGETS test_client
        RUNTIME DESTINATION bin)