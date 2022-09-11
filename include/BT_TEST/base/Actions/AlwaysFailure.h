#pragma once

#include "../../NodeBase.h"

namespace BT_TEST
{
    namespace NODE
    {
        class ACTION_AlwaysFailure : public ActionBase
        {
        public:
            ACTION_AlwaysFailure() : ActionBase() { setStatus(NodeStatus::FAILURE); }
            virtual ~ACTION_AlwaysFailure() = default;

            Action getActionType() const override { return Action::AlwaysFailure; }
            char *getName() const override { return Cvt::getActionName(getActionType()); }

            NodeStatus Tick() override
            {
                printf("name:%s, uid:%d Ticked\n", getName(), getUID());
                return NodeStatus::FAILURE;
            }

            void Reset() override {}

        private:
        };
    }
}