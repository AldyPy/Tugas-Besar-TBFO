import os
import sys

parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_directory)

FORWARD_SLASH = "/"
LEFT_BRACKET = "<"
RIGHT_BRACKET = ">"
BLANK = ""
SPACE = " "
QUOTEMARK = "\""
BACKSLASH_N = "\n"
EQUALS = "="
EXCLAMATION_MARK = "!"

##########################################
# RETURNS A DICTIONARY: KEYS ARE REGULAR TAGS AND VALUES ARE THE RESPECTIVE TOKENS
# TagTokenDictionary = {"<html" : "HTML", "</html>" : "ENDHTML" ...}

def InitializeTagTokenDictionary() -> dict:
    Tokens = "COMMENT ENDCOMMENT EMPTYCOMMENT HTML ENDHTML HEAD ENDHEAD BODY ENDBODY TITLE ENDTITLE SCRIPT ENDSCRIPT H1 H2 H3 H4 H5 H6 ENDH1 ENDH2 ENDH3 ENDH4 ENDH5 ENDH6 P ENDP EM ENDEM B ENDB ABBR ENDABBR STRONG ENDSTRONG SMALL ENDSMALL DIV ENDDIV A ENDA BUTTON ENDBUTTON FORM ENDFORM TABLE ENDTABLE TD ENDTD TR ENDTR TH ENDTH LINK BR HR IMG INPUT CLOSETAG".split()

    TagTokenKeys = list()
    for token in Tokens:
        if token == "CLOSETAG":
            TagTokenKeys.append(">")

        # Endtag token key (e.g. </html>)
        elif token == "COMMENT":
            TagTokenKeys.append(f"<!--")
        elif token == "ENDCOMMENT":
            TagTokenKeys.append(f"-->")
        elif token == "EMPTYCOMMENT":
            TagTokenKeys.append(f"<!---->")
            
        elif token[0:3] == "END":
            TagTokenKeys.append(f"</{token[3:]}>".lower())

        
        # Normal token
        else:
            TagTokenKeys.append(f"<{token.lower()}")

    TagTokenDictionary = dict()
    for i in range(len(Tokens)):
        TagTokenDictionary[TagTokenKeys[i]] = Tokens[i]

    return TagTokenDictionary

def InitializeAttrTokenDictionary() -> dict:
# RETURNS A DICTIONARY: KEYS ARE FORMATTED ATTRIBUTES AND VALUES ARE THE RESPECTIVE TOKENS
# AttrTokenDictionary.keys() = [str(id=""), str(style=""), str(class=""), ...]
    
    AttrTokens = "ID_ATTR CLASS_ATTR STYLE_ATTR REL_ATTR HREF_ATTR SRC_ATTR ALT_ATTR TYPE_BUTTON_ATTR TYPE_INPUT_ATTR ACTION_ATTR METHOD_ATTR".split()

    AttrTokenKeys = list()
    for token in AttrTokens:
        AttrTokenKeys.append(f"{token[0:len(token) - 5].lower()}=\"\"")

    AttrTokenDictionary = dict()
    for i in range(len(AttrTokens)):
        AttrTokenDictionary[AttrTokenKeys[i]] = AttrTokens[i]

    return AttrTokenDictionary

def InitializeAttrLists() -> list[str]:
# RETURNS A LIST OF EACH ATTR LOWERCASED
# AttrList = ["id", "style", "class" ...]
    
    AttrTokens = "ID_ATTR CLASS_ATTR STYLE_ATTR REL_ATTR HREF_ATTR SRC_ATTR ALT_ATTR TYPE_BUTTON_ATTR TYPE_INPUT_ATTR ACTION_ATTR METHOD_ATTR".split()

    # id, class, style, etc.
    AttrList = list()
    for token in AttrTokens:
        AttrList.append(f"{token[0:len(token) - 5].lower()}")

    return AttrList

def InitializeAttrEqualsLists() -> list[str]:
# RETURNS A LIST OF EACH ATTR LOWERCASED PLUS EQUALS SIGN
# AttrList = ["id=", "style=", "class=" ...]
    
    AttrTokens = "ID_ATTR CLASS_ATTR STYLE_ATTR REL_ATTR HREF_ATTR SRC_ATTR ALT_ATTR TYPE_BUTTON_ATTR TYPE_INPUT_ATTR ACTION_ATTR METHOD_ATTR".split()

    # id, class, style, etc.
    AttrList = list()
    for token in AttrTokens:
        AttrList.append(f"{token[0:len(token) - 5].lower()}=")

    return AttrList

