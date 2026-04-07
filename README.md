
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
