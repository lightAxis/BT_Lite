#!usr/bin/env python3

from enum import IntEnum
from dataclasses import dataclass, field
from tokenize import Name
from typing import List, Dict, Tuple
import xml.etree.ElementTree as ETree


class eNodeType(IntEnum):
    UNDEFINED = 0,
    Action = 1,
    Condition = 2,
    Control = 3,
    Decorator = 4,
    SubTree = 5,


class eAction_base(IntEnum):
    AlwaysFailure = 0,
    AlwaysSuccess = 1,


class eCondition_base(IntEnum):
    pass


class eControl_base(IntEnum):
    Fallback = 0,
    IfThenElse = 1,
    ManualSelector = 2,
    Parallel = 3,
    ReactiveFallback = 4,
    ReactiveSequence = 5,
    Sequence = 6,
    SequenceStar = 7,
    Switch2 = 8,
    Switch3 = 9,
    Switch4 = 10,
    Switch5 = 11,
    Switch6 = 12,
    WhileDoElse = 13,


class eDecorator_base(IntEnum):
    BlackboardCheckBool = 1,
    BlackboardCheckDouble = 2,
    BlackboardCheckInt = 3,
    BlackboardCheckString = 4,
    Delay = 5,
    ForceFailure = 6,
    ForceSuccess = 7,
    Inverter = 8,
    KeepRunningUntilFailure = 9,
    Repeat = 10,
    RetryUntilSuccessful = 11,
    Timeout = 12,


class eSubTree_base(IntEnum):
    RootTree = 0,
    pass


class eInputOutput(IntEnum):
    input_port = 0,
    output_port = 1,


@dataclass
class SubTree_t:
    Tag: str = None
    Name: str = None
    NodePtr: ETree.Element = None


@dataclass
class NodeParam_t:
    Direction: eInputOutput = None
    VariableType: str = None
    Name: str = None
    Desc: str = None


@dataclass
class TreeNodesModel_t:
    Tag: str = None
    NodeType: eNodeType = None
    ID: str = None
    Attrib: Dict[str, str] = None
    Params: List[NodeParam_t] = None


@dataclass
class TotalTree_t:
    Tag: str = None
    NodeType: eNodeType = None
    Name: str = None
    Attrib: Dict[str, str] = None
    UID: int = None
    ChildNum: int = None
    Children: List[int] = None
    TreeNodePtr: ETree.Element = None
    isCustom: bool = False
    CustomPtr: TreeNodesModel_t = None


@dataclass
class ParentChild_t:
    ParentIdx: int = None
    ChildrenIdxs: List[int] = None


@dataclass
class CustomParam_t:
    Type: str = None
    Name: str = None


@dataclass
class ConstParam_t:
    Type: str = None
    Value: str = None
    Index: int = None


@dataclass
class CustomGenerations_t:
    Actions: List[TreeNodesModel_t] = None
    Conditions: List[TreeNodesModel_t] = None
    Controls: List[TreeNodesModel_t] = None
    Decorators: List[TreeNodesModel_t] = None
    SubTrees: List[TreeNodesModel_t] = None
    Params: List[CustomParam_t] = None
    ConstParams: List[CustomParam_t] = None


@dataclass
class GrootXMLParser_out_t:
    TreeNodesModels: List[TreeNodesModel_t] = None
    TotalTree: List[TotalTree_t] = None
    ParentChilds: List[ParentChild_t] = None


@dataclass
class GenerationIngredients_t:
    outputPathBase: str = None
    templatePathBase: str = None
    BT_Name: str = None
    ParsedGroot: GrootXMLParser_out_t = None
    CustomGenerations: CustomGenerations_t = None
