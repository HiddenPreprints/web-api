FROM python:3.7

COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt
RUN pip install gunicorn

COPY . /code/
WORKDIR /code/

RUN rm -rf /tmp/multiproc-tmp && mkdir /tmp/multiproc-tmp
ENV prometheus_multiproc_dir=/tmp/multiproc-tmp

CMD python manage.py collectstatic --noinput & gunicorn --workers=3 --bind=0.0.0.0:8001 epapi.wsgi:application
