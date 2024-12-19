#!/bin/bash

check_env_vars() {
    local required_vars=(
        "MYSQL_DB_HOST"
        "MYSQL_DB_PORT"
        "MYSQL_DB_NAME"
        "MYSQL_DB_USER"
        "MYSQL_DB_PASSWORD"
        "CELERY_BROKER_URL"
        "CELERY_RESULT_BACKEND"
        "DEFAULT_REDIS_URL"
        "ACCESS_TOKEN_REDIS_URL"
        "REFRESH_TOKEN_REDIS_URL"
        "NODE_SERVICE_URL"
        "MONGO_URL"
        "MONGO_DB"
    )

    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            echo "Error: $var is not set"
            exit 1
        fi
    done
}

# 运行检查
check_env_vars

# 启动 Daphne
echo "Starting Django ASGI server..."
exec daphne \
    -b 0.0.0.0 \
    -p 8000 \
    crawlsy.asgi:application