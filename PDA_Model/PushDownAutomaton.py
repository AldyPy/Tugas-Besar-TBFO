#################################
""" TUBES TBFO """
""" MODEL PUSH DOWN AUTOMATA """
#################################


# definisi epsilon, dan huruf
epsilon = ""
lowercaseletters = "qwertyuiopasdfghjklzxcvbnm "

# Definisi type stack menggunakan list
# Stack mempunyai 4 primitif penting di PDA: isEmpty, push, pop, dan top
# top mengembalikan elemen paling atas Stack
# push menambahkan elemen ke top dari stack
# pop mengambil satu elemen dari top stack dan mengembalikan nilainya
# isEmpty ya isEmpty
class stack:
    def __init__(self, start_element: str):
        self.elements = [start_element]
    
    def top(self):
        return f"{self.elements[0]}"

    def push(self, value):
        self.elements.append("dummy")
        for i in range(len(self.elements) - 1, 0, -1):
            self.elements[i] = self.elements[i-1]
        self.elements[0] = value
    
    def pop(self):
        val = self.top()
        self.elements = self.elements[1:len(self.elements):]
        return val

    def isEmpty(self) -> bool:
        return len(self.elements) == 1 # Stack only contains 'Z' (starting element)


# Python jelek; creating multiple instances of stacks point to the same address in memory 
# jadi harus bikin baru trus copy manual satu per satu :(
def copystack(s: stack):
    s_out = stack('Never gonna give you up')
    _ = s_out.pop()

    for i in s.elements:
        s_out.elements.append(i)
    
    return s_out


# definisi type state 
# mempunyai satu parameter, yaitu nama
# name              : str (nama state, e.g. P, Q, F)
class state:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

# definisi type NODE
# Node adalah abstract data type yang digunakan sebagai pengganti STATE dalam kalkulasi PDA.
# Node terdiri dari state saat ini, sisa input string, serta isi stack.
# Isi Node akan digunakan dalam fungsi transisi
class node:
    def __init__(self, state: state, inputstr: list[str], stack: stack):
        self.state = state
        self.inputstr = inputstr
        self.stack = stack

    def __str__(self):
        titik_titik = "..." if len(self.inputstr) > 5 else ""
        return f"State: {self.state}\nInput Token: {self.inputstr[0:7]}{titik_titik}\nStack: {self.stack.elements[0:7]})"
    

# definisi single transition function
# mempunyai lima komponen, yaitu sebagai berikut
# startstate        : state
# endstate          : state
# transition symbol : char (di python tidak ada char jadi digunakan string)
# startstack        : simbol yang di-'consume' pada top dari stack ketika melakukan transisi (tidak lebih dari satu)
# endstack          : simbol yang di push ke stack setelah melakukan transisi (bisa lebih dari satu)
class singleTransition:
    def __init__ (self, startstate: state, symbol: str, startstack: str, endstate: state, endstack: list[str]):
        
        self.startstate = startstate
        self.endstate = endstate
        self.startstack = startstack
        self.endstack = endstack
        self.symbol = symbol

    def __str__(self):
        return f"({self.startstate},{self.symbol},{self.startstack} -> {self.endstate},{self.endstack})"

# definisi transition function (yaitu a set of single transition functions)
# mempunyai dua parameter, yaitu sebagai berikut
# name                          : str
# set of single functions       : set of single transition function
class transitionFunction():
    def __init__ (self, name: str, transitions: set[singleTransition]):
        self.name = name
        self.transitions = transitions
    
    def addTransition(self, transition: singleTransition):
        self.transitions.add(transition)

    def __str__(self):
        return f"{self.transitions}"


