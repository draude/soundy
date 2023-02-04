import numpy as np
import pyaudio
import threading
import tkinter as tk

def generate_sine_wave(frequency, duration, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    return 0.5 * np.sin(2 * np.pi * frequency * t) * volume

def callback(in_data, frame_count, time_info, status):
    wave = generate_sine_wave(frequency, 1/frequency, sample_rate)
    return (wave.tobytes(), pyaudio.paContinue)

def start_stream():
    global stream, pa
    if hasattr(stream, "is_active") and stream.is_active():
        return
    stream = pa.open(format=pyaudio.paFloat32,
                     channels=1,
                     rate=sample_rate,
                     output=True,
                     stream_callback=callback,
                     output_device_index=2)
    stream.start_stream()

def stop_stream():
    global stream
    try:
        if stream.is_active():
            stream.stop_stream()
            stream.close()
    except:
        print("Stream already stopped")

def update_frequency(value):
    global frequency
    frequency = value

def update_volume(value):
    global volume
    volume = value

root = tk.Tk()
root.title("Sine Wave Synthesizer")

frequency = 440
sample_rate = 44100
volume = 0.2

pa = pyaudio.PyAudio()
stream = None

slider = tk.Scale(root, from_=20, to=20000, orient="horizontal", command=update_frequency)
slider.pack()

volume_slider = tk.Scale(root, from_=0, to=1, orient="horizontal", command=update_volume)
volume_slider.pack()

start_button = tk.Button(root, text="Start", command=start_stream)
start_button.pack()

stop_button = tk.Button(root, text="Stop", command=stop_stream)
stop_button.pack()

root.mainloop()
