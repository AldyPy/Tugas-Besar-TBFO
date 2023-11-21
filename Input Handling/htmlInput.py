def readChar(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        while True:
            char = file.read(1)
            if not char:
                break
            yield char


def getText(namafile: str):
    html_reader = readChar(namafile)
    text = ""
    while True:
        next_character = next(html_reader, None)
        if next_character is None:
            break 
        elif (next_character == " " or next_character== "\n"):
            pass
        else:
            text += next_character
            
    return text
        

    