FROM python:3.10-slim

WORKDIR /app
ADD . /app

RUN apt update && apt install -y python3-tk

COPY requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt && flask init-db

EXPOSE 80

CMD ["python", "app.py"]