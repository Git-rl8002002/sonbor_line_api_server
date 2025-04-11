#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Date        : 20250407
# update      : 20250411
# Author      : Jason Hung
# Version     : V2.0
# Description : SonBor Line Messaging API - LINE SDK v3 寫法


##########################
#
# line bot sdk ver 3.0
#
##########################
from flask import Flask, request, abort
from linebot.v3.webhook import WebhookHandler
from linebot.v3.messaging import MessagingApi, ReplyMessageRequest, TextMessage , Configuration
from linebot.v3.webhooks import MessageEvent, TextMessageContent, StickerMessageContent, ImageMessageContent
from linebot.v3.exceptions import InvalidSignatureError          
from linebot.v3.messaging.exceptions import ApiException      
from linebot.v3.messaging.api_client import ApiClient
from linebot.v3.messaging.configuration import Configuration

import traceback, logging, control.dao
from control.dao import dao

db = dao()

##############################
# line bot - token / secret
##############################
config        = Configuration(access_token=control.dao.para['line_bot_api_token'])
api_client    = ApiClient(configuration=config)
messaging_api = MessagingApi(api_client)
handler       = WebhookHandler(control.dao.para['handler_key'])

app = Flask(__name__)

########
# log
########
log_format = "%(asctime)s %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S")

##############
# /callback
##############
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature!")
        traceback.print_exc()
        return 'Invalid signature', 400

    return 'OK'

#####################
# get_user_profile
#####################
def get_user_profile(user_id):
    try:
        return messaging_api.get_profile(user_id)
    except ApiException as e:
        logging.info(f"<ERROR> get_user_profile: status={e.status}, body={e.body}")
        return None

##############
# get_quote
##############
def get_quota():
    try:
        total_quota = messaging_api.get_message_quota().value
        used_quota  = messaging_api.get_message_quota_consumption().total_usage
        remaining   = total_quota - used_quota
        return total_quota, used_quota, remaining
    except ApiException as e:
        logging.error(f"<ERROR> get_quota failed: status={e.status}, body={e.body}")
        # 若發生錯誤，回傳預設值 -1
        return -1, -1, -1

####################################
# webhook handler - text message
####################################
@handler.add(MessageEvent, message=TextMessageContent)
def handle_text(event):
    user_id = event.source.user_id
    text = event.message.text.strip()

    profile = get_user_profile(user_id)
    total_quota, used_quota, remaining = get_quota()

    user_name = profile.display_name if profile else "User"

    print(f"\n(收到文字) \n {user_name} \t {user_id} \t {total_quota} / {used_quota} = {remaining}")

    reply_text = f"收到文字 Hi , {user_name} welcome join."
    messaging_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text=reply_text)]
        )
    )

####################################
# webhook handler - sticker message
####################################
@handler.add(MessageEvent, message=StickerMessageContent)
def handle_sticker(event):
    user_id = event.source.user_id
    profile = get_user_profile(user_id)
    total_quota, used_quota, remaining = get_quota()

    user_name = profile.display_name if profile else "User"
    print(f"\n(收到貼圖) \n {user_name} \t {user_id} \t {total_quota} / {used_quota} = {remaining}")

    reply_text = f"\U0001F464 收到貼圖 ! Hi , {user_name} welcome join."
    messaging_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text=reply_text)]
        )
    )

####################################
# webhook handler - image message
####################################
@handler.add(MessageEvent, message=ImageMessageContent)
def handle_image(event):
    user_id = event.source.user_id
    profile = get_user_profile(user_id)
    total_quota, used_quota, remaining = get_quota()

    user_name = profile.display_name if profile else "User"
    print(f"\n(收到圖片) \n {user_name} \t {user_id} \t {total_quota} / {used_quota} = {remaining}")

    messaging_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text=f"\U0001F4F7 收到圖片！ Hi , {user_name} welcome join.")]
        )
    )
########################################
# webhook handler - unsupport message
########################################
@handler.add(MessageEvent)
def handle_unknown(event):
    user_id = event.source.user_id
    profile = get_user_profile(user_id)
    total_quota, used_quota, remaining = get_quota()

    msg_type = event.message.type
    user_name = profile.display_name if profile else "User"

    print(f"\n(收到不支援) \n  {user_name} \t {user_id} \t {total_quota} / {used_quota} = {remaining}")

    messaging_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text=f"\u26A0\uFE0F 不支援的訊息類型：{msg_type}")]
        )
    )
#####################################################################################################################################################################################################################
#
# Main
#
#####################################################################################################################################################################################################################
if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")


