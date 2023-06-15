FROM quay.io/jitesoft/alpine:latest

# Path: /app
WORKDIR /app

ADD . /app

# install python3
RUN apk add --no-cache python3
# install pip
RUN apk add --no-cache py3-pip

# Path: /app
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]