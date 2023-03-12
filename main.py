import logging
import os
import time
import requests
import telegram
from dotenv import load_dotenv
from requests import HTTPError, ConnectionError


def start(admin_chat_id, chat_id, bot):

    bot.send_message(
        chat_id=chat_id,
        text='Здравствуйте! Этот бот предназначен для отправки уведомлений о проверке Ваших уроков.',
    )

    url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': devman_token}
    timestamp = None

    while True:
        try:
            params = {'timestamp': timestamp}
            response = requests.get(url, headers=headers, timeout=5, params=params)
            response.raise_for_status()
            lesson_data = response.json()
            attempts = lesson_data['new_attempts']
            for attempt in attempts:
                timestamp = attempt['timestamp']
                if attempt['is_negative']:
                    status = 'необходимы дальнейшие улучшения'
                else:
                    status = 'урок сдан, можно приступать к следующему'
                lesson_url = attempt['lesson_url']
                lesson_title = attempt['lesson_title']

            bot.send_message(
                chat_id=chat_id,
                text=f'Преподаватель проверил работу "{lesson_title}", {status}. \n{lesson_url}',
            )

        except requests.exceptions.ReadTimeout:
            pass

        except HTTPError as http_error:
            log_text = f'\nHTTP error occurred: {http_error}'
            logging.info(log_text)
            send_log(admin_chat_id, bot, log_text)

        except ConnectionError as connection_error:
            log_text = f'\nConnection error occurred: {connection_error}'
            logging.info(log_text)
            send_log(admin_chat_id, bot, log_text)
            time.sleep(5)


def send_log(admin_chat_id, bot, log_text):
    bot.send_message(
        chat_id=admin_chat_id,
        text=log_text,
    )


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    bot_token = os.getenv('BOT_TOKEN')
    devman_token = os.getenv('DEVMAN_TOKEN')
    chat_id = os.getenv('CHAT_ID')
    admin_chat_id = os.getenv('ADMIN_CHAT_ID')
    bot = telegram.Bot(token=bot_token)
    logging.info('Bot started')
    send_log(admin_chat_id, bot, 'Bot started')
    start(chat_id, bot)