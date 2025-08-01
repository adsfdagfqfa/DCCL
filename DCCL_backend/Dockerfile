# FROM python:3.10-slim
FROM nvidia/cuda:11.8.0-devel-ubuntu22.04

# 安装 Python 3.10
RUN apt-get update && \
    apt-get install -y python3.10 python3-pip && \
    ln -s /usr/bin/python3.10 /usr/bin/python
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_ENV=production
CMD ["gunicorn", "run:app", "-c", "gunicorn.conf.py"]