FROM python:3
WORKDIR /usr/src/project3
ADD requirements.txt /usr/src/project3
RUN pip install -r requirements.txt
ADD . /usr/src/project3