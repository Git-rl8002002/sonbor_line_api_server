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
from flask import Flask, request, abort , jsonify
from linebot.v3.webhook import WebhookHandler
from linebot.v3.messaging import MessagingApi, ReplyMessageRequest, TextMessage , Configuration , PushMessageRequest
from linebot.v3.webhooks import MessageEvent, TextMessageContent, StickerMessageContent, ImageMessageContent
from linebot.v3.exceptions import InvalidSignatureError          
from linebot.v3.messaging.exceptions import ApiException , NotFoundException     
from linebot.v3.messaging.api_client import ApiClient
from linebot.v3.messaging.configuration import Configuration

import traceback , logging , json , requests , control.config
from control.dao import dao

dao = dao()

app = Flask(__name__)

##############################
# line bot - token / secret
##############################
config        = Configuration(access_token=control.config.para['line_bot_api_token'])
handler       = WebhookHandler(control.config.para['handler_key'])
api_client    = ApiClient(configuration=config)
messaging_api = MessagingApi(api_client)


########
# log
########
log_format = "%(asctime)s %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S")


#####################
# get_user_profile
#####################
def get_user_profile(user_id):
    
    try:
        return messaging_api.get_profile(user_id)
    
    except ApiException as e:
        logging.error(f"[Error] get_user_profile: status={e.status}, body={e.body}")
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
        logging.error(f"[Error] get_quota failed: status={e.status}, body={e.body}")
        # 若發生錯誤，回傳預設值 -1
        return -1, -1, -1

###################################################
#
# /push_msg
#
# method : POST
# usage  : 
#           r_a_id : receiver message user's UID
#           p_msg  : push message content
#
###################################################
@app.route("/push_msg", methods=['POST'])
def push_msg():
    
    ### push message to line from line bot sdk api
    try:
        
        ### variables
        r_a_id = request.form.get('r_a_id')
        p_msg  = request.form.get('p_msg')

        ### receiver User profile 
        r_a_name   = dao.get_line_account_profile(r_a_id , 'user_name') or "unknow line username"
        r_a_status = dao.get_line_account_profile(r_a_id , 'user_status') or "unknow line user status"
        r_company  = dao.res_line_uid_data(r_a_id) or "unknow company name"

        ### response json 
        r_j_msg = {
                    "status":"successfully" , 
                    "r_a_name":r_a_name , 
                    "r_a_id":r_a_id , 
                    'r_a_status':r_a_status  , 
                    "p_msg":p_msg
                   }

        ### active push mesage
        if dao.push_message_v2(r_a_id, p_msg) == 1:
        
                ### save push message by UID company
                dao.save_line_push_msg_db(r_company , r_a_name , r_a_id , p_msg)
                r_j_msg["status"] = "successfully"

                logging.info(json.dumps(r_j_msg , ensure_ascii=False , indent=2))

                return jsonify(r_j_msg) , 200
        else:
                
                ### response json 
                r_j_msg['status'] = "failed"
                logging.warning(json.dumps(r_j_msg , ensure_ascii=False , indent=2))

                return jsonify(r_j_msg) , 500
        
    except Exception as e:
        logging.error(f"[Error] push_msg exception : {str(e)}")
        return jsonify(r_j_msg) , 500


##############
# /callback
##############
@app.route("/callback", methods=['POST'])
def callback():
    
    signature = request.headers.get('X-Line-Signature')
    body      = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    
    except InvalidSignatureError:
        
        print("Invalid signature!")
        traceback.print_exc()
        
        return 'Invalid signature', 400

    return 'OK'




