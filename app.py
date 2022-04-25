from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi(
    'WBpYgoqz4yDqwrgEai8WOttoHYbPB2AOz/A889Nl7BkRz5yDOO3QF6/YY9fsSTpsF3Jsah4DxpGK1uTfcYJ4TmY8DIijj3dXm640VFlRFvNfjHmADMgvk0Z6QfgCjVKIcB+14GC38BdwHdlINpoUIgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d099a533a2e3968a6904b5e5bf04186d')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '貓頭鷹問號'

    if '貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )
        line_bot_api.reply_message(
            event.reply_token,
            sticker_message)
        return

    if msg in ['hi', 'Hi']:
        r = '嗨'
    elif msg == '你是誰':
        r = '我是貓頭鷹'
    elif '小杰' in msg:
        r = '杰哥不要！！！'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()
