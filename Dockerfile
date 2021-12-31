# Using official python runtime base image
FROM python:3.10-alpine

RUN apk update \
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev

# Install our requirements.txt
COPY requirements.txt /requirements.txt
RUN pip3 --no-cache-dir install -r requirements.txt

# Set the application directory
ENV APP_ROOT '/app'
RUN mkdir -p $APP_ROOT

WORKDIR $APP_ROOT

# Copy our code from the current folder to /app inside the container
COPY . $APP_ROOT

EXPOSE 5000

ENTRYPOINT gunicorn \
        --access-logfile="-"                   \
        --error-logfile="-"                    \
        --bind=0.0.0.0:5000                    \
        --worker-class=sync                    \
        --workers=1                            \
        --keep-alive=10                        \
        --graceful-timeout=10                  \
        app:app

