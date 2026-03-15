# Use the latest stable Ubuntu image as a base
FROM ubuntu:24.04

# Avoid prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install the libraries
RUN apt-get update && apt-get install -y \
    libjxl-tools \
    libjpeg-tools \
    libopenjp2-tools \
    libjxr-tools \
    && rm -rf /var/lib/apt/lists/*

# Set a default command to verify installations
CMD ["/bin/bash"]