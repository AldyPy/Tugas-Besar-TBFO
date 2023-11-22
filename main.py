from Input_Handling.htmlInput import*
from Input_Handling.PDAconfig import*
from PDA_Model.PushDownAutomaton import*
import argparse

parser = argparse.ArgumentParser(description='Description of your script')
parser.add_argument('pdaconfig', help='Description of arg1')
parser.add_argument('htmlpath', help='Description of arg2')

arguments = parser.parse_args()


def isHTML_Accepted(PDAConfigpath: str, HTMLpath: str) -> bool:

    PDA = getPDA(PDAConfigpath)

    InputStr = getText(HTMLpath)
    start_node = node(PDA.start_state, InputStr, stack(PDA.start_symbol))
    start_nodes = PDA.epsilonclosure(start_node)
    # newset = set()
    # for i in start_nodes:
    #     print(i)
    # newset |= PDA.epsilonclosure(i)

    # for i in newset:
    #     print(i)

    return compute(PDA, start_nodes, 0)

# main
if (isHTML_Accepted(str(arguments.pdaconfig), str(arguments.htmlpath))):
    print("\x1b[32mAccepted\x1b[30m")
else:
    print("\x1b[31mSyntax Error\x1b[30m")