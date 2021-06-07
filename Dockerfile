FROM alpine:3.7

MAINTAINER Vladislav Kraskov <vvkraskov@.edu.hse.ru>

# Update package manager
RUN apk update
RUN apk upgrade

# Has stuff like gcc, make, and libc6-dev
RUN apk add --update py3-pip
RUN apk add --update build-base
RUN apk add --update make
# Valgrind!
RUN apk add --update git
COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt
# Run it as if it were valgrind
#ENTRYPOINT ["valgrind"]
#CMD ["--help"]
