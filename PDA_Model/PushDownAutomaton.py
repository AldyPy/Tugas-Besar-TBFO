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
        return f"{self.elements[-1 + len(self.elements)]}"

    def push(self, value):
        self.elements.append(value)
    
    def pop(self):
        val = self.top()
        self.elements = self.elements[0:-1+len(self.elements):]
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
    def __init__(self, state: state, inputstr: str, stack: stack):
        self.state = state
        self.inputstr = inputstr
        self.stack = stack

    def __str__(self):
        return f"({self.state},{self.inputstr},{''.join(str(item) for item in self.stack.elements)})"
    

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
        return f"({self.startstate},{self.startstack},{self.symbol} -> {self.endstate},{self.endstack})"

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
            print("WHAAAAAAA")
            return False
        else:
            return True
    
    # Definisi Epsilon Closure dari NODE -> Node yang bisa dicapai tanpa baca input (a.k.a. melalui epsilon)
    # IMPORTANT note: Elements from the stack may or may not be modified
    def epsilonclosure(PDA, P: node) -> set[node]:
        result = {P}

        for i in PDA.delta.transitions: # Find all satisfiable epsilon transitions
            if i.startstate == P.state and i.symbol == epsilon and i.startstack == P.stack.top():

                # Create resulting node
                a = node(i.endstate, P.inputstr, P.stack)

                # Push and pop to the stack
                if (i.startstack != epsilon):
                    _ = a.stack.pop()
                
                if (i.endstack != epsilon):
                    for j in i.endstack:
                        a.stack.push(j)

                result |= {a}

        
        return result
    
    # Definisi transition: mengembalikan set of possible current nodes 
    # setelah simbol digunakan untuk "maju"
    def transition(PDA, P: node) -> set[node]:
        resultingNodes = set()
        symbol = P.inputstr[0]
        
        # print(symbol)

        for i in (PDA.delta.transitions):

            if (P.state == i.startstate) and (symbol == i.symbol) and (
                    (i.startstack == P.stack.top()) or (i.startstack == epsilon)
                ):
                # print("UUUUUUWUUUUUU")
                # Create resulting node
                a = node(i.endstate, P.inputstr[1:], copystack(P.stack))

                # Push and pop to the stack
                if (i.startstack != epsilon):
                    _ = a.stack.pop()
                
                if (i.endstack != epsilon):
                    for j in i.endstack:
                        a.stack.push(j)

                print(i.startstack, i.endstack)   # For debugging; print resulting node set
                print(a)                          
                resultingNodes.add(a)

        actualResultingNodes = set()                # The correct result after unioning the previous
        for i in resultingNodes:                    # result all with the resulting state snodes' e-Closures
            actualResultingNodes |= PDA.epsilonclosure(i)
        
        return actualResultingNodes     # Jika tidak ditemukan transisi yang bisa dijalankan,
                                        #  maka actualResultingNodes akan kosong


# Definisi compute: fungsi yang mengembalikan TRUE jika input string diterima language PDA
# dan FALSE jika tidak. Jangan lupa pemanggilan fungsi harus menggunakan epsilon closure 
# dari node pertama (pada argument current_nodes).
def compute(PDA: PushDownAutomaton, current_nodes: set[node]) -> bool:

    # Jika inputstring sudah habis, cek jika set of states mengandung setidaknya satu final state
    stop = True
    for i in current_nodes:
        if i.inputstr != epsilon: 
            # print("P epsilon")
            stop = False
    
    if (stop):
        if PDA.acceptkey == 'F':
            for i in current_nodes:
                if i.state in PDA.F:
                    return True
        
        elif PDA.acceptkey == 'E':
            for i in current_nodes:
                if i.stack.isEmpty():
                    print(current_nodes)
                    return True
                
        return False
    
    else:
    # Otherwise, lanjutkan pemroresan PDA
        setOfEndNodes = set()
        for i in current_nodes:
            setOfEndNodes |= PDA.transition(i) # Semua achievable state dari set current state yg ada

        return compute(PDA, setOfEndNodes)