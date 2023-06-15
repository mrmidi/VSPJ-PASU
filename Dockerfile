FROM quay.io/jitesoft/alpine:latest

# Path: /app
WORKDIR /app

ADD . /app

# install git
RUN apk add --no-cache git

# Path: /app
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]