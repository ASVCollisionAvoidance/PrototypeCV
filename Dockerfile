FROM julianbei/alpine-opencv-microimage:p2-3.1

RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install -r requirements.txt

# Define default command.
CMD ["python3 --version"]
