#!usr/bin/env python3

from dataclasses import dataclass
from re import I
from typing import List
import os
import filecmp
import sys
import argparse

try:
    import em
except ImportError as e:
    print("Failed to import em: " + str(e))
    print("")
    print("You may need to install it using:")
    print("    pip3 install --user empy")
    print("")
    sys.exit(1)

import em


import xml.etree.ElementTree as ET


@dataclass
class variables:
    name: str
    type: str
    direction: str


var: List[variables] = []
var.append(variables(name="var1", type="int", direction="in"))
var.append(variables(name="var2", type="float", direction="out"))


def makeGen():
    param = []
    for var_ in var:
        st = ""
        if var_.direction == "in":
            st = "const "+str(var_.type)+" &"+str(var_.name)
        elif var_.direction == "out":
            st = str(var_.type)+" *"+str(var_.name)
        param.append(st)
    return "("+", ".join(param)+")"


def make():
    param = []
    for var_ in var:
        st = ""
        if var_.direction == "in":
            st = str(var_.name)
        elif var_.direction == "out":
            st = "&"+str(var_.name)
        param.append(st)
    return "("+", ".join(param)+")"


em_globals = {
    "func_name": "thisisTestname__",
    "var": var,
    "makeGen": makeGen,
    "make": make,
    "here": os.path.abspath(__file__)
}


asdf = em_globals["func_name"]

ofile = open("./now.cpp", 'w')
interpreter = em.Interpreter(output=ofile, globals=em_globals, options={
    em.RAW_OPT: True, em.BUFFERED_OPT: True
})

interpreter.file(open("now.cpp.em"))
interpreter.shutdown()
ofile.close()

tree = ET.parse('test.xml')

root = tree.getroot()


def prints(root):
    print("----------------")
    print(len(root))
    print(root.tag)
    print(root.attrib)
    for key in root.attrib.keys():
        print(key, root.attrib[key])

    if (len(root) > 0):
        for root_ in root:
            prints(root_)


prints(root)
