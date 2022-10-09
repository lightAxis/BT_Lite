#!usr/bin/env python3

from dataclasses import dataclass
from typing import List, Dict
import os
import sys
import argparse

try:
    import em
except ImportError as e:
    print("Failed to import em in python3 :", str(e))
    print("")
    print("you may need to install it using")
    print(" pip3 install --user empy")
    print("")
    sys.exit(1)

from GrootXMLParser.GrootXMLParser import GrootXMLParser as GXMLP
from Generator.Generator import Generator as CodeGen

if __name__ == "__main__":
    print("this is main")
    now = os.path.abspath(__file__)
    now_dir = os.path.dirname(now)
    xml_path = os.path.join(now_dir, "test.xml")
    print(now)
    print(now_dir)
    print(xml_path)

    Parser: GXMLP = GXMLP(xml_path)
    ParserResult = Parser.Parse()

    now_test_gen = os.path.dirname(now_dir)
    now_test_gen = os.path.join(now_test_gen, "test_gen")

    codegen: CodeGen = CodeGen(ParserResult, "BT_TEST", now_test_gen)
    codegen.Generate()

else:
    raise NameError("Strange started without main")
