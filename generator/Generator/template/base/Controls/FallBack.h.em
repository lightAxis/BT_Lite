#pragma once

#include "../../NodeBase.h"

namespace @(NAMESPACE)
{
    namespace NODE
    {
        template <uint8_t ChildN>
        class CONTROL_Fallback : public ControlBase<ChildN>
        {
        public:
            CONTROL_Fallback() : ControlBase<ChildN>() {}
            virtual ~CONTROL_Fallback() = default;

            Control getControlType() const override { return Control::Fallback; }
            char *getName() const override { return Cvt::getControlName(getControlType()); }

            NodeStatus TickContent() override
            {
                for (uint8_t i = _last_child_idx; i < this->_child_num; i++)
                {
                    NodeStatus result = this->_children[i]->Tick();
                    if (result == NodeStatus::SUCCESS)
                    {
                        _last_child_idx = 0;
                        return NodeStatus::SUCCESS;
                    }
                    else if (result == NodeStatus::RUNNING)
                    {
                        _last_child_idx = i;
                        return NodeStatus::RUNNING;
                    }
                }
                _last_child_idx = 0;
                return NodeStatus::FAILURE;
            }

        private:
            uint8_t _last_child_idx{0};
        };
    }
}