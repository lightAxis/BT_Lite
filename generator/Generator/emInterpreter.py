#!usr/bin/env python3

from typing import Dict
import em
import os


def Generate(templatePath: str, outputPath: str, em_globals: Dict) -> None:
    ofile = open(outputPath, 'w')
    interpreter = em.Interpreter(output=ofile, globals=em_globals, options={
        em.RAW_OPT: True, em.BUFFERED_OPT: True
    })
    interpreter.file(open(templatePath))
    interpreter.shutdown()
    ofile.close()
    pass
