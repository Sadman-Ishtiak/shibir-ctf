
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

ciphertext = "Swrlat_Ahaqucp_F0y0w_PAWPJ_OK_M4r1q_j41"
common_words = ["POETRY", "POEM", "VERSE", "RHYME", "SONNET", "HAIKU", "STANZA", "LYRIC", "BALLAD", "EPIC", "ODE", 
                "NURUL", "AKHTER", "RABBANI", "SADDAM", "SHADIK", "MANNA", "SULTAN", "TOFAIL", "RAB", "JALAL",
                "DUCSU", "BICS", "STUDENT", "UNION", "VICE", "PRESIDENT", "BANGLADESH", "DHAKA", "UNIVERSITY",
                "BUY", "BUYF", "BUYFLOWERS", "BUYFOOD", "BUYFISH", "BUYING", "BOUGHT",
                "MIFTAH", "AUTHOR", "FLAG", "CTF", "KEY", "PASSWORD", "SECRET", "VP",
                "EXPLAIN", "EVERYTHING", "THROUGH", "SPEAKS", "UNUSUAL"]

print("Trying Dictionary Keys:")
for key in common_words:
    decrypted = vigenere_decrypt(ciphertext, key)
    print(f"Key {key:15}: {decrypted}")

print("\nTrying keys starting with BUYF:")
# Try to append 1-3 letters to BUYF
import itertools
chars = string.ascii_uppercase
for l1 in chars:
    key = "BUYF" + l1
    decrypted = vigenere_decrypt(ciphertext, key)
    # Check if first word looks readable (e.g., contains vowels)
    first_word = decrypted.split('_')[0]
    if any(v in first_word.lower() for v in 'aeiou'):
        # print(f"Key {key}: {decrypted}")
        pass

# Try brute forcing assuming specific plaintext words
# e.g. "Swrlat" -> "She..."
