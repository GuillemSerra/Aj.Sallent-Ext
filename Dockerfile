FROM ubuntu:16.04

# basic flask environment
RUN apt-get update && apt-get install -y python-pip python-dev build-essential libssl-dev libffi-dev

RUN apt-get update && apt-get install -y libmysqlclient-dev python-mysqldb libicu-dev

# application folder
ENV APP_DIR /app
WORKDIR ${APP_DIR}

RUN pip install --upgrade pip && \
    pip install flask && \
    pip install pyicu

# expose web server port
# only http, for ssl use reverse proxy
EXPOSE 80

# exectute start up script
ENTRYPOINT ["/usr/bin/python", "app.py"]

