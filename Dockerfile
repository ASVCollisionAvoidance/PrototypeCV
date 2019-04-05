FROM jjanzic/docker-python3-opencv python
RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install -r requirements.txt
