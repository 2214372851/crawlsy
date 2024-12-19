# Crawlsy

Crawlsy 是一个分布式爬虫管理平台，支持多种爬虫框架，致力于提供一个简单、高效、稳定的爬虫管理系统。

## 1. 功能特性

### 1.1 节点管理
- [x] 分布式架构，支持多个爬虫节点
- [x] 节点自动发现，通过心跳机制同步状态
- [x] 节点健康检查，自动检测离线节点
- [x] 节点资源监控（CPU、内存等）
- [x] 节点唯一标识（UUID）
- [x] 节点状态实时同步

### 1.2 用户系统
- [x] 基于 JWT 的双令牌认证机制
- [x] 访问令牌自动刷新
- [x] 用户管理
- [x] 角色管理
- [x] 权限管理
- [x] 操作日志记录
- [x] 飞书账号关联

### 1.3 爬虫管理
- [x] 在线 IDE，支持在线编辑爬虫代码
- [x] 文件管理（创建、编辑、删除、重命名）
- [x] 文件上传下载
- [x] 文本文件在线编辑
- [x] 项目文件大小限制
- [x] 任务调度（通过 Celery）
- [x] 定时任务（通过 Celery Beat）
- [x] 任务监控（通过 Celery）
- [x] 任务日志（通过 Celery）

### 1.4 系统监控
- [x] 系统状态监控
- [x] 节点状态监控
- [x] 任务状态监控
- [x] 飞书 WebHook 通知

### 1.5 告警系统
- [x] 告警规则管理
- [x] 多指标监控（CPU、内存、带宽、负载等）
- [x] 告警级别（严重、警告、提示）
- [x] 告警对象管理
- [x] 告警记录追踪
- [x] 飞书消息通知
- [x] 自定义告警间隔
- [x] WebHook 支持

## 2. 快速开始

### 2.1 环境要求
- Python 3.12+
- Redis
- MySQL
- MongoDB

### 2.2 使用 Docker Compose 部署

1. 克隆项目
```bash
git clone https://github.com/your-username/crawlsy.git
cd crawlsy
```


3. 启动服务

> 注意：
> 1. 此方式会创建 Redis、MySQL、MongoDB 容器来运行，请确保你有足够的磁盘空间来存储数据

```bash
docker-compose up -d
```

### 2.3 使用 Docker 部署


在命令行中执行以下命令：


```bash
docker run -d \
  -p 8001:8001 \
  -v ./log:/app/log \
  -v spider_data:/data \
  -e SECRET_KEY='your-secret-key' \
  -e TOKEN_ISS='SpiderStudio-ISS@2024' \
  -e CELERY_BROKER_URL='redis://redis:6379/4' \
  -e CELERY_RESULT_BACKEND='redis://redis:6379/4' \
  -e MYSQL_DB_HOST='mysql' \
  -e MYSQL_DB_PORT='3306' \
  -e MYSQL_DB_NAME='SpiderManage' \
  -e MYSQL_DB_USER='SpiderManage' \
  -e MYSQL_DB_PASSWORD='your-password' \
  -e DEFAULT_REDIS_URL='redis://redis:6379/0' \
  -e ACCESS_TOKEN_REDIS_URL='redis://redis:6379/1' \
  -e REFRESH_TOKEN_REDIS_URL='redis://redis:6379/2' \
  -e NODE_SERVICE_URL='redis://redis:6379/3' \
  -e MONGO_URL='mongodb://mongoroot:password@mongo:27017/' \
  -e MONGO_DB='SpiderManage' \
  crawlsy/crawlsy:latest
```

