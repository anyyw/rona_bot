FROM arm32v7/python:3.7.8-slim-buster
RUN apt-get update && apt-get install -y --no-install-recommends \
    libffi-dev \
    python-dev \
    make \
    ffmpeg \
    gcc
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD [ "python", "bot.py" ]
