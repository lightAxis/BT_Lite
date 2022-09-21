#!usr/bin/env python3

import os

from GrootXMLParser.EnumsStructs import *
from GrootXMLParser import ParseVariable

from Generator import emInterpreter
from . import GenClassname


def MakeClassNames(node: TreeNodesModel_t) -> Tuple[str, str, str]:
    """make class names with tree nodes model struct

    Args:
        node (TreeNodesModel_t): tree nodes model struct

    Returns:
        Tuple[str, str, str]: nodeTypeStr, nodeName, nodeClassName
    """
    nodeTypeStr = node.Tag
    nodeName = node.ID
    nodeClassName = nodeTypeStr.upper()+"_"+nodeName
    return nodeTypeStr, nodeName, nodeClassName
    pass


def MakeDelegateInfos(param: NodeParam_t) -> Tuple[str, str, str, str]:
    """Make delegate and param of custom classes

    Args:
        param (NodeParam_t): node param struct of custom classe

    Returns:
        Tuple[str, str, str, str, str]: paramStr, paramName, delegateType, delegateNewTypeName, delegateVariableName
    """

    paramStr: str = None
    if (param.Direction == eInputOutput.input_port):
        paramStr = "const "+param.VariableType+"&"
    elif (param.Direction == eInputOutput.output_port):
        paramStr = param.VariableType+"*"

    paramName = param.Name

    delegateType: str = None
    if (param.Direction == eInputOutput.input_port):
        delegateType = "delegate<"+param.VariableType+"(void)>"
    elif (param.Direction == eInputOutput.output_port):
        delegateType = "delegate<void(const "+param.VariableType+"&)>"

    delegateNewTypeName: str = None
    if (param.Direction == eInputOutput.input_port):
        delegateNewTypeName = "_getter_"+param.Name
    elif (param.Direction == eInputOutput.output_port):
        delegateNewTypeName = "_setter_"+param.Name

    delegateVariableName: str = None
    if (param.Direction == eInputOutput.input_port):
        delegateVariableName = "_get_"+param.Name
    elif (param.Direction == eInputOutput.output_port):
        delegateVariableName = "_set_"+paramName

    return paramStr, paramName, delegateType, delegateNewTypeName, delegateVariableName
    pass


def MakeCustomClassTickStrs(node: TreeNodesModel_t) -> Tuple[str, str, str]:
    """make custom class tick strings

    Args:
        node (TreeNodesModel_t): tree nodes model structure

    Returns:
        Tuple[str, str, str]: delegateType, tickNewTypeName, tickVariableName
    """
    params: List[str] = []
    for param in node.Params:
        paramStr, _, _, _, _ = MakeDelegateInfos(param)
        params.append(paramStr)
    pass
    params.append("NodeBase *")

    delegateType = "delegate<NodeStatus(" + ", ".join(params) + ")>"
    tickNewTypeName = "TickDel"
    tickVariableName = "_tickDel"

    return delegateType, tickNewTypeName, tickVariableName


def MakeClassConstructorStrs(node: TreeNodesModel_t) -> Tuple[str, List[str]]:
    """make custom class constructor strings

    Args:
        node (TreeNodesModel_t): custom treenodesmodel struct

    Returns:
        Tuple[str, List[str]]: paramDefstr, paramInits
    """
    paramDefs: List[str] = []
    paramInits: List[str] = []

    for param in node.Params:
        _, _, _, paramType, paramVariableName = MakeDelegateInfos(param)
        paramDefs.append(paramType+" "+param.Name)
        paramInits.append(paramVariableName+"("+param.Name+")")

    _, tickNewTypeName, tickVariableName = MakeCustomClassTickStrs(node)
    paramDefs.append(tickNewTypeName+"* tickDel")
    paramInits.append(tickVariableName+"(tickDel)")

    return ", ".join(paramDefs), paramInits
    pass


def MakeClassCustomTickFunction(node: TreeNodesModel_t) -> Tuple[List[str], str, List[str]]:
    """make class custom tick function strs

    Args:
        node (TreeNodesModel_t): tree node to make custom tick function

    Returns:
        Tuple[List[str], str, List[str]]: beforeTickStrs, tickStr, afterTickStrs
    """
    beforeTickStrs: List[str] = []
    TickStr: str + None
    TickStrParams: List[str] = []
    afterTickStrs: List[str] = []

    input_temp_value_num: int = 0
    for param in node.Params:
        if param.Direction == eInputOutput.output_port:
            tempVariableName = "temp_"+param.Name+str(input_temp_value_num)
            beforeTickStrs.append(param.VariableType+" "+tempVariableName)
            _, _, _, _, setterName = MakeDelegateInfos(param)
            TickStrParams.append("&"+tempVariableName)
            afterTickStrs.append(
                setterName+"("+tempVariableName+")")
        elif param.Direction == eInputOutput.input_port:
            _, _, _, _, getterName = MakeDelegateInfos(param)
            TickStrParams.append(getterName+"()")

    TickStrParams.append("this")
    TickStr = ", ".join(TickStrParams)

    return beforeTickStrs, TickStr, afterTickStrs
    pass
