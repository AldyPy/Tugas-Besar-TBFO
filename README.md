# Tugas Besar Teori Bahasa Formal Otomata IF2124

## Project Description
This is a project that aims to create a Python program that **can parse HTML documents and extract their structure and content**. The project uses a *pushdown automata*, which is a type of finite state machine that can handle nested structures, to model the syntax and semantics of HTML. The project will implement the following features:

- ***A lexer*** that can tokenize the HTML source code into meaningful units, such as tags, attributes, and text.
- ***A parser*** that can recognize the grammar rules of HTML and build a parse tree that represents the hierarchical structure of the document.
- ***A validator*** that can check the validity and well-formedness of the HTML document according to the HTML specification.
- ***A renderer*** that can display the HTML document in a command line interface.

The project will include a documentation of the design and implementation details. The project will demonstrate the power and versatility of Python as a programming language, and the usefulness and elegance of pushdown automata as a computational model. The project will be a valuable learning experience for anyone interested in web development, programming languages, and automata theory.

## Project Structure
Here is this repository's project structure!
```
│   config.txt
│   grammar.txt
│   LICENSE
│   main.py
│   README.md
│
├───Input_Handling
│       htmltokenizer.py
│       PDAconfig.py
│       __init__.py
│    
│
├───PDA_Model
│       driver.py
│       PushDownAutomaton.py
│       __init__.py
│    
│
└───testcase
        comments_test.html
        comments_test2.html
        comments_test3.html
        customtc.html
        tabletest.html
        tabletest2.html
        tc1.html
        tc10.html
        tc11.html
        tc2.html
        tc3.html
        tc4.html
        tc5.html
        tc6.html
        tc7.html
        tc8.html
        tc9.html
        testcase_rafly.html
 
```

## How to Run
```
python main.py config.txt "[html file]"
```

If you want to see behind the scene / process of the PDA in action, you can go ahead turn on the ***Debug*** mode, which is a function parameter in the ***compute*** function located in ```main.py```.

## Contributors
|Anggota|NIM|
|-------|---|
|Shafiq Irvansyah|13522003|
|Raden Rafly Hanggaraksa Budiarto|13522014|
|Renaldy Arief Susanto|13522022|