####################################
# webhook handler - text message
####################################
@handler.add(MessageEvent, message=TextMessageContent)
def handle_text(event):
    
    ############
    # User 
    ############
    source_type = event.source.type  # 'user', 'group', or 'room'

    if source_type == 'user':
        
        user_id = event.source.user_id
        text    = event.message.text.strip()

        profile = get_user_profile(user_id)
        total_quota, used_quota, remaining = get_quota()

        user_name = profile.display_name if profile else "User"

        ### 判斷是否包含 [廠商]
        if "[廠商]" in text:
            # 分割字串，抓取 [廠商] 後面的公司名稱
            company_name = text.split(']')[1].strip()
                
            r_msg = {
                        'msg':'收到文字',
                        'company':company_name,
                        'username':user_name,
                        'uid':user_id,
                        'text':text,
                        'Total quote':total_quota,
                        'Used quote':used_quota,
                        'Remaining':remaining,
                        'reply_msg':''
            }

            dao.save_line_user_sonbor_db(user_name , user_id , company_name)
        
            ### LINE reply text
            reply_text = f"您好 , \U0001F464 {user_name} , \u2705 歡迎加入 {company_name} Line 官方帳號"
            
            ### server reply message
            r_msg['reply_msg'] = reply_text
            logging.info(json.dumps(r_msg , ensure_ascii=False , indent=2))

            ### LINE reply message
            messaging_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=reply_text)]
                )
            )

        else:
            company_name = dao.res_line_uid_data(user_id)

            r_msg = {
                        'msg':'收到文字',
                        'company':company_name,
                        'username':user_name,
                        'uid':user_id,
                        'text':text,
                        'Total quote':total_quota,
                        'Used quote':used_quota,
                        'Remaining':remaining,
                        'reply_msg':''
            } 

            ### save to sonbor db
            if not company_name or company_name.strip().lower() == 'null':
                
                try:
                    ### LINE reply text
                    reply_text = f"您好 , {user_name} \n📢 請輸入廠商名稱 ==> [廠商]松柏資訊"

                    ### server reply message
                    r_msg['reply_msg'] = reply_text
                    logging.info(json.dumps(r_msg , ensure_ascii=False , indent=2))

                    ### LINE push message
                    messaging_api.push_message(
                        PushMessageRequest(
                            to=user_id,
                            messages=[
                                TextMessage(text=reply_text)
                            ]
                        )
                    )
                except Exception as e:
                    logging.error(f"[Error] handler text - push message : {str(e)}")

            else:

                dao.save_line_user_sonbor_db(user_name , user_id , company_name)

                ### LINE reply text
                reply_text = f"您好 , \U0001F464 {user_name} , \u2705 歡迎加入 {company_name} Line 官方帳號"
                
                ### server reply message
                r_msg['reply_msg'] = reply_text
                logging.info(json.dumps(r_msg , ensure_ascii=False , indent=2))

                ### LINE reply message
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
    
    ############
    # User 
    ############
    source_type = event.source.type  # 'user', 'group', or 'room'

    if source_type == 'user':
        
        user_id = event.source.user_id

        profile = get_user_profile(user_id)
        total_quota, used_quota, remaining = get_quota()

        user_name = profile.display_name if profile else "User"
        
        company_name = dao.res_line_uid_data(user_id)

        r_msg = {
                    'msg':'收到貼圖',
                    'company':company_name,
                    'username':user_name,
                    'uid':user_id,
                    'Total quote':total_quota,
                    'Used quote':used_quota,
                    'Remaining':remaining,
                    'reply_msg':''
        } 
        
        ### save to sonbor db
        if not company_name or company_name.strip().lower() == 'null':
            
            try:
                ### LINE reply text
                reply_text = f"您好 , {user_name} \n📢 請輸入廠商名稱 ==> [廠商]松柏資訊"

                ### server reply message
                r_msg['reply_msg'] = reply_text
                logging.info(json.dumps(r_msg , ensure_ascii=False , indent=2))

                ### LINE push message
                messaging_api.push_message(
                    PushMessageRequest(
                        to=user_id,
                        messages=[
                            TextMessage(text=reply_text)
                        ]
                    )
                )
            except Exception as e:
                logging.error(f"[Error] handler text - push message : {str(e)}")

        else:

            dao.save_line_user_sonbor_db(user_name , user_id , company_name)
        
            ### LINE reply text
            reply_text = f"您好 , \U0001F464 {user_name} , \u2705 歡迎加入 {company_name} Line 官方帳號"
            
            ### server reply message
            r_msg['reply_msg'] = reply_text
            logging.info(json.dumps(r_msg , ensure_ascii=False , indent=2))

            ### LINE reply message
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
    
   ############
    # User 
    ############
    source_type = event.source.type  # 'user', 'group', or 'room'

    if source_type == 'user':
        
        user_id = event.source.user_id

        profile = get_user_profile(user_id)
        total_quota, used_quota, remaining = get_quota()

        user_name = profile.display_name if profile else "User"
        
        company_name = dao.res_line_uid_data(user_id)

        r_msg = {
                    'msg':'收到圖片',
                    'company':company_name,
                    'username':user_name,
                    'uid':user_id,
                    'Total quote':total_quota,
                    'Used quote':used_quota,
                    'Remaining':remaining,
                    'reply_msg':''
        } 

        
        ### save to sonbor db
        if not company_name or company_name.strip().lower() == 'null':
            
            try:
                ### LINE reply text
                reply_text = f"您好 , {user_name} \n📢 請輸入廠商名稱 ==> [廠商]松柏資訊"

                ### server reply message
                r_msg['reply_msg'] = reply_text
                logging.info(json.dumps(r_msg , ensure_ascii=False , indent=2))

                ### LINE push message
                messaging_api.push_message(
                    PushMessageRequest(
                        to=user_id,
                        messages=[
                            TextMessage(text=reply_text)
                        ]
                    )
                )
            except Exception as e:
                logging.error(f"[Error] handler text - push message : {str(e)}")

        else:

            dao.save_line_user_sonbor_db(user_name , user_id , company_name)
        
            ### LINE reply text
            reply_text = f"您好 , \U0001F464 {user_name} , \u2705 歡迎加入 {company_name} Line 官方帳號"
            
            ### server reply message
            r_msg['reply_msg'] = reply_text
            logging.info(json.dumps(r_msg , ensure_ascii=False , indent=2))

            ### LINE reply message
            messaging_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=reply_text)]
                )
            )


