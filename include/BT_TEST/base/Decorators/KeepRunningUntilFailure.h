#pragma once

#include "../../NodeBase.h"

namespace BT_TEST
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

            NodeStatus Tick() override
            {
                NodeStatus result;

                result = _child->Tick();
                if (result != NodeStatus::FAILURE)
                {
                    setStatus(NodeStatus::RUNNING);
                    return getStatus();
                }
                setStatus(NodeStatus::FAILURE);
                return getStatus();
            }

            void Reset() override {}

        private:
        };
    }
}