FROM python:3.9

ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN dpkg-reconfigure --frontend noninteractive tzdata

ADD ./requirements.txt /code/requirements.txt

WORKDIR /code
RUN pip install -r requirements.txt
ADD . /code

CMD ["python", "./bot.py"]
