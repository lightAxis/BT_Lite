#include <stdio.h>

#include <BT_TEST/BT_TEST.h>

namespace MY
{
    using namespace BT_TEST;

    class testTick
    {
    public:
        NodeStatus TickDelegate(const float &f, int *i, NODE::NodeBase *node)
        {
            printf("this is node : %s , customActionTick\n", node->getName());
            printf("now state : %s\n", Cvt::getNodeStatusName(node->getStatus()));
            printf("%f, %d\n", f, *i);
            *i = f * 10;
            printf("%f, %d\n", f, *i);
            return NodeStatus::SUCCESS;
        }

        NodeStatus TickDelegate2(const float &f, float *i, NODE::NodeBase *node)
        {
            printf("this is node : %s , customActionTick\n", node->getName());
            printf("now state : %s\n", Cvt::getNodeStatusName(node->getStatus()));
            printf("%f, %f\n", f, *i);
            *i = f * 10;
            printf("%f, %f\n", f, *i);
            return NodeStatus::SUCCESS;
        }

        delegate<NodeStatus(const float &, int *, NODE::NodeBase *)> makeTickDel()
        {
            delegate<NodeStatus(const float &, int *, NODE::NodeBase *)> del;
            del.set<testTick, &testTick::TickDelegate>(*this);
            return del;
        }

        delegate<NodeStatus(const float &, float *, NODE::NodeBase *)> makeTickDel2()
        {
            delegate<NodeStatus(const float &, float *, NODE::NodeBase *)> del;
            del.set<testTick, &testTick::TickDelegate2>(*this);
            return del;
        }

    private:
    };
}

int main(int argc, char **argv)
{
    MY::testTick tickk;

    BT_TEST::RootTree.set_CustomAction1_tickDel(tickk.makeTickDel());
    BT_TEST::RootTree.set_CustomAction2_tickDel(tickk.makeTickDel2());

    BT_TEST::RootTree.build();

    BT_TEST::StatusChangeLog_t *logs;
    int logCount = 0;
    for (int i = 0; i < 3; i++)
    {
        BT_TEST::logger.clearLogs();
        BT_TEST::RootTree.Tick();
        logs = BT_TEST::logger.getLogs();
        logCount = BT_TEST::logger.getLogSize();
    }
    return 0;
}