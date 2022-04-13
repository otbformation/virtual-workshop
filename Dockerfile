FROM ubuntu:20.04 

RUN echo "Europe/Paris" > /etc/timezone

RUN apt-get update -y \
 && apt-get upgrade -y
 && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        libxcb1 \
        libxcb-composite0 \
        libxcb-glx0 \
        libxcb-icccm4 \
        libxcb-image0 \
        libxcb-keysyms1 \
        libxcb-randr0 \
        libxcb-render0 \
        libxcb-render-util0 \
        libxcb-util1 \
        libxcb-shm0 \
        libxcb-xfixes0 \
        libxcb-xinerama0 \
        libxcb-xinput0 \
        libxcb-xkb1 \
        libx11-xcb1 \
        libglu1-mesa \
        libxrender1 \
        libxi6 \
        libxkbcommon0 \
        libxkbcommon-x11-0 \
        libxinerama1 \
        python3 \ 
        python3-dev \
        python3-numpy \
        libtool \
 && rm -rf /var/lib/apt/lists/*
 
RUN curl https://www.orfeo-toolbox.org/packages/OTB-8.0.0-Linux64.run -o OTB-8.0.0-Linux64.run \
&& chmod +x OTB-8.0.0-Linux64.run \
&& ./OTB-8.0.0-Linux64.run --target /opt/otb

RUN pip install --no-cache-dir notebook

ARG NB_USER=jovyan
ARG NB_UID=1000
ENV USER ${NB_USER}
ENV NB_UID ${NB_UID}
ENV HOME /home/${NB_USER}

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}
	
# Make sure the contents of our repo are in ${HOME}
COPY . ${HOME}
USER root
RUN chown -R ${NB_UID} ${HOME}
USER ${NB_USER}

CMD ["ln -s /usr/lib/x86_64-linux-gnu/libpython3.8.so /opt/otb/lib/libpython3.8.so.rh-python38-1.0"]

ENTRYPOINT ["/bin/bash","-c","source /opt/otb/otbenv.profile && /bin/bash"]

