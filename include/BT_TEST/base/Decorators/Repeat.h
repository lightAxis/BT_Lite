#pragma once

#include "../../NodeBase.h"

namespace BT_TEST
{
    namespace NODE
    {
        class DECORATOR_Repeat : public DecoratorBase
        {
            typedef delegate<uint8_t(void)> repeat_getter;

        public:
            DECORATOR_Repeat(repeat_getter repeat_get) : DecoratorBase(),
                                                         _repeat_get(repeat_get) {}
            virtual ~DECORATOR_Repeat() = default;

            Decorator getDecoratorType() const override { return Decorator::Repeat; }
            char *getName() const override { return Cvt::getDecoratorName(getDecoratorType()); }

            NodeStatus Tick() override
            {
                uint8_t repeatNum = _repeat_get();
                NodeStatus result;

                for (uint8_t i = 0; i < repeatNum; i++)
                {
                    result = _child->Tick();
                    if (result != NodeStatus::SUCCESS)
                    {
                        setStatus(result);
                        return getStatus();
                        break;
                    }
                }
                setStatus(NodeStatus::SUCCESS);
                return getStatus();
            }

            void Reset() override {}

        private:
            repeat_getter _repeat_get;
        };
    }
}