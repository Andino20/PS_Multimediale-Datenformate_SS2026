#!/bin/bash
docker run --rm -v "$(pwd)":/app mmdf:latest python src/main.py "$@"