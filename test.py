import time

import telebot
import datetime
import requests

TOKEN_BOT = '2137380397:AAE5M-KsMuWxMQtJftw1WA4rhYJtWLrPRz4'
PUBLIC_ID = '@ftnotifi'

bot = telebot.TeleBot(TOKEN_BOT)
bot.send_message(PUBLIC_ID, 'TEST')
