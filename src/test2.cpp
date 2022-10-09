#include <stdio.h>
#include <fstream>
#include <string.h>
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
            customCond1++;
            if (customCond1 >= 5)
                return NodeStatus::FAILURE;
            return NodeStatus::SUCCESS;
        }

        NodeStatus TickDelegate4(NODE::NodeBase *node)
        {
            printf("this is node : %s, customTick4\n", node->getName());
            customCond2++;
            if (customCond2 >= 3)
                return NodeStatus::FAILURE;
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
            del.set<testTick, &testTick::TickDelegate4>(*this);
            return del;
        }

    private:
        int customCond1{0};
        int customCond2{0};
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

    BT_GEN::StatusChangeLog_t *logs;
    std::ofstream filePtr{"test.bin", std::ios::out | std::ios::binary};
    uint64_t now = 204284323;
    uint16_t logNum;

    for (int i = 0; i < 6; i++)
    {
        BT_GEN::logger.clearLogs();
        BT_GEN::RootTree.Tick();

        logs = BT_GEN::logger.getLogs();
        logNum = BT_GEN::logger.getLogSize() * sizeof(BT_GEN::StatusChangeLog_t);
        for (int i = 0; i < BT_GEN::logger.getLogSize(); i++)
        {
            printf("uid:%d, prevs:%d, stat:%d, data:%04X\n", logs[i].uid, logs[i].prev_status, logs[i].status, logs[i].data);
        }
        printf("_loggerdde_________________________\n");

        filePtr.write(reinterpret_cast<const char *>(&logNum), sizeof(uint16_t));
        filePtr.write(reinterpret_cast<const char *>(&now), sizeof(uint64_t));
        for (int i = 0; i < BT_GEN::logger.getLogSize(); i++)
        {
            filePtr.write(reinterpret_cast<const char *>(&(logs[i].data)), sizeof(uint16_t));
        }

        now = now + 1 * 1000000;
    }

    filePtr.close();

    // std::ifstream filePtr2{"test.bin", std::ios::binary};
    // char logNum2_[2];
    // uint16_t logNum2;
    // filePtr2.seekg(0, std::ios::beg);
    // filePtr2.read(logNum2_, 2);
    // memcpy(&logNum2, logNum2_, sizeof(uint16_t));

    // filePtr2.close();

    return 0;
}