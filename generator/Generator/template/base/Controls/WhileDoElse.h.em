#pragma once

#include "../../NodeBase.h"

namespace @(NAMESPACE)
{
    namespace NODE
    {
        template <uint8_t ChildN>
        class CONTROL_WhileDoElse : public ControlBase<ChildN>
        {
        public:
            CONTROL_WhileDoElse() : ControlBase<ChildN>()
            {
                static_assert(ChildN == 3, "WhildDoElse node must have exact 3 children");
            }
            virtual ~CONTROL_WhileDoElse() = default;

            Control getControlType() const override { return Control::WhileDoElse; }
            char *getName() const override { return Cvt::getControlName(getControlType()); }

            NodeStatus TickContent() override
            {
                printf("name:%s, uid:%d\n", getName(), this->getUID());
                NodeStatus result = this->_children[0]->Tick();
                uint8_t _child_to_tick{0};
                if (result == NodeStatus::SUCCESS)
                    _child_to_tick = 1;
                else if (result == NodeStatus::FAILURE)
                    _child_to_tick = 2;
                else
                {
                    return NodeStatus::RUNNING;
                }

                result = this->_children[_child_to_tick]->Tick();
                return result;
            }

        private:
        };
    }
}