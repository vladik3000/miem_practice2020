FROM python:3-alpine

MAINTAINER Vladislav Kraskov <vvkraskov@.edu.hse.ru>

# Update package manager
RUN apk update
RUN apk upgrade

RUN pip install --upgrade pip
# Has stuff like gcc, make, and libc6-dev
#RUN apk add --update build-base
#RUN apk add --update make
#RUN apk add --update valgrind
RUN mkdir -p works groups results
# Valgrind!
#RUN apk add --update git
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
# Run it as if it were valgrind
#ENTRYPOINT ["valgrind"]
#CMD ["--help"]
