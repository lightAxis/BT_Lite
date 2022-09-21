#!usr/bin/env python3

from enum import IntEnum
from dataclasses import dataclass, field
from tokenize import Name
from typing import List, Dict, Tuple
import xml.etree.ElementTree as ETree


class eNodeType(IntEnum):
    Action = 0,
    Condition = 1,
    Control = 2,
    Decorator = 3,
    SubTree = 4,


class eAction_base(IntEnum):
    AlwaysFailure = 0,
    AlwaysSuccess = 1,


class eCondition_base(IntEnum):
    pass


class eControl_base(IntEnum):
    Fallback = 0,
    IfThenElse = 1,
    Parallel = 2,
    ReactiveFallback = 3,
    ReactiveSequence = 4,
    Sequence = 5,
    SequenceStar = 6,
    Switch2 = 7,
    Switch3 = 8,
    Switch4 = 9,
    Switch5 = 10,
    Switch6 = 11,
    WhileDoElse = 12,


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
