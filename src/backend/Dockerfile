# Set the base image
FROM python:3.7-slim-buster

# File Author / Maintainer
MAINTAINER Fabiano Alencar

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y \
        apache2 \
        apache2-dev \
        build-essential \ 
        libapache2-mod-wsgi-py3 \
        cmake\
        pkg-config\
        libx11-dev\
        libatlas-base-dev\
        libgtk-3-dev\
        libboost-python-dev\
    && apt-get clean \ 
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install --upgrade pip

# Copy over and install the requirements
COPY /face_recognition_app/requirements.txt /var/www/apache-flask/face_recognition_app/requirements.txt

#RUN pip3 install virtualenv
#WORKDIR /var/www/apache-flask/app
#RUN virtualenv env

RUN pip3 install --no-cache-dir -r /var/www/apache-flask/face_recognition_app/requirements.txt

# Copy over the apache configuration file and enable the site
COPY ./apache-flask.conf /etc/apache2/sites-available/apache-flask.conf
RUN a2ensite apache-flask
RUN a2enmod headers

#Copy over the wsgi file
COPY ./apache-flask.wsgi /var/www/apache-flask/apache-flask.wsgi

COPY ./run.py /var/www/apache-flask/run.py
COPY ./face_recognition_app /var/www/apache-flask/face_recognition_app/

RUN chown www-data:www-data -R /var/www/apache-flask/

RUN a2dissite 000-default.conf
RUN a2ensite apache-flask.conf

EXPOSE 80

WORKDIR /var/www/apache-flask

CMD  /usr/sbin/apache2ctl -D FOREGROUND