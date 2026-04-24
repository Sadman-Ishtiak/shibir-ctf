import wave
import struct

MORSE_CODE_DICT = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z',
    '-----': '0', '.----': '1', '..---': '2', '...--': '3', '....-': '4',
    '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9',
    '.-.-.-': '.', '--..--': ',', '..--..': '?', '.----.': "'", '-.-.--': '!',
    '-..-.': '/', '-.--.': '(', '-.--.-': ')', '.-...': '&', '---...': ':',
    '-.-.-.': ';', '-...-': '=', '.-.-.': '+', '-....-': '-', '..--.-': '_',
    '.-..-.': '"', '...-..-': '$', '.--.-.': '@',
    '{': '{', '}': '}' # Handling brackets if they appear as literals or specialized code, though standard Morse doesn't have {}, often in CTFs they use specialized or mapped codes. 
    # Let's assume standard letters/numbers first. If braces are encoded, they might be distinct.
    # Actually, BICS77{...} usually implies the braces are part of the format but the content inside is what's encoded, OR the braces are encoded too.
    # Common codes for braces: Open brace: -.--. (same as parenthesis) or distinct. 
    # Let's decode to dots/dashes first, then map.
}

# Reverse mapping if needed, but we need dot/dash to char.

def decode():
    with wave.open('flag_new.wav', 'r') as f:
        frames = f.readframes(f.getnframes())
        samples = struct.unpack(f"<{len(frames)//2}h", frames)

    threshold = 10000
    window_size = 100
    
    windowed_states = []
    for i in range(0, len(samples), window_size):
        chunk = samples[i:i+window_size]
        mx = max(abs(s) for s in chunk)
        windowed_states.append(1 if mx > threshold else 0)

    if not windowed_states:
        return

    current_state = windowed_states[0]
    current_count = 0
    
    rle = []
    for s in windowed_states:
        if s == current_state:
            current_count += 1
        else:
            rle.append((current_state, current_count * window_size))
            current_state = s
            current_count = 1
    rle.append((current_state, current_count * window_size))

    # Process RLE into Morse symbols
    morse_sequence = ""
    
    # Thresholds
    # Dot < 8000
    # Dash > 8000
    
    # Inter-element gap (silence) < 9000
    # Inter-letter gap (silence) > 9000 and < 20000
    # Inter-word gap (silence) > 20000
    
    current_char_symbols = ""
    decoded_message = ""
    
    for state, duration in rle:
        if state == 1: # Tone
            if duration < 8000:
                current_char_symbols += "."
            else:
                current_char_symbols += "-"
        else: # Silence
            if duration < 9000:
                # Just a gap between parts of a letter
                pass
            elif duration < 20000:
                # Gap between letters
                if current_char_symbols:
                    if current_char_symbols in MORSE_CODE_DICT:
                        decoded_message += MORSE_CODE_DICT[current_char_symbols]
                    else:
                        decoded_message += f"[{current_char_symbols}]"
                    current_char_symbols = ""
            else:
                # Gap between words
                if current_char_symbols:
                    if current_char_symbols in MORSE_CODE_DICT:
                        decoded_message += MORSE_CODE_DICT[current_char_symbols]
                    else:
                        decoded_message += f"[{current_char_symbols}]"
                    current_char_symbols = ""
                decoded_message += " "

    # Append last char
    if current_char_symbols:
        if current_char_symbols in MORSE_CODE_DICT:
            decoded_message += MORSE_CODE_DICT[current_char_symbols]
        else:
            decoded_message += f"[{current_char_symbols}]"

    print("Decoded Message:")
    print(decoded_message)

decode()
