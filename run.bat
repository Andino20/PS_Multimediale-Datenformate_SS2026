@echo off
docker run --rm -v "%cd%:/app" mmdf:latest python src/main.py %*