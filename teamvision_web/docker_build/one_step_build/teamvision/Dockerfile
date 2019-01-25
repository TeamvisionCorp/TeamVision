FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /web/www/teamvision
ADD requirements.txt /web/www/teamvision
ADD startup.sh /web/www/teamvision
WORKDIR /web/www/teamvision
RUN chmod 777 startup.sh
RUN pip install -r requirements.txt
