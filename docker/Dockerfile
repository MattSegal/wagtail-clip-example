FROM ubuntu:focal

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING UTF-8
ENV TIMEZONE Australia/Melbourne

WORKDIR /app

RUN echo "Updating apt sources." && apt-get -qq update

# Install generic useful stuff.
# curl: for HTTP debugging
# iputils-ping: for pinging things
# postgresql-client: for talking to PostgreSQL database
# postgresql-common: PostgreSQL database-cluster manager
# python3-setuptools: So we can install Pip
# python3-dev: Header files for the Python C API so we can compile C stuff or something.
# build-essential: More buildy things
RUN echo "Installing generic stuff." && \
  apt-get -qq install \
  curl \
  iputils-ping \
  postgresql-client \
  postgresql-common \
  python3-setuptools \
  python3-dev \
  build-essential \
  git-all

RUN echo "Downloading and installing pip for Python 3.8" && \
  curl https://bootstrap.pypa.io/get-pip.py --silent --output /tmp/get-pip.py && \
  python3 /tmp/get-pip.py


# Install Python packages
COPY app/requirements.txt .

RUN \
  echo "Installing python packages..." && \
  pip install -r requirements.txt


# Mount the codebase
ADD app /app
