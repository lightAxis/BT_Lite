#pragma once

namespace BT_TEST
{
    enum class Condition
    {
        // Groot

        // Custom
        CustomCondition1 = 0,
        CustomCondition2 = 1,
    };

    namespace Cvt
    {
        char *getConditionName(Condition condition)
        {
            switch (condition)
            {
            case Condition::CustomCondition1:
                return const_cast<char *>("CustomCondition1");
            case Condition::CustomCondition2:
                return const_cast<char *>("CustomCondition2");
            }
            return const_cast<char *>("None");
        }
    }
}