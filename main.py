import logging
import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
from openai import OpenAI
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- 初始设置 ---

# 加载 .env 文件中的环境变量
load_dotenv()

# 设置日志记录
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 从环境变量获取密钥和配置
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

# 初始化 OpenAI 客户端
try:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
except Exception as e:
    logger.error(f"无法初始化 OpenAI 客户端: {e}")
    openai_client = None

# --- 数据库操作 ---

def get_db_connection():
    """创建并返回一个数据库连接"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        return conn
    except psycopg2.OperationalError as e:
        logger.error(f"数据库连接失败: {e}")
        return None

def log_to_db(user_id: int, user_message: str, bot_response: str):
    """将聊天记录写入数据库"""
    conn = get_db_connection()
    if conn is None:
        logger.error("无法记录到数据库，因为没有数据库连接。")
        return

    try:
        with conn.cursor() as cur:
            # SQL 查询语句
            query = sql.SQL("INSERT INTO chat_logs (user_id, user_message, bot_response) VALUES (%s, %s, %s)")
            cur.execute(query, (user_id, user_message, bot_response))
        conn.commit()
    except Exception as e:
        logger.error(f"写入数据库时出错: {e}")
        conn.rollback()
    finally:
        conn.close()

# --- OpenAI 交互 ---

def get_llm_response(prompt: str) -> str:
    """调用 OpenAI API 获取回复"""
    if not openai_client:
        logger.error("OpenAI 客户端未初始化，无法获取回复。")
        return "抱歉，我的大脑（AI模型）暂时无法连接，请稍后再试。"

    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"调用 OpenAI API 时出错: {e}")
        return "抱歉，我在思考时遇到了一个问题，请稍后再试。"

# --- Telegram 机器人处理器 ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /start 命令"""
    user = update.effective_user
    await update.message.reply_html(
        f"你好，{user.mention_html()}！\n\n我是一个集成了 OpenAI 的聊天机器人。你可以直接向我发送任何问题。我也会将我们的对话记录下来。",
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理用户的文本消息"""
    user_id = update.effective_user.id
    user_message = update.message.text
    logger.info(f"收到来自用户 {user_id} 的消息: {user_message}")

    # 1. 获取 OpenAI 的回复
    bot_response = get_llm_response(user_message)

    # 2. 将回复发送给用户
    await update.message.reply_text(bot_response)

    # 3. 将对话记录到数据库
    log_to_db(user_id, user_message, bot_response)

def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """记录由更新引起的错误"""
    logger.error("出现异常:", exc_info=context.error)

# --- 主函数 ---

def main():
    """启动机器人"""
    if not TELEGRAM_TOKEN:
        logger.critical("未找到 TELEGRAM_TOKEN，机器人无法启动！")
        return

    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # 添加命令和消息处理器
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # 添加错误处理器
    application.add_error_handler(error_handler)

    logger.info("机器人正在启动...")
    # 以轮询方式运行机器人
    application.run_polling()

if __name__ == '__main__':
    main()