########################################
# webhook handler - unsupport message
########################################
@handler.add(MessageEvent)
def handle_unknown(event):
    
    ############
    # User 
    ############
    source_type = event.source.type  # 'user', 'group', or 'room'

    if source_type == 'user':
        
        user_id = event.source.user_id

        profile = get_user_profile(user_id)
        total_quota, used_quota, remaining = get_quota()

        user_name = profile.display_name if profile else "User"
        
        company_name = dao.res_line_uid_data(user_id)

        r_msg = {
                    'msg':'收到不支援',
                    'company':company_name,
                    'username':user_name,
                    'uid':user_id,
                    'Total quote':total_quota,
                    'Used quote':used_quota,
                    'Remaining':remaining,
                    'reply_msg':''
        } 
        
        ### save to sonbor db
        if not company_name or company_name.strip().lower() == 'null':
            
            try:
                
                ### LINE reply text
                reply_text = f"您好 , {user_name} \n📢 請輸入廠商名稱 ==> [廠商]松柏資訊"

                ### server reply message
                r_msg['reply_msg'] = reply_text
                logging.info(json.dumps(r_msg , ensure_ascii=False , indent=2))
                
                ### LINE push message
                messaging_api.push_message(
                    PushMessageRequest(
                        to=user_id,
                        messages=[
                            TextMessage(text=reply_text)
                        ]
                    )
                )
            except Exception as e:
                logging.error(f"[Error] handler text - push message : {str(e)}")

        else:

            dao.save_line_user_sonbor_db(user_name , user_id , company_name)
        
            ### line reply message
            reply_text = f"您好 , \U0001F464 {user_name} , \u2705 歡迎加入 {company_name} Line 官方帳號"

            ### server reply message
            r_msg['reply_msg'] = reply_text
            logging.info(json.dumps(r_msg , ensure_ascii=False , indent=2))

            ### LINE reply message
            messaging_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=reply_text)]
                )
            )



#####################################################################################################################################################################################################################
#
# Main
#
#####################################################################################################################################################################################################################
if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")


