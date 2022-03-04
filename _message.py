import telepot
import time
from telepot.loop import MessageLoop
from _config import config
from _logger import logger

message_chat_id_list = eval(config["TELEGRAM_DEFAULT_CHAT_ID"])
graph_chat_id_list = []
bot = telepot.Bot(config["TELEGRAM_TOKEN"])

def initialize_listening():
    MessageLoop(bot, handle).run_as_thread()

    if message_chat_id_list is not None and \
            isinstance(message_chat_id_list, list) and \
            message_chat_id_list != []:
        for chat_id in message_chat_id_list:
            bot.sendMessage(chat_id, "봇이 (재)시작합니다.(v1.1)")

def handle(msg):
    global message_chat_id_list, graph_chat_id_list

    content_type, chat_type, chat_id = telepot.glance(msg)
    if chat_id in message_chat_id_list and msg is not None:
        if 'text' in msg.keys() and msg['text'] == 'quit':
            bot.sendMessage(chat_id, "구매 정보를 받지 않습니다. quit 또는 graph 제외한 문자열을 입력하면 구독합니다.")
            message_chat_id_list.remove(chat_id)
        if 'text' in msg.keys() and msg['text'] == 'graph':
            if chat_id in graph_chat_id_list:
                bot.sendMessage(chat_id, "그래프를 수신하지 않습니다. graph 를 입력해서 추가합니다.")
                graph_chat_id_list = list(filter(lambda x: chat_id != x, graph_chat_id_list))
            else:
                bot.sendMessage(chat_id, "10분마다 그래프를 수신합니다. graph 를 입력해서 제외합니다.")
                graph_chat_id_list.append(chat_id)
    else:
        message_chat_id_list.append(chat_id)
        bot.sendMessage(
            chat_id, "15분 단위로 구매 정보를 받습니다. 'quit'를 입력하면 해제합니다.")

    message_chat_id_list = list(set(message_chat_id_list))
    graph_chat_id_list = list(set(graph_chat_id_list))

    logger.info(str(msg))


def send_message_with_image(_caption, _file):
    for chat_id in message_chat_id_list:
        if chat_id in graph_chat_id_list:
            logger.info(f"send caption:{_caption} with image to chat_id:{chat_id}")
            bot.sendPhoto(chat_id, photo=open(_file, 'rb'), caption=_caption)
        else:
            logger.info(f"{chat_id} is skipped because it's not in graph_chat_id_list")

def send_message(_message):
    for chat_id in message_chat_id_list:
        logger.info(f"send message:{_message} with image to chat_id:{chat_id}")
        bot.sendMessage(chat_id, _message, parse_mode="Markdown")


if __name__ == "__main__":
    # Keep the program running.
    MessageLoop(bot, handle).run_as_thread()
    logger.info('Telegram working only, on listening...')
    logger.warn("For working expectedly, run python main.py, instead")
    while 1:
        time.sleep(10)
