# Create an up to date minimal Debian Jessi build

# Pull base image
FROM debian:jessie

# Update packages
RUN apt-get update && \
  apt-get upgrade -y && \
  apt-get clean -y && \
  apt-get autoclean -y && \
  apt-get autoremove -y && \
  rm -rf /usr/share/locale/* && \
  rm -rf /var/cache/debconf/*-old && \
  rm -rf /var/lib/apt/lists/* && \
  rm -rf /usr/share/doc/*

# Configuración para usar cache, se debe generar
# el archio de forma externa
#COPY etc/apt/apt.conf.d/01proxy /etc/apt/apt.conf.d/01proxy

# Configuración para debian
RUN  export DEBIAN_FRONTEND=noninteractive
ENV  DEBIAN_FRONTEND noninteractive
RUN  dpkg-divert --local --rename --add /sbin/initctl
RUN dpkg --add-architecture i386
RUN apt-get -y update

RUN apt-get install -y \
    python-pip \
    build-essential \
    git \
    python \
    python-dev \
    libglu1-mesa-dev \
    # We ignore this packages as we are not gonna run our kivy projects inside this
    # container, just compile them with buildozer
    #libsdl2-dev \
    #libsdl2-image-dev \
    #libsdl2-mixer-dev \
    #libsdl2-ttf-dev \
    #libportmidi-dev \
    #libswscale-dev \
    #libavformat-dev \
    #libavcodec-dev \
    zlib1g-dev \
    build-essential \
    ccache \
    git \
    lib32stdc++6 \
    lib32z1 \
    lib32z1-dev \
    python2.7 \
    python2.7-dev \
    openjdk-7-jdk \
    unzip \
    zlib1g-dev \
    zlib1g:i386
    #ffmpeg \

#RUN apt-get install -y software-properties-common python-software-properties
#RUN apt-add-repository ppa:mc3man/trusty-media
#RUN apt-get update
#RUN apt-get install -y ffmpeg

#RUN add-apt-repository ppa:kivy-team/kivy
#RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys A863D2D6
#RUN apt-get install -y python-kivy
#RUN apt-get install -y python-kivy-examples

RUN apt-get install -y libffi-dev libssl-dev
RUN pip install Cython==0.23
RUN pip install kivy buildozer

ARG LOCAL_USER_ID
RUN useradd -ms /bin/bash user -u $LOCAL_USER_ID

USER user
WORKDIR /home/user
# Buildozer


