#pragma once

#include "../../NodeBase.h"

namespace @(NAMESPACE)
{
    namespace NODE
    {
        class ACTION_AlwaysFailure : public ActionBase
        {
        public:
            ACTION_AlwaysFailure() : ActionBase() {}
            virtual ~ACTION_AlwaysFailure() = default;

            Action getActionType() const override { return Action::AlwaysFailure; }
            char *getName() const override { return Cvt::getActionName(getActionType()); }

            NodeStatus TickContent() override
            {
                return NodeStatus::FAILURE;
            }

        private:
        };
    }
}