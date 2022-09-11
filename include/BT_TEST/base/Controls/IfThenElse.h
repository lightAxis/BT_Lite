#pragma once

#include "../../NodeBase.h"

namespace BT_TEST
{
    namespace NODE
    {
        template <uint8_t ChildN>
        class CONTROL_IfThenElse : public ControlBase<ChildN>
        {
        public:
            CONTROL_IfThenElse() : ControlBase<ChildN>()
            {
                static_assert(ChildN == 3, "IfThenElse node must have exact 3 children\n");
            }
            virtual ~CONTROL_IfThenElse() = default;

            Control getControlType() const override { return Control::IfThenElse; }
            char *getName() const override { return Cvt::getControlName(getControlType()); }

            NodeStatus Tick() override
            {
                printf("name:%s, uid:%d\n", getName(), this->getUID());
                NodeStatus result{NodeStatus::IDLE};
                if (!_isRunningReactive)
                {
                    result = this->_children[0]->Tick();

                    if (result == NodeStatus::SUCCESS)
                        _child_to_tick = 1;
                    else if (result == NodeStatus::FAILURE)
                        _child_to_tick = 2;
                    else
                    {
                        this->setStatus(NodeStatus::RUNNING);
                        return this->getStatus();
                    }
                }

                result = this->_children[_child_to_tick]->Tick();
                if (result == NodeStatus::RUNNING)
                    _isRunningReactive = true;
                else
                    _isRunningReactive = false;

                this->setStatus(result);
                return this->getStatus();
            }

            void Reset() override {}

        private:
            uint8_t _child_to_tick = 0;
            bool _isRunningReactive{false};
        };
    }
}