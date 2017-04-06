FROM python:3-onbuild
MAINTAINER emile@vauge.com

ADD . /howdoi
WORKDIR /howdoi

RUN python setup.py install

ENTRYPOINT [ "howdoi" ]
CMD [ "-h" ]
