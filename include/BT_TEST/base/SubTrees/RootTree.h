#pragma once

#include "../../NodeBase.h"

namespace BT_TEST
{
    namespace NODE
    {
        class SUBTREE_RootTree : public SubTreeBase
        {
        public:
            SUBTREE_RootTree() : SubTreeBase() {}
            virtual ~SUBTREE_RootTree() = default;

            SubTree getSubTreeType() const override { return SubTree::RootTree; }
            char *getName() const override { return Cvt::getSubTreeName(getSubTreeType()); }

            NodeStatus TickContent() override
            {
                NodeStatus result = _child->Tick();
                return result;
            }
        };
    }
}