import os

class tts:
    def __init__(self):
        self.model_name = os.getenv("model_name", "voice_conversion_models/multilingual/vctk/freevc24")   # 语音合成器模型
        self.mode = os.getenv("mode", "cpu")   # cuda|cpu 是否启用GPU加速
        self.tmp_path = os.getenv("tmp_path", "tmp")   # 临时文件路径
        self.target_file = os.getenv("target_file", "draft/1.wav")   # 10秒左右的你的录音，用于生成目标音色

        self.source_file = self.tmp_path + "/fuckfif_tmp_source_voice.wav"
        self.output_file = self.tmp_path + "/fuckfif_tmp_output_voice.wav"

class vmic:
    def __init__(self):
        self.name = os.getenv("vmic_name", "VirtualPipeMic") # 虚拟麦克风名称

class config:
    def __init__(self):
        self.username = os.getenv("username", "") # fif账户
        self.password = os.getenv("password", "") # fif密码
        self.tts = tts()
        self.vmic = vmic()

        # 确保tts输出文件路径存在
        output_path = os.path.dirname(self.tts.output_file)
        if not os.path.isdir(output_path):
            os.mkdir(output_path)

config = config()