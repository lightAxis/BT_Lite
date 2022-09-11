#pragma once

#include "generated/Tree_gen.h"

namespace BT_TEST
{

    namespace NODE
    {
        class AlwaysRunning : public ActionBase
        {
        public:
            AlwaysRunning() : ActionBase() {}
            virtual ~AlwaysRunning() = default;

            Action getActionType() const override { return Action::CustomAction1; }
            char *getName() const override { return Cvt::getActionName(getActionType()); }
            NodeStatus Tick() override
            {
                printf("name:%s, uid:%d Ticked\n", getName(), this->getUID());
                return getStatus();
            }
            void Reset() override {}

        private:
        };

        class testTick
        {
        public:
            NodeStatus TickDelegate(const float &f, int *i, NodeBase *node)
            {
                printf("this is node : %s , customActionTick\n", node->getName());
                printf("now state : %s\n", Cvt::getNodeStatusName(node->getStatus()));
                printf("%f, %d\n", f, *i);
                *i = f * 10;
                printf("%f, %d\n", f, *i);
                return NodeStatus::SUCCESS;
            }

            delegate<NodeStatus(const float &, int *, NodeBase *)> makeTickDel()
            {
                delegate<NodeStatus(const float &, int *, NodeBase *)> del;
                del.set<testTick, &testTick::TickDelegate>(*this);
                return del;
            }
        };

    }

    static void
    test()
    {
        NODE::CONTROL_IfThenElse<3> ifthenelse;

        NODE::ACTION_AlwaysSuccess succ1;
        NODE::ACTION_AlwaysFailure fail1;
        NODE::AlwaysRunning runn1;
        runn1.setStatus(NodeStatus::RUNNING);

        PARAM::PARAM_Const_uint8_t u1(5);
        PARAM::PARAM_Const_uint8_t u2(3);
        PARAM::PARAM_Const_uint8_t u3(32);

        PARAM::PARAM_b1 b1;
        b1.set(34);
        PARAM::PARAM_b3 b3;
        b3.set(533);

        NODE::testTick asdfadsf;

        NODE::ACTION_CustomAction1::_tickDel ACTION_CustomAction_tickDel;
        ACTION_CustomAction_tickDel = asdfadsf.makeTickDel();

        return;
    }

    static Tree RootTree;
}
