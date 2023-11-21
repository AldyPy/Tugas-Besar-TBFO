import os
import sys

parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_directory)

from PDA_Model.PushDownAutomaton import *

# Mengembalikan set dari tiap kata dalam line
def getWords(line):
    Words = []
    Word = ""
    for char in line:
        if (char == " "):
            Words.append(Word)
            Word =""

        elif (char =="#"):
            Words.append(Word)
            break
    
        else:
            Word += char

    return Words


def getPDA(file_name):
    # Buka File
    f = open(file_name, 'r')
    # Inisialisasi
    delta = transitionFunction("delta",set())
    line_count =1
    states = set()
    input_symbols = set()
    stack_symbols = set()
    starting_state = set()
    starting_stack = set()
    accepting_states = set()
    accept = set()

    states_dict = {} # Keynya string valuenya state,  Productions dijadiin transition function

    for line in f:
        if (line_count ==1):
            for i in getWords(line):
                states_dict[i] = state(i)
                states.add(states_dict[i])
        elif (line_count ==2 ):
            input_symbols |= set(getWords(line))
        elif (line_count ==3):
            stack_symbols|= set(getWords(line))
        elif (line_count==4):
            starting_state = states_dict[getWords(line)[0]]
        elif (line_count ==5):
            starting_stack = getWords(line)[0]
        elif (line_count ==6):
            for i in getWords(line):
                accepting_states |= {states_dict[i]}
        elif (line_count == 7):
            if ("F" in getWords(line)):
                accept |= {"F"}
            if ("E" in getWords(line)):
                accept |= {"E"}
        else:
            _ = getWords(line)
            
            s1=_[0]
            s2=_[1]
            s3= epsilon if (_[2] == "epsilon") else _[2]
            s4= epsilon if (_[3] == "epsilon") else _[3]
            s5= epsilon if (_[4] == "epsilon") else _[4]
            
            
            delta.addTransition(singleTransition(states_dict[s1], states_dict[s2], s3, s4, s5))
                
            
        line_count += 1
    
    PDA = PushDownAutomaton(starting_state,
                            input_symbols,
                            stack_symbols,
                            delta,
                            starting_state,
                            starting_stack,
                            accepting_states,
                            str(accept.pop()))

    return PDA