#pragma once

#include "../../NodeBase.h"

namespace BT_TEST
{
    namespace NODE
    {
        class ACTION_CustomAction1 : public ActionBase
        {
            typedef delegate<float(void)> _getter_b1;
            typedef delegate<void(const int &)> _setter_b2;

        public:
            typedef delegate<NodeStatus(const float &, int *, NodeBase *)> TickDel;
            ACTION_CustomAction1(_getter_b1 b1, _setter_b2 b2, TickDel *tickDel) : ActionBase(),
                                                                                   _get_b1(b1), _set_b2(b2), _tickDel(tickDel) {}
            virtual ~ACTION_CustomAction1() = default;

            Action getActionType() const override { return Action::CustomAction1; }
            char *getName() const override { return Cvt::getActionName(getActionType()); }

            NodeStatus TickContent() override
            {
                int temp;
                NodeStatus result = (*_tickDel)(_get_b1(), &temp, this);
                _set_b2(temp);
                return result;
            }

        private:
            _getter_b1 _get_b1;
            _setter_b2 _set_b2;
            TickDel *_tickDel;
        };
    }
}