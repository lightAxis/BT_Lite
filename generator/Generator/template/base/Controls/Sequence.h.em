#pragma once

#include "../../NodeBase.h"

namespace @(NAMESPACE)
{
    namespace NODE
    {
        template <uint8_t ChildN>
        class CONTROL_Sequence : public ControlBase<ChildN>
        {
        public:
            CONTROL_Sequence() : ControlBase<ChildN>() {}
            virtual ~CONTROL_Sequence() = default;

            Control getControlType() const override { return Control::Sequence; }
            char *getName() const override { return Cvt::getControlName(getControlType()); }

            NodeStatus Tick() override
            {
                printf("name:%s, uid:%d Ticked\n", getName(), this->getUID());
                for (uint8_t i = _last_child_idx; i < this->_child_num; i++)
                {
                    NodeStatus result = this->_children[i]->Tick();
                    if (result == NodeStatus::FAILURE)
                    {
                        _last_child_idx = 0;
                        this->setStatus(NodeStatus::FAILURE);
                        return this->getStatus();
                    }
                    else if (result == NodeStatus::RUNNING)
                    {
                        _last_child_idx = i;
                        this->setStatus(NodeStatus::RUNNING);
                        return this->getStatus();
                    }
                }
                _last_child_idx = 0;
                this->setStatus(NodeStatus::SUCCESS);
                return this->getStatus();
            }

            void Reset() override {}

        private:
            uint8_t _last_child_idx{0};
        };
    }
}