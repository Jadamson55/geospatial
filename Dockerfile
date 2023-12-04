FROM python:3.10

ENV PYTHONPATH=/usr/app:/usr/app/vendor

WORKDIR /usr/app

COPY ./src/geospatial/requirements.txt ./
RUN pip install -r ./requirements.txt

RUN apt-get update

CMD /bin/bash
