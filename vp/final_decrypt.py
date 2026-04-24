
import string

def vigenere_decrypt(ciphertext, key):
    result = ""
    key_index = 0
    key = [k for k in key if k.isalpha()]
    if not key: return ciphertext
    
    for char in ciphertext:
        if char.isalpha():
            shift = (ord(key[key_index % len(key)].upper()) - ord('A'))
            start = ord('A') if char.isupper() else ord('a')
            decrypted_char = chr((ord(char) - start - shift) % 26 + start)
            result += decrypted_char
            key_index += 1
        else:
            result += char
    return result

ciphertext_content = "Swrlat_Ahaqucp_F0y0w_PAWPJ_OK_M4r1q_j41"
key_for_content = "BUYF"
decrypted_content = vigenere_decrypt(ciphertext_content, key_for_content)
print(decrypted_content)
