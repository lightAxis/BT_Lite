#pragma once

#include "../../NodeBase.h"

namespace @(NAMESPACE)
{
    namespace NODE
    {
        class DECORATOR_KeepRunningUntilFailure : public DecoratorBase
        {
        public:
            DECORATOR_KeepRunningUntilFailure() : DecoratorBase() {}
            virtual ~DECORATOR_KeepRunningUntilFailure() = default;

            Decorator getDecoratorType() const override { return Decorator::KeepRunningUntilFailure; }
            char *getName() const override { return Cvt::getDecoratorName(getDecoratorType()); }

            NodeStatus TickContent() override
            {
                NodeStatus result;

                result = _child->Tick();
                if (result != NodeStatus::FAILURE)
                {
                    return NodeStatus::RUNNING;
                }
                return NodeStatus::FAILURE;
            }

        private:
        };
    }
}