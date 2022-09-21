#include <stdio.h>

#include <BT_GEN/BT_GEN.h>

namespace MY
{
    using namespace BT_GEN;

    class testTick
    {
    public:
        NodeStatus TickDelegate(const uint8_t &f, NODE::NodeBase *node)
        {
            printf("this is node : %s , customActionTick1\n", node->getName());
            printf("now state : %s\n", Cvt::getNodeStatusName(node->getStatus()));
            printf("current input : %d\n", (int)f);
            return NodeStatus::SUCCESS;
        }

        NodeStatus TickDelegate2(const int &i, int *o, NODE::NodeBase *node)
        {
            printf("this is node : %s , customActionTick2\n", node->getName());
            printf("now state : %s\n", Cvt::getNodeStatusName(node->getStatus()));
            printf("before params : %d, %d\n", i, *o);
            *o = i * 10;
            printf("after params : %d, %d\n", i, *o);
            return NodeStatus::SUCCESS;
        }

        NodeStatus TickDelegate3(NODE::NodeBase *node)
        {
            printf("this is node : %s, customTickk3\n", node->getName());
            return NodeStatus::SUCCESS;
        }

        NodeStatus TickDelegate4(NODE::NodeBase *node)
        {
            printf("this is node : %s, customTick4\n", node->getName());
            return NodeStatus::SUCCESS;
        }

        delegate<NodeStatus(const uint8_t &, NODE::NodeBase *)> makeTickDel()
        {
            delegate<NodeStatus(const uint8_t &, NODE::NodeBase *)> del;
            del.set<testTick, &testTick::TickDelegate>(*this);
            return del;
        }

        delegate<NodeStatus(const int &, int *, NODE::NodeBase *)> makeTickDel2()
        {
            delegate<NodeStatus(const int &, int *, NODE::NodeBase *)> del;
            del.set<testTick, &testTick::TickDelegate2>(*this);
            return del;
        }

        delegate<NodeStatus(NODE::NodeBase *)> makeTickDel3()
        {
            delegate<NodeStatus(NODE::NodeBase *)> del;
            del.set<testTick, &testTick::TickDelegate3>(*this);
            return del;
        }

        delegate<NodeStatus(NODE::NodeBase *)> makeTickDel4()
        {
            delegate<NodeStatus(NODE::NodeBase *)> del;
            del.set<testTick, &testTick::TickDelegate3>(*this);
            return del;
        }

    private:
    };
}

int main(int argc, char **argv)
{
    MY::testTick tickk;

    BT_GEN::RootTree.set_CustomAction1_tickDel(tickk.makeTickDel());
    BT_GEN::RootTree.set_CustomAction2_tickDel(tickk.makeTickDel2());
    BT_GEN::RootTree.set_CustomCondition1_tickDel(tickk.makeTickDel3());
    BT_GEN::RootTree.set_CustomCondition2_tickDel(tickk.makeTickDel4());

    BT_GEN::RootTree.build();

    BT_GEN::RootTree.Tick();

    return 0;
}