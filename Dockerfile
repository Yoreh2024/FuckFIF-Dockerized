FROM python:3.10

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && \
    apt install -y ffmpeg pulseaudio && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m fif
USER fif

# RUN mkdir -p ~/.local/share/tts && \
#     curl -L https://github.com/coqui-ai/TTS/releases/download/v0.13.0_models/voice_conversion_models--multilingual--vctk--freevc24.zip -o /tmp/models.zip && \
#     unzip /tmp/models.zip -d ~/.local/share/tts && \
#     rm /tmp/models.zip

COPY --chown=fif:fif . /fuckfif

USER root
RUN pip3 install --no-index --find-links=/fuckfif/depend/requirements --requirement /fuckfif/requirements.txt
RUN playwright install-deps
USER fif

RUN playwright install chromium-headless-shell

RUN rm -r ~/.local/share/tts && \
    ln -s /fuckfif/model/tts ~/.local/share

CMD pulseaudio --start --system=false --exit-idle-time=-1 && \
    python /fuckfif/src/main.py && \
    tail -f /dev/null