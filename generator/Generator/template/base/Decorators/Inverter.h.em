#pragma once

#include "../../NodeBase.h"

namespace @(NAMESPACE)
{
    namespace NODE
    {
        class DECORATOR_Inverter : public DecoratorBase
        {
        public:
            DECORATOR_Inverter() : DecoratorBase() {}
            virtual ~DECORATOR_Inverter() = default;

            Decorator getDecoratorType() const override { return Decorator::Inverter; }
            char *getName() const override { return Cvt::getDecoratorName(getDecoratorType()); }

            NodeStatus Tick() override
            {
                printf("name:%s, uid:%d Ticked\n", getName(), this->getUID());
                NodeStatus result = _child->Tick();
                if (result == NodeStatus::SUCCESS)
                    result = NodeStatus::FAILURE;
                else if (result == NodeStatus::FAILURE)
                    result = NodeStatus::SUCCESS;
                else
                    result = NodeStatus::RUNNING;

                setStatus(result);
                return getStatus();
            }

            void Reset() override {}

        private:
        };
    }
}
