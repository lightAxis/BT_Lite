#pragma once

#include "../../NodeBase.h"

namespace BT_TEST
{
    namespace NODE
    {
        class ACTION_CustomAction1 : public ActionBase
        {
            typedef delegate<float(void)> _getter;
            typedef delegate<void(const int &)> _setter;

        public:
            typedef delegate<NodeStatus(const float &, int *, NodeBase *)> _tickDel;
            ACTION_CustomAction1(_getter b1, _setter b2, _tickDel *tickDel) : ActionBase(),
                                                                              _b1_get(b1), _b2_set(b2), _tick_del(tickDel) {}
            virtual ~ACTION_CustomAction1() = default;

            Action getActionType() const override { return Action::CustomAction1; }
            char *getName() const override { return Cvt::getActionName(getActionType()); }

            NodeStatus Tick() override
            {
                printf("name:%s, uid:%d Ticked\n", getName(), getUID());
                int temp;
                NodeStatus result = (*_tick_del)(_b1_get(), &temp, this);
                _b2_set(temp);
                setStatus(result);
                return getStatus();
            }

            void Reset() override {}

        private:
            _getter _b1_get;
            _setter _b2_set;
            _tickDel *_tick_del;
        };
    }
}