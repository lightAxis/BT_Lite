#!usr/bin/env python3

from typing import List, Dict, Tuple
import os
import xml.etree.ElementTree as ETree

from .EnumsStructs import *
from . import ParseTreeNodesModel
from . import ParseTotalTree


class GrootXMLParser:
    def __init__(self, xmlPath: str):
        self._xmlPath = xmlPath
        self._tree = ETree.parse(xmlPath)
        self._root = self._tree.getroot()

        self._subTrees: List[SubTree_t] = []
        self._mainSubTree: ETree.Element = None
        self._TreeNodesModels: List[TreeNodesModel_t] = []
        self._totalTree: List[TotalTree_t] = []
        self._ParentChilds: List[ParentChild_t] = []

    def Parse(self) -> GrootXMLParser_out_t:

        self.__fillStacks()
        return GrootXMLParser_out_t(TreeNodesModels=self._TreeNodesModels,
                                    TotalTree=self._totalTree,
                                    ParentChilds=self._ParentChilds)

    def __fillStacks(self) -> None:
        """Fill all Stacks
        """
        _MainTreeName = self._root.attrib['main_tree_to_execute']

        # search root node
        _MainTreeRoot: ETree.Element = None
        _TreeNodeModelRoot: ETree.Element = None
        for node in self._root:
            if node.tag == 'BehaviorTree':
                self._subTrees.append(
                    SubTree_t(Tag=node.tag, NodePtr=node, Name=node.attrib['ID']))
            elif node.tag == 'TreeNodesModel':
                _TreeNodeModelRoot = node

        # find main tree node ptr
        for subtree in self._subTrees:
            if subtree.Name == _MainTreeName:
                _MainTreeRoot = subtree.NodePtr
                break

        # if no main tree found, failed
        if _MainTreeRoot == None:
            raise NameError("cannot find main tree in XML file")
        self._mainSubTree = _MainTreeRoot

        # if TreeNodeModel exists, do parse
        if _TreeNodeModelRoot != None:
            self._TreeNodesModels = ParseTreeNodesModel.Parse(
                _TreeNodeModelRoot)

        # parse total Tree & ParentChild
        self._totalTree, self._ParentChilds = ParseTotalTree.Parse(
            self._mainSubTree, self._subTrees, self._TreeNodesModels)
