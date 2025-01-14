FROM python:3.12-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/log && \
    mkdir -p /etc/supervisor/conf.d && \
    mkdir -p /data/spider_project && \
    mkdir -p /data/spider_temp && \
    mkdir -p /app/log

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV TZ=Asia/Shanghai

RUN pip install poetry -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . /app/
RUN rm -f /app/.env

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN poetry install --no-root

EXPOSE 8001

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]