#!usr/bin/env python3

from ast import Param
import os

from GrootXMLParser.EnumsStructs import *
from GrootXMLParser import ParseVariable

from Generator import emInterpreter
from . import GenClassname


def Generate(input: GenerationIngredients_t) -> None:

    __GenNodes_Common(input)
    __GenParams_Common(input)
    __GenEnums_Common(input)
    __GenParamServer_Common(input)
    __GenTree_Common(input)
    pass


def __GenEnums_Common(input: GenerationIngredients_t) -> None:
    em_globals = {
        'NAMESPACE': input.BT_Name
    }
    templatePath = os.path.join(
        input.templatePathBase, "generated/Enums_gen.h.em")
    outputPath = os.path.join(
        input.outputPathBase, "generated/Enums_gen.h"
    )
    emInterpreter.Generate(templatePath=templatePath,
                           outputPath=outputPath, em_globals=em_globals)
    pass


def __GenNodes_Common(input: GenerationIngredients_t) -> None:
    Actions: List[str] = []
    Conditions: List[str] = []
    Controls: List[str] = []
    Decorators: List[str] = []
    SubTrees: List[str] = []

    for action in input.CustomGenerations.Actions:
        Actions.append(action.ID)
    for condition in input.CustomGenerations.Conditions:
        Conditions.append(condition.ID)
    for control in input.CustomGenerations.Controls:
        Controls.append(control.ID)
    for decorator in input.CustomGenerations.Decorators:
        Decorators.append(decorator.ID)
    for subtree in input.CustomGenerations.SubTrees:
        SubTrees.append(subtree.ID)

    em_globals = {
        'NAMESPACE': input.BT_Name,
        'Actions': Actions,
        'Conditions': Conditions,
        'Controls': Controls,
        'Decorators': Decorators,
        'SubTrees': SubTrees}
    templatePath = os.path.join(
        input.templatePathBase, "generated/Nodes_gen.h.em")
    outputPath = os.path.join(
        input.outputPathBase, "generated/Nodes_gen.h")
    emInterpreter.Generate(templatePath=templatePath,
                           outputPath=outputPath, em_globals=em_globals)
    pass


def __GenParams_Common(input: GenerationIngredients_t) -> None:
    Params: List[str] = []

    for param in input.CustomGenerations.Params:
        Params.append(param.Name)

    em_globals = {
        'NAMESPACE': input.BT_Name,
        'Params': Params}
    templatePath = os.path.join(
        input.templatePathBase, "generated/Params_gen.h.em")
    outputPath = os.path.join(
        input.outputPathBase, "generated/Params_gen.h")
    emInterpreter.Generate(templatePath=templatePath,
                           outputPath=outputPath, em_globals=em_globals)
    pass


def __GenParamServer_Common(input: GenerationIngredients_t) -> None:
    Params_Dict: Dict[str, str] = {}

    for param in input.CustomGenerations.Params:
        Params_Dict[param.Name] = param.Type

    em_globals = {
        'NAMESPACE': input.BT_Name,
        'Params_Dict': Params_Dict}
    templatePath = os.path.join(
        input.templatePathBase, "generated/ParamServer_gen.h.em")
    outputPath = os.path.join(
        input.outputPathBase, "generated/ParamServer_gen.h")

    emInterpreter.Generate(templatePath=templatePath,
                           outputPath=outputPath, em_globals=em_globals)
    pass


def __GenTree_Common(input: GenerationIngredients_t) -> None:

    @dataclass
    class NodeNames_t:
        className: str = None
        variableName: str = None
        initializeStr: str = None

    @dataclass
    class DelegateNames_t:
        className: str = None
        variableName: str = None
        initializeStr: str = None
        classNamePtr: str = None
        variableNamePtr: str = None
        initializeStrPtr: str = None

    @dataclass
    class ParamNames_t:
        className: str = None
        variableName: str = None
        initializeStr: str = None

    NodeName_List: List[NodeNames_t] = []
    DelegateName_List: List[DelegateNames_t] = []
    ConstParamName_List: List[ParamNames_t] = []
    CustomParamName_List: List[ParamNames_t] = []
    BuildStr_List: List[str] = []

    for node in input.ParsedGroot.TotalTree:
        _temp = NodeNames_t()
        _temp.className, _temp.variableName, _temp.initializeStr = GenClassname.MakeNodeClassNames(
            node, input.CustomGenerations.ConstParams)
        NodeName_List.append(_temp)

    for custom in input.ParsedGroot.TreeNodesModels:
        if custom.NodeType == eNodeType.SubTree:
            continue
        _temp: DelegateNames_t = DelegateNames_t()
        _temp.className, _temp.variableName, _temp.initializeStr = GenClassname.MakeCustomNodeDelegateNames(
            custom)
        _temp.classNamePtr, _temp.variableNamePtr, _temp.initializeStrPtr = GenClassname.MakeCustomNodeDelPtrNames(
            custom)
        DelegateName_List.append(_temp)

    for constparam in input.CustomGenerations.ConstParams:
        _temp: ParamNames_t = ParamNames_t()
        _temp.className, _temp.variableName, _temp.initializeStr = GenClassname.MakeConstParamClassNames(
            constparam)
        ConstParamName_List.append(_temp)

    for customparam in input.CustomGenerations.Params:
        _temp: ParamNames_t = ParamNames_t()
        _temp.className, _temp.variableName, = GenClassname.MakeCustomParamClassNames(
            customparam)
        _temp.initializeStr = ""
        CustomParamName_List.append(_temp)

    for parentchild in input.ParsedGroot.ParentChilds:
        parentVariableName = NodeName_List[parentchild.ParentIdx].variableName
        for childIdx in parentchild.ChildrenIdxs:
            childVariableName = NodeName_List[childIdx].variableName
            BuildStr_List.append(parentVariableName +
                                 ".addChild(&"+childVariableName+");")

    em_globals = {
        'NAMESPACE': input.BT_Name,
        'NodeName_List': NodeName_List,
        'DelegateName_List': DelegateName_List,
        'ConstParamName_List': ConstParamName_List,
        'CustomParamName_List': CustomParamName_List,
        'BuildStr_List': BuildStr_List
    }
    templatePath = os.path.join(
        input.templatePathBase, "generated/Tree_gen.h.em")
    outputPath = os.path.join(
        input.outputPathBase, "generated/Tree_gen.h")
    emInterpreter.Generate(templatePath=templatePath,
                           outputPath=outputPath, em_globals=em_globals)
    pass
