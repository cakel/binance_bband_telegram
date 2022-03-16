from _logger import logger
from _message import initialize_listening
from _trade import bollinger_trade_logic
from _message import send_message_with_image, send_message
from _config import config
from time import sleep
import datetime


def mainloop():
    img_cnt = -1
    msg_cnt = -1
    last_message_type = "Undefined"
    this_message_type = "Undefined"
    _message = "*미정*"

    while True:

        now = datetime.datetime.now()
        now_time = now.strftime('%Y년%m월%d일 %H시%M분%S초')
        (current_price, current_upper, current_lower,
         current_price_percentage) = bollinger_trade_logic()
        _caption = f"{now_time} 현재가:{current_price:.2f}, {config['BINANCE_TRACE_INTERVAL']} BB상단:{current_upper:.2f}/하단:{current_lower:.2f}/비율:{current_price_percentage:.2f}%"

        # Graph First time and after, every 10Min
        if img_cnt > 60:
            try:
                send_message_with_image(_caption, "output.jpg")
            except Exception as _e:
                logger.warn("Error while sending message : {}".format(str(_e)))
            img_cnt = 0

        if img_cnt < 9999999:  # Don't have to count more than 9999999
            img_cnt += 1

        # Determine Sell(매도) or Buy(매수) or Skip(다음)
        if current_price_percentage >= 90:
            _message = "*매도* : BB상단 근접(90%) 또는 넘어감(>100%)" + _caption
            this_message_type = "Sell"

        elif current_price_percentage <= 10:
            _message = "*구매* : BB하단 근접(10%) 또는 내려감(<0%)" + _caption
            this_message_type = "Buy"

        else:
            this_message_type = "Skip"

        logger.debug("DETERMINE: last_message_type:{}, this_message_type:{}, current_price_percentage:{}, msg_cnt:{}".format(
            last_message_type, this_message_type, current_price_percentage, msg_cnt))

        # Send Message
        if (this_message_type == "Sell" or this_message_type == "Buy") and \
           ((last_message_type != this_message_type) or msg_cnt > 90):
            last_message_type = this_message_type
            try:
                send_message(_message)
            except Exception as _e:
                logger.warn(
                    "Error while sending message : {}".format(str(_e)))
            msg_cnt = 0  # Reset Count until 90 (900s = 15Min)

        if msg_cnt < 9999999: # Don't have to count more than 9999999
            msg_cnt += 1

        logger.info(f"Loop Message/Image Counter Up - msg_cnt:{msg_cnt} / img_cnt:{img_cnt}")
        sleep(10)  # 10 Second


if __name__ == "__main__":
    logger.info(f"=== Program Loop Start ===")
    initialize_listening()
    mainloop()
    pass
