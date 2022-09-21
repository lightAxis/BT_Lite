#pragma once

#include "../../NodeBase.h"

namespace BT_TEST
{
    namespace NODE
    {
        template <uint8_t ChildN>
        class CONTROL_SequenceStar : public ControlBase<ChildN>
        {
        public:
            CONTROL_SequenceStar() : ControlBase<ChildN>() {}
            virtual ~CONTROL_SequenceStar() = default;

            Control getControlType() const override { return Control::SequenceStar; }
            char *getName() const override { return Cvt::getControlName(getControlType()); }

            NodeStatus TickContent() override
            {
                for (uint8_t i = _last_child_idx; i < this->_child_num; i++)
                {
                    NodeStatus result = this->_children[i]->Tick();
                    if (result == NodeStatus::FAILURE)
                    {
                        _last_child_idx = i;
                        return NodeStatus::FAILURE;
                    }
                    else if (result == NodeStatus::RUNNING)
                    {
                        _last_child_idx = i;
                        return NodeStatus::RUNNING;
                    }
                }
                _last_child_idx = 0;
                return NodeStatus::SUCCESS;
            }

        private:
            uint8_t _last_child_idx{0};
        };
    }
}