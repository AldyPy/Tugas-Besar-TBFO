def readChar(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        while True:
            char = file.read(1)
            if not char:
                break
            yield char


html_file_path = 'test.html'
html_reader = readChar(html_file_path)

# Contoh iterasi, menampilkan file html
while True:
    next_character = next(html_reader, None)
    if next_character is None:
        break 
    print(next_character, end="")
