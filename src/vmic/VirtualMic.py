import os
import subprocess

class VirtualMic:
    def __init__(self, device_name, rate=44100, channels=2):
        self.device_name = device_name
        self.rate = rate
        self.channels = channels
        # 创建一个虚拟的 PipeWire 音频源
        subprocess.run([
            "pw-loopback",
            "-m", "[ FL FR ]",
            "--capture-props", f"media.class=Audio/Sink node.name={self.device_name} node.description={self.device_name}"
        ], check=True)
        print("[VirtualMic] 虚拟声卡初始化完成。")

    def play(self, file_path):
        # 使用 pw-play 将音频数据发送到虚拟设备
        print("[VirtualMic] 音频流开始从{}读到虚拟声卡中。".format(file_path))
        try:
            subprocess.run([
                "pw-play",
                "-t", "raw",
                "-r", str(self.rate),
                "-c", str(self.channels),
                "--target", self.device_name,
                file_path
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"[VirtualMic] 播放失败: {e}")