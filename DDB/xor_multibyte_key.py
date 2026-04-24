import sys

def xor_with_key(data, key_bytes):
    xor_data = bytearray(len(data))
    key_len = len(key_bytes)
    for i in range(len(data)):
        xor_data[i] = data[i] ^ key_bytes[i % key_len]
    return xor_data

def find_readable_strings(data, min_len=4):
    strings = []
    current_string = []
    for byte_val in data:
        if 32 <= byte_val <= 126:  # ASCII printable characters
            current_string.append(chr(byte_val))
        else:
            if len(current_string) >= min_len:
                strings.append("".join(current_string))
            current_string = []
    if len(current_string) >= min_len:
        strings.append("".join(current_string))
    return strings

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: python {sys.argv[0]} <binary_file> <xor_key_string>")
        sys.exit(1)

    binary_file_path = sys.argv[1]
    xor_key_string = sys.argv[2]
    xor_key_bytes = xor_key_string.encode('utf-8')

    try:
        with open(binary_file_path, 'rb') as f:
            binary_data = f.read()
    except FileNotFoundError:
        print(f"Error: Binary file not found at {binary_file_path}")
        sys.exit(1)
    
    print(f"XORing '{binary_file_path}' with key '{xor_key_string}' and searching for readable strings...")
    
    xor_result = xor_with_key(binary_data, xor_key_bytes)
    readable_strings = find_readable_strings(xor_result, min_len=8) # Increased min_len for better results

    if readable_strings:
        print("\n--- Readable Strings Found ---")
        for s in readable_strings:
            # Filter for strings that might contain flag-like patterns or keywords
            if "BICSCTF" in s or "flag" in s.lower() or "token" in s.lower() or "auth" in s.lower():
                print(s)
        print("------------------------------")
    else:
        print("No significant readable strings found with the given key.")
