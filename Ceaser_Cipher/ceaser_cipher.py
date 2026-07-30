"""Simple Caesar cipher decrypter.

Usage: run and input the encrypted sentence and the shift used to encrypt.
The program will print the decrypted sentence.
"""

import sys


def decrypt_caesar(text: str, shift: int) -> str:
    """Decrypts text encrypted with a Caesar cipher using the given shift.

    Shift is the amount that was used to encrypt; decryption shifts letters
    backward by that amount (or forward by 26-shift).
    Non-alphabetic characters are left unchanged. Case is preserved.
    """
    result = []
    shift = shift % 26
    for ch in text:
        if 'a' <= ch <= 'z':
            base = ord('a')
            result.append(chr((ord(ch) - base - shift) % 26 + base))
        elif 'A' <= ch <= 'Z':
            base = ord('A')
            result.append(chr((ord(ch) - base - shift) % 26 + base))
        else:
            result.append(ch)
    return ''.join(result)


def main():
    try:
        encrypted = input("Encrypted sentence: ")
        raw_shift = input("Shift (integer): ")
        shift = int(raw_shift.strip())
    except (EOFError, KeyboardInterrupt):
        sys.exit(0)
    except Exception:
        print("Invalid shift. Please provide an integer.")
        sys.exit(1)

    decrypted = decrypt_caesar(encrypted, shift)
    print("Decrypted:", decrypted)


if __name__ == '__main__':
    main()
