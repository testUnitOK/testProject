FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
        nginx \
        python3 \
        python3-pip \
        postgresql \
        libpq-dev \
        git && \
    rm -rf /var/lib/apt/lists/*

COPY app.py .
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY requirements.txt .

RUN rm -f /etc/nginx/sites-enabled/default

RUN pip3 install --break-system-packages --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["bash", "-c", "service nginx start && gunicorn --bind 0.0.0.0:8000 app:app"]
#CMD ["bash", "-c", "service nginx start && tail -f /dev/null"]
