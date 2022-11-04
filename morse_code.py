morse_characters = {
    '0': '-----',
    '1': '.----',
    '2': '..---',
    '3': '...--',
    '4': '....-',
    '5': '.....',
    '6': '-....',
    '7': '--...',
    '8': '---..',
    '9': '----.',
    'A': '.-',
    'B': '-...',
    'C': '-.-.',
    'D': '-..',
    'E': '.',
    'F': '..-.',
    'G': '--.',
    'H': '....',
    'I': '..',
    'J': '.---',
    'K': '-.-',
    'L': '.-..',
    'M': '--',
    'N': '-.',
    'O': '---',
    'P': '.--.',
    'Q': '--.-',
    'R': '.-.',
    'S': '...',
    'T': '-',
    'U': '..-',
    'V': '...-',
    'W': '.--',
    'X': '-..-',
    'Y': '-.--',
    'Z': '--..',
    '.': '.-.-.-',
    ',': '--..--',
    '?': '..--..',
    ':': '---...',
    '/': '-..-.',
    '-': '-....-',
    '=': '-...-',
    '\'': '.----.',
    '_': '..--.-',
    '!': '-.-.--',
    '(': '-.--.-',
    ')': '-.--.-',
    '&': '.-...',
    '"': '.-..-.',
    ';': '-.-.-.',
    '$': '...-..-',
    '\n': '-.-...',
    ' ': ' ',
}

ascii_characters = {morse_characters[char]: char for char in morse_characters.keys()}


def ascii_to_morse(ascii_in):
    # Converts ASCII to available morse code.
    morse_out = ''
    for char in ascii_in:
        if char.upper() in morse_characters.keys():
            morse_out += morse_characters[char.upper()]
            morse_out += ' '
    return morse_out


def morse_to_ascii(morse_in):
    # Converts morse code to available ASCII characters. I had to do this a little
    # differently from the ASCII to Morse Code function, because "split(' ')"
    # would simply ignore all the spaces.
    morse_in += ' '
    # Added because the symbol is examined at the beginning of a space.
    ascii_out = ''
    symbol = ''
    space = 0
    for char in morse_in:
        if char == '.' or char == '-':
            space = 0
            symbol += char
        elif char == ' ':
            # When the function encounters a space, it looks for the symbol in the ASCII dictionary.
            space += 1
            if symbol in ascii_characters.keys():
                # If the symbol is valid in morse code, it is added to the output and the
                # symbol is reset. Otherwise, the symbol is ignored.
                ascii_out += ascii_characters[symbol]
                symbol = ''
            else:
                symbol = ''
        if space == 2:
            ascii_out += ' '
            space = 0
    return ascii_out
