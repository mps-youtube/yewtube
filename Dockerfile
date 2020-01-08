ARG PYTHON_IMAGE=3
FROM python:${PYTHON_IMAGE}

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

RUN pip install pafy youtube-dl

COPY mpsyt /usr/local/bin
COPY mps_youtube /tmp/mps_youtube

RUN mkdir -p $(python -m site --user-site)
RUN mv /tmp/mps_youtube $(python -m site --user-site)/mps_youtube

ENTRYPOINT ["mpsyt"]
