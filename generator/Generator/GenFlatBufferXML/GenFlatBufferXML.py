#!usr/bin/env python3

from GrootXMLParser import EnumsStructs
import os

from xml.etree.ElementTree import Element, SubElement, ElementTree


def Generate(input: EnumsStructs.GenerationIngredients_t) -> None:
    root = Element("TreeModel")

    nodes = Element("Nodes")
    node_models = Element("Node_Models")
    root.append(nodes)
    root.append(node_models)

    node1 = Element("node")
    node1.set('uid', '2')
    nodes.append(node1)

    children1 = Element("children_uid")
    children1.set('array', 'child')
    node1.append(children1)

    child1 = Element("child")
    child1.text = "3"
    child2 = Element("child")
    child2.text = "4"
    child3 = Element("child")
    child3.text = "5"
    children1.append(child1)
    children1.append(child2)
    children1.append(child3)

    portremaps1 = Element("port_remaps")
    portremaps1.set('array', 'PortModel')
    node1.append(portremaps1)

    portModel1 = Element("PortModel")
    portModel1.set('port_name', 'dd')
    portModel1.set('set', 'fee')
    portremaps1.append(portModel1)

    portModel2 = Element("PortModel")
    portModel2.set('port_name', 'dd2')
    portModel2.set('set', 'fee2')
    portremaps1.append(portModel2)

    node2 = Element("node")
    node2.set('uid', '3')
    nodes.append(node2)

    __pretty_print(root)

    tree = ElementTree(root)

    buf = open("testtt.xml", 'wb')
    tree.write(buf, encoding='utf-8', xml_declaration=True)
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
