FROM python:3.11.0-alpine
# set work directory
WORKDIR /usr/src/app
# set environment variabs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev
RUN apk add --update make
RUN pip install --upgrade pip
RUN pip install pip-tools
COPY ./requirements.in .
COPY ./requirements-dev.in .
COPY ./Makefile .
RUN make compile
RUN make sync

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# copy project
COPY . .

# add and run as non-root user
RUN adduser -D myuser
USER myuser

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
