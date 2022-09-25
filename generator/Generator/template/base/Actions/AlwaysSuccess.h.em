#pragma once

#include "../../NodeBase.h"

namespace @(NAMESPACE)
{
    namespace NODE
    {
        class ACTION_AlwaysSuccess : public ActionBase
        {
        public:
            ACTION_AlwaysSuccess() : ActionBase() {}
            virtual ~ACTION_AlwaysSuccess() = default;

            Action getActionType() const override { return Action::AlwaysSuccess; }
            char *getName() const override { return Cvt::getActionName(getActionType()); }

            NodeStatus TickContent() override
            {
                return NodeStatus::SUCCESS;
            }

        private:
        };
    }
}