# COMP7940 Chatbot

A Telegram chatbot powered by OpenAI GPT-3.5-turbo with PostgreSQL conversation logging. Built for the COMP7940 course.

## Features

- **AI-Powered Conversations** — Responds to user messages using OpenAI's GPT-3.5-turbo model.
- **Chat Logging** — Stores all conversations (user ID, message, and bot response) in a PostgreSQL database.
- **Telegram Integration** — Runs as a Telegram bot using long-polling.
- **Containerized Deployment** — Dockerized for deployment on AWS App Runner.

## Architecture

```
User sends message on Telegram
        │
        ▼
  handle_message()
        │
        ▼
  get_llm_response()  ──►  OpenAI GPT-3.5-turbo API
        │
        ▼
  Reply sent to user on Telegram
        │
        ▼
  log_to_db()  ──►  PostgreSQL (chat_logs table)
```

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application language |
| [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) (v22.7) | Telegram Bot API framework |
| [OpenAI Python SDK](https://github.com/openai/openai-python) (v2.30.0) | OpenAI API client |
| PostgreSQL (via psycopg2) | Chat history database |
| Docker | Containerization |
| AWS App Runner + ECR | Cloud deployment |

## Prerequisites

- Python 3.10+
- A [Telegram Bot Token](https://core.telegram.org/bots#how-do-i-create-a-bot) (from BotFather)
- An [OpenAI API key](https://platform.openai.com/api-keys)
- A PostgreSQL database with a `chat_logs` table

### Database Setup

Create the `chat_logs` table in your PostgreSQL database:

```sql
CREATE TABLE chat_logs (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    user_message TEXT NOT NULL,
    bot_response TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Iamspeed66666/comp7940-chatbot.git
cd comp7940-chatbot
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install psycopg2-binary
```

> **Note:** `psycopg2-binary` must be installed separately as it is not included in `requirements.txt`.

### 3. Configure environment variables

Copy the example file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with the following values:

```
TELEGRAM_TOKEN=your-telegram-bot-token
OPENAI_API_KEY=your-openai-api-key
DB_HOST=your-database-host
DB_NAME=your-database-name
DB_USER=your-database-user
DB_PASSWORD=your-database-password
DB_PORT=5432
```

### 4. Run the bot

```bash
python main.py
```

The bot will start polling for messages. Open your bot in Telegram and send `/start` to begin.

## Bot Commands

| Command | Description |
|---|---|
| `/start` | Displays a welcome message |
| *(any text)* | Sends the message to OpenAI and replies with the AI-generated response |

## Deployment

The project includes a GitHub Actions workflow (`.github/workflows/main.yml`) that automatically deploys on every push to `main`:

1. Builds a Docker image
2. Pushes it to Amazon ECR
3. Deploys to AWS App Runner

Required GitHub Secrets for deployment:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`
- `AWS_ECR_REPOSITORY`
- `AWS_APP_RUNNER_SERVICE_ARN`

## Project Structure

```
├── main.py                 # Application entry point (bot logic, OpenAI, DB)
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container image definition
├── .env.example            # Environment variable template
├── .gitignore              # Git ignore rules
└── .github/
    └── workflows/
        └── main.yml        # CI/CD pipeline for AWS deployment
```

## License

This project is for educational purposes as part of the COMP7940 course.

Repository: comp7940-chatbot
This is a Telegram chatbot built for COMP7940 (a university course) that integrates OpenAI's GPT-3.5-turbo for AI-powered conversations and PostgreSQL for logging chat history. It's designed to be deployed on AWS App Runner via Docker.

Codebase Structure
File/Directory	Purpose
main.py	The entire application — a single-file Python bot
requirements.txt	Pinned Python dependencies
Dockerfile	Container image definition for deployment
.env.example	Template for required environment variables
.gitignore	Ignores Python caches, virtual envs, .env, and IDE files
.github/workflows/main.yml	CI/CD pipeline for deploying to AWS
git	An empty file (likely accidental)
Key Technologies
Python — The sole programming language.
python-telegram-bot (v22.7) — Async Telegram Bot API framework used for receiving and sending messages.
OpenAI Python SDK (v2.30.0) — Client library to call OpenAI's gpt-3.5-turbo chat completion API.
PostgreSQL (via psycopg2) — Relational database used to log all conversations (user messages + bot responses).
python-dotenv — Loads environment variables from a .env file.
Docker — The app is containerized for deployment.
AWS App Runner + ECR — The CI/CD pipeline builds a Docker image, pushes it to Amazon ECR, and deploys it to AWS App Runner.
How main.py is Organized
The file follows a clean top-down structure with four logical sections (annotated in Chinese comments):

Initialization (lines 1–36)

Loads environment variables (TELEGRAM_TOKEN, OPENAI_API_KEY, DB credentials).
Configures logging.
Initializes the OpenAI client.
Database Operations (lines 38–72)

get_db_connection() — Creates a PostgreSQL connection using psycopg2.
log_to_db() — Inserts a row into a chat_logs table with the user ID, their message, and the bot's response.
OpenAI Interaction (lines 74–93)

get_llm_response(prompt) — Sends the user's message to the gpt-3.5-turbo model with a system prompt ("You are a helpful assistant") and returns the AI's reply.
Telegram Bot Handlers (lines 95–145)

/start command handler — Greets the user with an HTML-formatted welcome message.
handle_message() — The main message handler: takes user text → calls OpenAI → replies to user → logs to database.
error_handler() — Logs any unhandled exceptions.
main() — Builds the Telegram Application, registers handlers, and starts long-polling (the bot continuously polls Telegram's servers for new messages).
Message Flow
Code
User sends message on Telegram
        ↓
handle_message() receives it
        ↓
get_llm_response() calls OpenAI GPT-3.5-turbo
        ↓
Bot replies to the user on Telegram
        ↓
log_to_db() saves (user_id, message, response) to PostgreSQL
Deployment Pipeline (.github/workflows/main.yml)
On every push to main:

Checks out the code
Configures AWS credentials (from GitHub Secrets)
Logs into Amazon ECR
Builds & pushes the Docker image (tagged with the commit SHA)
Deploys the new image to AWS App Runner
Notable Observations
Single-file app: Everything lives in main.py — no modules, no separation of concerns beyond functions. This is typical for a course project.
No tests: There are no test files or testing frameworks.
No psycopg2 in requirements.txt: The code imports psycopg2, but it's not listed in requirements.txt. This would cause a runtime error unless psycopg2 (or psycopg2-binary) is installed via the Dockerfile or another mechanism. (The Dockerfile appears empty/unreadable, so this may be an issue.)
Comments are in Chinese: All inline comments and docstrings are written in Chinese, indicating the developer's primary language.
The git file at the repo root appears to be an empty/accidental file — it has no content.
