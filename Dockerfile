FROM python:latest
ENV PYTHONUNBUFFERED 1
ENV C_FORCE_ROOT true

RUN mkdir /code/
ADD ./src /code/
WORKDIR /code/

RUN pip install pipenv
RUN pipenv install --system
RUN apt-get update && apt-get install -y libproj-dev gdal-bin
