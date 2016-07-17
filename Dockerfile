FROM python:latest
MAINTAINER Justin Garrison <justinleegarrison@gmail.com>

RUN apt-get update && apt-get install -y mplayer mpv
RUN pip install mps-youtube youtube-dl
RUN apt-get clean && apt-get purge

ENTRYPOINT ["mpsyt"]
