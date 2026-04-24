import sys

def xor_bruteforce(data, search_string):
    search_bytes = search_string.encode('utf-8')
    found_flags = []
    
    for key in range(256):
        xor_key = bytes([key])
        xor_data = bytearray(len(data))
        for i in range(len(data)):
            xor_data[i] = data[i] ^ xor_key[0]
        
        # Try to find the search string in the XOR'd data
        # We'll also try to extract a larger readable chunk if found
        try:
            index = xor_data.find(search_bytes)
            if index != -1:
                # Extract a readable chunk around the found string
                # Let's say 100 bytes before and 200 bytes after
                start = max(0, index - 100)
                end = min(len(xor_data), index + len(search_bytes) + 200)
                
                # Try to decode as UTF-8, handling errors
                try:
                    chunk = xor_data[start:end].decode('utf-8', errors='ignore')
                    found_flags.append(f"Found with key {key} (0x{key:02x}):\n{chunk}\n{'='*50}")
                except UnicodeDecodeError:
                    pass # Ignore if not decodable as UTF-8
        except ValueError:
            pass # search_bytes not found

    return found_flags

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: python {sys.argv[0]} <binary_file> <search_string>")
        sys.exit(1)

    binary_file_path = sys.argv[1]
    search_term = sys.argv[2]

    try:
        with open(binary_file_path, 'rb') as f:
            binary_data = f.read()
    except FileNotFoundError:
        print(f"Error: Binary file not found at {binary_file_path}")
        sys.exit(1)
    
    print(f"Searching for '{search_term}' in '{binary_file_path}' with single-byte XOR bruteforce...")
    results = xor_bruteforce(binary_data, search_term)

    if results:
        for result in results:
            print(result)
    else:
        print(f"'{search_term}' not found after single-byte XOR bruteforce.")
