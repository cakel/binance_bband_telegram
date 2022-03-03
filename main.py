from _logger import logger
from _message import initialize_listening
from _trade import bollinger_trade_logic
from _message import send_message_with_image, send_message
from time import sleep
import datetime


def mainloop():
    img_cnt = -1
    msg_cnt = -1
    last_message_type = "Undefined"
    this_message_type = "Undefined"
    while True:

        now = datetime.datetime.now()
        now_time = now.strftime('%Y년%m월%d일 %H시%M분%S초')
        (current_price, current_upper, current_lower,
         current_price_percentage) = bollinger_trade_logic()
        _caption = f"{now_time} 현재가:{current_price:.2f}, 15분 BB상단:{current_upper:.2f}/하단:{current_lower:.2f}/비율:{current_price_percentage:.2f}%"

        # Graph First time and after, every 10Min
        if img_cnt % 60 == 0:
            try:
                send_message_with_image(_caption, "output.jpg")
            except Exception as _e:
                logger.warn("Error while sending message : {}".format(str(_e)))
            img_cnt = 1
        else:
            img_cnt += 1

        # Sending message condition
        if current_price_percentage > 90 or current_price_percentage < 10:
            if current_price_percentage > 90:
                _message = "*매도* : BB(90%)/상단 근접/넘어감(>100)" + _caption
                this_message_type = "Sell"

            elif current_price_percentage < 10:
                _message = "*구매* : BB(10%)/하단 근접/내려감(<0)" + _caption
                this_message_type = "Buy"

            # Buy -> Sell or vice versa
            # Message Count is ready to send.
            if last_message_type != this_message_type or msg_cnt == -1:
                last_message_type = this_message_type
                try:
                    send_message(_message)
                except Exception as _e:
                    logger.warn(
                        "Error while sending message : {}".format(str(_e)))

                msg_cnt = 0  # Count until it's ready to send message again

        if msg_cnt > 6:  # The Count ready cool time is 60s
            msg_cnt = -1    # Ready to send
        else:
            msg_cnt += 1    # Wait and add count

        sleep(10)  # 10 Second


if __name__ == "__main__":
    logger.info("=== Program Loop Start ===")
    initialize_listening()
    mainloop()
    pass
