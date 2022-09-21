#pragma once

#include "../../NodeBase.h"

namespace BT_TEST
{
    namespace NODE
    {
        template <uint8_t ChildN>
        class CONTROL_Parallel : public ControlBase<ChildN>
        {
        public:
            CONTROL_Parallel(delegate<uint8_t()> failThr, delegate<uint8_t()> succThr) : ControlBase<ChildN>(),
                                                                                         _failThr_get(failThr),
                                                                                         _succThr_get(succThr) {}
            virtual ~CONTROL_Parallel() = default;

            Control getControlType() const override { return Control::Parallel; }
            char *getName() const override { return Cvt::getControlName(getControlType()); }

            NodeStatus TickContent() override
            {
                printf("fail thr : %d, succ thr : %d\n", _failThr_get(), _succThr_get());

                uint8_t succ_count{0};
                uint8_t fail_count{0};
                NodeStatus result{NodeStatus::IDLE};

                for (uint8_t i = 0; i < this->_child_num; i++)
                {
                    result = this->_children[i]->Tick();
                    if (result == NodeStatus::SUCCESS)
                        succ_count++;
                    else if (result == NodeStatus::FAILURE)
                        fail_count++;
                }

                if (succ_count >= _succThr_get())
                {
                    return NodeStatus::SUCCESS;
                }
                else if (fail_count >= _failThr_get())
                {
                    return NodeStatus::FAILURE;
                }
                return NodeStatus::SUCCESS;
            }

        private:
            delegate<uint8_t(void)> _failThr_get;
            delegate<uint8_t(void)> _succThr_get;
        };
    }
}