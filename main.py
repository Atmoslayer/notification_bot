import logging
import os
import time
import requests
import telegram
from dotenv import load_dotenv
from requests import HTTPError, ConnectionError

logger = logging.getLogger('bot_logger')


class BotLogsHandler(logging.Handler):

    def __init__(self, bot, admin_chat_id):
        self.bot = bot
        self.admin_chat_id = admin_chat_id
        super().__init__()

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(
            chat_id=self.admin_chat_id,
            text=log_entry,
        )


def start(chat_id, bot, devman_token):

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
            logger.warning(log_text)

        except ConnectionError as connection_error:
            log_text = f'\nConnection error occurred: {connection_error}'
            logger.warning(log_text)
            time.sleep(5)


def main():
    load_dotenv()
    bot_token = os.getenv('BOT_TOKEN')
    devman_token = os.getenv('DEVMAN_TOKEN')
    chat_id = os.getenv('CHAT_ID')
    admin_chat_id = os.getenv('ADMIN_CHAT_ID')
    bot = telegram.Bot(token=bot_token)

    logger.setLevel(logging.INFO)
    log_handler = BotLogsHandler(bot, admin_chat_id)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    log_handler.setFormatter(formatter)
    log_handler.setLevel(logging.INFO)

    logger.addHandler(log_handler)
    logger.info('The bot started')
    start(chat_id, bot, devman_token)


if __name__ == '__main__':
    main()

