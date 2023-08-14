from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btn_send_new_posts = KeyboardButton(text='Post')
btn_get_screenshot = KeyboardButton(text='Screenshot')
admin_keyboard = ReplyKeyboardMarkup(keyboard=[[btn_send_new_posts, btn_get_screenshot]], resize_keyboard=True, input_field_placeholder='Choose option')
