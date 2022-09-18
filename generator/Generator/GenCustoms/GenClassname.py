#!usr/bin/env python3

import os
from pydoc import classname

from GrootXMLParser.EnumsStructs import *
from GrootXMLParser import ParseVariable


def MakeNodeClassNames(node: TotalTree_t, ConstParams: List[ConstParam_t]) -> Tuple[str, str, str]:
    """make class and variable name of node from totaltree_t.
    variable name is used at tree_gen.h

    Args:
        node (TotalTree_t): node to input

    Returns:
        Tuple[str, str, str]: className, variableName, initalizeParams
    """
    nodeTypeStr: str = node.NodeType.name.upper()
    nodeName: str = node.Name

    className = nodeTypeStr+"_"+nodeName
    variableName = "_"+className+"_"+str(node.UID)

    if (node.NodeType == eNodeType.Control):
        className = className+"<"+str(node.ChildNum)+">"

    params: List[str] = []
    for key in node.Attrib.keys():
        if (key != 'ID'):
            params.append(__makeParameterInputStr(node, key, ConstParams))

    if (node.isCustom == True) and (node.NodeType != eNodeType.SubTree):
        _, tickDelname, _ = MakeCustomNodeDelPtrNames(node.CustomPtr)
        params.append(tickDelname)

    paramsStr: str = ", ".join(params)

    return className, variableName, paramsStr
    pass


def __makeParameterInputStr(node: TotalTree_t, paramKey: str, constParams: List[ConstParam_t]) -> str:
    """make input string of node's initialization parameter

    Args:
        node (TotalTree_t): owner node of parameter
        paramKey (str): parameter key of param

    Returns:
        str: paramDelegateStr
    """

    paramType, paramName, isParamConst = ParseVariable.Parse(
        node.Attrib[paramKey])

    variableName: str = None
    if (isParamConst == True):
        temp: ConstParam_t = ConstParam_t()
        for constparam in constParams:
            if constparam.Type == paramType and constparam.Value == paramName:
                temp = constparam
                break

        _, variableName, _ = MakeConstParamClassNames(temp)
    elif (isParamConst == False):
        temp: CustomParam_t = CustomParam_t(Type=paramType, Name=paramName)
        _, variableName = MakeCustomParamClassNames(temp)

    direction: eInputOutput = None
    if (node.isCustom == True):
        for param in node.CustomPtr.Params:
            if param.Name == paramKey:
                direction = param.Direction
                break
    elif (node.isCustom == False):
        direction = eInputOutput.input_port

    directionStr: str = None
    if (direction == eInputOutput.input_port):
        directionStr = "makeGetter()"
    elif (direction == eInputOutput.output_port):
        directionStr = "makeSetter()"

    return variableName+"."+directionStr
    pass


def MakeCustomNodeDelegateNames(customNode: TreeNodesModel_t) -> Tuple[str, str, str]:
    """make class and varaible name of custom node's delegates

    Args:
        customNode (TreeNodesModel_t): input Treenodemodel

    Returns:
        Tuple[str, str]: className, variableName, initValue
    """
    nodeTypeStr: str = customNode.Tag.upper()
    nodeName: str = customNode.ID

    className: str = nodeTypeStr+"_"+nodeName+"::_tickDel"
    variableName: str = "_"+nodeName+"_tickDel"
    initValue: str = "nullptr"
    return className, variableName, initValue
    pass


def MakeCustomNodeDelPtrNames(customNode: TreeNodesModel_t) -> Tuple[str, str, str]:
    """make class and varaible name of custom node's delegates pointer

    Args:
        customNode (TreeNodesModel_t): input Treenodemodel

    Returns:
        Tuple[str, str, str]: className, variableName, initValue
    """
    className, variableName, _ = MakeCustomNodeDelegateNames(customNode)
    classNamePtr = className+"*"
    variableNamePtr = variableName+"Ptr"
    initValuePtr = "&"+variableName
    return classNamePtr, variableNamePtr, initValuePtr
    pass


def MakeCustomParamClassNames(param: CustomParam_t) -> Tuple[str, str]:
    """make class and variable name of custom param from customparam_t
    variable name is used at tree_gen.h

    Args:
        param (CustomParam_t): customparam to input

    Returns:
        Tuple[str, str]: className, variableName
    """
    className: str = "PARAM_"+param.Name
    variableName = "_"+className

    return className, variableName
    pass


def MakeConstParamClassNames(param: ConstParam_t) -> Tuple[str, str, str]:
    """make class and variable name of const param from constparam_t
    variable name is used at tree_gen.h

    Args:
        param (ConstParam_t): constparam to input
        index (int): index of constparam list

    Returns:
        Tuple[str, str, str]: className, variableName, constValue
    """
    className: str = "PARAM_Const_"+param.Type
    variableName: str = "_"+className+"_"+str(param.Index)

    return className, variableName, param.Value
    pass
