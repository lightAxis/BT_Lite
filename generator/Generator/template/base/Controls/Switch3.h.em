#pragma once

#include "../../NodeBase.h"

namespace @(NAMESPACE)
{
    namespace NODE
    {
        template <uint8_t ChildN, typename Variable>
        class CONTROL_Switch3 : public ControlBase<ChildN>
        {
            typedef delegate<Variable(void)> case_getter;

        public:
            CONTROL_Switch3(case_getter case1, case_getter case2, case_getter case3,
                            case_getter variable) : ControlBase<ChildN>(),
                                                    _variable_get(variable)
            {
                static_assert(ChildN == 4, "Switch3 node must have exact 4 children");
                _case_gets[0] = case1;
                _case_gets[1] = case2;
                _case_gets[2] = case3;
            }
            virtual ~CONTROL_Switch3() = default;
            Control getControlType() const override { return Control::Switch3; }
            char *getName() const override { return Cvt::getControlName(getControlType()); }

            NodeStatus Tick() override
            {
                printf("name:%s, uid:%d Ticked\n", getName(), this->getUID());
                uint8_t child_idx = 3;
                for (uint8_t i = 0; i < 3; i++)
                {
                    if (_variable_get() == _case_gets[i]())
                    {
                        child_idx = i;
                        break;
                    }
                }
                NodeStatus result = this->_children[child_idx]->Tick();
                this->setStatus(result);
                return this->getStatus();
            }
            void Reset() override {}

        private:
            case_getter _case_gets[3];
            case_getter _variable_get;
        };
    }
}