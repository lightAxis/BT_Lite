#pragma once

#include "../../NodeBase.h"

namespace BT_TEST
{
    namespace NODE
    {
        template <typename T1, typename T2>
        class ACTION_CustomAction1 : public ActionBase
        {
            typedef delegate<T1(void)> _getter;
            typedef delegate<void(const T2 &)> _setter;
            typedef delegate<NodeStatus(const T1 &, T2 *, NodeBase *)> _tickDel;

        public:
            ACTION_CustomAction1(_getter b1, _setter b2, _tickDel tickDel) : ActionBase(),
                                                                             _b1_get(b1), _b2_set(b2), _tick_del(tickDel) {}
            virtual ~ACTION_CustomAction1() = default;

            Action getActionType() const override { return Action::CustomAction1; }
            char *getName() const override { return Cvt::getActionName(getActionType()); }

            NodeStatus Tick() override
            {
                printf("this is node : %s , uid : %d", getName(), getUID());
                T2 temp;
                NodeStatus result = _tick_del(_b1_get(), &temp, this);
                _b2_set(temp);
                setStatus(result);
                return getStatus();
            }

            void Reset() override {}

        private:
            _getter _b1_get;
            _setter _b2_set;
            _tickDel _tick_del;
        };
    }
}