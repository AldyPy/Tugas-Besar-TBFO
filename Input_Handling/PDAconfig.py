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

        elif (char =="\n"):
            Words.append(Word)
            break
    
        else:
            Word += char

    return Words

def getFiveWords(line):
    
    count = 0
    current_word = ""
    words = ["" for i in range(5)]
    for i in line:
        
        if i == " " and count < 4:
            words[count] = current_word
            count += 1
            current_word = ""

        elif count == 4:
            if i != "\n":
                words[4] += i

        else:
            current_word += i
    
    return words

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
        if (line_count == 1):
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
        elif (line_count == 6):
            for i in getWords(line):
                accepting_states |= {states_dict[i]}
        elif (line_count == 7):
            if ("F" in getWords(line)):
                accept |= {"F"}
            if ("E" in getWords(line)):
                accept |= {"E"}
        elif (line[0] == '\n'):
            pass
        elif (line.strip(" ")[0] in ['#', '\n']):
            pass

        else:
        
            _ = getFiveWords(line.strip())
            
            s1=_[0]
            if _[1] == "epsilon":
                s2 = epsilon
            else:
                s2 = _[1]

            try:
                if _[2] == "epsilon":
                    s3 = epsilon
                else:
                    s3 = _[2]
            except:
                print(line_count)
                print(_)

            s4= _[3]

            listOfStackValues = []

            try:
                s5 = _[4]
            except:
                print("S5")
                print(line_count)

            if s5 in ['[', ']']:
                listOfStackValues.append(s5) 

            else:
                i = 0
                
                while i < len(s5):
                    
                    char = s5[i]
                    if char != '[':
                        listOfStackValues.append(char)
                        i += 1
                    else:
                        token = ""
                        i -=- 1
                        char = s5[i]
                        while char != ']':
                            token += char
                            i += 1
                            char = s5[i]
                        
                        if token == "EMPTY":
                            pass
                        else:
                            listOfStackValues.append(token)
                        i += 1

                try:
                    delta.addTransition(singleTransition(states_dict[s1], s2, s3, states_dict[s4], listOfStackValues[::-1]))
                except:
                    print(_)
                    print(line_count)
            
            
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