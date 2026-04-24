import wave
import struct

def analyze():
    with wave.open('flag_new.wav', 'r') as f:
        frames = f.readframes(f.getnframes())
        samples = struct.unpack(f"<{len(frames)//2}h", frames)

    threshold = 10000
    state = 0 # 0 for silence, 1 for tone
    durations = [] # list of (state, length)
    current_length = 0

    # Process samples
    # We can process sample by sample, but it's slow in python.
    # Let's iterate. To speed up, we can assume the frequency is not too high relative to envelope.
    # Actually, let's just use a simple state machine.
    
    # Optimization: iterate and check if abs(sample) > threshold.
    # However, a sine wave crosses zero. So we need a window or "hold" time.
    # If we see a value > threshold, we are in "tone". If we don't see one for X samples, we are in silence.
    # Let's use a window size of 100 samples (~2ms).
    
    window_size = 100
    max_in_window = 0
    
    # We will compress the samples into windows
    windowed_states = []
    for i in range(0, len(samples), window_size):
        chunk = samples[i:i+window_size]
        mx = max(abs(s) for s in chunk)
        windowed_states.append(1 if mx > threshold else 0)

    # Now RLE on windowed_states
    if not windowed_states:
        return

    current_state = windowed_states[0]
    current_count = 0
    
    rle = []
    for s in windowed_states:
        if s == current_state:
            current_count += 1
        else:
            rle.append((current_state, current_count * window_size)) # Convert back to samples
            current_state = s
            current_count = 1
    rle.append((current_state, current_count * window_size))

    # Analyze durations
    tones = [x[1] for x in rle if x[0] == 1]
    silences = [x[1] for x in rle if x[0] == 0]

    print("Tone durations (sorted):")
    print(sorted(tones))
    print("\nSilence durations (sorted):")
    print(sorted(silences))

analyze()
