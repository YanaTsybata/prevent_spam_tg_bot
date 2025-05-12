# prevent_spam_tg_bot

# Telegram Spam Detection Bot

A simple yet powerful Telegram bot designed to keep your group chats clean by automatically detecting and removing different types of spam.

## Features

- **Link Spam Detection**: Automatically removes messages containing links/URLs
- **Sticker Removal**: Removes stickers posted in group chats
- **Repeated Message Detection**: Identifies and removes messages that have been sent 3 times in a row
- **Service Message Cleanup**: Automatically deletes join/leave notifications
- **Simple Response System**: Responds to basic commands and mentions


## Requirements

- Python 3.7+
- python-telegram-bot library (v13.0+)

## Installation

1. Clone this repository or download the code:
   ```
   git clone https://github.com/yourusername/telegram-spam-bot.git
   ```

2. Install the required dependencies:
   ```
   pip install python-telegram-bot
   ```

3. Update the bot token in the code:
   - Open `main.py`
   - Replace the `TOKEN` value with your bot token from @BotFather
   - Replace `BOT_USERNAME` with your bot's username

## Running the Bot

1. Navigate to the project directory:
   ```
   cd telegram-spam-bot
   ```

2. Run the bot:
   ```
   python main.py
   ```

3. You should see "Starting bot..." and "Polling..." in the console if everything is working correctly.

## Bot Setup in Telegram

1. Add the bot to your group
2. Make the bot an administrator with at least these permissions:
   - Delete messages
   - Read messages

## Usage

### Commands

- `/start` - Introduces the bot
- `/help` - Shows help information

### Spam Detection

The bot automatically checks for and removes:
- Messages with links (in groups/supergroups)
- Stickers (in groups/supergroups)
- Messages repeated 3 times in a row (in groups/supergroups)
- Join/leave notifications (service messages)

### Bot Responses

- The bot responds to direct mentions using its username
- In private chats, the bot responds to all messages

## Customization

You can customize the bot by modifying these parameters in the code:

- `DELETE_DELAY`: Time in seconds before deletion notification messages are removed (default: 10)
- Response messages: Edit the `handle_response` function to customize bot replies
- Warning messages: Change the text for notification messages when spam is detected

## Troubleshooting

- Make sure the bot has admin privileges in the group
- Check console output for error messages
- Ensure the bot is running (you should see "Polling..." in the console)


---

*Note: This bot is designed for educational purposes. Always respect Telegram's Terms of Service when deploying bots.*
