FROM python:3.13.13-slim-trixie

RUN apt-get update && apt-get install -y \
    libjxl-tools \
    libjpeg-tools \
    libopenjp2-tools \
    libjxr-tools \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /app