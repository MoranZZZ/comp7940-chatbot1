# 🎓 COMP7940 CampusBot — HKBU 智能校园助手

一个基于 **Telegram + OpenAI GPT-3.5-turbo + PostgreSQL** 的智能校园聊天机器人，为 HKBU（香港浸会大学）学生提供课程咨询、校园生活指南和学习建议。

## ✨ 功能特性

| 功能 | 说明 |
|---|---|
| 🤖 AI 智能对话 | 接入 OpenAI GPT-3.5-turbo，智能回答学生问题 |
| 💾 对话日志持久化 | 所有聊天记录自动存入 PostgreSQL 数据库 |
| 📜 聊天历史查询 | `/history` 命令查看最近 5 条对话 |
| 📊 机器人统计 | `/stats` 查看运行时长、消息总数、用户数 |
| 🗑 记录清除 | `/clear` 一键清空个人聊天记录 |
| 🐳 Docker 一键部署 | `docker compose up` 即可启动全部服务 |
| ☁️ CI/CD 自动部署 | 推送到 `main` 分支自动部署至 AWS App Runner |

## 🏗 系统架构

```
Telegram 用户发送消息
        │
        ▼
  handle_message()          ← Telegram Bot (python-telegram-bot)
        │
        ▼
  get_llm_response()  ───►  OpenAI GPT-3.5-turbo API
        │
        ▼
  回复发送至 Telegram 用户
        │
        ▼
  log_to_db()  ───►  PostgreSQL (chat_logs 表)
```

## 🛠 技术栈

