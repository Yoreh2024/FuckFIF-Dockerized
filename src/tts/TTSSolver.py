import subprocess
import os
from pathlib import Path

class TTSSolver:
    def __init__(self, text, target_voice_path, prompt):
        print("[TTS] 正在初始化神经网络。")
        self.target_voice_path = target_voice_path
        self.text = text

    def get_voice(self, text):
        return self.get_file(text, None)

    def get_file(self, text: str, path=None):
        if not text.strip():
            print("[TTS] 输入文本为空，无法合成语音。")
            return
        
        print("[TTS] 正在合成语音。")

        if len(text.split(" ")) <= 2:
            text = text + " " + text

        # 如果没有提供路径，则使用默认输出路径
        if path is None:
            path = "tmp/temp.wav"

        # 构建 f5-tts_infer-cli 命令
        command = [
            "f5-tts_infer-cli",
            "-m F5-TTS",
            "-p", "/model/model_1200000.pt",
            "-v", "/model/vocab.txt",
            "-r", self.target_voice_path,
            "-s", self.text,
            "-t", text,
            "-w", str(path)
        ]

        try:
            # 执行命令并等待完成
            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(f"[TTS] 生成的音频已保存到 {path}")
        except subprocess.CalledProcessError as e:
            print(f"[TTS] 语音合成失败: {e.stderr}")
            return None

        return path