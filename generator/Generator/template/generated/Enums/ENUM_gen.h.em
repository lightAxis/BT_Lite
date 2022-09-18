#pragma once

@# global spec
@# 'NAMESPACE': str
@# 'Base_Dict': Dict[str, int]
@# 'Custom_Dict': Dict[str, int]
@# 'EnumName': str
@# 

namespace @(NAMESPACE)
{
    enum class @(EnumName)
    {
        // Groot
@[for enum in Base_Dict.keys()]@
        @(enum) = @(Base_Dict[enum]),
@[end for]
        // Custom
@[for enum in Custom_Dict.keys()]@
        @(enum) = @(Custom_Dict[enum]),
@[end for]
    };

    namespace Cvt
    {
        char *get@(EnumName)Name(@(EnumName) @(EnumName)_)
        {
            switch (@(EnumName)_)
            {
@[for enum in Base_Dict.keys()]@
            case @(EnumName)::@(enum):
                return const_cast<char *>("@(enum)");
@[end for]
@[for enum in Custom_Dict.keys()]@
            case @(EnumName)::@(enum):
                return const_cast<char *>("@(enum)");
@[end for]
            }
            return const_cast<char *>("None");
        }
    }
}