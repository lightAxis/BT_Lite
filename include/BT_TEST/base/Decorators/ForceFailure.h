#pragma once

#include "../../NodeBase.h"

namespace BT_TEST
{
    namespace NODE
    {
        class DECORATOR_ForceFailure : public DecoratorBase
        {
        public:
            DECORATOR_ForceFailure() : DecoratorBase() {}
            virtual ~DECORATOR_ForceFailure() = default;

            Decorator getDecoratorType() const override { return Decorator::ForceFailure; }
            char *getName() const override { return Cvt::getDecoratorName(getDecoratorType()); }

            NodeStatus TickContent() override
            {
                _child->Tick();
                return NodeStatus::FAILURE;
            }

        private:
        };
    }
}
