import time

from tts.TTSSolver import TTSSolver
from vmic.VirtualMic import VirtualMic


class Speaker:
    def __init__(self, tts_model_name, mode, vmic, target_voice_path):
        target_voice_path="3.wav", 
        self.target_voice_path = target_voice_path;
        self.tts_solver = TTSSolver(tts_model_name, mode, target_voice_path)
        self.virtual_mic = VirtualMic(device_name=vmic)
        pass

    def speak(self, text: str):
        print("[Speaker] 正在合成语音。")
        self.tts_solver.get_file(text, self.target_voice_path, prompt="I think success has no rules, but you can learn a lot from failure.")
        print("[Speaker] 正在播放语音。")
        self.virtual_mic.play("tmp/temp.wav")
        print("[Speaker] 语音播放完成。")
        return
