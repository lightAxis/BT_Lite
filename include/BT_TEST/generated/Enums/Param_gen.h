#pragma once

namespace BT_TEST
{
    enum class Param
    {
        // Groot
        Const = 0,

        // Custom
        b1__int = 1,
        b2__int = 2,
        b3__float = 3,
        b4__float = 4,
    };

    namespace Cvt
    {
        char *getParamName(Param param)
        {
            switch (param)
            {
            case Param::Const:
                return const_cast<char *>("Const");
            case Param::b1__int:
                return const_cast<char *>("b1__int");
            case Param::b2__int:
                return const_cast<char *>("b2__int");
            case Param::b3__float:
                return const_cast<char *>("b3__float");
            case Param::b4__float:
                return const_cast<char *>("b4__float");
            }
            return const_cast<char *>("None");
        }
    }
}