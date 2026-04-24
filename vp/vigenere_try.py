
def vigenere_decrypt(ciphertext, key):
    result = ""
    key_index = 0
    key = [k for k in key if k.isalpha()] # simplistic handling
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
keys = ["VP", "DUCSU", "POETRY", "POEM", "CGPA", "BENGALI", "AOEN", "AOEN77", "MIFTAH", "STUDENT", "UNION", "CENTRAL", "BANGLADESH", "SHADIK", "KAYEM", "NURUL", "HAQUE", "NUR", "SADDAM", "HUSSAIN", "GOLAM", "RABBANI", "AKHTER", "HOSSEN"]

print("Trying Vigenere keys:")
for key in keys:
    decrypted = vigenere_decrypt(ciphertext, key)
    print(f"Key {key}: {decrypted}")

# Try AutoKey or dictionary attack?
# Maybe the key is 'AOEN'?
