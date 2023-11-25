database = {
    "<html": 'HTML',
    "<head" : 'HEAD',
    "<body" : 'BODY',
    "<script" : 'SCRIPT',
    "<link" : 'LINK',
    "</body" : 'ENDBODY',
    "</head" : 'ENDHEAD',
    "</html" : 'ENDHTML'
}

def handleNonSpacedTags(database,tempTokens,words,line):
    word = words.split("><")
    print(word)
    word = [word[0]] + ["<" + c for c in word[1:]]
    for usedWord in word:
        if ">" in usedWord:
            usedWord = usedWord[:-1]
        print("\nWord keolah")
        print(usedWord)
        if usedWord in database:
            tuples = []
            tuples.append(database[usedWord])
            tuples.append(line)
            tempTokens.append(tuples)

def handleSpacedTags(database,waitingToBeClosed,words,line):
    if words[0] == "<":
        if words[-1] == ">":
            words = words[:-1]
        print("A:")
        print(words)
        if words in database:
            tuples = []
            tuples.append(database[words])
            tuples.append(line)
            waitingToBeClosedTokens.append(tuples)

tokens = []
line = 1
closedTagCounter = 0
with open('test2.html') as file:
    waitingToBeClosedTokens = []
    for lineWithNewLine in file:
        lineWthoutNewLine = lineWithNewLine.rstrip()
        for words in lineWthoutNewLine.split():
            if "><" in words:
                handleNonSpacedTags(database,waitingToBeClosedTokens,words,line)
            else:
                handleSpacedTags(database,waitingToBeClosedTokens,words,line)
            closedTagCounter = words.count(">")
            for i in range(closedTagCounter):
                if (len(waitingToBeClosedTokens) != 0):
                    tokens.append(waitingToBeClosedTokens.pop(0))
                    if not("END" in tokens[-1][0]):
                        tokens.append(["CLOSETAG",line])
                    closedTagCounter -= 1
        line += 1

print("\n=============================")
print(waitingToBeClosedTokens)
print("=============================")
print(tokens)
print("=============================")

# l = []
# print(l.pop(0))
# print(l)