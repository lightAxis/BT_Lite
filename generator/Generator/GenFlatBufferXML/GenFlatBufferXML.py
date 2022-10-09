#!usr/bin/env python3

from tkinter import E
from GrootXMLParser import EnumsStructs
import os

from typing import List, Dict, Tuple

from xml.etree.ElementTree import Element, SubElement, ElementTree


def Generate(input: EnumsStructs.GenerationIngredients_t) -> None:
    root = Element("BehaviorTree")

    root.append(__MakeNodes(input))
    root.append(__MakeNodeModels(input))

    __pretty_print(root)

    tree = ElementTree(root)

    buf = open("BehaviorTree.xml", 'wb')
    tree.write(buf, encoding='utf-8', xml_declaration=True)
    pass


def __MakeNodes(input: EnumsStructs.GenerationIngredients_t) -> Element:

    nodes: Element = Element('nodes')
    nodes.set("array", "TreeNode")

    for tree_t in input.ParsedGroot.TotalTree:
        node: Element = Element("TreeNode")
        node.set("uid", str(tree_t.UID))
        node.append(__MakeChildrenUIDs(tree_t))
        node.set("status", "IDLE")
        node.set("instance_name", tree_t.Name)
        node.set("registration_name", tree_t.Name)
        node.append(__MakePortRemaps(tree_t))
        nodes.append(node)

    return nodes
    pass


def __MakeChildrenUIDs(node: EnumsStructs.TotalTree_t) -> Element:
    children = Element("children_uid")
    children.set("array", "uid")

    for uid in node.ChildrenIdx:
        element = Element("uid")
        element.text = str(uid)
        children.append(element)
    return children
    pass


def __MakePortRemaps(node: EnumsStructs.TotalTree_t) -> Element:
    portRemap: Element = Element("port_remaps")
    portRemap.set("array", "PortConfig")

    for key in node.Attrib.keys():
        if (key == "ID"):
            continue

        element = Element("PortConfig")
        element.set("port_name", key)
        element.set("remap", node.Attrib[key])
        portRemap.append(element)
    return portRemap
    pass


def __MakeNodeModels(input: EnumsStructs.GenerationIngredients_t) -> Element:
    nodeModels: Element = Element("node_models")
    nodeModels.set("array", "NodeModel")

    for nodemodel in input.CustomGenerations.Actions:
        nodeModels.append(__MakeNodeModel(nodemodel))
    for nodemodel in input.CustomGenerations.Conditions:
        nodeModels.append(__MakeNodeModel(nodemodel))
    for nodemodel in input.CustomGenerations.Controls:
        nodeModels.append(__MakeNodeModel(nodemodel))
    for nodemodel in input.CustomGenerations.Decorators:
        nodeModels.append(__MakeNodeModel(nodemodel))
    for nodemodel in input.CustomGenerations.SubTrees:
        nodeModels.append(__MakeNodeModel(nodemodel))

    return nodeModels
    pass


def __MakeNodeModel(nodemodel: EnumsStructs.TreeNodesModel_t) -> Element:
    element = Element("NodeModel")
    element.set("registration_name", nodemodel.ID)
    element.set("type", nodemodel.NodeType.name)
    element.append(__MakePorts(nodemodel))
    return element
    pass


def __MakePorts(node: EnumsStructs.TreeNodesModel_t) -> Element:
    ports = Element("ports")
    ports.set("array", "PortModel")

    for param in node.Params:
        element = Element("PortModel")
        element.set("port_name", param.Name)
        element.set("direction", param.Direction.name)
        element.set("type_info", param.VariableType)
        if (param.Desc == None):
            element.set("description", "")
        else:
            element.set("description", param.Desc)
        ports.append(element)

    return ports
    pass


def __pretty_print(current, parent=None, index=-1, depth=0):
    for i, node in enumerate(current):
        __pretty_print(node, current, i, depth + 1)
    if parent is not None:
        if index == 0:
            parent.text = '\n' + ('\t' * depth)
        else:
            parent[index - 1].tail = '\n' + ('\t' * depth)
        if index == len(parent) - 1:
            current.tail = '\n' + ('\t' * (depth - 1))
