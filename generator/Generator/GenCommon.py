#!usr/bin/env python3

import os
from shutil import copyfile
import em

from GrootXMLParser.EnumsStructs import *
from GrootXMLParser import ParseVariable

from . import emInterpreter


def Generate(input: GenerationIngredients_t) -> None:
    """Generate common sources\n
    - Enums.h
    - NodeBase.h
    - Nodes.h
    - (NAMESPACE).h
    - Delegate.h

    Args:
        input (GenerationIngredients_t): Parsed Results from GrootXMLParser module
    """

    __generate(templatePath=os.path.join(input.templatePathBase, "Enums.h.em"),
               outputPath=os.path.join(input.outputPathBase, "Enums.h"),
               BT_name=input.BT_Name)

    __generate(templatePath=os.path.join(input.templatePathBase, "NodeBase.h.em"),
               outputPath=os.path.join(input.outputPathBase, "NodeBase.h"),
               BT_name=input.BT_Name)

    __generate(templatePath=os.path.join(input.templatePathBase, "Nodes.h.em"),
               outputPath=os.path.join(input.outputPathBase, "Nodes.h"),
               BT_name=input.BT_Name)

    __generate(templatePath=os.path.join(input.templatePathBase, "Params.h.em"),
               outputPath=os.path.join(input.outputPathBase, "Params.h"),
               BT_name=input.BT_Name)

    __generate(templatePath=os.path.join(input.templatePathBase, "ParamBase.h.em"),
               outputPath=os.path.join(input.outputPathBase, "ParamBase.h"),
               BT_name=input.BT_Name)

    __generate_Logger(input)

    __generate(templatePath=os.path.join(input.templatePathBase, "MAIN.h.em"),
               outputPath=os.path.join(
                   input.outputPathBase, input.BT_Name + ".h"),
               BT_name=input.BT_Name)

    templatePathBase = os.path.join(input.templatePathBase, "Delegate.h.em")
    outputPathBase = os.path.join(input.outputPathBase, "Delegate.h")
    copyfile(templatePathBase, outputPathBase)

    pass


def __generate(templatePath: str, outputPath: str, BT_name: str):
    em_global = {'NAMESPACE': BT_name}

    emInterpreter.Generate(templatePath=templatePath,
                           outputPath=outputPath, em_globals=em_global)

    pass


def __generate_Logger(input: GenerationIngredients_t):
    em_global = {
        'NAMESPACE': input.BT_Name,
        'NODE_NUM': len(input.ParsedGroot.TotalTree)
    }
    templatePath: str = os.path.join(input.templatePathBase, "Logger.h.em")
    outputPath: str = os.path.join(input.outputPathBase, "Logger.h")

    emInterpreter.Generate(templatePath=templatePath,
                           outputPath=outputPath, em_globals=em_global)
    pass
