#!usr/bin/env python3

from .EnumsStructs import *


def Parse(MainSubTree: ETree.Element, SubTrees: List[SubTree_t], CustomNodes: List[TreeNodesModel_t]) -> Tuple[List[TotalTree_t], List[ParentChild_t]]:
    """Parse total tree and parent-child infos from mainTree

    Args:
        MainSubTree (ETree.Element): main root tree
        SubTrees (List[SubTree_t]): all subtrees list
        CustomNodes (List[TreeNodesModel_t]): all custom node infos

    Returns:
        Tuple[List[TotalTree_t], List[ParentChild_t]]: totalTree, parentChild
    """

    resultsTotalTree: List[TotalTree_t] = []
    resultsParentChild: List[TotalTree_t] = []

    _uid: int = 1
    root: TotalTree_t = __parseTatalTree_t_Root(MainSubTree)
    root.UID = _uid

    resultsTotalTree.append(root)

    for info in resultsTotalTree:
        children: ETree.Element = __expandChildrenFromTreeNode(
            node=info.TreeNodePtr, subTrees=SubTrees)

        if len(children) > 0:
            new_ParentChild: ParentChild_t = ParentChild_t()
            new_ParentChild.ParentIdx = info.UID - 1
            new_ParentChild.ChildrenIdxs = list(
                range(len(resultsTotalTree), len(resultsTotalTree)+len(children)))
            resultsParentChild.append(new_ParentChild)

        for child in children:
            new_TotalTree_t: TotalTree_t = __parseTotalTree_t(
                Node=child, CustomNodes=CustomNodes)
            _uid = _uid + 1
            new_TotalTree_t.UID = _uid
            resultsTotalTree.append(new_TotalTree_t)

    return resultsTotalTree, resultsParentChild
    pass


def __expandChildrenFromTreeNode(node: ETree.Element, subTrees: List[SubTree_t]) -> ETree.Element:
    if node.tag == 'SubTree':
        for subt in subTrees:
            if subt.Name == node.attrib["ID"]:
                return subt.NodePtr
        raise NameError("No matching subtree name in Subtree lists")
    else:
        return node
    pass


def __parseTatalTree_t_Root(Node: ETree.Element) -> TotalTree_t:
    result: TotalTree_t = TotalTree_t()
    result.Attrib = Node.attrib
    result.ChildNum = 1
    result.NodeType = eNodeType.SubTree
    result.Tag = "BehaviorTree"
    result.isCustom = False
    result.Name = "RootTree"
    result.TreeNodePtr = Node
    if Node.attrib['ID'] != "RootTree":
        raise NameError("RootTree name is strange, is if named 'RootTree' ??")
    return result
    pass


def __parseTotalTree_t(Node: ETree.Element, CustomNodes: List[TreeNodesModel_t]) -> TotalTree_t:
    result: TotalTree_t = TotalTree_t()
    # parse Tag
    result.Tag = Node.tag
    # parse Attrib
    result.Attrib = Node.attrib
    # parse TreeNodePtr
    result.TreeNodePtr = Node
    # parse ChildNum
    result.ChildNum = len(Node)
    # parse NodeType, Name, isCustom, CustomPtr
    result.NodeType, result.Name, result.isCustom, result.CustomPtr = __parseNodeTypeFromNode(
        Tag=Node.tag, ID=Node.attrib.get('ID'), CustomNodes=CustomNodes)

    return result
    pass


def __parseNodeTypeFromNode(Tag: str, ID: str, CustomNodes: List[TreeNodesModel_t]) -> Tuple[eNodeType, str, bool, TreeNodesModel_t]:
    nodeType: eNodeType = None
    nodeName: str = None
    isCustomType: bool = False
    CustomPtr: TreeNodesModel_t = None

# check is base type
    if ID == None:
        for enum in eAction_base:
            if Tag == enum.name:
                nodeType = eNodeType.Action
                nodeName = enum.name
                break
        if (nodeType == None):
            for enum in eCondition_base:
                if Tag == enum.name:
                    nodeType = eNodeType.Condition
                    nodeName = enum.name
                    break
        if (nodeType == None):
            for enum in eControl_base:
                if Tag == enum.name:
                    nodeType = eNodeType.Control
                    nodeName = enum.name
                    break
        if (nodeType == None):
            for enum in eDecorator_base:
                if Tag == enum.name:
                    nodeType = eNodeType.Decorator
                    nodeName = enum.name
                    break
        if (nodeType == None):
            for enum in eSubTree_base:
                if Tag == enum.name:
                    nodeType = eNodeType.SubTree
                    nodeName = enum.name
                    break
        if (nodeType != None):
            isCustomType = False
            return nodeType, nodeName, isCustomType, None
    else:
        # check if custom type
        for node in CustomNodes:
            if ID == node.ID:
                nodeType = node.NodeType
                isCustomType = True
                CustomPtr = node
                nodeName = node.ID
                return nodeType, nodeName, isCustomType, CustomPtr

    raise NameError("Cannot parse node type from base & custom node infos")
    pass
