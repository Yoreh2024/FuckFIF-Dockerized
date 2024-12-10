FROM python:3.10
RUN pip3 install playwright git+https://github.com/SWivid/F5-TTS.git

RUN playwright install-deps && \
    playwright install chromium-headless-shell

RUN apt install -y pipewire ffmpeg

RUN mkdir /model && \
    curl -L -o /model/model_1200000.pt https://www.modelscope.cn/models/AI-ModelScope/F5-TTS/resolve/master/F5TTS_Base/model_1200000.pt && \
    curl -L -o /model/vocab.txt https://www.modelscope.cn/models/AI-ModelScope/F5-TTS/resolve/master/F5TTS_Base/vocab.txt

ARG CACHE_BUST=1

COPY . /fuckfif

CMD tail -f /dev/null