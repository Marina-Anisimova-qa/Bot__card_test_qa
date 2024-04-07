# Для работы необходимо установить одну внешнюю библиотеку Telebot
# pip install pyTelegramBotAPI
from telebot import TeleBot, types
from faker import Faker

# Укажем токен телеграм-бота из BotFather'а и зададим режим форматирования (parse_mode) с помощью HTML-тегов.
bot = TeleBot(token='7117390411:AAE8J0pkqNbtbwxIZk7wVsT-cw0kwKswJk4', parse_mode='html')
faker = Faker()
# Массив с доступными расширениями файлов. Можно изменить, и добавятся/удалятся кнопки выбора на клавиатуре.


# Добавим меню кастомных команд, и пропишем туда стандартную команду /start. С её помощью можно будет перезапустить бота и начать по-новой.
bot.set_my_commands([types.BotCommand('/start', 'перезапуск бота')])

# Начальный шаг #1. Функция приветствия, приветствует пользователя и предлагает выбрать расширение файла.
# С помощью хэндлера говорим, что данная функция будет запускаться при первом контакте с ботом командой /start.
@bot.message_handler(commands=['start'])
def welcome(message):

    # Получаем имя пользователя Telegram, чтобы можно было обратиться к нему по имени.
   sti = open('welcome.jpg', 'rb')
   bot.send_sticker(message.chat.id, sti)
   formats = ['VISA', 'Mastercard', 'Maestro', 'JCB', 'Вернуться в начало']
    # Добавляем клавиатуру под поле ввода сообщения. Там отрисуются все кнопки из массива с расширениями.
    # Максимум будет 5 кнопок в ряд (параметр row_width=5).
   markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
   markup.add(*formats, row_width=3)
   username = message.from_user.first_name
    # Отправляем приветственное сообщение.
   reply = bot.send_message(message.chat.id, f"Привет, <b>{username}</b>! 👋🏻\n Я умею генерировать номер тестовой банковской карты\nВыбери тип карты: ⬇️",
         reply_markup=markup)


# Шаг #3. Проверка выбранной единицы измерения. Если всё хорошо, отправляется сообщение предложением ввести размер файла.

@bot.message_handler()
def message_handler(message: types.Message):
    # проверяем текст сообщения на совпадение с текстом какой либо из кнопок
    # в зависимости от типа карты присваем занчение переменной 'card_type'
    if message.text == 'VISA':
        card_type = 'visa'
    elif message.text == 'Mastercard':
        card_type = 'mastercard'
    elif message.text == 'Maestro':
        card_type = 'maestro'
    elif message.text == 'JCB':
        card_type = 'jcb'
    elif (message.text == 'Вернуться в начало' or message.text == '/start'):
            bot.send_message(
            chat_id=message.chat.id,
            text='Давай начнем сначала',)
            welcome(message)

        # То возвращаемся на первый начальный шаг.

    else:
        # если текст не совпал ни с одной из кнопок
        # выводим ошибку
        bot.send_message(
            chat_id=message.chat.id,
            text='Не понимаю тебя :(',
        )
        return

    # получаем номер тестовой карты выбранного типа
    # card_type может принимать одно из зачений ['maestro', 'mastercard', 'visa13', 'visa16', 'visa19',
    # 'amex', 'discover', 'diners', 'jcb15', 'jcb16']
    card_number = faker.credit_card_full(card_type)
    # и выводим пользователю
    bot.send_message(
        chat_id=message.chat.id,
        text=f'Тестовая карта {card_type}:\n<code>{card_number}</code>'
    )



# Главная функция, запускаем поллинг бота.
def main():
    bot.infinity_polling()

# Специальная конструкция для точки входа программы (главной функции). В нашем случае это main().
if __name__ == '__main__':
    main()
