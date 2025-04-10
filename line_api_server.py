#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Date        : 20250407
# update      : 20250408
# Author      : Jason Hung
# Version     : V2.0
# Description : SonBor Line Messaging API - LINE SDK v2 寫法

from flask import Flask, request, abort , jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError
import traceback , pymysql , pyodbc

import control.dao
from control.dao import dao
db = dao()


############
# 讀取憑證
############
line_bot_api_key = control.dao.para['line_bot_api']
handler_key      = control.dao.para['handler']

#######################
# 初始化 LINE SDK v2
#######################
line_bot_api = LineBotApi(line_bot_api_key)
handler = WebhookHandler(handler_key)

app = Flask(__name__)

############
# 主動推播
############
@app.route("/callback_u", methods=['GET', 'POST'])
def callback_u():
    user_id = request.args.get('to')
    message = request.args.get('t')
    pid = request.args.get('pid')  # optional
    sid = request.args.get('sid')  # optional

    if user_id and message:
        try:
            print(f"Receiver: user_id={user_id}, message={message}")
            line_bot_api.push_message(
                user_id,
                TextSendMessage(text=message)
            )
            return "Message sent!"
        except Exception as e:
            traceback.print_exc()
            return f"Failed to send: {e}", 500
    else:
        return "Missing parameters", 400

#################
# webhook 入口
#################
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        traceback.print_exc()
        abort(400)

    return 'OK'

####################
# webhook 事件處理
####################
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    text    = event.message.text.strip()

    print(f"User ID: {user_id}")
    print(f"訊息：{text}")

    if text.startswith("公告"):
        message_content = text.replace("公告：", "", 1).strip()

        # 假設你有一組公告名單
        broadcast_users = ["U6c62b506b6a6eb52427be571dfdf2b5d"]  # 替換成實際 user ID

        for uid in broadcast_users:
            try:
                line_bot_api.push_message(
                    uid,
                    TextSendMessage(text=f"[公告]\n{message_content}")
                )
            except Exception as e:
                print(f"推播給 {uid} 失敗：{e}")

        reply_text = "已公告給所有使用者。"
    else:
        # 一般回覆
        reply_text = f"你說的是：{text} \n你的UID : {user_id}"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )



#####################################################################################################################################################################################################################
#
# Main
#
#####################################################################################################################################################################################################################
if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")