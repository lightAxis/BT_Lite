#!usr/bin/env python3

import os
from platform import node

from GrootXMLParser.EnumsStructs import *
from GrootXMLParser import ParseVariable

from Generator import emInterpreter


def Generate(input: GenerationIngredients_t) -> None:

    __GenEnumWithType(input, eNodeType.Action)
    __GenEnumWithType(input, eNodeType.Condition)
    __GenEnumWithType(input, eNodeType.Control)
    __GenEnumWithType(input, eNodeType.Decorator)
    __GenEnumWithType(input, eNodeType.SubTree)
    __GenParamEnum(input)
    pass


def __GenEnumWithType(input: GenerationIngredients_t, nodeType: eNodeType) -> None:
    Base_Dict: Dict[str, int] = {}
    Custom_Dict: Dict[str, int] = {}

    i = 0
    if (nodeType == eNodeType.Action):
        for enum in eAction_base:
            Base_Dict[enum.name] = i
            i = i + 1
        for action in input.CustomGenerations.Actions:
            Custom_Dict[action.ID] = i
            i = i + 1
    elif nodeType == eNodeType.Condition:
        for enum in eCondition_base:
            Base_Dict[enum.name] = i
            i = i + 1
        for condition in input.CustomGenerations.Conditions:
            Custom_Dict[condition.ID] = i
            i = i + 1
    elif nodeType == eNodeType.Control:
        for enum in eControl_base:
            Base_Dict[enum.name] = i
            i = i + 1
        for control in input.CustomGenerations.Controls:
            Custom_Dict[control.ID] = i
            i = i + 1
    elif nodeType == eNodeType.Decorator:
        for enum in eDecorator_base:
            Base_Dict[enum.name] = i
            i = i + 1
        for decorator in input.CustomGenerations.Decorators:
            Custom_Dict[decorator.ID] = i
            i = i + 1
    elif nodeType == eNodeType.SubTree:
        for enum in eSubTree_base:
            Base_Dict[enum.name] = i
            i = i + 1
        for subtree in input.CustomGenerations.SubTrees:
            Custom_Dict[subtree.ID] = i
            i = i + 1

    em_globals = {
        'NAMESPACE': input.BT_Name,
        'Base_Dict': Base_Dict,
        'Custom_Dict': Custom_Dict,
        'EnumName': nodeType.name
    }

    templatePath = os.path.join(
        input.templatePathBase, "generated/Enums/ENUM_gen.h.em")
    outputPath = os.path.join(input.outputPathBase,
                              "generated/Enums", nodeType.name + "_gen.h")
    emInterpreter.Generate(templatePath=templatePath,
                           outputPath=outputPath, em_globals=em_globals)
    pass


def __GenParamEnum(input: GenerationIngredients_t):
    Base_Dict: Dict[str, int] = {}
    Custom_Dict: Dict[str, int] = {}

    Base_Dict['Const'] = 0
    i = 1
    for param in input.CustomGenerations.Params:
        Custom_Dict[param.Name] = i
        i = i + 1

    em_globals = {
        'NAMESPACE': input.BT_Name,
        'Base_Dict': Base_Dict,
        'Custom_Dict': Custom_Dict,
        'EnumName': 'Param'
    }

    templatePath = os.path.join(
        input.templatePathBase, "generated/Enums/ENUM_gen.h.em")
    outputPath = os.path.join(input.outputPathBase,
                              "generated/Enums", "Param_gen.h")
    emInterpreter.Generate(templatePath=templatePath,
                           outputPath=outputPath, em_globals=em_globals)
    pass
