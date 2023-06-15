FROM quay.io/jitesoft/alpine:latest

# Path: /app
WORKDIR /app

ADD . /app


# install python3
RUN apk add --no-cache python3
# install pip
RUN apk add --no-cache py3-pip py3-scipy py3-numpy py3-matplotlib py3-pandas py3-pillow py3-lxml
# install dev packages
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev openssl-dev gfortran build-base g++ openblas-dev freetype-dev libpng-dev cmake

# Path: /app
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]