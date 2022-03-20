from telebot import types
import telebot
button1 = types.InlineKeyboardButton('Да, напомни', callback_data='button1')
keyboard1 = types.InlineKeyboardMarkup().add(button1)

button2 = types.InlineKeyboardButton('Исправил уже', callback_data='button2')
keyboard2 = types.InlineKeyboardMarkup().add(button2)