
def decrypt_file(input_path, output_path):
    with open(input_path, 'rb') as f_in:
        data = f_in.read()
    
    decrypted_data = bytearray()
    for byte in data:
        # Shift -5 and handle wrapping (0-255)
        # Note: The problem statement says "hanged at least 5 times" and analysis showed +5 shift.
        # So we need -5 shift.
        # Python bytes are integers 0-255.
        decrypted_byte = (byte - 5) % 256
        decrypted_data.append(decrypted_byte)
        
    with open(output_path, 'wb') as f_out:
        f_out.write(decrypted_data)

if __name__ == "__main__":
    decrypt_file('encrypted.file', 'restored.png')
