# Бот для уведомлений о проверке уроков на на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
Проект позволяет получать уведомления о проверке работ с помощью телеграмм-бота. При возвращении урока с ревью, бот 
отправляет сообщение, содержащее статус проверки и ссылку на проверенный урок.
## Как установить
Необходимо создать телеграм-бота с помощью отца ботов @BotFather, написав ему и выбрав имена для бота. 
После этого будет получен токен, подобный этому: `1234567890:ABCDEFGHIjklmnoPqrsStuvwxyzINet1234`.
После этого необходимо получить свой токен в разделе [API Девмана](https://dvmn.org/api/docs/) на подобии этого:
`12345678abcdefghijklmnopurjamkf6oenv77ab`.
Для того, чтобы бот мог общаться с пользователем, нужно получить его telegram id, это можно сделать, написал боту @getmyid_bot.
После этого будет получен id на подобие этого: `1234567891`
Для хранения токенов в проекте используются переменные окружения. После получения токены необходимо добавить в файл `.env`.
Пример заполненного файла:
```
BOT_TOKEN=1234567890:ABCDEFGHIjklmnoPqrsStuvwxyzINet1234
DEVMAN_TOKEN=12345678abcdefghijklmnopurjamkf6oenv77ab
CHAT_ID=1234567891
```
Python3 должен быть уже установлен.
Затем используйте `pip` (или `pip3`, если есть конфликт с Python2) для установки зависимостей:
```
>>>pip install -r requirements.txt
```
## Запуск бота
Перед запуском нужно отправить боту команду /start, так как бот не может первым писать сообщения.
Бот запускается командой:
```
>>>python3 main.py           
```
## Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).