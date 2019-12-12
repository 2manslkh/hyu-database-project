#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# VERSION 0
# =============================================================================
"""Official Hostel Hunt Bot.

This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram.error import TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError
# import read_write_to_firebase as pb
import logging
import time
import random
import re
import connector as sqlc

from saved_strings import MSG_1, VALID_CLAIM, INVALID_CLAIM_1, INVALID_CLAIM_2, INVALID_CLAIM_3
from credentials import TELEGRAM_CRED

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Telegram bot Auth Key
AuthKey = TELEGRAM_CRED

# GLOBAL VARS
TIME_INTERVAL_BETWEEN_HINTS = 60
ALL_TOKENS = sqlc.get_all_tokenid()
MASTER_ID = '0' # set to bot owner tele id

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

# =============================================================================
# HOUSEKEEPING COMMANDS begin the command with _
# =============================================================================

def _error(bot, update, error):
    """ Error handler """
    
    try:
        raise error
    except ChatMigrated as e:
        print(e.new_chat_id)
        return e.new_chat_id
        
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)
    

# =============================================================================
# LEVEL 0 COMMANDS
# =============================================================================
def start(bot, update):
    """ Start the bot and gives rules to the player """
    
    # Get ID of sender
    user_id = update.message.chat.id
        
    msg  = """Hi! I am the official bot for Hostel Hunt 2019.\n\n
Please read the rules carefully in the image below:"""
    
    # Check if user already exists, else Record New User
    if user_id not in sqlc.get_current_users():
        sqlc.add_user(user_id)

    # Output message
    bot.send_message(chat_id=user_id, text=msg)
    bot.send_photo(chat_id=user_id, photo=open('photos/hostelhunt instructions1.png', 'rb'))
    bot.send_photo(chat_id=user_id, photo=open('photos/hostelhunt instructions2.png', 'rb'))
    #//TODO: CHANGE PHOTO
    
def register(bot, update,args):
    """ Start the bot and gives rules to the player """
    
    # Get ID of sender
    user_id = update.message.chat.id
    
    if (len(args) != 1):
        bot.send_message(chat_id=user_id, text="Register your student ID. /register <studentID>")
    else:
        student_id = args[0]
        if re.match("^[0-9]*$", student_id) == None:
            bot.send_message(chat_id=user_id, text="Register your student ID. /register <studentID>")
        else:
            if int(student_id) in sqlc.get_current_users_student_id():
                msg = "Student ID already registered!"
            else:
                sqlc.update_student_id(user_id,int(student_id))
                msg = "Successfully registered, {}!".format(student_id)
            bot.send_message(chat_id=user_id, text=msg)
    
def gethint(bot, update, args=[]):
    # Get ID of sender
    user_id = update.message.chat.id
    # Get current time
    now = time.time()
    # Get last_hint_time
    last_time = sqlc.get_last_hint_time(user_id)
    # if last_hint_time is None, get new hint
    if last_time == None:
        output_msg = sqlc.get_hint(user_id)
        sqlc.update_last_hint_time(user_id,now)
    elif (int(now) - int(last_time) >= TIME_INTERVAL_BETWEEN_HINTS):
        output_msg = sqlc.get_hint(user_id)
        sqlc.update_last_hint_time(user_id,now)
    else:
        output_msg = "Please try again in {} seconds.".format(int(last_time + TIME_INTERVAL_BETWEEN_HINTS - time.time()))
    
    bot.send_message(user_id, text=output_msg)
        
def claim(bot, update, args=[]):
    # Get ID of sender
    user_id = update.message.chat.id
    
    if len(args) == 1:
        
        code = args[0]
        
        unclaimed = sqlc.get_unclaimed_hints()
        unclaimed_users = sqlc.get_unclaimed_users()

        if code in unclaimed:
            if user_id in unclaimed_users:
                sqlc.claim_token(user_id,code)
                
                bot.send_message(user_id, text=VALID_CLAIM)
            else:
                bot.send_message(user_id, text=INVALID_CLAIM_1)
        else:
            bot.send_message(user_id, text=INVALID_CLAIM_2)
        
        if code not in ALL_TOKENS:
            bot.send_message(user_id, text=INVALID_CLAIM_1)
    else:
        bot.send_message(user_id, text=INVALID_CLAIM_3)
        
def update(bot, update):
    ''' To broadcast message to everyone '''
    # Get ID of sender
    user_id = update.message.chat.id

    if user_id == MASTER_ID:
        all_users = sqlc.get_current_users()
        for user in all_users:
            try:
                bot.send_message(user, text=MSG_1)
            except:
                pass

# =============================================================================
# OTHER COMMANDS
# =============================================================================
    
def test(bot, update):
    print(update.message.chat.id)

def echo(bot, update):
    """Echo the user message."""
    
    # Check if sender is not a group
    if int(update.message.chat.id) > 0:
        update.message.reply_text(update.message.text)

# =============================================================================
# MAIN BOT
# =============================================================================

def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(AuthKey)
    
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Telegram Commands / Command Handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("gethint", gethint, pass_args=True))
    dp.add_handler(CommandHandler("register", register, pass_args=True))
    dp.add_handler(CommandHandler("claim", claim, pass_args=True))
    dp.add_handler(CommandHandler("update", update))
    
    # log all errors
    dp.add_error_handler(_error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
