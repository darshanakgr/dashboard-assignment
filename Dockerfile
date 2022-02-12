FROM python:3.10-slim

WORKDIR /app
ADD . /app

COPY requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt
EXPOSE 80

CMD ["python", "app.py"]