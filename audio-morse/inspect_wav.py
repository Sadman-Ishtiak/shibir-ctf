import wave
import struct

try:
    with wave.open('flag_new.wav', 'r') as wav_file:
        print(f"Channels: {wav_file.getnchannels()}")
        print(f"Sample width: {wav_file.getsampwidth()}")
        print(f"Frame rate: {wav_file.getframerate()}")
        print(f"Number of frames: {wav_file.getnframes()}")
        
        # Read some frames to see amplitude
        frames = wav_file.readframes(1000)
        # Assuming 16-bit audio based on file output from previous turn (little-endian)
        samples = struct.unpack(f"<{len(frames)//2}h", frames)
        print(f"First 50 samples: {samples[:50]}")
        
        # Check max/min amplitude in a chunk to gauge volume
        wav_file.rewind()
        frames_all = wav_file.readframes(wav_file.getnframes())
        samples_all = struct.unpack(f"<{len(frames_all)//2}h", frames_all)
        print(f"Max Amplitude: {max(samples_all)}")
        print(f"Min Amplitude: {min(samples_all)}")

except Exception as e:
    print(f"Error: {e}")
