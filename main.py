from Input_Handling.PDAconfig import*
from PDA_Model.PushDownAutomaton import*
import argparse

parser = argparse.ArgumentParser(description='Description of your script')
parser.add_argument('pdaconfig', help='Description of arg1')
parser.add_argument('htmlpath', help='Description of arg2')

arguments = parser.parse_args()

tc1 =   ["HTML", "CLOSETAG",
            "BODY", "CLOSETAG", 
                "H1", "CLOSETAG", "ENDH1",
            "ENDBODY",
            "HEAD",
                "TITLE", "CLOSETAG", "ENDTAG",
            "ENDHEAD",
        "HTML"]

tc2 =   ["HTML", "CLOSETAG", 
            "HEAD", "CLOSETAG",
               "TITLE", "CLOSETAG", "ENDTITLE"
            "ENDHEAD",
            "BODY", "CLOSETAG",
                "H1", "CLOSETAG", "ENDH1"
                "P", "CLOSETAG", "ENDP",
            "ENDBODY",
        "ENDHTML"]

tc3 =   ["HTML", "CLOSETAG", 
            "HEAD", "CLOSETAG", "ENDHEAD",
            "BODY", "CLOSETAG",
            "ENDBODY",
        "ENDHTML"]

tc4 = ["HTML", "CLOSETAG", "BODY", "ENDBODY", "HEAD", "ENDHEAD", "ENDHTML"]


def isHTML_Accepted(PDAConfigpath: str, HTMLpath: str) -> bool:

    PDA = getPDA(PDAConfigpath)


    # InputStr = getText(HTMLpath)
    InputStr = tc4
    start_node = node(PDA.start_state, InputStr, stack(PDA.start_symbol))
    start_nodes = PDA.epsilonclosure(start_node)

    # print(len(PDA.delta.tr))
    # for i in PDA.delta.transitions:
    #     if i.startstack == "/":
            # print(i)

    # for i in newset:
    #     print(i)

    return compute(PDA, start_nodes, 1, debugmode=True)

# main
if (isHTML_Accepted(str(arguments.pdaconfig), str(arguments.htmlpath))):
    print("\x1b[32mAccepted\x1b[30m")
else:
    print("\x1b[31mSyntax Error\x1b[30m")

# print("        HEAD_BLOCK TITLE epsilon TITLE_TAG [ENDTITLE]\n".strip())