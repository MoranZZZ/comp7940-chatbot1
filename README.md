# COMP7940 CampusBot

A smart campus chatbot built with Telegram, HKBU GenAI API, and PostgreSQL for COMP7940 at Hong Kong Baptist University (HKBU). It provides course advice, campus life tips, and study guidance to students.

## Features

- AI-powered conversation using HKBU GenAI API (GPT-4o-mini)
- Chat log persistence with PostgreSQL
- Chat history retrieval, bot statistics, and record clearing via bot commands
- Containerized deployment with Docker
- Optional CI/CD pipeline for automatic deployment to AWS App Runner

## Tech Stack

- Python 3.11
- python-telegram-bot v22.7
- HKBU GenAI REST API (via requests)
- PostgreSQL (psycopg2, with AWS RDS support)
- Docker and Docker Compose
- AWS App Runner + ECR (optional)

## Quick Start

1. Fork and clone this repository.
2. Copy `.env.example` to `.env` and fill in the required values:
   - `TELEGRAM_TOKEN` — your Telegram bot token from @BotFather
   - `HKBU_API_KEY` — your API key from the HKBU GenAI platform (https://genai.hkbu.edu.hk)
   - Database connection details (`DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_PORT`)
3. Run `docker compose up --build` to start the bot.

Open Telegram, find your bot, and send `/start` to begin chatting.

## Environment Variables

| Variable | Description |
|---|---|
| `TELEGRAM_TOKEN` | Telegram bot token from @BotFather |
| `HKBU_API_KEY` | API key from HKBU GenAI platform |
| `HKBU_BASE_URL` | GenAI API base URL (default: `https://genai.hkbu.edu.hk/general/rest`) |
| `HKBU_MODEL_NAME` | Model name (default: `gpt-4-o-mini`) |
| `HKBU_API_VERSION` | API version (default: `2024-05-01-preview`) |
| `DB_HOST` | PostgreSQL host address |
| `DB_NAME` | Database name |
| `DB_USER` | Database username |
| `DB_PASSWORD` | Database password |
| `DB_PORT` | Database port (default: `5432`) |

## Bot Commands

- `/start` — Welcome message
- `/help` — List all available commands
- `/history` — View your last 5 chat records
- `/stats` — View bot statistics (uptime, total messages, user count)
- `/clear` — Clear your chat history
- Send any text message to get an AI-powered response

## Project Structure

- `main.py` — Main application (bot logic, HKBU GenAI API calls, database operations)
- `requirements.txt` — Python dependencies
- `Dockerfile` — Docker image build file
- `docker-compose.yml` — Docker Compose orchestration
- `init.sql` — Database initialization script (creates the chat_logs table)
- `.env.example` — Environment variable template
- `.github/workflows/main.yml` — CI/CD pipeline for AWS deployment

## Running Without Docker (Optional)

1. Create and activate a Python virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Set up a PostgreSQL database and run `init.sql` to initialize the table.
4. Configure your `.env` file with all required variables.
5. Run `python main.py`.

## AWS Deployment (Optional)

The included GitHub Actions workflow automatically builds a Docker image, pushes it to Amazon ECR, and deploys to AWS App Runner on every push to the `main` branch. Configure the following secrets in your repository settings: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`, `AWS_ECR_REPOSITORY`, and `AWS_APP_RUNNER_SERVICE_ARN`.

## License

This is a course project for COMP7940. For educational use only.
