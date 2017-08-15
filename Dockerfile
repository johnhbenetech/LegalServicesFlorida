FROM ubuntu:16.04

ENV DEBIAN_FRONTEND noninteractive

ENV DJANGO_DATABASE_NAME openref4
ENV DJANGO_DATABASE_USER postgres
ENV DJANGO_DATABASE_PASSWORD 'postgres'
ENV DJANGO_DATABASE_HOST 127.0.0.1
ENV DJANGO_DATABASE_PORT 5432

ENV DJANGO_EMAIL_SUBJECT 'Weekly update'
ENV DJANGO_EMAIL_FROM 'noreply@noreply.com'
ENV DJANGO_EMAIL_TO 'admin1@test.com,anotheradmin@gmail.com'

ENV DJANGO_SMTP_HOST 'localhost'
ENV DJANGO_SMTP_PORT 25
ENV DJANGO_SMTP_USER 'test@test.com'
ENV DJANGO_SMTP_PASSWORD 'smtppassword'

RUN apt-get update && apt-get install -y \
    git \
    vim \
    python3 \
    python3-pip \
    nginx \
    supervisor \
    libpq-dev \
    pwgen && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip

RUN pip3 install uwsgi

# nginx config
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY nginx-site.conf /etc/nginx/sites-available/default

# supervisor config
COPY supervisor.conf /etc/supervisor/conf.d/

# uWSGI config
COPY uwsgi.ini /home/django/
COPY uwsgi_params /home/django/

COPY start.sh /home/django/

ADD requirements.txt /home/django/

WORKDIR /home/django

ADD . /home/django/

EXPOSE 80

CMD ["/bin/bash", "/home/django/start.sh"]