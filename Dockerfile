FROM tensorflow/tensorflow:2.8.0

WORKDIR /app

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg

RUN apt-get install -y libpq-dev python-dev

RUN apt-get install -y git
COPY ./requirements.txt .

RUN pip install --no-cache-dir -U -r requirements.txt

RUN pip install git+https://github.com/GGolfz/spleeter.git@master#egg=spleeter
COPY . .

CMD ["python3", "app.py"]
