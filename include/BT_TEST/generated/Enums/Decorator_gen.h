#pragma once

namespace BT_TEST
{
    enum class Decorator
    {
        // Groot
        BlackboardCheckBool = 1,
        BlackboardCheckDouble = 2,
        BlackboardCheckInt = 3,
        BlackboardCheckString = 4,
        Delay = 5,
        ForceFailure = 6,
        ForceSuccess = 7,
        Inverter = 8,
        KeepRunningUntilFailure = 9,
        Repeat = 10,
        RetryUntilSuccessful = 11,
        Timeout = 12,

        // Custom
        CustomDecorator1 = 13,
        CustomDecorator2 = 14,
    };

    namespace Cvt
    {
        char *getDecoratorName(Decorator decorator)
        {
            switch (decorator)
            {
            case Decorator::BlackboardCheckBool:
                return const_cast<char *>("BlackboardCheckBool");
            case Decorator::BlackboardCheckDouble:
                return const_cast<char *>("BlackboardCheckDouble");
            case Decorator::BlackboardCheckInt:
                return const_cast<char *>("BlackboardCheckInt");
            case Decorator::BlackboardCheckString:
                return const_cast<char *>("BlackboardCheckString");
            case Decorator::Delay:
                return const_cast<char *>("Delay");
            case Decorator::ForceFailure:
                return const_cast<char *>("ForceFailure");
            case Decorator::ForceSuccess:
                return const_cast<char *>("ForceSuccess");
            case Decorator::Inverter:
                return const_cast<char *>("Inverter");
            case Decorator::KeepRunningUntilFailure:
                return const_cast<char *>("KeepRunningUntilFailure");
            case Decorator::Repeat:
                return const_cast<char *>("Repeat");
            case Decorator::RetryUntilSuccessful:
                return const_cast<char *>("RetryUntilSuccessful");
            case Decorator::Timeout:
                return const_cast<char *>("Timeout");
            case Decorator::CustomDecorator1:
                return const_cast<char *>("CustomDecorator1");
            case Decorator::CustomDecorator2:
                return const_cast<char *>("CustomDecorator2");
            }
            return const_cast<char *>("None");
        }
    }
}