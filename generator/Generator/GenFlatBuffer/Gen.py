#!usr/bin/env python3

from dataclasses import dataclass
from typing import List, Dict, Tuple

from GrootXMLParser import EnumsStructs
import os

from .flatbuffer_python import flatbuffers
from .LogSerialization import BehaviorTree
from .LogSerialization import NodeModel
from .LogSerialization import NodeStatus
from .LogSerialization import NodeType
from .LogSerialization import PortConfig
from .LogSerialization import PortDirection
from .LogSerialization import PortModel
from .LogSerialization import StatusChange
from .LogSerialization import StatusChangeLog
from .LogSerialization import Timestamp
from .LogSerialization import TreeNode


def Generate(input: EnumsStructs.GenerationIngredients_t):
    builder = flatbuffers.Builder(100)

    nodes_List = []
    for treenode in input.ParsedGroot.TotalTree:
        nodes_List.append(__MakeNode(treenode, builder))
    BehaviorTree.StartNodesVector(builder, len(nodes_List))
    for node in nodes_List:
        builder.PrependUOffsetTRelative(node)
    TreeNodes = builder.EndVector()

    nodeModels_List = []
    for model in input.CustomGenerations.Actions:
        nodeModels_List.append(__MakeNodeModel(model, builder))
    for model in input.CustomGenerations.Conditions:
        nodeModels_List.append(__MakeNodeModel(model, builder))
    for model in input.CustomGenerations.Controls:
        nodeModels_List.append(__MakeNodeModel(model, builder))
    for model in input.CustomGenerations.Decorators:
        nodeModels_List.append(__MakeNodeModel(model, builder))
    for model in input.CustomGenerations.SubTrees:
        nodeModels_List.append(__MakeNodeModel(model, builder))
    BehaviorTree.StartNodeModelsVector(builder, len(nodeModels_List))
    for nodemodel in nodeModels_List:
        builder.PrependUOffsetTRelative(nodemodel)
    NodeModels = builder.EndVector()

    BehaviorTree.Start(builder)
    BehaviorTree.AddRootUid(builder, 1)
    BehaviorTree.AddNodes(builder, TreeNodes)
    BehaviorTree.AddNodeModels(builder, NodeModels)
    BT = BehaviorTree.End(builder)

    builder.Finish(BT)
    buf = builder.Output()

    buffer = open("Tree.fbl", 'wb')
    buffer.write(buf)
    buffer.close()

    pass


def __MakeNode(node: EnumsStructs.TotalTree_t, builder: flatbuffers.Builder):

    childrenUID = __MakeChildrenUID(node, builder)
    portRemaps = __MakePortRemap(node, builder)
    instanceName = builder.CreateString(node.Name)
    registrationName = builder.CreateString(node.Name)
    TreeNode.Start(builder)
    TreeNode.AddUid(builder, node.UID)
    TreeNode.AddChildrenUid(builder, childrenUID)
    TreeNode.AddStatus(builder, NodeStatus.NodeStatus.IDLE)
    TreeNode.AddInstanceName(builder, instanceName)
    TreeNode.AddRegistrationName(builder, registrationName)
    TreeNode.AddPortRemaps(builder, portRemaps)
    return TreeNode.End(builder)
    pass


def __MakeChildrenUID(node: EnumsStructs.TotalTree_t, builder: flatbuffers.Builder):
    TreeNode.StartChildrenUidVector(
        builder, len(node.Children))
    for uid in node.Children:
        builder.PrependUOffsetTRelative(uid)
    return builder.EndVector()
    pass


def __MakePortRemap(node: EnumsStructs.TotalTree_t, builder: flatbuffers.Builder):
    ports = []

    for key in node.Attrib.keys():
        if key == "ID":
            continue

        portName = builder.CreateString(key)
        remap = builder.CreateString(node.Attrib[key])
        PortConfig.Start(builder)
        PortConfig.AddPortName(builder, portName)
        PortConfig.AddRemap(builder, remap)
        tempPortConfig = PortConfig.End(builder)
        ports.append(tempPortConfig)

    TreeNode.StartPortRemapsVector(builder, len(ports))
    for port in ports:
        builder.PrependUOffsetTRelative(port)
    return builder.EndVector()
    pass


def __MakeNodeModel(customNode: EnumsStructs.TreeNodesModel_t, builder: flatbuffers.Builder):
    ports = __MakePort(customNode, builder)
    registrationName = builder.CreateString(customNode.ID)
    NodeModel.Start(builder)
    NodeModel.AddRegistrationName(builder, registrationName)
    NodeModel.AddType(builder, __ConvertNodeType(customNode.NodeType))
    NodeModel.AddPorts(builder, ports)
    return NodeModel.End(builder)
    pass


def __MakePort(customNode: EnumsStructs.TreeNodesModel_t, builder: flatbuffers.Builder):
    ports = []
    for param in customNode.Params:
        portName = builder.CreateString(param.Name)
        typeInfo = builder.CreateString(param.VariableType)
        if (param.Desc != None):
            description = builder.CreateString(param.Desc)
        else:
            description = builder.CreateString("")
        PortModel.Start(builder)
        PortModel.AddPortName(builder, portName)
        PortModel.AddDirection(
            builder, __ConvertPortDirection(param.Direction))
        PortModel.AddTypeInfo(builder, typeInfo)
        PortModel.AddDescription(builder, description)
        port = PortModel.End(builder)
        ports.append(port)

    NodeModel.StartPortsVector(builder, len(ports))
    for port in ports:
        builder.PrependUOffsetTRelative(port)
    return builder.EndVector()
    pass


def __ConvertPortDirection(Enum: EnumsStructs.eInputOutput) -> int:
    if (Enum == EnumsStructs.eInputOutput.input_port):
        return PortDirection.PortDirection.INOUT
    elif (Enum == EnumsStructs.eInputOutput.output_port):
        return PortDirection.PortDirection.OUTPUT
    raise NameError("port direction inout is not supported!!")
    pass


def __ConvertNodeType(enum: EnumsStructs.eNodeType) -> int:
    if (enum == EnumsStructs.eNodeType.UNDEFINED):
        return NodeType.NodeType.UNDEFINED
    elif enum == EnumsStructs.eNodeType.Action:
        return NodeType.NodeType.ACTION
    elif enum == EnumsStructs.eNodeType.Condition:
        return NodeType.NodeType.CONDITION
    elif enum == EnumsStructs.eNodeType.Control:
        return NodeType.NodeType.CONTROL
    elif enum == EnumsStructs.eNodeType.Decorator:
        return NodeType.NodeType.DECORATOR
    elif enum == EnumsStructs.eNodeType.SubTree:
        return NodeType.NodeType.SUBTREE

    raise NameError(
        "parser strange. no right nodetype for treenodemodels, param")
    pass
