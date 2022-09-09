#pragma once

namespace BT_TEST
{
    enum class NodeStatus
    {
        IDLE = 0,
        RUNNING = 1,
        SUCCESS = 2,
        FAILURE = 3,
    };

    enum class NodeType
    {
        UNDEFINED = 0,
        ACTION = 1,
        CONDITION = 2,
        CONTROL = 3,
        DECORATOR = 4,
        SUBTREE = 5,
    };

    enum class PortDirection
    {
        INPUT = 0,
        OUTPUT = 1,
        INOUT = 2,
    };

    namespace Cvt
    {
        char *getNodeStatusName(NodeStatus status)
        {
            switch (status)
            {
            case NodeStatus::IDLE:
                return const_cast<char *>("IDLE");
            case NodeStatus::RUNNING:
                return const_cast<char *>("RUNNING");
            case NodeStatus::SUCCESS:
                return const_cast<char *>("SUCCESS");
            case NodeStatus::FAILURE:
                return const_cast<char *>("FAILURE");
            }
            return const_cast<char *>("None");
        }

        char *getNodeTypeName(NodeType type)
        {
            switch (type)
            {
            case NodeType::UNDEFINED:
                return const_cast<char *>("UNDEFINED");
            case NodeType::ACTION:
                return const_cast<char *>("ACTION");
            case NodeType::CONDITION:
                return const_cast<char *>("CONDITION");
            case NodeType::CONTROL:
                return const_cast<char *>("CONTROL");
            case NodeType::DECORATOR:
                return const_cast<char *>("DECORATOR");
            case NodeType::SUBTREE:
                return const_cast<char *>("SUBTREE");
            }
            return const_cast<char *>("None");
        }

        char *getPortDirectionName(PortDirection direction)
        {
            switch (direction)
            {
            case PortDirection::INPUT:
                return const_cast<char *>("INPUT");
            case PortDirection::OUTPUT:
                return const_cast<char *>("OUTPUT");
            case PortDirection::INOUT:
                return const_cast<char *>("NOUT");
            }
            return const_cast<char *>("None");
        }
    }
}