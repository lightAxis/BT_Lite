#pragma once

#include "../../NodeBase.h"

namespace BT_TEST
{
    namespace NODE
    {
        class DECORATOR_Delay : public DecoratorBase
        {
        public:
            DECORATOR_Delay() : DecoratorBase() {}
            virtual ~DECORATOR_Delay() = default;

            Decorator getDecoratorType() const override { return Decorator::Delay; }
            char *getName() const override { return Cvt::getDecoratorName(getDecoratorType()); }

            NodeStatus Tick() override
            {
                printf("name:%s, uid:%d Ticked\n", getName(), this->getUID());
                assert(0); // Delay node is not implemented
                return NodeStatus::FAILURE;
            }

            void Reset() override {}

        private:
        };
    }
}
