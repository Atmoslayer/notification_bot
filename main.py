import logging
import os
import time
import requests
from dotenv import load_dotenv
from requests import HTTPError, ConnectionError
from telegram.ext import Updater, CommandHandler
from telegram import ReplyKeyboardRemove


def start(update, context):
    user = update.message.from_user

    reply_markup = ReplyKeyboardRemove()
    update.message.reply_text(
        text='Здравствуйте! Этот бот предназначен для отправки уведомлений о проверке Ваших уроков.',
        reply_markup=reply_markup,
    )

    url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': devman_token}
    timestamp = None

    while True:
        try:
            params = {'timestamp': timestamp}
            response = requests.get(url, headers=headers, timeout=5, params=params)
            response.raise_for_status()
            response_data = response.json()
            attempts = response_data['new_attempts']
            for attempt in attempts:
                timestamp = attempt['timestamp']
                if attempt['is_negative']:
                    status = 'необходимы дальнейшие улучшения'
                else:
                    status = 'урок сдан, можно приступать к следующему'
                lesson_url = attempt['lesson_url']
                lesson_title = attempt['lesson_title']

            message = f'Преподаватель проверил работу "{lesson_title}", {status}. \n{lesson_url}'
            update.message.reply_text(
                text=message,
                reply_markup=reply_markup,
            )

        except requests.exceptions.ReadTimeout:
            pass

        except HTTPError as http_error:
            logging.info(f'\nHTTP error occurred: {http_error}')

        except ConnectionError as connection_error:
            logging.info(f'\nConnection error occurred: {connection_error}')
            time.sleep(5)


if __name__ == '__main__':

    load_dotenv()
    bot_token = os.getenv('BOT_TOKEN')
    devman_token = os.getenv('DEVMAN_TOKEN')
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    updater.start_polling()
    logging.info('Бот вышел в сеть')
    updater.idle()


