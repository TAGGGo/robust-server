FROM python:3.9-bullseye
ENV PYTHONUNBUFFERED=1
WORKDIR /code/web
RUN sed /etc/apt/sources.list && \
    apt-get update && apt-get install -y \
    sudo \
    bash \
    curl \
    python3-dev\ 
    ca-certificates \
    gnupg\
    libpq-dev \
    && curl https://www.postgresql.org/media/keys/ACCC4CF8.asc \
        | gpg --dearmor \
        | sudo tee /etc/apt/trusted.gpg.d/apt.postgresql.org.gpg >/dev/null \
    && sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ bullseye-pgdg main" \
> /etc/apt/sources.list.d/postgresql.list' \
    && sudo apt-get update -y \
    && sudo apt-get upgrade -y \
    && sudo apt install postgresql-14 -y \
    && rm -rf /tmp/*


COPY requirements.txt /code/web
RUN pip install pip -U && \
    pip install -r requirements.txt
COPY . /code/web

ENTRYPOINT ["/code/web/entrypoint-initenv.sh"]
