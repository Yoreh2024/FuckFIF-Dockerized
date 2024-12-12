import os
from TTS.api import TTS

from config import config

class TTSSolver:
    def __init__(self, model, mode, target_voice_path):
        print("[TTS] 正在初始化神经网络。")
        self.model = model
        self.target_voice_path = target_voice_path
        self.tts = TTS(model_name=model, progress_bar=False).to(mode)

    def get_voice(self, text):
        # return self.model.voice(text)
        return

    def get_file(self, source_voice_path, target_voice_path, output_voice_path):
        self.source_voice_path = source_voice_path
        self.target_voice_path = target_voice_path
        self.output_voice_path = output_voice_path

        if not os.path.exists(self.source_voice_path):
            print("[TTS] 源音频文件未被正常下载。")
            exit(1)

        print("[TTS] 正在合成语音。")
        self.tts.voice_conversion_to_file(
            source_wav=self.source_voice_path, 
            target_wav=self.target_voice_path, 
            file_path=self.output_voice_path)
        return