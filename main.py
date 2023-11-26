from Input_Handling.PDAconfig import*
from Input_Handling.htmltokenizer import*
from PDA_Model.PushDownAutomaton import*
import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('pdaconfig', help='')
parser.add_argument('htmlpath', help='')

arguments = parser.parse_args()

# main
PDA = getPDA(arguments.pdaconfig)
InputTokens, rowinfo, colinfo = TokenizeThisHtmlFile(arguments.htmlpath)

start_node = node(PDA.start_state, InputTokens, stack(PDA.start_symbol))
start_nodes = PDA.epsilonclosure(start_node)

# DEBUGGER MODE HERE!
# set the debugmode to true and you good to go!
RemainingTokensLength,Accepted = compute(PDA, start_nodes, 1, debugmode = True)
ErrorIndex = len(InputTokens) - RemainingTokensLength

if (Accepted):
    print("\x1b[32mAccepted\x1b[30m")
else:
    if ErrorIndex == len(InputTokens) - 1: 
        # I don't know why but I guess the indexing got messed up somewhere
        Line = rowinfo[0]
        Column = colinfo[0]
    else:
        Line = rowinfo[ErrorIndex+1]
        Column = colinfo[ErrorIndex+1]
    print(f"\x1b[31mSyntax Error\x1b[36m" + f" at [Ln {Line}, Col {Column}]\x1b[30m")