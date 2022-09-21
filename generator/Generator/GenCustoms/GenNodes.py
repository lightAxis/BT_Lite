#!usr/bin/env python3

import os

from GrootXMLParser.EnumsStructs import *
from GrootXMLParser import ParseVariable

from Generator import emInterpreter
from . import GenCustomClassname


def Generate(input: GenerationIngredients_t):

    __GenCustomNodes(input.CustomGenerations.Actions, input)
    __GenCustomNodes(input.CustomGenerations.Conditions, input)
    __GenCustomNodes(input.CustomGenerations.Controls, input)
    __GenCustomNodes(input.CustomGenerations.Decorators, input)
    __GenCustomNodes(input.CustomGenerations.SubTrees, input)
    pass


def __GenCustomNodes(Nodes: List[TreeNodesModel_t], input: GenerationIngredients_t):
    for node in Nodes:
        __GenCustomNode(node, input)
    pass


def __GenCustomNode(Node: TreeNodesModel_t, input: GenerationIngredients_t):
    @dataclass
    class Def_t:
        TypedefStr: str = None
        TypedefName: str = None
        VariableName: str = None

    @dataclass
    class TickFunc_t:
        before: List[str] = None
        Tick: str = None
        after: List[str] = None

    DelegateInfos: List[Def_t] = []
    TickDelInfo: Def_t = Def_t()
    TickFuncInfo: TickFunc_t = TickFunc_t()
    ClassConstructorStr: str = None
    ClassConstructorInits: List[str] = []
    ClassName: str = None
    NodeName: str = None
    NodeType: str = None

    # get all delegate Infos
    for param in Node.Params:
        tempDelegateDef: Def_t = Def_t()
        _, _, tempDelegateDef.TypedefStr, tempDelegateDef.TypedefName, tempDelegateDef.VariableName = GenCustomClassname.MakeDelegateInfos(
            param)
        DelegateInfos.append(tempDelegateDef)
    # get tick function strings
    TickFuncInfo.before, TickFuncInfo.Tick, TickFuncInfo.after = GenCustomClassname.MakeClassCustomTickFunction(
        Node)
    # get tick delegate strings
    TickDelInfo.TypedefStr, TickDelInfo.TypedefName, TickDelInfo.VariableName = GenCustomClassname.MakeCustomClassTickStrs(
        Node)
    # make class constructor string
    ClassConstructorStr, ClassConstructorInits = GenCustomClassname.MakeClassConstructorStrs(
        Node)
    # get className, Nodename
    _, NodeName, ClassName = GenCustomClassname.MakeClassNames(Node)
    # get Nodetype of this node
    NodeType = Node.NodeType.name

    em_globals = {
        'NAMESPACE': input.BT_Name,
        'DelegateInfos': DelegateInfos,
        'TickDelInfo': TickDelInfo,
        'TickFuncInfo': TickFuncInfo,
        'ClassConstructorStr': ClassConstructorStr,
        'ClassConstructorInits': ClassConstructorInits,
        'ClassName': ClassName,
        'NodeType': NodeType,
        'NodeName': NodeName
    }

    templatePath = os.path.join(
        input.templatePathBase, "generated/CUSTOMNODE.h.em")
    if (Node.NodeType == eNodeType.SubTree):
        templatePath = os.path.join(
            input.templatePathBase, "generated/CUSTOMNODE_SUBTREE.h.em")
    outputPath = os.path.join(input.outputPathBase,
                              "generated/"+NodeType+"s/"+NodeName+".h")
    emInterpreter.Generate(templatePath=templatePath,
                           outputPath=outputPath, em_globals=em_globals)

    pass
