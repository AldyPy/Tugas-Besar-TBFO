import os
import sys

parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_directory)

from Input_Handling.htmltokenizer import *
from Input_Handling.PDAconfig import *
from PDA_Model.PushDownAutomaton import *
# Contoh driver program

""" CONTOH PENGGUNAAN PDA """
# kita buat PDA sederhana yang menerima:
# {w w^R | w^R adalah reverse dari w, w terdiri dari huruf kecil alfabet}}
# (BUKAN PALINDROM)

# Contoh : momoomom, abcddcba,       (accepted)
#        : misaka, level, MomoomoM   (rejected)

# States
q0 = state("q0")
Q = {q0}

# Epsilon, Gamma, dan  delta
Epsilon = set()
Gamma = set()
delta = transitionFunction("delta", set())

for i in lowercaseletters:
    Epsilon |= {i}
    Gamma |= {i}
    delta.addTransition(singleTransition(q0, i, epsilon, q0, i))
    delta.addTransition(singleTransition(q0, i, i, q0, epsilon))

# Definisi PDA: State awal sekaligus satu-satunya state = q0, start_symbol stack adalah Z,
# dan PDA menerima string ketika empty stack
wwR = PushDownAutomaton(
    Q=Q,
    Epsilon=Epsilon,
    Gamma=Gamma,
    delta=delta,
    start_state=q0,
    start_symbol='Z',
    F={},
    AcceptKey='E'
)


print()

# MAIN

a = input("Input a string of form w w^R: ")
# start_node = node(wwR.start_state, a, stack(wwR.start_symbol))
# wwR = getPDA("config.txt")

# for i in wwR.delta.transitions:
#     print(i)

# inputstr = getText("test2.html")
# print(inputstr)



# inputstr = "abba"
inputstr = a
# print(inputstr,end="")

start_node = node(wwR.start_state, inputstr, stack(wwR.start_symbol))
                  
correct = compute(wwR, wwR.epsilonclosure(start_node))
if correct:
    print("Yes, that's correct.")
else:
    print("Whoa, that doesn't seem right.")