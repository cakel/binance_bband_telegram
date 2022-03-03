import telepot
import time
from telepot.loop import MessageLoop
from _config import config
from _logger import logger

chat_id_list = eval(config["TELEGRAM_DEFAULT_CHAT_ID"])
bot = telepot.Bot(config["TELEGRAM_TOKEN"])


def initialize_listening():
    MessageLoop(bot, handle).run_as_thread()

    if chat_id_list is not None and \
            isinstance(chat_id_list, list) and \
            chat_id_list != []:
        for chat_id in chat_id_list:
            bot.sendMessage(chat_id, "봇이 (재)시작합니다.")

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if chat_id in chat_id_list and \
            msg is not None and \
            'text' in msg.keys() and \
            msg['text'] == 'quit':
        bot.sendMessage(
            chat_id, "...Unsubscribed... To subscribe, type anything")
        chat_id_list.remove(chat_id)
    else:
        chat_id_list.append(chat_id)
        bot.sendMessage(
            chat_id, "...Subscribed... To unsubscribe, type 'quit'")

    chat_id_list = list(set(chat_id_list))  # Remove duplicate
    logger.info(str(msg))


def send_message_with_image(_caption, _file):
    for chat_id in chat_id_list:
        logger.info(f"send caption:{_caption} with image to chat_id:{chat_id}")
        bot.sendPhoto(chat_id, photo=open(_file, 'rb'), caption=_caption)

def send_message(_message):
    for chat_id in chat_id_list:
        logger.info(f"send message:{_message} with image to chat_id:{chat_id}")
        bot.sendMessage(chat_id, _message, parse_mode="Markdown")


if __name__ == "__main__":
    # Keep the program running.
    MessageLoop(bot, handle).run_as_thread()
    logger.info('Telegram working only, on listening...')
    logger.warn("For working expectedly, run python main.py, instead")
    while 1:
        time.sleep(10)
