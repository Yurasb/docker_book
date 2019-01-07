FROM python:3.6

RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt
WORKDIR /app
COPY app /app
COPY cmd.sh /

EXPOSE 9090 9191
USER uwsgi

CMD ["/cmd.sh"]