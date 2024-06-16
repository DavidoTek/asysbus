#!/usr/bin/env python3
# Extracts the ASB_CMD defines from asb_proto.h and prints them in python format

import os


FILE_PATH = os.path.dirname(os.path.abspath(__file__))
ASB_PROTO_H = os.path.join(FILE_PATH, "../../src/asb_proto.h")
ASB_PROTO_PY = os.path.join(FILE_PATH, "asb_proto.py")


# Read the ASB_CMD defines from asb_proto.h
python_defines = ""
with open(ASB_PROTO_H, "r") as f:
    lines = f.readlines()
    for line in lines:
        if not "ASB_CMD" in line:
            continue
        
        c_keywords = line.split()

        python = c_keywords[1] + " = " + c_keywords[2]
        if len(c_keywords) > 3:
            c_keywords[3] = c_keywords[3].replace("//", "  # ")
            python += " ".join(c_keywords[3:])
        python += "\n"
        python_defines += python

print(python_defines)
