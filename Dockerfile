FROM tensorflow/tensorflow:2.6.1

WORKDIR /app

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg

RUN apt-get install -y libpq-dev python-dev

COPY ./requirements.txt .

RUN pip install --no-cache-dir -U -r requirements.txt

COPY . .

CMD ["python3", "app.py"]
