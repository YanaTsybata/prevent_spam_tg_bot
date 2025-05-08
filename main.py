from typing import Final
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, filters, MessageHandler

TOKEN: Final = 'YourToken'
BOT_USERNAME: Final = '@YourBotName'
DELETE_DELAY: Final = 10  # Seconds to wait before deleting messages

# Dictionary to store message history for each chat
message_history = {}


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Thanks for chatting with me! I will help you clean your chat")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I am Spam bot. Please type something so I can respond")


# Responses
def handle_response(text: str) -> str:
    processed: str = text.lower()
    if 'hello' in processed:
        return 'Hey there!'
    if 'how are you' in processed:
        return 'I am good!'
    return 'I do not understand what you wrote'


# Auto-delete messages after delay
async def delete_after_delay(message, delay_seconds):
    await asyncio.sleep(delay_seconds)
    try:
        await message.delete()
    except Exception as e:
        print(f"Error deleting message: {e}")


# Check for spam URLs
async def link_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.message.text is None:
        return False

    message_type = update.message.chat.type
    text = update.message.text

    # Only check for links in group and supergroup chats
    if ('http://' in text or 'https://' in text) and message_type in ['group', 'supergroup']:
        warning_msg = await update.message.reply_text('The message is deleted as spam')
        # Schedule the warning message for deletion after delay
        asyncio.create_task(delete_after_delay(warning_msg, DELETE_DELAY))
        await update.message.delete()
        return True  # Indicate that spam was detected and handled

    return False  # No spam detected


# Check for repeated messages spam
async def message_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.message.text is None:
        return False

    chat_id = update.message.chat.id
    text = update.message.text
    message_type = update.message.chat.type

    if message_type not in ['group', 'supergroup']:
        return False

    if chat_id not in message_history:
        message_history[chat_id] = []

    # Append (text, message) to the history
    message_history[chat_id].append((text, update.message))

    # Check for repeated messages
    if len(message_history[chat_id]) >= 3:
        last_three = message_history[chat_id][-3:]
        if last_three[0][0] == last_three[1][0] == last_three[2][0]:
            warning_msg = await update.message.reply_text('The repeated messages are deleted as spam')
            asyncio.create_task(delete_after_delay(warning_msg, DELETE_DELAY))

            # Delete all three repeated messages
            for _, msg_obj in last_three:
                try:
                    await msg_obj.delete()
                except Exception as e:
                    print(f"Error deleting repeated message: {e}")
            return True

    # Keep only the last 10 messages in history
    if len(message_history[chat_id]) > 10:
        message_history[chat_id] = message_history[chat_id][-10:]

    return False



# Handle stickers
async def sticker_del(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.message.sticker is None:
        return False

    message_type = update.message.chat.type

    # Only delete stickers in group and supergroup chats
    if message_type in ['group', 'supergroup']:
        warning_msg = await update.message.reply_text('Sticker deleted')
        # Schedule the warning message for deletion after delay
        asyncio.create_task(delete_after_delay(warning_msg, DELETE_DELAY))
        await update.message.delete()
        return True  # Indicate that sticker was detected and handled

    return False


# Handler for sticker messages
async def handle_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await sticker_del(update, context)


# Main message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return

    # First check for spam links
    is_spam = await link_spam(update, context)
    if is_spam:
        return  # Skip further processing if spam was detected

    # Then check for repeated message spam
    is_repeat_spam = await message_spam(update, context)
    if is_repeat_spam:
        return  # Skip further processing if repeat spam was detected

    message_type: str = update.message.chat.type
    text: str = update.message.text if update.message.text else ""

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    # Handle group and supergroup messages
    if message_type in ['group', 'supergroup']:
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
            bot_msg = await update.message.reply_text(response)
            print(f'Bot response: {response}')
        else:
            return
    else:
        # Handle private messages
        response: str = handle_response(text)
        bot_msg = await update.message.reply_text(response)
        print(f'Bot response: {response}')


# Function to delete service messages
async def delete_service_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.delete()
        print("Service message deleted")
    except Exception as e:
        print(f"Error deleting message: {e}")


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))

    # Add service message handler
    app.add_handler(MessageHandler(
        filters.StatusUpdate.NEW_CHAT_MEMBERS | filters.StatusUpdate.LEFT_CHAT_MEMBER,
        delete_service_messages
    ))

    # Add sticker handler
    app.add_handler(MessageHandler(filters.Sticker.ALL, handle_sticker))

    # Add text message handler - only one handler for all text messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Add error handler
    app.add_error_handler(error)

    # Start polling
    print('Polling...')
    app.run_polling(poll_interval=3)