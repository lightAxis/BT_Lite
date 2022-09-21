#pragma once

#include "../../NodeBase.h"

namespace BT_TEST
{
    namespace NODE
    {
        class DECORATOR_ForceSuccess : public DecoratorBase
        {
        public:
            DECORATOR_ForceSuccess() : DecoratorBase() {}
            virtual ~DECORATOR_ForceSuccess() = default;

            Decorator getDecoratorType() const override { return Decorator::ForceSuccess; }
            char *getName() const override { return Cvt::getDecoratorName(getDecoratorType()); }

            NodeStatus TickContent() override
            {
                _child->Tick();
                return NodeStatus::SUCCESS;
            }

        private:
        };
    }
}
