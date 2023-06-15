FROM quay.io/ansible/python-base:latest

# Path: /app
WORKDIR /app

ADD . /app

# Path: /app
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]