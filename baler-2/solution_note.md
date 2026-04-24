# Solution Note: Decrypting joybangla.bin

## Challenge Overview
The file `joybangla.bin` contained a message encrypted using a **repeating key XOR** cipher. The goal was to recover the key, decrypt the message, and extract the flag.

## Methodology

### 1. Determining Key Length
To find the length of the key, we calculated the normalized **Hamming distance** between adjacent blocks of ciphertext for various key lengths. The smallest distances typically correspond to the correct key length or its multiples.

- **Observed optimal length:** 8 bytes (and its multiples 16, 24, etc.).

### 2. Recovering the Key
Once the key length ($L=8$) was determined, we transposed the ciphertext into $L$ blocks. For each position $i$ (from 0 to 7) in the key, we analyzed the bytes at indices $i, i+L, i+2L...$
By assuming that the original text contained standard ASCII printable characters (and specifically that space ` ` is the most common character), we could determine the byte that, when XORed with the column, resulted in the most "English-like" distribution.

### 3. The Key
The recovered key is:
**`J0Y_B4N9`**

### 4. Decryption & Flag Extraction
We applied the key `J0Y_B4N9` to the entire file using bitwise XOR.

```python
key = b"J0Y_B4N9"
# decrypted_byte[i] = ciphertext_byte[i] ^ key[i % len(key)]
```

The resulting plaintext contained the flag split into four hidden segments:
1. `[BICS77{J0Y_]`
2. `[B4N9L4_C#4P]`
3. `[4T1_L349U3_K]`
4. `[3_L47H1_D1N}]`

### Final Flag
**`BICS77{J0Y_B4N9L4_C#4P4T1_L349U3_K3_L47H1_D1N}`**
