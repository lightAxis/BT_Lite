cmake_minimum_required(VERSION 3.11)
project(BT_Lite)

find_package(Python3 COMPONENTS Interpreter)
if (NOT ${Python3_FOUND})
    message(FATAL_ERROR "Python is needed to generate sources.")
endif ()

include_directories(include)
add_executable(test src/test.cpp)

message(${Python3_EXECUTABLE})
message(${CMAKE_SOURCE_DIR}/generator/BT_generator.py)
message(${CMAKE_SOURCE_DIR}/test_gen/BT_GEN/BT_GEN.h)

add_custom_command(
    OUTPUT "${CMAKE_SOURCE_DIR}/test_gen/BT_GEN/BT_GEN.h"
    COMMAND 
        "${Python3_EXECUTABLE}" 
        "${CMAKE_SOURCE_DIR}/generator/BT_generator.py"
    DEPENDS "${CMAKE_SOURCE_DIR}/generator/BT_generator.py" "${CMAKE_SOURCE_DIR}/generator/test.xml"
    COMMENT "generating bt"
)

include_directories(test_gen)
set_property(SOURCE src/test2.cpp APPEND PROPERTY OBJECT_DEPENDS ${CMAKE_SOURCE_DIR}/test_gen/BT_GEN/BT_GEN.h)
add_executable(test2 src/test2.cpp)