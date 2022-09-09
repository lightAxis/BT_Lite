#pragma once

namespace BT_TEST
{
    enum class Control
    {
        // Groot
        Fallback = 0,
        IfThenElse = 1,
        Parallel = 2,
        ReactiveFallback = 3,
        ReactiveSequence = 4,
        Sequence = 5,
        SequenceStar = 6,
        Switch2 = 7,
        Switch3 = 8,
        Switch4 = 9,
        Switch5 = 10,
        Switch6 = 11,
        WhildDoElse = 12,

        // Custom
        CustomControl1 = 13,
        CustomControl2 = 14,
    };

    namespace Cvt
    {
        char *getControlName(Control control)
        {
            switch (control)
            {
            case Control::Fallback:
                return const_cast<char *>("Fallback");
            case Control::IfThenElse:
                return const_cast<char *>("IfThenElse");
            case Control::Parallel:
                return const_cast<char *>("Parallel");
            case Control::ReactiveFallback:
                return const_cast<char *>("ReactiveFallback");
            case Control::ReactiveSequence:
                return const_cast<char *>("ReactiveSequence");
            case Control::Sequence:
                return const_cast<char *>("Sequence");
            case Control::SequenceStar:
                return const_cast<char *>("SequenceStar");
            case Control::Switch2:
                return const_cast<char *>("Switch2");
            case Control::Switch3:
                return const_cast<char *>("Switch3");
            case Control::Switch4:
                return const_cast<char *>("Switch4");
            case Control::Switch5:
                return const_cast<char *>("Switch5");
            case Control::Switch6:
                return const_cast<char *>("Switch6");
            case Control::WhildDoElse:
                return const_cast<char *>("WhildDoElse");
            case Control::CustomControl1:
                return const_cast<char *>("CustomControl1");
            case Control::CustomControl2:
                return const_cast<char *>("CustomControl2");
            }
            return const_cast<char *>("None");
        }
    }
}