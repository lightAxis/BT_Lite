#!usr/bin/env python3

from typing import List, Dict, Tuple
import os
import xml.etree.ElementTree as ETree
import em
import shutil

from GrootXMLParser.EnumsStructs import *
from GrootXMLParser import ParseVariable

from . import GenCommon
from . import GenBase
from .GenCustoms import GenCustoms


class Generator:
    def __init__(self, GrootXmlResult: GrootXMLParser_out_t, BT_Name: str, CodeGenPath: str):
        self._ParsedGroot = GrootXmlResult
        self._BT_Name = BT_Name
        self._CodeGenPath = os.path.join(CodeGenPath, self._BT_Name)

        _temp = os.path.dirname(os.path.abspath(__file__))
        self._templatePath = os.path.join(_temp, "template")

        self._CustomGenerations = self.__getCustomGenerations()

        self._GenerationIngredient: GenerationIngredients_t = GenerationIngredients_t(
            outputPathBase=self._CodeGenPath,
            templatePathBase=self._templatePath,
            BT_Name=self._BT_Name,
            ParsedGroot=self._ParsedGroot,
            CustomGenerations=self._CustomGenerations)
        pass

    def Generate(self) -> None:

        if (os.path.exists(self._CodeGenPath) == True):
            shutil.rmtree(self._CodeGenPath)
        self.__makeBTDirectory(self._CodeGenPath)

        GenCommon.Generate(self._GenerationIngredient)

        pass

    def __makeBTDirectory(self, CodeGenPath: str) -> None:
        if (os.path.exists(CodeGenPath) == False):
            os.mkdir(CodeGenPath)
        pass

    def __getCustomGenerations(self) -> CustomGenerations_t:
        CustomActions: List[TreeNodesModel_t] = []
        CustomConditions: List[TreeNodesModel_t] = []
        CustomControls: List[TreeNodesModel_t] = []
        CustomDecorators: List[TreeNodesModel_t] = []
        CustomSubTrees: List[TreeNodesModel_t] = []
        CustomParams: List[CustomParam_t] = []
        ConstParams: List[ConstParam_t] = []

        CustomParams_Dict: Dict[str, bool] = {}
        ConstParams_Dict: Dict[str, List[str]] = {}

        for treeNodeModel in self._ParsedGroot.TreeNodesModels:
            if treeNodeModel.NodeType == eNodeType.Action:
                CustomActions.append(treeNodeModel)
            elif treeNodeModel.NodeType == eNodeType.Condition:
                CustomConditions.append(treeNodeModel)
            elif treeNodeModel.NodeType == eNodeType.Control:
                CustomControls.append(treeNodeModel)
            elif treeNodeModel.NodeType == eNodeType.Decorator:
                CustomDecorators.append(treeNodeModel)
            elif treeNodeModel.NodeType == eNodeType.SubTree:
                CustomSubTrees.append(treeNodeModel)

        constParamIndex = 0
        for node in self._ParsedGroot.TotalTree:
            for key in node.Attrib.keys():
                param = node.Attrib[key]
                if param.find("__") > 0:
                    typeName, Value, isConst = ParseVariable.Parse(param)
                    if (isConst == False) and (CustomParams_Dict.get(Value) == None):
                        new_customParam: CustomParam_t = CustomParam_t(
                            Type=typeName, Name=Value)
                        CustomParams.append(new_customParam)
                        CustomParams_Dict[Value] = True
                    elif (isConst == True):
                        if (ConstParams_Dict.get(typeName) == None):
                            new_constParam: ConstParam_t = ConstParam_t(
                                Type=typeName, Value=Value, Index=constParamIndex)
                            constParamIndex = constParamIndex + 1
                            ConstParams.append(new_constParam)
                            ConstParams_Dict[typeName] = [Value]
                        elif ((Value in ConstParams_Dict.get(typeName)) == False):
                            new_constParam: ConstParam_t = ConstParam_t(
                                Type=typeName, Value=Value, Index=constParamIndex)
                            constParamIndex = constParamIndex + 1
                            ConstParams.append(new_constParam)
                            ConstParams_Dict[typeName].append(Value)

        result_customGenerations = CustomGenerations_t(
            Actions=CustomActions,
            Conditions=CustomConditions,
            Controls=CustomControls,
            Decorators=CustomDecorators,
            SubTrees=CustomSubTrees,
            Params=CustomParams,
            ConstParams=ConstParams)
        return result_customGenerations
        pass
    pass
