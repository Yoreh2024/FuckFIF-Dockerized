import time

from config import config
tts = config.tts
vmic = config.vmic

from tts.TTSSolver import TTSSolver
from vmic.VirtualMic import VirtualMic


class Speaker:
    def __init__(self):
        self.tts_solver = TTSSolver(tts.model_name, tts.mode, tts.target_file)
        self.virtual_mic = VirtualMic(vmic.name, "s16le", "24000", "1")
        pass

    def speak(self):
        print("[Speaker] 正在合成语音。")
        self.tts_solver.get_file(tts.source_file, tts.target_file, tts.output_file)
        print("[Speaker] 正在播放语音。")
        self.virtual_mic.play(tts.output_file)
        print("[Speaker] 语音播放完成。")
        return
