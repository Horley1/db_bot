from telebot import types
import telebot
button1 = types.InlineKeyboardButton('Да, напомни', callback_data='button1')
keyboard1 = types.InlineKeyboardMarkup().add(button1)

button2 = types.InlineKeyboardButton('Исправил уже', callback_data='button2')
keyboard2 = types.InlineKeyboardMarkup().add(button2)

button3 = types.KeyboardButton('⚙Меню⚙')
keyboard3 = types.ReplyKeyboardMarkup(resize_keyboard=True).add(button3)

button4 = types.InlineKeyboardButton('⏱Период задолжности⏱', callback_data='button4')
button5 = types.InlineKeyboardButton('🔙Назад🔙', callback_data='button5')
button6 = types.InlineKeyboardButton('😈Средний балл по оценкам😈', callback_data='button6')
button7 = types.InlineKeyboardButton('📚Домашние задания📚', callback_data='button7')
button8 = types.InlineKeyboardButton('🙌🏻Вопросы и предложения🙌🏻', callback_data='button8')
keyboard5 = types.InlineKeyboardMarkup(row_width=1).add(button4, button6, button7, button8)

button9 = types.InlineKeyboardButton('📝Регистрация📝', callback_data='button9')
button10 = types.InlineKeyboardButton('Что я умею❓', callback_data='button10')
button11 = types.InlineKeyboardButton('🙅Как храняться личные данные?🙅', callback_data='button11')
button12 = types.InlineKeyboardButton('💿Контактные данные💿', callback_data='button12')
keyboard4 = types.InlineKeyboardMarkup(row_width=1).add(button9, button10, button11, button12)


button13 = types.InlineKeyboardButton('－', callback_data='button13')
button14 = types.InlineKeyboardButton('＋', callback_data='button14')
button15 = types.InlineKeyboardButton('5', callback_data='button15')

