stringData = "<HTML ref <tete>>  ashjfbshjaf   </HTML>"

currentWord = ''
i = 0

data = []
isOpen = False
for char in stringData:
    if (char == "<") and (isOpen == False):
        currentWord = ""
        isOpen = True
        data.append(currentWord)
    elif char == ">":
        isOpen = False
        currentWord += ">"
        data.append(currentWord)
        
        # print(currentWord)
    if isOpen:
        currentWord += char
print(data)