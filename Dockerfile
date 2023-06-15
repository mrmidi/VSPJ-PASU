FROM python:3.9

# Path: /app
WORKDIR /app

ADD . /app

# Path: /app
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]