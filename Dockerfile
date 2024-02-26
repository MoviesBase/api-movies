ARG environment
FROM python:3.10.9
# flake8: noqa: E501
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y libxml2-dev libxmlsec1-dev \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /local
ADD /app /local
ADD /config /local/config
RUN pip install -r /local/config/requirements.txt

CMD bash -c "python /check_service.py --service-name movies-db --ip movies-db --port 3306 && python manage.py makemigrations && python manage.py migrate && gunicorn uservice.wsgi --workers 1 --threads 100 --max-requests 1000 --max-requests-jitter 15 -b 0.0.0.0:8888"

WORKDIR /local