def ValidateEndTags(token_array: list[str], arr1: list[str], arr2: list[str]):
# IN THE ARRAY IF THERE EXISTS A CLOSETAG THAT IS ASSCOSIATED WITH AN ENDTAG OR COMMENT: 
# COMBINES IT WITH THE PREV ELEMENT. WILL ALSO REMOVE THE ELEMENTS FROM THE TWO OTHER 
# INPUT ARRAY

    RemovalIndices = list()
    for i in range(1, len(token_array)):
        try:
            if (token_array[i] == (RIGHT_BRACKET)) and (((token_array[i-1][1]) in [FORWARD_SLASH, EXCLAMATION_MARK]) or token_array[i-1][-1] == "-"):
                RemovalIndices.append(i)
                token_array[i - 1] += RIGHT_BRACKET
        except:
            pass

    # Remove elements
    token_array = [N for i,N in enumerate(token_array) if i not in RemovalIndices]
    arr1 = [N for i,N in enumerate(arr1) if i not in RemovalIndices]
    arr2 = [N for i,N in enumerate(arr2) if i not in RemovalIndices]

    # Concats and recognizes Comments for cases ["<!--RANDOM", "-->"], ["<!--RANDOM-->"] and ["<!-- RANDOM-->"]
    RemovalIndices = list()
    for i in range(0, len(token_array)):
        length = len(token_array[i])
        if (token_array[i][0:4] == "<!--") and (token_array[i][length-3:length] == "-->"):
            token_array[i] = token_array[i][0:4] + token_array[i][length-3:length]

        elif (token_array[i][0:4] == "<!--") and (token_array[i] != "<!---->"):
            token_array[i] = token_array[i][0:4]

        elif (len(token_array[i]) >= 3) and (token_array[i] != "<!---->"):
            if token_array[i][ len(token_array[i])-3:len(token_array[i]) ] == "-->":
                token_array[i] = token_array[i][len(token_array[i])-3:len(token_array[i])]

    # Remove elements
    token_array = [N for i,N in enumerate(token_array) if i not in RemovalIndices]
    arr1 = [N for i,N in enumerate(arr1) if i not in RemovalIndices]
    arr2 = [N for i,N in enumerate(arr2) if i not in RemovalIndices]

    return token_array,arr1,arr2

def ValidateAttributes(processed_array: list[str], arr1: list[str], arr2: list[str]):
# IN THE ARRAY IF THERE EXISTS A DOUBLE QUOTATION MARK AS A STRING ELEMENT: COMBINES 
# WITH THE PREV ELEMENT. WILL ALSO REMOVE THE ELEMENTS FROM THE TWO OTHER INPUT ARRAYS 
# (BUAT ROW LINE ERROR MSG)

    RemovalIndices = list()
    for i in range(1, len(processed_array)):
        if (processed_array[i] == (QUOTEMARK + QUOTEMARK)) and (processed_array[i-1][-1] == EQUALS):

            RemovalIndices.append(i)
            processed_array[i - 1] += (QUOTEMARK + QUOTEMARK)

    # Remove elements
    processed_array = [N for i,N in enumerate(processed_array) if i not in RemovalIndices]
    arr1 = [N for i,N in enumerate(arr1) if i not in RemovalIndices]
    arr2 = [N for i,N in enumerate(arr2) if i not in RemovalIndices]

    return processed_array,arr1,arr2

def RemoveComments(processed_array: list[str], arr1: list[str], arr2: list[str]):
# AFTER TOKENIZATION: REMOVES COMMENT, ENDCOMMENT TOKENS, AND EVERYTHING THAT 
# EXISTS BETWEEN THEM. ALSO REMOVES ENDCOMMENT TOKEN
# -> ini supaya PDA tidak harus nambah 30+ transisi hanya buat nerima komentar di 
# state mana aja soalnya komentarnya banyak...

    RemovalIndices = list()
    remove = False
    remove
    for i in range(len(processed_array)):
        if processed_array[i] == "COMMENT":
            remove = True
        elif processed_array[i] == "ENDCOMMENT":
            RemovalIndices.append(i)
            remove = False
        elif processed_array[i] == "EMPTYCOMMENT":
            RemovalIndices.append(i)

        if remove:
            RemovalIndices.append(i)
        
    processed_array = [N for i,N in enumerate(processed_array) if i not in RemovalIndices]
    arr1 = [N for i,N in enumerate(arr1) if i not in RemovalIndices]
    arr2 = [N for i,N in enumerate(arr2) if i not in RemovalIndices]

    return processed_array,arr1,arr2
        

