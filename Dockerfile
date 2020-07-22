FROM 3.9.0b5-alpine3.12
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD [ "python", "bot.py" ]
