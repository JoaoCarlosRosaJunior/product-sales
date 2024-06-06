FROM python:3.11.7

RUN apt-get update \
    && pip install --no-cache-dir --upgrade pip

WORKDIR /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/requirements.txt
COPY . /app

EXPOSE 5000

CMD ["python3", "src/server.py"]
