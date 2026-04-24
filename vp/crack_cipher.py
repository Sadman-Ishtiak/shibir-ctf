
def caesar_decrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - start - shift) % 26 + start)
        else:
            result += char
    return result

ciphertext = "Swrlat_Ahaqucp_F0y0w_PAWPJ_OK_M4r1q_j41"
words = ciphertext.split('_')

print("Trying Caesar shifts:")
for shift in range(26):
    decrypted = caesar_decrypt(ciphertext, shift)
    print(f"Shift {shift}: {decrypted}")

print("\nAssuming Vigenere/Polyalphabetic. Trying to match specific words.")
# Try to map 'OK' to common 2-letter words
targets = ["OF", "IS", "IN", "TO", "IT", "ON", "AT", "BY", "MY", "UP", "DO", "GO", "NO", "SO", "WE", "BE", "HE", "ME"]
for target in targets:
    # Key assuming OK -> target
    k1 = (ord('O') - ord(target[0])) % 26
    k2 = (ord('K') - ord(target[1])) % 26
    print(f"OK -> {target}: k1={k1}, k2={k2}")

