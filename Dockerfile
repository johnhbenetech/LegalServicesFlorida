FROM ubuntu:16.04

ENV DEBIAN_FRONTEND noninteractive

ENV DJANGO_DATABASE_NAME openref3
ENV DJANGO_DATABASE_USER postgres
ENV DJANGO_DATABASE_PASSWORD ''
ENV DJANGO_DATABASE_HOST 192.168.1.12
ENV DJANGO_DATABASE_PORT 5432

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