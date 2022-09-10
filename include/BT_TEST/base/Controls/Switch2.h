#pragma once

#include "../../NodeBase.h"

namespace BT_TEST
{
    namespace NODE
    {
        template <uint8_t ChildN, typename Variable>
        class CONTROL_Switch2 : public ControlBase<ChildN>
        {
            typedef delegate<Variable(void)> case_getter;

        public:
            CONTROL_Switch2(case_getter case1, case_getter case2, case_getter variable) : ControlBase<ChildN>(),
                                                                                          _variable_get(variable)
            {
                static_assert(ChildN == 3, "Switch node must have exact children");
                _case_gets[0] = case1;
                _case_gets[1] = case2;
            }
            virtual ~CONTROL_Switch2() = default;
            Control getControlType() const override { return Control::Switch2; }
            char *getName() const override { return Cvt::getControlName(getControlType()); }

            NodeStatus Tick() override
            {
                printf("name:%s, uid:%d Ticked\n", getName(), this->getUID());
                uint8_t child_idx = 2;
                for (uint8_t i = 0; i < 2; i++)
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
            case_getter _case_gets[2];
            case_getter _variable_get;
        };
    }
}