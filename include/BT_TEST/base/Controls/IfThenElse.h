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
                NodeStatus result = this->_children[0]->Tick();
                if (result == NodeStatus::SUCCESS)
                {
                    result = this->_children[1]->Tick();
                    this->setStatus(result);
                    return this->getStatus();
                }
                else if (result == NodeStatus::FAILURE)
                {
                    result = this->_children[2]->Tick();
                    this->setStatus(result);
                    return this->getStatus();
                }
                this->setStatus(NodeStatus::RUNNING);
                return this->getStatus();
            }

            void Reset() override
            {
            }

        private:
        };
    }
}