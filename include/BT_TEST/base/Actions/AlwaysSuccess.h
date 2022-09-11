#pragma once

#include "../../NodeBase.h"

namespace BT_TEST
{
    namespace NODE
    {
        class ACTION_AlwaysSuccess : public ActionBase
        {
        public:
            ACTION_AlwaysSuccess() : ActionBase() { setStatus(NodeStatus::SUCCESS); }
            virtual ~ACTION_AlwaysSuccess() = default;

            Action getActionType() const override { return Action::AlwaysSuccess; }
            char *getName() const override { return Cvt::getActionName(getActionType()); }

            NodeStatus Tick() override
            {
                printf("name:%s, uid:%d Ticked\n", getName(), getUID());
                return NodeStatus::SUCCESS;
            }

            void Reset() override {}

        private:
        };
    }
}