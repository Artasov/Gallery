from transliterate import translit

def utf8_to_ascii(string):
    translit_string = translit(string, 'ru', reversed=True)
    ascii_string = translit_string.encode('ascii', 'ignore').decode('ascii')
    return ascii_string

def is_ascii(string):
    return all(ord(char) < 128 for char in string)