import os
import time
import wave

class VirtualMic:
    def __init__(self, device_name, format, rate, channels):
        self.device_name = device_name
        self.format = format
        self.rate = rate
        self.channels = channels
        print("[VirtualMic] 虚拟声卡初始化完成。")

    def play(self, file_path):
        print("[VirtualMic] 音频流开始从{}读到虚拟声卡中。".format(file_path))

        with wave.open(file_path, 'rb') as wav_file:
            n_frames = wav_file.getnframes()
            frame_rate = wav_file.getframerate()
            duration = n_frames / float(frame_rate)

        time.sleep(duration)

        print("[VirtualMic] 音频流结束。".format(file_path))
        return