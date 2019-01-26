FROM python:3-stretch

LABEL maintainer="Justin Garrison <justinleegarrison@gmail.com>" \
    org.label-schema.schema-version="1.0" \
    org.label-schema.name="mps-youtube" \
    org.label-schema.description="Terminal based YouTube player and downloader " \
    org.label-schema.url="https://github.com/mps-youtube/mps-youtube/wiki" \
    org.label-schema.vcs-url="https://github.com/mps-youtube/mps-youtube" \
    org.label-schema.docker.cmd="docker run -v /dev/snd:/dev/snd -it --rm --privileged --name mpsyt mpsyt"

RUN DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y mplayer mpv && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean && apt-get purge

RUN pip install mps-youtube youtube-dl

ENTRYPOINT ["mpsyt"]
