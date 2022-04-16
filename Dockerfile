FROM python:3.8

WORKDIR /usr/src/app

# Install requirements
COPY . /usr/src/app
RUN pip install poetry
RUN poetry install
