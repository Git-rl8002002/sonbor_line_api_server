#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Date        : 20250407
# update      : 202504010
# Author      : Jason Hung
# Version     : v1.1
# Description : v1.0 SonBor Line Messaging API - LINE SDK v2 寫法
#               v1.1 package api for VB  

from flask import Flask, request, abort , jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError
from apscheduler.schedulers.background import BackgroundScheduler
import traceback , pymysql , time , requests , pyodbc

from control.dao import dao
import control.dao
db = dao()

#####################################################################################################################################################################################################################
#
# line_message_api
#
#####################################################################################################################################################################################################################
class line_message_api:

    #################
    # parameter 
    #################

    # line push token and secret
    line_bot_api_key = control.dao.para['line_bot_api']
    handler_key      = control.dao.para['handler']

    #######################
    # 初始化 LINE SDK v2
    #######################
    line_bot_api = LineBotApi(line_bot_api_key)
    handler      = WebhookHandler(handler_key)

    
    ############
    # 主動推播
    ############
    def line_message_timer(self):
        user_id  = "U6c62b506b6a6eb52427be571dfdf2b5d"
        profile  = self.line_bot_api.get_profile(user_id)
        message1 = f"Check {user_id} , UID 中 ..."
        message2 = f"name : {profile.display_name} \nUID : {user_id} \n ok 已經註冊過."
        
        try:
            print(f"Receiver: display_name={profile.display_name} , user_id={user_id}, message={message1} , {message2}")
            
            self.line_bot_api.push_message(
                user_id,
                [
                    TextSendMessage(text=message1),
                    TextSendMessage(text=message2)
                ]
            )

            # 檢查訊息使用量
            self.check_message_usage()
            
        except Exception as e:
            traceback.print_exc()
            return f"Failed to send: {e}", 500


    ##################
    # 檢查使用量
    ##################
    def check_message_usage(self):
        
        channel_access_token = control.dao.para['line_bot_api']
        admin_user_id        = control.dao.para['admin_uid']
        user1_user_id        = control.dao.para['user1_uid']
        warning_threshold    = 10  # 當剩餘訊息低於這數字時提醒
        
        url     = "https://api.line.me/v2/bot/message/quota/consumption"
        headers = {
            "Authorization": f"Bearer {channel_access_token}"
        }

        try:
            response = requests.get(url, headers=headers)
            data = response.json()

            used = data.get("totalUsage", 0)

            # 假設你是 Free 方案，訊息總額為 500
            total_quota = 200
            remaining   = total_quota - used

            print(f"目前已使用 {used} 則，剩餘 {remaining} 則")

            if remaining < warning_threshold:
                self.line_bot_api.push_message(
                    admin_user_id,
                    TextSendMessage(text=f"⚠️ 免費訊息剩餘 {remaining} 則，請注意！")
                )
            else:
                print(f"📢 免費訊息剩餘 {remaining} 則，訊息數尚充足。")
                self.line_bot_api.push_message(
                    user1_user_id,
                    TextSendMessage(text=f"📢 免費訊息剩餘 {remaining} 則，訊息數尚充足。")
                )

        except Exception as e:
            print("查詢訊息用量失敗：", e)


    ############
    # webhook
    ############
    @handler.add(MessageEvent, message=TextMessage)
    def handle_message(self,event):
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
                    self.line_bot_api.push_message(
                        uid,
                        TextSendMessage(text=f"[公告]\n{message_content}")
                    )
                except Exception as e:
                    print(f"推播給 {uid} 失敗：{e}")

            reply_text = "已公告給所有使用者。"
        else:
            
            # 已經註冊
            conn = self.get_db_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute(f"SELECT c_status FROM line_message_api where c_user='{user_id}'")
                    result = cursor.fetchone()
                    #return jsonify(result)
            finally:
                conn.close()

            # 一般回覆
            reply_text = f"你說的是：{text} \n你的UID : {user_id} \n{result[0]} , 已經註冊過."

        self.line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )

    


#####################################################################################################################################################################################################################
#
# Main
#
#####################################################################################################################################################################################################################
if __name__ == "__main__":
    
    #########
    # loop 
    #########
    '''
    scheduler = BackgroundScheduler()
    scheduler.add_job(line_message_timer, 'interval', seconds=10)  
    scheduler.start()

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
    '''

    db.get_mssql_data()
    db.get_mysql_data()
    