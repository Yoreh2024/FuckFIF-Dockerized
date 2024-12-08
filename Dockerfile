FROM python:3.10

RUN apt update && \
    apt install -y pulseaudio ffmpeg
RUN pip3 install playwright coqui-tts
RUN playwright install-deps

RUN useradd -m fif
USER fif

RUN playwright install chromium-headless-shell
    
RUN mkdir -p ~/.local/share/tts && \
    curl -L https://github.com/coqui-ai/TTS/releases/download/v0.10.1_models/tts_models--multilingual--multi-dataset--your_tts.zip -o /tmp/models.zip && \
    unzip /tmp/models.zip -d ~/.local/share/tts && \
    rm /tmp/models.zip

RUN git clone https://github.com/Yoreh2024/FuckFIF-Dockerized ~/fuckfif

ENV tts_start_mode=cpu

CMD pulseaudio --start --system=false --exit-idle-time=-1 && \
    python ~/fuckfif/src/main.py