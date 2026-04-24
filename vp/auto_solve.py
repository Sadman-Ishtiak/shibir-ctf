
import string
import math

# English letter frequencies (approximate)
english_freqs = {
    'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702,
    'F': 0.02228, 'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00153,
    'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749, 'O': 0.07507,
    'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056,
    'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974,
    'Z': 0.00074
}

def get_chi_squared(text):
    text = [c.upper() for c in text if c.isalpha()]
    if not text:
        return float('inf')
    
    counts = {char: 0 for char in string.ascii_uppercase}
    for char in text:
        counts[char] += 1
    
    chi_squared = 0
    for char in string.ascii_uppercase:
        observed = counts[char]
        expected = len(text) * english_freqs[char]
        chi_squared += ((observed - expected) ** 2) / expected
        
    return chi_squared

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

# Try all keys of length 1 to 10
print("Brute-forcing best keys by Chi-Squared score...")

best_keys = []

# We already suspect the key starts with 'BUYF'.
# Let's try to complete it.
base_key = "BUYF"
print(f"Assuming key starts with {base_key}...")

# Try appending 0 to 6 chars
import itertools
chars = string.ascii_uppercase

for length in range(0, 5): # Try appending up to 4 chars
    for suffix in itertools.product(chars, repeat=length):
        key = base_key + "".join(suffix)
        decrypted = vigenere_decrypt(ciphertext, key)
        score = get_chi_squared(decrypted)
        best_keys.append((score, key, decrypted))

best_keys.sort()
print("\nTop 10 candidates with 'BUYF' prefix:")
for score, key, decrypted in best_keys[:10]:
    print(f"Key: {key}, Score: {score:.2f}, Text: {decrypted}")
