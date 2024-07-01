FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code/

# Install dependencies
COPY requirements.txt /code/
RUN pip --no-cache-dir install -r requirements.txt

COPY . /code/

EXPOSE 8000