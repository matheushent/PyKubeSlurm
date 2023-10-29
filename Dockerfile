FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

ARG PYTHON_VERSION=3.10.4
ARG PYTHON_MAJOR=3

WORKDIR /app

RUN apt update && \
    apt install -y \
    pkg-config \
    curl \
    gcc \
    libbz2-dev \
    libev-dev \
    libffi-dev \
    libgdbm-dev \
    liblzma-dev \
    libncurses-dev \
    libreadline-dev \
    libssl-dev \
    make \
    tk-dev \
    wget \
    zlib1g-dev

RUN wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.xz -P /tmp && \
    tar xvf /tmp/Python-${PYTHON_VERSION}.tar.xz -C /tmp/

RUN cd /tmp/Python-${PYTHON_VERSION} && \
    ./configure \
    --prefix=/usr \
    --enable-optimizations && \
    make altinstall

RUN cd /tmp && rm -rf /tmp/Python*

RUN curl -sSL https://install.python-poetry.org | \
    POETRY_HOME=/opt/poetry POETRY_VERSION=1.5.1 python3.10 && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

RUN ln -s /usr/bin/python3.10 /usr/bin/python

COPY ./pyproject.toml ./poetry.lock* /app/
RUN poetry install

COPY ./README.md /app/

COPY ./pykubeslurm /app/pykubeslurm

CMD [ "pykubeslurm", "run" ]