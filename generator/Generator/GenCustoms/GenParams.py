#!usr/bin/env python3

import os

from GrootXMLParser.EnumsStructs import *
from GrootXMLParser import ParseVariable

from Generator import emInterpreter


def Generate(input: GenerationIngredients_t):
    for param in input.CustomGenerations.Params:
        __generateParam(param, input)
    pass


def __generateParam(param: CustomParam_t, input: GenerationIngredients_t):

    className: str = None
    paramName: str = None
    paramType: str = None

    className, paramName, paramType = __makeParamStrs(param)

    em_globals = {
        'NAMESPACE': input.BT_Name,
        'className': className,
        'paramName': paramName,
        'paramType': paramType}

    templatePath = os.path.join(
        input.templatePathBase, "generated/Params/PARAM.h.em")
    outputPath = os.path.join(
        input.outputPathBase, "generated/Params/"+paramName+".h")
    emInterpreter.Generate(templatePath=templatePath,
                           outputPath=outputPath, em_globals=em_globals)
    pass


def __makeParamStrs(param: CustomParam_t) -> Tuple[str, str, str]:
    """make param strings

    Args:
        param (CustomParam_t): custom param t

    Returns:
        Tuple[str, str, str]: className, paramName, paramType
    """

    className: str = "PARAM_"+param.Name
    paramName: str = param.Name
    paramType: str = param.Type

    return className, paramName, paramType
    pass
