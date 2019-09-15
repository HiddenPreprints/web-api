FROM python:3.7

COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt

COPY . /code/
WORKDIR /code/

RUN rm -rf /tmp/multiproc-tmp && mkdir /tmp/multiproc-tmp
ENV prometheus_multiproc_dir=/tmp/multiproc-tmp

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000

