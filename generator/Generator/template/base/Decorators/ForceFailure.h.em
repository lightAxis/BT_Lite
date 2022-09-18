#pragma once

#include "../../NodeBase.h"

namespace @(NAMESPACE)
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

            NodeStatus Tick() override
            {
                printf("name:%s, uid:%d Ticked\n", getName(), this->getUID());
                _child->Tick();
                setStatus(NodeStatus::FAILURE);
                return getStatus();
            }

            void Reset() override {}

        private:
        };
    }
}
