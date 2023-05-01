FROM python:3.10.7
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /notification_bot
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD [ "python", "main.py" ]