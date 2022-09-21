#pragma once

#include "../../NodeBase.h"

namespace BT_TEST
{
    namespace NODE
    {
        template <uint8_t ChildN, typename Variable>
        class CONTROL_Switch6 : public ControlBase<ChildN>
        {
            typedef delegate<Variable(void)> case_getter;

        public:
            CONTROL_Switch6(case_getter case1, case_getter case2, case_getter case3,
                            case_getter case4, case_getter case5, case_getter case6,
                            case_getter variable) : ControlBase<ChildN>(),
                                                    _variable_get(variable)
            {
                static_assert(ChildN == 7, "Switch6 node must have exact 7 children");
                _case_gets[0] = case1;
                _case_gets[1] = case2;
                _case_gets[2] = case3;
                _case_gets[3] = case4;
                _case_gets[4] = case5;
                _case_gets[5] = case6;
            }
            virtual ~CONTROL_Switch6() = default;
            Control getControlType() const override { return Control::Switch6; }
            char *getName() const override { return Cvt::getControlName(getControlType()); }

            NodeStatus TickContent() override
            {
                uint8_t child_idx = 6;
                for (uint8_t i = 0; i < 6; i++)
                {
                    if (_variable_get() == _case_gets[i]())
                    {
                        child_idx = i;
                        break;
                    }
                }
                NodeStatus result = this->_children[child_idx]->Tick();
                return result;
            }

        private:
            case_getter _case_gets[6];
            case_getter _variable_get;
        };
    }
}