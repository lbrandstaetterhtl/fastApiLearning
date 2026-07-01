def ceaser(text: str, shift: int) -> str:
    result = ""

    for char in text:
        if char.isalpha():
            basis = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - basis - shift) % 26 + basis)
        else:
            result += char

    return result

def vigenere(text: str, key: str) -> str:
    result = ""
    key = key.lower()
    key_index = 0

    for char in text:
        if char.isalpha():
            key_char = key[key_index % len(key)]

            shift = ord(key_char) -ord('a')

            basis = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - basis - shift) % 26 + basis)

            key_index += 1
        else:
            result += char

    return result