| 技术 | 用途 |
|---|---|
| Python 3.11 | 应用开发语言 |
| [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) v22.7 | Telegram Bot API 框架 |
| [OpenAI Python SDK](https://github.com/openai/openai-python) v2.30.0 | OpenAI API 客户端 |
| PostgreSQL 15 (psycopg2) | 聊天记录数据库 |
| Docker & Docker Compose | 容器化部署 |
| AWS App Runner + ECR | 云端部署（可选） |

---

## 🚀 快速开始（Fork 后只需 3 步！）

> **核心思路：Fork 本仓库后，你只需要创建并修改一个 `.env` 文件，然后用 Docker Compose 一键启动即可。**

### 📋 前置准备

在开始之前，请确保你已拥有以下内容：

1. **Telegram Bot Token**
   - 在 Telegram 中搜索 [@BotFather](https://t.me/BotFather)
   - 发送 `/newbot`，按提示设置 Bot 名称
   - 获得一个形如 `123456789:ABCdefGHI...` 的 Token

2. **OpenAI API Key**
   - 前往 [OpenAI API Keys](https://platform.openai.com/api-keys)
   - 创建一个新的 API Key（需要有余额/绑定付费方式）

3. **Docker & Docker Compose**
   - 安装 [Docker Desktop](https://www.docker.com/products/docker-desktop/)（已自带 Docker Compose）

---

### ✅ 第一步：Fork 并克隆仓库

```bash
# 1. 在 GitHub 上点击右上角 "Fork" 按钮，将仓库复制到你的账号下

# 2. 克隆你 Fork 的仓库到本地
git clone https://github.com/<你的用户名>/comp7940-chatbot.git
cd comp7940-chatbot
```

### ✅ 第二步：创建并配置 `.env` 文件

```bash
# 复制环境变量模板
cp .env.example .env
```

用任意文本编辑器打开 `.env` 文件，填入你自己的密钥：

```dotenv
# ===== 🔑 你只需要修改以下两项 =====

# Telegram Bot Token（从 @BotFather 获取）
TELEGRAM_TOKEN=在这里粘贴你的Telegram-Bot-Token

# OpenAI API Key（从 OpenAI 平台获���）
OPENAI_API_KEY=在这里粘贴你的OpenAI-API-Key

# ===== 🗄 数据库配置（使用 Docker Compose 部署则无需修改以下内容）=====

DB_HOST=db
DB_NAME=chatbot_db
DB_USER=chatbot_user
DB_PASSWORD=changeme
DB_PORT=5432
```

> ⚠️ **重要提示：**
> - 如果你使用 Docker Compose 部署（推荐），数据库配置保持默认即可，**只需填写 `TELEGRAM_TOKEN` 和 `OPENAI_API_KEY` 两项**。
> - `.env` 文件已被 `.gitignore` 忽略，**你的密钥不会被意外提交到 GitHub**。

### ✅ 第三步：一键启动

```bash
docker compose up --build
```

等待构建完成后，你会看到类似以下日志：

```
chatbot-1  | 2026-04-08 12:00:00 - __main__ - INFO - 机器人正在启动...
```

🎉 **大功告成！** 现在打开 Telegram，搜索你的 Bot，发送 `/start` 即可开始对话！

---

## 📝 Bot 命令一览

| 命令 | 功能 |
|---|---|
| `/start` | 显示欢迎消息 |
| `/help` | 显示所有可用命令 |
| `/history` | 查看你最近的 5 条聊天记录 |
| `/stats` | 查看机器人统计信息（运行时长、消息数、用户数） |
| `/clear` | 清除你的所有聊天记录 |
| *(直接发送文字)* | AI 校园助手即时回答你的问题 |

---

## 📂 项目结构

```
comp7940-chatbot/
├── main.py                 # 主程序（Bot 逻辑、OpenAI 调用、数据库操作）
├── requirements.txt        # Python 依赖包列表
├── Dockerfile              # Docker 镜像构建文件
├── docker-compose.yml      # Docker Compose 编排文件（Bot + PostgreSQL）
├── init.sql                # 数据库初始化脚本（自动创建 chat_logs 表）
├── .env.example            # 环境变量模板 ← 复制为 .env 后填入你的密钥
├── .gitignore              # Git 忽略规则（已忽略 .env）
└── .github/
    └── workflows/
        └── main.yml        # CI/CD 流水线（自动部署到 AWS）
```

---

## 🖥 不使用 Docker 的本地运行方式（可选）

如果你不想使用 Docker，也可以手动运行：

```bash
# 1. 创建虚拟环境
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 确保你有一个运行中的 PostgreSQL 数据库，并执行 init.sql 初始化表
psql -h <数据库地址> -U <用户名> -d <数据库名> -f init.sql

# 4. 配置 .env 文件（将 DB_HOST 改为你的数据库实际地址）

# 5. 运行机器人
python main.py
```

---

## ☁️ AWS 云端部署（可选）

本项目包含 GitHub Actions CI/CD 流水线，推送到 `main` 分支时会自动：

1. 构建 Docker 镜像
2. 推送至 Amazon ECR
3. 部署至 AWS App Runner

需要在 GitHub 仓库的 **Settings → Secrets and variables → Actions** 中配置以下 Secrets：

| Secret 名称 | 说明 |
|---|---|
| `AWS_ACCESS_KEY_ID` | AWS 访问密钥 ID |
| `AWS_SECRET_ACCESS_KEY` | AWS 访问密钥 |
| `AWS_REGION` | AWS 区域（如 `ap-east-1`） |
| `AWS_ECR_REPOSITORY` | ECR 仓库名称 |
| `AWS_APP_RUNNER_SERVICE_ARN` | App Runner 服务 ARN |

---

## 🗄 数据库表结构

`init.sql` 会在 PostgreSQL 启动时自动创建以下表：

```sql
CREATE TABLE IF NOT EXISTS chat_logs (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    user_message TEXT NOT NULL,
    bot_response TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## ❓ 常见问题

<details>
<summary><b>Q: 启动后 Bot 没有响应怎么办？</b></summary>

- 检查 `.env` 中的 `TELEGRAM_TOKEN` 是否正确
- 确保没有其他程序在使用同一个 Bot Token
- 查看 Docker 日志：`docker compose logs chatbot`
</details>

<details>
<summary><b>Q: 提示 OpenAI API 错误？</b></summary>

- 确认 `OPENAI_API_KEY` 有效且账户有余额
- 检查网络是否能访问 OpenAI API
</details>

<details>
<summary><b>Q: 数据库连接失败？</b></summary>

- 如使用 Docker Compose，确保 `DB_HOST=db`（不要改为 `localhost`）
- 检查 PostgreSQL 容器是否正常运行：`docker compose ps`
</details>

<details>
<summary><b>Q: 如何停止机器人？</b></summary>

```bash
docker compose down        # 停止并移除容器
docker compose down -v     # 停止并移除容器和数据卷（会清空数据库）
```
</details>

---

## 📄 License

本项目为 COMP7940 课程教学项目，仅供学习使用。
