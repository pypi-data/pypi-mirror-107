def code(word: str, key: int = 1):
    numbers = [(ord(i) + key) % 55295 for i in word]
    new_word = ''.join([chr(i) for i in numbers])
    return new_word


def decode(word: str, key: int = 1):
    numbers = [(ord(i) - key) % 55295 for i in word]
    new_word = ''.join([chr(i) for i in numbers])
    return new_word
