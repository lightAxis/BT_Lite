#pragma once

#include "../../NodeBase.h"

namespace @(NAMESPACE)
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

            NodeStatus Tick() override
            {
                printf("name:%s, uid:%d\n", getName(), this->getUID());
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
                    this->setStatus(NodeStatus::SUCCESS);
                    return this->getStatus();
                }
                else if (fail_count >= _failThr_get())
                {
                    this->setStatus(NodeStatus::FAILURE);
                    return this->getStatus();
                }
                this->setStatus(NodeStatus::RUNNING);
                return this->getStatus();
            }

            void Reset() override {}

        private:
            delegate<uint8_t(void)> _failThr_get;
            delegate<uint8_t(void)> _succThr_get;
        };
    }
}