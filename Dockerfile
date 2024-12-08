FROM python:3.10

RUN apt update && \
    apt install -y pulseaudio alsa-utils
RUN pip3 install playwright coqui-tts

RUN playwright install chromium

RUN useradd -m fif
USER fif

RUN git clone https://github.com/Yoreh2024/FuckFIF-Dockerized /home/fif/fuckfif

CMD ["pulseaudio --start --daemonize=no --exit-idle-time=-1 && \
    tail -f /dev/null"]
# \
#     "pulseaudio --start --system=false --daemonize=no --exit-idle-time=-1 && \
#     pactl load-module module-pipe-source source_name=VirtualPipeMic file=/tmp/VirtualPipeMic format=s16le rate=44100 channels=2 && \
#     pacmd update-source-proplist VirtualPipeMic device.description=VirtualPipeMic && \
#     pacmd set-default-source VirtualPipeMic && \