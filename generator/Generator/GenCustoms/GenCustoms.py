#!usr/bin/env python3

import os
from re import template

from GrootXMLParser.EnumsStructs import *

from Generator import emInterpreter

from . import GenEnums, GenCommon


def Generate(input: GenerationIngredients_t) -> None:

    __makeDir(outputPathBase=input.outputPathBase)

    GenCommon.Generate(input)
    GenEnums.Generate(input)
    pass


def __makeDir(outputPathBase: str):
    dirsToMake: List[str] = []
    dirsToMake.append(os.path.join(outputPathBase, "generated"))
    dirsToMake.append(os.path.join(outputPathBase, "generated/Actions"))
    dirsToMake.append(os.path.join(outputPathBase, "generated/Decorators"))
    dirsToMake.append(os.path.join(outputPathBase, "generated/Controls"))
    dirsToMake.append(os.path.join(outputPathBase, "generated/Conditions"))
    dirsToMake.append(os.path.join(outputPathBase, "generated/SubTrees"))
    dirsToMake.append(os.path.join(outputPathBase, "generated/Params"))
    dirsToMake.append(os.path.join(outputPathBase, "generated/Enums"))
    for dir in dirsToMake:
        if os.path.exists(dir) == False:
            os.mkdir(dir)
    pass
