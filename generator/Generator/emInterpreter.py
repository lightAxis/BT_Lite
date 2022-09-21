#!usr/bin/env python3

from typing import Dict
import em
import os


def Generate(templatePath: str, outputPath: str, em_globals: Dict) -> None:
    """using empy, generate the code from template and output file path

    Args:
        templatePath (str): path for template. .em 
        outputPath (str): output path for file
        em_globals (Dict): all globals Dict used when generate code using empy
    """
    ofile = open(outputPath, 'w')
    interpreter = em.Interpreter(output=ofile, globals=em_globals, options={
        em.RAW_OPT: True, em.BUFFERED_OPT: True
    })
    interpreter.file(open(templatePath))
    interpreter.shutdown()
    ofile.close()
    print("generating.. "+outputPath)
    pass
