FROM ubuntu

RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install software-properties-common -y \
    && add-apt-repository ppa:deadsnakes/ppa -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install python3.11 -y \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1 \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 2 \
    && apt-get install python-is-python3 -y

RUN apt-get install -y curl \
    && curl -sSL https://install.python-poetry.org | python - \
    && apt install -y python3.11 python3.11-distutils \
    && curl -sSl https://bootstrap.pypa.io/get-pip.py | python -

RUN apt-get install -y libsqlite3-dev \
    && apt-get install python3.11-dev -y \
    && apt-get install -y libgmp-dev \
        portaudio19-dev \
        libssl-dev \
        libpcap-dev \
        libffi-dev \
        libxml2-dev \
        libxslt1-dev \
        libblas-dev \
        libatlas-base-dev \
    && apt-get install -y gcc-x86-64-linux-gnu

CMD cd root \
    && mkdir src

ENTRYPOINT export PATH="/root/.local/bin:$PATH" && cd root/src && /bin/bash