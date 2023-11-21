def terminalsToPDA(pda,terminals):
    sigma = []
    state = pda[0][0]
    print(state)
    for element in terminals:
        temp = []
        temp.append(state)
        temp.append(element)
        temp.append(element)
        temp.append(state)
        temp.append("epsilon")
        sigma.append(temp)
    # print(f"pdaterminal: {sigma}")
    return sigma


def cfgToPDA(path):
    nonTerminals = []
    terminals = []
    pda = []
    state = "Q"
    with open(path,'r') as f:
        line = f.readline()
        sigma = []
        while line:
            count = 1
            currentTerminal = ""
            for word in line.split():
                if (word != "->" and word != "|"):
                    if count == 1:
                        currentNonTerminal = word
                        nonTerminals.append(word)
                        sigma.append(state)
                        sigma.append("epsilon")
                        sigma.append(currentNonTerminal)
                    else:
                        for char in word:
                            if (not(char in terminals)):
                                terminals.append(char)
                        sigma.append(state)
                        sigma.append(word)
                    count += 1
            # print(sigma)
            pda.append(sigma)
            sigma = []
            line = f.readline()
    # print(f"terminal: {terminals}")
    return pda, terminals

def processedListPDA(pda,terminals):
    temp = []
    for sigma in pda:
        state = sigma[0]
        headSigma = []
        headSigma = [sigma[0],sigma[1],sigma[2]]
        tailSigma = []
        for elements in sigma[3:]:
            if (elements == state and len(headSigma) != 3):
                temp.append(headSigma)
                headSigma = [sigma[0],sigma[1],sigma[2],elements]
            elif (elements == sigma[-1]):
                headSigma.append(elements)
                temp.append(headSigma)
            else:
                headSigma.append(elements)
    pdaTerminals = terminalsToPDA(temp,terminals)
    for terminalSigma in pdaTerminals:
        temp.append(terminalSigma)
    # print(f"temp: {temp}")
    return temp


def writeToFile(processedPDA):
    with open('output.txt', 'w') as f:
        for row in processedPDA:
            f.write(' '.join([str(a) for a in row]) + '\n')

pda, terminals = cfgToPDA("grammar.txt")
a=processedListPDA(pda,terminals)
writeToFile(a)

# def converterCFG(cfg_path):
#     pda,terminals = cfgToPDA(cfg_path)
#     processedPDA = processedListPDA(pda,terminals)
#     writeToFile(processedPDA)
