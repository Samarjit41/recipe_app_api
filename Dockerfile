#The base image that we're going to pull from Docker Hub that we're going to build 
#on top of to add the dependencies that we need for our project.
FROM python:3.9-alpine3.13 
#Next we define the maintainer
LABEL maintainer="samarjit.common@gmail.com"
#- PYTHONUNBUFFERED=1 ensures Django’s runserver logs 
#and Celery worker logs stream directly to your console.
# it tells Python that you don't want to buffer the output.
#The output from Python will be printed directly to the console, 
#which prevents any delays of messages
#getting from our Python running application to the screen 
#so we can see the logs immediately in the screen as they're running.
ENV PYTHONUNBUFFERED=1

#this block will copy our requirements on text file from our local machine to 
#/tmp/requirements.txt And this copies the requirements file that we added earlier
# into the Docker image.We can then use not to install the Python requirements in a moment.
#Then what we do is we copy the app directory, which we're going to create in a moment,
# and that's the directory that's going to contain our Django app and we copy it to 
#/app inside the container
#next we setup the working directory and it's the default directory that will commands are going
#to be run from when we run commands on our Docker image.
#And basically we're setting it to the location where our Django project is going to 
#be sent to so that when we run the commands, we don't need to specify the full path of the 
#Django Management Command.It will automatically be running from before slash app directory.
#next we setup the port And what this does is it allows us to access that port on the container 
#that's running from our image.And this way we can connect to the Django Development Server.
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
#Next, we're going to add a run command that is going to install some dependencies on our machine.
#we run this command on the alpine image that we are using when we're building our image.
#So we've broken the commands down onto one run block, so you could technically specify run, 
#and then each one of these lines individually have a what happens in that case is it creates 
#a new image layer for every single command that we run, and we want to avoid doing that to keep 
#our images lightweight
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \ 
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user
ENV PATH="/py/bin:$PATH"

USER django-user

