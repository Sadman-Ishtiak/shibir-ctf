key = b"J0Y_B4N9"
with open("joybangla.bin", "rb") as f:
    data = f.read()

decrypted = bytearray()
for i in range(len(data)):
    decrypted.append(data[i] ^ key[i % len(key)])

with open("decrypted.txt", "wb") as f:
    f.write(decrypted)

print("Decryption complete.")
