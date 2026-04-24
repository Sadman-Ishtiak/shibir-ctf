import sys

def hamming_distance(b1, b2):
    dist = 0
    for byte1, byte2 in zip(b1, b2):
        dist += bin(byte1 ^ byte2).count('1')
    return dist

def score_text(text):
    # Simple scoring: count printable characters and spaces
    score = 0
    for b in text:
        if 32 <= b <= 126 or b in [9, 10, 13]:
            score += 1
        if chr(b).isalpha() or chr(b) == ' ':
            score += 2 # Give more weight to letters and spaces
    return score

def solve():
    try:
        with open('joybangla.bin', 'rb') as f:
            ciphertext = f.read()
    except FileNotFoundError:
        print("File not found.")
        return

    # 1. Find Key Length
    best_avg_dists = []
    for k in range(2, 41):
        dists = []
        chunks = [ciphertext[i:i+k] for i in range(0, len(ciphertext), k)]
        if len(chunks) < 4: continue
        
        # Compare first 4 chunks
        for i in range(len(chunks)-1):
            for j in range(i+1, min(i+4, len(chunks))):
                 if len(chunks[i]) == k and len(chunks[j]) == k:
                    d = hamming_distance(chunks[i], chunks[j])
                    dists.append(d / k)
        
        if dists:
            avg_dist = sum(dists) / len(dists)
            best_avg_dists.append((avg_dist, k))

    best_avg_dists.sort()
    print("Top 5 likely key lengths:")
    for dist, k in best_avg_dists[:5]:
        print(f"Length: {k}, Dist: {dist:.4f}")

    # 2. Try to decrypt with top key lengths
    for _, key_len in best_avg_dists[:3]:
        print(f"\n--- Trying Key Length {key_len} ---")
        full_key = bytearray(key_len)
        
        for i in range(key_len):
            block = ciphertext[i::key_len]
            best_byte = 0
            max_score = -1
            
            # Try all possible bytes for this position
            for candidate in range(256):
                decrypted_block = bytes([b ^ candidate for b in block])
                # Score based on English letter frequency roughly (or just spaces/printable)
                # Most common char in English is space. Let's try to assume the most frequent char in decrypted block is space.
                # Or just use the generic scorer.
                
                # Frequency analysis approach:
                # Assume space (32) is the most frequent character
                # But let's just use the score_text function on the block for robustness
                
                current_score = 0
                for b in decrypted_block:
                     if 32 <= b <= 126 or b in [10, 13]: # Printable
                        current_score += 1
                     if 97 <= b <= 122: # Lowercase
                        current_score += 2
                     if b == 32: # Space
                        current_score += 5
                
                if current_score > max_score:
                    max_score = current_score
                    best_byte = candidate
            
            full_key[i] = best_byte
        
        print(f"Guessed Key (Hex): {full_key.hex()}")
        try:
            print(f"Guessed Key (Str): {full_key.decode('ascii', errors='replace')}")
        except:
            pass
            
        decrypted = bytes([ciphertext[i] ^ full_key[i % key_len] for i in range(len(ciphertext))])
        print("Decrypted start:", decrypted[:100])
        if b"flag" in decrypted.lower() or b"FLAG" in decrypted:
             print("POTENTIAL FLAG FOUND!")

if __name__ == "__main__":
    solve()
