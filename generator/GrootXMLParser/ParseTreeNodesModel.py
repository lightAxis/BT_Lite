#!usr/bin/env python3

from GrootXMLParser.EnumsStructs import *
from GrootXMLParser import ParseVariable


def Parse(TreeNodeModel_nodes: ETree.Element) -> List[TreeNodesModel_t]:
    result: List[TreeNodesModel_t] = []

    for node in TreeNodeModel_nodes:
        spec: TreeNodesModel_t = __parseTreeNodesModel(node)
        result.append(spec)

    return result


def __parseTreeNodesModel(TreeNodeModel: ETree.Element) -> TreeNodesModel_t:
    """Parse tree nodes model in each TreeNodeModel. must under TreeNodesModel->{node}

    Args:
        TreeNodeModel (ETree.Element): node for parse
    Returns:
        TreeNodesModel_t: parsed struct
    """
    spec: TreeNodesModel_t = TreeNodesModel_t()
    # parse Nodetype
    for nodeType in eNodeType:
        if TreeNodeModel.tag == nodeType.name:
            spec.NodeType = nodeType
            break
    if spec.NodeType == None:
        raise NameError(
            "error occured at parsing TreeNodesModel. Cannot parse NodeType")
    # parse Tag
    spec.Tag = TreeNodeModel.tag
    # parse Attrib
    spec.Attrib = TreeNodeModel.attrib
    # parse ID
    spec.ID = TreeNodeModel.attrib['ID']
    # parse Params
    spec.Params = []
    for nodeparam in TreeNodeModel:
        _nodeparam: NodeParam_t = __parse_NodeParam_t(nodeparam)
        spec.Params.append(_nodeparam)
    return spec


def __parse_NodeParam_t(node: ETree.Element):
    """parse NodeParam_t from ETree element. must under TreeNodesModel->{custom node}->{node}

    Args:
        node (ETree.Element): node for parse 

    Returns:
        NodeParam_t: parsed NodeParam_t
    """
    spec: NodeParam_t = NodeParam_t()
    # parse Direction
    for inputoutput in eInputOutput:
        if node.tag == inputoutput.name:
            spec.Direction = inputoutput
            break
    if spec.Direction == None:
        raise NameError(
            "error occured at parsing Nodeparam at TreeNodesModel. cannot parse input & output direction!")
    # parse Description
    spec.Desc = node.text
    # parse variable name
    spec.Name = node.attrib['name']
    # parse variable type

    spec.VariableType, _, _ = ParseVariable.Parse(node.attrib['default'])

    return spec
