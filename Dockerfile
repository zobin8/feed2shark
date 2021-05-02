FROM python:3.11
LABEL maintainer="Strubbl-dockerfile@linux4tw.de"

ENV DATA_DIR /data
COPY . feed2toot
RUN \
  mkdir $DATA_DIR \
  && cd feed2toot \
  && python setup.py install

VOLUME $DATA_DIR
WORKDIR $DATA_DIR
CMD ["feed2toot", "--verbose", "--debug","-c", "./feed2toot.ini"]