##############################################################
def TokenizeThisHtmlFile(path: str) -> (list[set], list[int], list[int]):

    TagDictionary = InitializeTagTokenDictionary()
    AttributeDictionary = InitializeAttrTokenDictionary()
    AttributeList = InitializeAttrLists()

    Tokens = list()
    TokenRowIndices = list()
    TokenColIndices = list()

    AttributeValue = BLANK
    prevWord = BLANK
    ignore = 0x0
    idxRow = 1
    idxCol = 1
    
    currentWord = BLANK
    file = open(path, 'r')

    while(0x1):

        # Mesin karakter
        char = file.read(1)
        if not char: break

        if char == QUOTEMARK:

            ignore = ~(ignore)
            if not ignore:
                currentWord += QUOTEMARK
            else:
                AttributeValue += char

            idxCol += 1

        if ignore:
            pass

        elif char == EQUALS:


            # Kasus id =, style =, class =, etc.
            # print("PREVWORD = ", prevWord)
            if prevWord in AttributeList:
                
                Tokens[len(Tokens) - 1] += EQUALS
                TokenColIndices[len(Tokens) - 1] += 1

            # Kasus id=, style, class=, etc.
            elif currentWord in AttributeList:
                currentWord += EQUALS
                Tokens.append(currentWord)
                TokenRowIndices.append(idxRow)
                TokenColIndices.append(idxCol)
            
            else:
                Tokens.append(currentWord + char)
                TokenRowIndices.append(idxRow)
                TokenColIndices.append(idxCol)
                prevWord = currentWord
            
            currentWord = BLANK

        elif char == LEFT_BRACKET:
            
            # debugPrint(currentWord)
            if currentWord not in [BLANK]:
                Tokens.append(currentWord)
                TokenRowIndices.append(idxRow)
                TokenColIndices.append(idxCol)
                prevWord = currentWord

            currentWord = LEFT_BRACKET
        
            idxCol += 1

        elif char == RIGHT_BRACKET:

            # debugPrint(currentWord)
            if currentWord not in [BLANK]: # lmao
                Tokens.append(currentWord)
                TokenRowIndices.append(idxRow)
                TokenColIndices.append(idxCol)
                prevWord = currentWord
            Tokens.append(RIGHT_BRACKET)
            TokenRowIndices.append(idxRow)
            TokenColIndices.append(idxCol+1)
            currentWord = BLANK

            idxCol += 1

        elif char == SPACE:
            if currentWord not in [BLANK]:
                prevWord = currentWord
                Tokens.append(currentWord)
                TokenRowIndices.append(idxRow)
                TokenColIndices.append(idxCol)
                currentWord = BLANK

            idxCol += 1

        elif char == BACKSLASH_N:
            if currentWord not in [BLANK]:
                prevWord = currentWord
                Tokens.append(currentWord)
                TokenRowIndices.append(idxRow)
                TokenColIndices.append(idxCol)
                currentWord = BLANK
            idxRow += 1
            idxCol = 1

        else:
            currentWord += char
            idxCol += 1

    Tokens,TokenRowIndices,TokenColIndices = ValidateAttributes(Tokens,TokenRowIndices,TokenColIndices)
    Tokens,TokenRowIndices,TokenColIndices = ValidateEndTags(Tokens,TokenRowIndices,TokenColIndices)

    ActualTokens = list()
    for i in Tokens:
        if i in TagDictionary.keys():
            ActualTokens.append(TagDictionary[i])
        elif i in AttributeDictionary.keys():
            ActualTokens.append(AttributeDictionary[i])
        else:
            ActualTokens.append("RANDOM")
    
    # uncomment this to return the nontokenized strings instead.
    # return Tokens,TokenRowIndices,TokenColIndices,

    q,w,e = RemoveComments(ActualTokens,TokenRowIndices,TokenColIndices)
    return q,w,e

def debugPrint(i:str):
    if i == BLANK:
        print("BLANKS")
    elif i == BACKSLASH_N:
        print("ENTERS")
    elif i == SPACE:
        print("SPACES")
    else:
        pass

#driver
if __name__ == "__main__":

    # Dictionaries
    print("~Token Dictionaries~")
    print("-"*20)
    print(InitializeTagTokenDictionary())
    print("-"*20)
    print(InitializeAttrTokenDictionary())
    print("-"*20)
    print(InitializeAttrLists())
    print("-"*20)

    # Tokenss
    print("\n"*5+"~Tokens~")
    t,trows,tcols = TokenizeThisHtmlFile("testcase/tabletest.html")

    print("If these lengths are the same, we're good to go:\n", len(t), len(trows), len(tcols))
    for i in range(len(t)):
        print(f"{i+1}. {t[i]} [Ln {trows[i]}, Col {tcols[i]}]\n")
