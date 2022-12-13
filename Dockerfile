FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# Author:
#  - Name: Aaron Kaplan
#  - Email: kaplan@deep-insights.ai

# Open container image
LABEL "org.opencontainers.image.created"="2022-12-T19:00:00Z0"
LABEL "org.opencontainers.image.authors"="aaron@lo-res.org"
LABEL "org.opencontainers.image.url"="https://github.com/aaronkaplan/simple-stable-diffusion-ui"
LABEL "org.opencontainers.image.documentation URL"="https://github.com/aaronkaplan/simple-stable-diffusion-ui"
LABEL "org.opencontainers.image.version"="0.1"
LABEL "org.opencontainers.image.vendor"="deepinsights.ai"
LABEL "org.opencontainers.image.licenses"="proprietory"
LABEL "org.opencontainers.image.title"="Simple stupid Stable Diffusion UI"
LABEL "org.opencontainers.image.description"="An extremely simple and stupid UI for running Stable Diffusion locally"
LABEL "org.opencontainers.image.base.digest"="tiangolo/uvicorn-gunicorn-fastapi:python3.8"

COPY app /app
WORKDIR /app

# Base OS libs
RUN apt update -y && apt upgrade -y 

# Do the pip stuff
COPY ./requirements.txt /
RUN pip install --upgrade pip
RUN pip install -r  /requirements.txt


#RUN pip install --no-cache-dir "uvicorn[standard]" gunicorn
#RUN pip install --no-cache-dir fastapi
#RUN pip install pydicom python-multipart


COPY app/start.sh /start.sh
RUN chmod +x /start.sh
# 
# COPY ./app/gunicorn_conf.py /gunicorn_conf.py

COPY app/start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh


ENV PYTHONPATH=/app
ENV ROOT_PATH=/
ENV PORT=8000
ENV UPLOAD_PATH=/tmp
ENV WORKERS_PER_CORE=2
ENV LOG_LEVEL=info


EXPOSE 8000

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn
CMD ["/start.sh"]

