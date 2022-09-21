#!usr/bin/env python3

from genericpath import isfile
import os

from GrootXMLParser.EnumsStructs import *
from GrootXMLParser import ParseVariable

from . import emInterpreter


def Generate(input: GenerationIngredients_t) -> None:
    """Generate Bases of BT\n
    - base/...h

    Args:
        input (GenerationIngredients_t): Parsed Results from GrootXMLParser module
    """

    __makeDir(input.outputPathBase)

    pathList: List[str] = []

    __getAllEmFilesInBase(os.path.join(
        input.templatePathBase, "base"), "", pathList)

    for localTemplatePath in pathList:
        fullTemplatePath = os.path.join(
            input.templatePathBase, "base", localTemplatePath)
        outputFileName, _ = os.path.splitext(localTemplatePath)
        outputPath = os.path.join(input.outputPathBase, "base", outputFileName)
        em_globals = {'NAMESPACE': input.BT_Name}
        emInterpreter.Generate(templatePath=fullTemplatePath,
                               outputPath=outputPath,
                               em_globals=em_globals)

    pass


def __makeDir(outputPathBase: str):
    dirsToMake: List[str] = []
    dirsToMake.append(os.path.join(outputPathBase, "base"))
    dirsToMake.append(os.path.join(outputPathBase, "base/Actions"))
    dirsToMake.append(os.path.join(outputPathBase, "base/Decorators"))
    dirsToMake.append(os.path.join(outputPathBase, "base/Controls"))
    dirsToMake.append(os.path.join(outputPathBase, "base/Conditions"))
    dirsToMake.append(os.path.join(outputPathBase, "base/SubTrees"))
    dirsToMake.append(os.path.join(outputPathBase, "base/Params"))
    for dir in dirsToMake:
        if os.path.exists(dir) == False:
            os.mkdir(dir)
    pass


def __getAllEmFilesInBase(basePath: str, localPath: str, pathList: List[str]):
    currentPath = os.path.join(basePath, localPath)
    if os.path.isfile(currentPath) == True:
        _, ext = os.path.splitext(currentPath)
        if (ext == '.em'):
            pathList.append(localPath)
    elif os.path.isdir(currentPath) == True:
        subfiles = os.listdir(currentPath)
        for subfile in subfiles:
            __getAllEmFilesInBase(basePath,
                                  os.path.join(localPath, subfile), pathList)
    pass
