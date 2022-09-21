#pragma once

#include "../../NodeBase.h"

namespace BT_TEST
{
    namespace NODE
    {
        class ACTION_CustomAction2 : public ActionBase
        {
            typedef delegate<float(void)> _getter;
            typedef delegate<void(const float &)> _setter;

        public:
            typedef delegate<NodeStatus(const float &, float *, NodeBase *)> _tickDel;
            ACTION_CustomAction2(_getter b1, _setter b2, _tickDel *tickDel) : ActionBase(),
                                                                              _b1_get(b1), _b2_set(b2), _tick_del(tickDel) {}
            virtual ~ACTION_CustomAction2() = default;

            Action getActionType() const override { return Action::CustomAction2; }
            char *getName() const override { return Cvt::getActionName(getActionType()); }

            NodeStatus TickContent() override
            {
                float temp;
                NodeStatus result = (*_tick_del)(_b1_get(), &temp, this);
                _b2_set(temp);
                return result;
            }

        private:
            _getter _b1_get;
            _setter _b2_set;
            _tickDel *_tick_del;
        };
    }
}