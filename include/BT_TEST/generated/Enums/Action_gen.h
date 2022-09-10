#pragma once

namespace BT_TEST
{
    enum class Action
    {
        // Groot
        AlwaysFailure = 0,
        AlwaysSuccess = 1,
        SetBlackBoard = 2,

        // Custom
        CustomAction1 = 3,
        CustomAction2 = 4,
    };

    namespace Cvt
    {
        char *getActionName(Action action)
        {
            switch (action)
            {
            case Action::AlwaysFailure:
                return const_cast<char *>("AlwaysFailure");
            case Action::AlwaysSuccess:
                return const_cast<char *>("AlwaysSuccess");
            case Action::SetBlackBoard:
                return const_cast<char *>("SetBlackBoard");
            case Action::CustomAction1:
                return const_cast<char *>("CustomAction1");
            case Action::CustomAction2:
                return const_cast<char *>("CustomAction2");
            }
            return const_cast<char *>("None");
        }
    }
}