# Sekarang kita sudah siap untuk mendefinisikan PDA
class PushDownAutomaton():
    def __init__ (self, 
                  Q: set[state],                # Q is the set of states
                  Epsilon: set[str],            # Epsilon is the set of input symbols recognized by the PDA
                  Gamma: set[str],              # Gamma = set of stack symbols
                  delta: transitionFunction,    # delta is the transition function
                  start_state: state,           # yg ini gua gk harus jelasin 
                  start_symbol: str,            # start_symbol = first symbol in stack
                  F: set[state],                # F is the set of final/accepting states. 
                                                # F = {} if PDA Accepts by empty stack

                  AcceptKey: str                # 'F' will denote a PDA that accepts by final state
                                                # 'E' will denote a PDA that accepts by empty stack
                ):

        self.Q = Q
        self.Epsilon = Epsilon
        self.Gamma = Gamma
        self.delta = delta
        self.start_state = start_state
        self.start_symbol = start_symbol
        self.F = F
        self.acceptkey = AcceptKey
    
    # Definisi transitionable: mengembalikan true jika inputstr bisa ditransisi i.e. ada simbol nya di Epsilon
    def transitionable(PDA, symbol: str) -> bool:
        if not (symbol in PDA.Epsilon):
            return False
        else:
            return True
    
    # Definisi Epsilon Closure dari NODE -> Node yang bisa dicapai tanpa baca input (a.k.a. melalui epsilon)
    # IMPORTANT note: Elements from the stack may or may not be modified
    def epsilonclosure(PDA, P: node) -> set[node]:
        result = {P}

        for i in PDA.delta.transitions: # Find all satisfiable epsilon transitions

            if ((i.startstate == P.state) and (i.symbol == epsilon) and (i.startstack == P.stack.top() or i.startstack == epsilon)):

                # Create resulting node
                a = node(i.endstate, P.inputstr, copystack(P.stack))

                # Push and pop to the stack
                if (i.startstack != epsilon):
                    _ = a.stack.pop()
                
                if (len(i.endstack) != 0):
                    for j in i.endstack:
                        a.stack.push(j)

                result |= {a}

        # for i in result:
        #     print(i)
        
        return result
    
    # Definisi transition: mengembalikan set of possible current nodes 
    # setelah simbol digunakan untuk "maju"
    def transition(PDA, P: node) -> set[node]:
        resultingNodes = set()
        symbol = P.inputstr[0]

        # print(P.inputstr)


        for i in (PDA.delta.transitions):
            
            # print(i.startstack)

            if (P.state == i.startstate) and ((symbol == i.symbol)) and (
                    (i.startstack == P.stack.top()) or (i.startstack == epsilon)
                ):
                # Create resulting node
                a = node(i.endstate, P.inputstr[1:], copystack(P.stack))

                # Push and pop to the stack
                if (i.startstack != epsilon):
                    _ = a.stack.pop()
                
                if (len(i.endstack) != 0):
                    for j in i.endstack:
                        a.stack.push(j)

                # print(i.startstack, i.endstack)   # For debugging; print resulting node set
                resultingNodes.add(a)

        if (P.stack.top() in PDA.Gamma):
            resultingNodes |= PDA.epsilonclosure(P)
            resultingNodes = resultingNodes.difference({P})

        # if (P.stack.top() == P.inputstr[0] and P.inputstr[0] == "/"):
        #     for j in resultingNodes:
        #         print("Resulting nodes\n", j)

        return resultingNodes       # Jika tidak ditemukan transisi yang bisa dijalankan,
                                    #  maka actualResultingNodes akan kosong

def isSameNode(node1: node, node2: node):
    return (node1.inputstr == node2.inputstr) and (node1.stack.elements == node2.stack.elements) and (node1.state == node2.state)

def isEmpty(arr: list):
    return (len(arr) == 0)

# Definisi compute: fungsi yang mengembalikan TRUE jika input string diterima language PDA
# dan FALSE jika tidak. Jangan lupa pemanggilan fungsi harus menggunakan epsilon closure 
# dari node pertama (pada argument current_nodes).
def compute(PDA: PushDownAutomaton, current_nodes: set[node], arr_length: int, debugmode: bool) -> (node,int,bool):

    # print("\n\n\n")
    # print("iteration =",  iterations)
    # Jika inputstring sudah habis, cek jika set of states mengandung setidaknya satu final state
    for i in current_nodes:

        if (isEmpty(i.inputstr)):

            # print("Ini kosong kok!\n")
            if PDA.acceptkey == 'E' and i.stack.isEmpty(): 
                return "",0xFFFFFFFF,True # returns -1 as error index if accepted, meaning there are no errors
            
            elif PDA.acceptkey == 'F':
                if i.state in PDA.F:
                    return "",0xFFFFFFFF,True   

    setOfEndNodes = set()
    for i in current_nodes:
        if not isEmpty(i.inputstr):
            setOfEndNodes |= PDA.transition(i) # Semua achievable state dari set current state yg ada

    # Removes non-unique elements from the set
    setOfEndNodes = list(setOfEndNodes)
    unique_elements = list()
    for i in range(len(setOfEndNodes)):
        unique = True
        for j in range(len(unique_elements)):
            condition1 = (setOfEndNodes[i].stack.elements == unique_elements[j].stack.elements)
            condition2 = (setOfEndNodes[i].inputstr == unique_elements[j].inputstr)
            condition3 = (setOfEndNodes[i].state == unique_elements[j].state)
            if (condition1 and condition2 and condition3):
                unique = False
                break
            
        if unique:
            unique_elements.append(setOfEndNodes[i])
        
    setOfEndNodes = set(unique_elements)
    
    if debugmode:
        print(f"\n------{arr_length}-------\n")
        for i in setOfEndNodes:
            print(i)

    if (isEmpty(setOfEndNodes)):
        return current_nodes.pop(),arr_length, False
    
    else:
        arr_length = len(current_nodes.pop().inputstr)
        return compute(PDA, setOfEndNodes, arr_length, debugmode)