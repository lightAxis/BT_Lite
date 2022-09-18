#!usr/bin/env python3

from .EnumsStructs import *


def Parse(variableStr: str) -> Tuple[str, str, bool]:
    """parse Param info from parameter string

    Args:
        variableStr (str): parameter string input

    Returns:
        Tuple[str, str, bool]: TypeName, InputValName, isConst
    """
    TypeName: str = None
    InputValName: str = None
    isConst: bool = None
    # parse isConst
    _type = variableStr
    _param_deli_idx = _type.find("{")
    if (_param_deli_idx == -1):
        isConst = True
    else:
        isConst = False
    # parse Typename
    _type = _type.replace('{', '')
    _type = _type.replace('}', '')
    _typedef_idx = _type.find('__')
    if (_typedef_idx == -1):
        raise NameError("Cannot convert Nodeparam, no typedef indicator")
    TypeName = _type[_typedef_idx+2:]
    # parse Inputval
    InputValName = _type[:_typedef_idx]

    return TypeName, InputValName, isConst
