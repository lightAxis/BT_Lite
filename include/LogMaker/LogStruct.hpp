#pragma once

#include <stdint.h>
#include <vector>

enum class eNodeStatus
{
    IDEL = 0,
    RUNNING,
    SUCCESS,
    FAILURE
};

enum class eNodeType
{
    UNDEFINED = 0,
    ACTION,
    CONDITION,
    CONTROL,
    DECORATOR,
    SUBTREE
};

enum class ePortDirection
{
    INPUT = 0,
    OUTPUT,
    INOUT
};

struct PortModel_t
{
    std::string port_name;
    ePortDirection direction;
    std::string type_info;
    std::string description;
};

struct PortConfig_t
{
    std::string port_name;
    std::string remap;
};

struct TreeNode_t
{
    uint16_t uid;
    std::vector<uint16_t> children_uid;
    eNodeStatus status;
    std::string instance_name;
    std::string registration_name;
    std::vector<PortConfig_t> port_remaps;
};

struct NodeModel_t
{
    std::string registration_name;
    eNodeType type;
    std::vector<PortModel_t> ports;
}

struct BehaviorTree_t
{
    uint16_t root_uid;
    std::vector<TreeNode_t> nodes;
    std::vector<NodeModel_t> node_models;
}

struct Timestamp_t
{
    uint16_t usec_since_epoch;
}

struct StatusChange_t
{
    uint16_t uid;
    eNodeStatus prev_status;
    eNodeStatus status;
    Timestamp_t timestamp;
}

struct StatusChangeLog_t
{
    BehaviorTree_t
}