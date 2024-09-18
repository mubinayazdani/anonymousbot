import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = 'token'
YOUR_CHAT_ID = 'chatid'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('welcome to my bot')


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_chat_id = update.message.chat.id  # Get the user's chat ID
    user_message = update.message.text  # Get the message text
    logger.info(f"Received message from User ID {user_chat_id}: {user_message}")  # Log received message

    # Send the message to your chat along with the user ID
    await context.bot.send_message(
        chat_id=YOUR_CHAT_ID,
        text=f"Message from User ID {user_chat_id}:\n{user_message}"
    )
    # Notify the user of successful sending
    await update.message.reply_text('your message has been sent')


async def reply_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /reply <user_id> <your_message>")
        return

    try:
        original_user_chat_id = int(context.args[0])  # Expect the first argument to be the user chat ID
        reply_message = ' '.join(context.args[1:])  # Join the rest of the arguments as the reply message

        logger.info(f"Replying to User ID {original_user_chat_id} with message: {reply_message}")

        # Send the reply to the original user
        await context.bot.send_message(chat_id=original_user_chat_id, text=reply_message)

        # Notify the sender that the reply has been sent
        await update.message.reply_text('Your reply has been sent!')
    except ValueError:
        await update.message.reply_text("Invalid user ID. Please provide a valid number.")
    except Exception as e:
        logger.error(f"Error sending reply: {str(e)}")
        await update.message.reply_text("Failed to send your reply. Please try again.")


def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()  # Use the correct token

    # Handlers for commands and messages
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(CommandHandler("reply", reply_command))

    # Start the bot
    application.run_polling()


if __name__ == '__main__':
    main()