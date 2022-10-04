#!usr/bin/env python3

from dataclasses import dataclass
from distutils.command.build import build
from readline import parse_and_bind
from tkinter import Variable
from typing import List, Dict, Tuple
from unicodedata import name
from xml.dom.expatbuilder import parseFragmentString

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
    nodes_List.reverse()
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
    nodeModels_List_base = []
    nodeModels_List_base = __MakeNodeModel_Base(builder)
    nodeModels_List.extend(nodeModels_List_base)

    BehaviorTree.StartNodeModelsVector(builder, len(nodeModels_List))
    nodeModels_List.reverse()
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
    buffer_size = len(buf).to_bytes(length=4, byteorder='little', signed=False)

    buffer = open("Tree.fbl", 'wb')
    buffer.write(buffer_size)
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
    children = node.Children.copy()
    children.reverse()
    for uid in children:
        builder.PrependUint16(uid)
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
    ports.reverse()
    for port in ports:
        builder.PrependUOffsetTRelative(port)
    return builder.EndVector()
    pass


def __MakeNodeModel_Base(builder: flatbuffers.Builder) -> List[int]:
    NodeModel_List: List[int] = []
    tempNode: EnumsStructs.TreeNodesModel_t = EnumsStructs.TreeNodesModel_t()
    params: List[EnumsStructs.NodeParam_t] = []

    # AlwaysFailure
    params = []
    tempNode.Params = params
    tempNode.ID = EnumsStructs.eAction_base.AlwaysFailure.name
    tempNode.NodeType = EnumsStructs.eNodeType.Action
    NodeModel_List.append(__MakeNodeModel(tempNode, builder))

    # AlwaysSuccess
    params = []
    tempNode.Params = params
    tempNode.ID = EnumsStructs.eAction_base.AlwaysSuccess.name
    tempNode.NodeType = EnumsStructs.eNodeType.Action
    NodeModel_List.append(__MakeNodeModel(tempNode, builder))

    # Fallback
    params = []
    tempNode.Params = params
    tempNode.ID = EnumsStructs.eControl_base.Fallback.name
    tempNode.NodeType = EnumsStructs.eNodeType.Control
    NodeModel_List.append(__MakeNodeModel(tempNode, builder))

    # IFThenElse
    params = []
    tempNode.Params = params
    tempNode.ID = EnumsStructs.eControl_base.IfThenElse.name
    tempNode.NodeType = EnumsStructs.eNodeType.Control
    NodeModel_List.append(__MakeNodeModel(tempNode, builder))

    # ManualSelector
    params = []
    params.append(EnumsStructs.NodeParam_t(Name='repeat_last_selection',
                                           Desc='if True, execute again the same child that was selected the last time',
                                           Direction=EnumsStructs.eInputOutput.input_port,
                                           VariableType='bool'))
    tempNode.Params = params
    tempNode.ID = EnumsStructs.eControl_base.ManualSelector.name
    tempNode.NodeType = EnumsStructs.eNodeType.Control
    NodeModel_List.append(__MakeNodeModel(tempNode, builder))

    # Parallel
    params = []
    params.append(EnumsStructs.NodeParam_t(Name='failure_threshold',
                                           Desc='number of children which need to fail to trigger a FAILURE',
                                           Direction=EnumsStructs.eInputOutput.input_port,
                                           VariableType='uint8_t'))
    params.append(EnumsStructs.NodeParam_t(Name='success_threshold',
                                           Desc='number of children which need to fail to trigger a SUCCESS',
                                           Direction=EnumsStructs.eInputOutput.input_port,
                                           VariableType='uint8_t'))
    tempNode.Params = params
    tempNode.ID = EnumsStructs.eControl_base.Parallel.name
    tempNode.NodeType = EnumsStructs.eNodeType.Control
    NodeModel_List.append(__MakeNodeModel(tempNode, builder))

    # ReactiveFallback
    params = []
    tempNode.Params = params
    tempNode.ID = EnumsStructs.eControl_base.ReactiveFallback.name
    tempNode.NodeType = EnumsStructs.eNodeType.Control
    NodeModel_List.append(__MakeNodeModel(tempNode, builder))

    # ReactiveSequence
    params = []
    tempNode.Params = params
    tempNode.ID = EnumsStructs.eControl_base.ReactiveSequence.name
    tempNode.NodeType = EnumsStructs.eNodeType.Control
    NodeModel_List.append(__MakeNodeModel(tempNode, builder))

    # Sequence
    params = []
    tempNode.Params = params
    tempNode.ID = EnumsStructs.eControl_base.Sequence.name
    tempNode.NodeType = EnumsStructs.eNodeType.Control
    NodeModel_List.append(__MakeNodeModel(tempNode, builder))

    # SequenceStar
    params = []
    tempNode.Params = params
    tempNode.ID = EnumsStructs.eControl_base.SequenceStar.name
    tempNode.NodeType = EnumsStructs.eNodeType.Control
    NodeModel_List.append(__MakeNodeModel(tempNode, builder))

    # Switch2
    params = []
    params.append(EnumsStructs.NodeParam_t(Name='case_1', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port,
                  VariableType='uint8_t'))
    params.append(EnumsStructs.NodeParam_t(Name='case_2', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port,
                  VariableType='uint8_t'))
    params.append(EnumsStructs.NodeParam_t(Name='variable', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port,
                  VariableType='uint8_t'))
    tempNode.Params = params
    tempNode.ID = EnumsStructs.eControl_base.Switch2.name
    tempNode.NodeType = EnumsStructs.eNodeType.Control
    NodeModel_List.append(__MakeNodeModel(tempNode, builder))

    # Switch3
    params = []
    params.append(EnumsStructs.NodeParam_t(Name='case_1', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port,
                  VariableType='uint8_t'))
    params.append(EnumsStructs.NodeParam_t(Name='case_2', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port,
                  VariableType='uint8_t'))
    params.append(EnumsStructs.NodeParam_t(Name='case_3', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port,
                  VariableType='uint8_t'))
    params.append(EnumsStructs.NodeParam_t(Name='variable', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port,
                  VariableType='uint8_t'))
    tempNode.Params = params
    tempNode.ID = EnumsStructs.eControl_base.Switch3.name
    tempNode.NodeType = EnumsStructs.eNodeType.Control
    NodeModel_List.append(__MakeNodeModel(tempNode, builder))

    # Switch4
    params = []
    params.append(EnumsStructs.NodeParam_t(Name='case_1', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port,
                  VariableType='uint8_t'))
    params.append(EnumsStructs.NodeParam_t(Name='case_2', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port,
                  VariableType='uint8_t'))
    params.append(EnumsStructs.NodeParam_t(Name='case_3', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port,
                  VariableType='uint8_t'))
    params.append(EnumsStructs.NodeParam_t(Name='case_4', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port,
                  VariableType='uint8_t'))
    params.append(EnumsStructs.NodeParam_t(Name='variable', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port,
                  VariableType='uint8_t'))
    tempNode.Params = params
    tempNode.ID = EnumsStructs.eControl_base.Switch4.name
    tempNode.NodeType = EnumsStructs.eNodeType.Control
    NodeModel_List.append(__MakeNodeModel(tempNode, builder))

    # Switch5
    params = []
    params.append(EnumsStructs.NodeParam_t(Name='case_1', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port,
                  VariableType='uint8_t'))
    params.append(EnumsStructs.NodeParam_t(Name='case_2', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port,
                  VariableType='uint8_t'))
    params.append(EnumsStructs.NodeParam_t(Name='case_3', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port,
                  VariableType='uint8_t'))
    params.append(EnumsStructs.NodeParam_t(Name='case_4', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port,
                  VariableType='uint8_t'))
    params.append(EnumsStructs.NodeParam_t(Name='case_5', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port,
                  VariableType='uint8_t'))
    params.append(EnumsStructs.NodeParam_t(Name='variable', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port,
                  VariableType='uint8_t'))
    tempNode.Params = params
    tempNode.ID = EnumsStructs.eControl_base.Switch5.name
    tempNode.NodeType = EnumsStructs.eNodeType.Control
    NodeModel_List.append(__MakeNodeModel(tempNode, builder))

    # Switch6
    params = []
    params.append(EnumsStructs.NodeParam_t(Name='case_1', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port,
                  VariableType='uint8_t'))
    params.append(EnumsStructs.NodeParam_t(Name='case_2', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port,
                  VariableType='uint8_t'))
    params.append(EnumsStructs.NodeParam_t(Name='case_3', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port,
                  VariableType='uint8_t'))
    params.append(EnumsStructs.NodeParam_t(Name='case_4', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port,
                  VariableType='uint8_t'))
    params.append(EnumsStructs.NodeParam_t(Name='case_5', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port,
                  VariableType='uint8_t'))
    params.append(EnumsStructs.NodeParam_t(Name='case_6', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port,
                  VariableType='uint8_t'))
    params.append(EnumsStructs.NodeParam_t(Name='variable', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port,
                  VariableType='uint8_t'))
    tempNode.Params = params
    tempNode.ID = EnumsStructs.eControl_base.Switch6.name
    tempNode.NodeType = EnumsStructs.eNodeType.Control
    NodeModel_List.append(__MakeNodeModel(tempNode, builder))

    # BlackboardCheckBool
    params = []
    params.append(EnumsStructs.NodeParam_t(Name='return_on_mismatch', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port, VariableType='bool'))
    params.append(EnumsStructs.NodeParam_t(Name='value_A', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port, VariableType='bool'))
    params.append(EnumsStructs.NodeParam_t(Name='value_A', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port, VariableType='bool'))
    tempNode.Params = params
    tempNode.ID = EnumsStructs.eDecorator_base.BlackboardCheckBool.name
    tempNode.NodeType = EnumsStructs.eNodeType.Decorator
    NodeModel_List.append(__MakeNodeModel(tempNode, builder))

    # BlackboardCheckDouble
    params = []
    params.append(EnumsStructs.NodeParam_t(Name='return_on_mismatch', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port, VariableType='float'))
    params.append(EnumsStructs.NodeParam_t(Name='value_A', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port, VariableType='float'))
    params.append(EnumsStructs.NodeParam_t(Name='value_A', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port, VariableType='float'))
    tempNode.Params = params
    tempNode.ID = EnumsStructs.eDecorator_base.BlackboardCheckDouble.name
    tempNode.NodeType = EnumsStructs.eNodeType.Decorator
    NodeModel_List.append(__MakeNodeModel(tempNode, builder))

    # BlackboardCheckInt
    params = []
    params.append(EnumsStructs.NodeParam_t(Name='return_on_mismatch', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port, VariableType='int'))
    params.append(EnumsStructs.NodeParam_t(Name='value_A', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port, VariableType='int'))
    params.append(EnumsStructs.NodeParam_t(Name='value_A', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port, VariableType='int'))
    tempNode.Params = params
    tempNode.ID = EnumsStructs.eDecorator_base.BlackboardCheckInt.name
    tempNode.NodeType = EnumsStructs.eNodeType.Decorator
    NodeModel_List.append(__MakeNodeModel(tempNode, builder))

    # BlackboardCheckString
    params = []
    params.append(EnumsStructs.NodeParam_t(Name='return_on_mismatch', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port, VariableType='char'))
    params.append(EnumsStructs.NodeParam_t(Name='value_A', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port, VariableType='char'))
    params.append(EnumsStructs.NodeParam_t(Name='value_A', Desc='',
                  Direction=EnumsStructs.eInputOutput.input_port, VariableType='char'))
    tempNode.Params = params
    tempNode.ID = EnumsStructs.eDecorator_base.BlackboardCheckString.name
    tempNode.NodeType = EnumsStructs.eNodeType.Decorator
    NodeModel_List.append(__MakeNodeModel(tempNode, builder))

    # Delay
    params = []
    params.append(EnumsStructs.NodeParam_t(Name='delay_msec', Desc='Tick the child after few milliseconds',
                  Direction=EnumsStructs.eInputOutput.input_port, VariableType='int'))
    tempNode.Params = params
    tempNode.ID = EnumsStructs.eDecorator_base.Delay.name
    tempNode.NodeType = EnumsStructs.eNodeType.Decorator
    NodeModel_List.append(__MakeNodeModel(tempNode, builder))

    # ForceFailure
    params = []
    tempNode.Params = params
    tempNode.ID = EnumsStructs.eDecorator_base.ForceFailure.name
    tempNode.NodeType = EnumsStructs.eNodeType.Decorator
    NodeModel_List.append(__MakeNodeModel(tempNode, builder))

    # ForceSuccess
    params = []
    tempNode.Params = params
    tempNode.ID = EnumsStructs.eDecorator_base.ForceSuccess.name
    tempNode.NodeType = EnumsStructs.eNodeType.Decorator
    NodeModel_List.append(__MakeNodeModel(tempNode, builder))

    # Inverter
    params = []
    tempNode.Params = params
    tempNode.ID = EnumsStructs.eDecorator_base.Inverter.name
    tempNode.NodeType = EnumsStructs.eNodeType.Decorator
    NodeModel_List.append(__MakeNodeModel(tempNode, builder))

    # KeepRunningUntilFailure
    params = []
    tempNode.Params = params
    tempNode.ID = EnumsStructs.eDecorator_base.KeepRunningUntilFailure.name
    tempNode.NodeType = EnumsStructs.eNodeType.Decorator
    NodeModel_List.append(__MakeNodeModel(tempNode, builder))

    # Repeat
    params = []
    params.append(EnumsStructs.NodeParam_t(Name='num_cycles', Desc='repeat a successful child up to N times, -1 is infinite',
                  Direction=EnumsStructs.eInputOutput.input_port, VariableType='uint16_t'))
    tempNode.Params = params
    tempNode.ID = EnumsStructs.eDecorator_base.Repeat.name
    tempNode.NodeType = EnumsStructs.eNodeType.Decorator
    NodeModel_List.append(__MakeNodeModel(tempNode, builder))

    # RetryUntilSuccessful
    params = []
    params.append(EnumsStructs.NodeParam_t(Name='num_attemps', Desc='execute again a failed child up to N times, -1 is infinite',
                  Direction=EnumsStructs.eInputOutput.input_port, VariableType='uint16_t'))
    tempNode.Params = params
    tempNode.ID = EnumsStructs.eDecorator_base.RetryUntilSuccessful.name
    tempNode.NodeType = EnumsStructs.eNodeType.Decorator
    NodeModel_List.append(__MakeNodeModel(tempNode, builder))

    # Timeout
    params = []
    params.append(EnumsStructs.NodeParam_t(Name='msec', Desc='after a certain amount of time. halt() the running child',
                  Direction=EnumsStructs.eInputOutput.input_port, VariableType='uint16_t'))
    tempNode.Params = params
    tempNode.ID = EnumsStructs.eDecorator_base.Timeout.name
    tempNode.NodeType = EnumsStructs.eNodeType.Decorator
    NodeModel_List.append(__MakeNodeModel(tempNode, builder))

    # RootTree
    params = []
    tempNode.Params = params
    tempNode.ID = EnumsStructs.eSubTree_base.RootTree.name
    tempNode.NodeType = EnumsStructs.eNodeType.SubTree
    NodeModel_List.append(__MakeNodeModel(tempNode, builder))

    return NodeModel_List
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
    ports.reverse()
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