当然你也可以使用 env 文件来配置环境变量，详见 [环境变量说明](#环境变量说明)
```bash
docker run -d \
  -p 8001:8001 \
  -v your_log_dir:/app/log \
  -v your_data_dir:/data \
  --env-file .env \
  crawlsy/crawlsy:latest
```

以下是 .env 文件的示例，请根据实际情况进行配置

```env
# Django 核心配置
SECRET_KEY=your-secret-key
TOKEN_ISS=SpiderStudio-ISS@2024
DEBUG=false

# Celery 配置
CELERY_BROKER_URL=redis://redis:6379/4
CELERY_RESULT_BACKEND=redis://redis:6379/4
CELERY_WORKER_CONCURRENCY=1
CELERY_WORKER_MAX_TASKS_PER_CHILD=50

# MySQL 配置
MYSQL_DB_HOST=mysql
MYSQL_DB_PORT=3306
MYSQL_DB_NAME=SpiderManage
MYSQL_DB_USER=SpiderManage
MYSQL_DB_PASSWORD=your-password

# Redis 配置
DEFAULT_REDIS_URL=redis://redis:6379/0
ACCESS_TOKEN_REDIS_URL=redis://redis:6379/1
REFRESH_TOKEN_REDIS_URL=redis://redis:6379/2
NODE_SERVICE_URL=redis://redis:6379/3

# MongoDB 配置
MONGO_URL=mongodb://mongoroot:password@mongo:27017/
MONGO_DB=SpiderManage

# 飞书配置（可选）
FEISHU_APP_ID=your-app-id
FEISHU_APP_SECRET=your-app-secret
FEISHU_CARD_ID=your-card-id
FEISHU_CARD_VERSION=0.0.7

# JWT 配置
REFRESH_TOKEN_OUT_TIME=86400
ACCESS_TOKEN_OUT_TIME=60

# IDE 配置
IDE_MAX_FILE_SIZE=10485760
PAGE_SIZE=10

# CORS 配置
CORS_ORIGIN_ALLOW_ALL=true
CORS_ALLOW_METHODS=*
CORS_ALLOW_CREDENTIALS=true
CORS_ALLOW_HEADERS=*
```

## 3. 架构设计

### 3.1 节点发现机制
节点管理通过子节点心跳同步数据实现 master 节点对集群中子节点的发现。节点之间通过唯一 ID 进行识别，
并且由于没有直接通讯不会暴露 IP，提高了集群安全性。

- 子节点启动时自动生成节点 ID
- 每 50 秒向 Redis 发送一次状态同步
- 状态数据过期时间为 60 秒
- master 节点通过 Redis 获取在线节点状态
- 超过 60 秒未同步的节点视为离线

### 3.2 认证机制
采用双 Token 机制（访问令牌与刷新令牌）实现无感刷新：

- 登录时返回访问令牌和刷新令牌
- 访问令牌过期后使用刷新令牌获取新的访问令牌
- 注销时使两个令牌同时失效

## 4. 环境变量说明

### 4.1 Django 核心配置
| 环境变量 | 说明 | 默认值 | 必选 |
|---------|------|--------|------|
| SECRET_KEY | Django 密钥 | - | 是 |
| TOKEN_ISS | JWT 签发者 | SpiderStudio-ISS@2024 | 是 |
| DEBUG | 调试模式 | false | 否 |

### 4.2 Celery 配置
| 环境变量 | 说明 | 默认值 | 必选 |
|---------|------|--------|------|
| CELERY_BROKER_URL | Celery Broker URL | redis://redis:6379/4 | 是 |
| CELERY_RESULT_BACKEND | Celery 结果后端 | redis://redis:6379/4 | 是 |
| CELERY_WORKER_CONCURRENCY | Worker 并发数 | 1 | 否 |
| CELERY_WORKER_MAX_TASKS_PER_CHILD | 每个 Worker 最大任务数 | 50 | 否 |

### 4.3 MySQL 配置
| 环境变量 | 说明 | 默认值 | 必选 |
|---------|------|--------|------|
| MYSQL_DB_HOST | MySQL 主机 | mysql | 是 |
| MYSQL_DB_PORT | MySQL 端口 | 3306 | 是 |
| MYSQL_DB_NAME | MySQL 数据库名 | SpiderManage | 是 |
| MYSQL_DB_USER | MySQL 用户名 | SpiderManage | 是 |
| MYSQL_DB_PASSWORD | MySQL 密码 | - | 是 |

### 4.4 Redis 配置
| 环境变量 | 说明 | 默认值 | 必选 |
|---------|------|--------|------|
| DEFAULT_REDIS_URL | 默认 Redis 连接 | redis://redis:6379/0 | 是 |
| ACCESS_TOKEN_REDIS_URL | 访问令牌 Redis 连接 | redis://redis:6379/1 | 是 |
| REFRESH_TOKEN_REDIS_URL | 刷新令牌 Redis 连接 | redis://redis:6379/2 | 是 |
| NODE_SERVICE_URL | 节点服务 Redis 连接 | redis://redis:6379/3 | 是 |

### 4.5 MongoDB 配置
| 环境变量 | 说明 | 默认值 | 必选 |
|---------|------|--------|------|
| MONGO_URL | MongoDB 连接 URL | mongodb://mongoroot:password@mongo:27017/ | 是 |
| MONGO_DB | MongoDB 数据库名 | SpiderManage | 是 |

### 4.6 飞书配置
| 环境变量 | 说明 | 默认值 | 必选 |
|---------|------|--------|------|
| FEISHU_APP_ID | 飞书应用 ID | - | 否 |
| FEISHU_APP_SECRET | 飞书应用密钥 | - | 否 |
| FEISHU_CARD_ID | 飞书卡片 ID | - | 否 |
| FEISHU_CARD_VERSION | 飞书卡片版本 | 0.0.7 | 否 |

### 4.7 JWT 配置
| 环境变量 | 说明 | 默认值 | 必选 |
|---------|------|--------|------|
| REFRESH_TOKEN_OUT_TIME | 刷新令牌过期时间(秒) | 86400 | 否 |
| ACCESS_TOKEN_OUT_TIME | 访问令牌过期时间(秒) | 60 | 否 |

### 4.8 IDE 配置
| 环境变量 | 说明 | 默认值 | 必选 |
|---------|------|--------|------|
| IDE_MAX_FILE_SIZE | IDE 最大文件大小(字节) | 10485760 | 否 |
| PAGE_SIZE | 分页大小 | 10 | 否 |

### 4.9 CORS 配置
| 环境变量 | 说明 | 默认值 | 必选 |
|---------|------|--------|------|
| CORS_ORIGIN_ALLOW_ALL | 允许所有源 | true | 否 |
| CORS_ALLOW_METHODS | 允许的请求方法 | * | 否 |
| CORS_ALLOW_CREDENTIALS | 允许携带认证信息 | true | 否 |
| CORS_ALLOW_HEADERS | 允许的请求头 | * | 否 |

### 4.10 注意事项
1. 必选项在部署时必须配置，否则系统无法正常运行
2. 可选项使用默认值即可，根据需要调整
3. 生产环境建议关闭 DEBUG 模式，并合理配置 CORS 策略
4. 所有密码和密钥类的配置项建议使用强随机值
5. 飞书配置（请详见Crawlsy文档）

## 5. 贡献指南

欢迎提交 Issue 和 Pull Request。

## 6. 开源协议

[MIT License](LICENSE)
