from telebot import types
import telebot
button1 = types.InlineKeyboardButton('Да, напомни', callback_data='button1')
keyboard1 = types.InlineKeyboardMarkup().add(button1)