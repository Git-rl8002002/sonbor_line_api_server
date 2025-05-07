#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Date        : 20250407
# update      : 20250505
# Author      : Jason Hung
# Version     : V2.0
# Description : SonBor Line Messaging API - LINE SDK v3 寫法


##########################
#
# line bot sdk ver 3.0
#
##########################
from flask import Flask, request, abort , jsonify , render_template
from linebot import LineBotApi
from linebot.v3.webhook import WebhookHandler
from linebot.v3.messaging import MessagingApi, ReplyMessageRequest, TextMessage , Configuration , PushMessageRequest
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, MessagingApiBlob
from linebot.v3.webhooks import MessageEvent, TextMessageContent, StickerMessageContent, ImageMessageContent
from linebot.v3.exceptions import InvalidSignatureError          
from linebot.v3.messaging.exceptions import ApiException , NotFoundException     
from linebot.v3.messaging.api_client import ApiClient
from linebot.v3.messaging.configuration import Configuration
from linebot.v3.messaging.models import RichMenuSize
from linebot.v3.messaging import RichMenuSize,RichMenuArea, RichMenuBounds,URIAction

from linebot.v3.messaging.models import RichMenuRequest, RichMenuArea, RichMenuBounds, MessageAction, PostbackAction
from linebot.v3.messaging.models.uri_action import URIAction

import traceback , logging , json , requests , control.config
from control.dao import dao

dao = dao()

app = Flask(__name__)

##############################
# line bot - token / secret
##############################
config              = Configuration(access_token=control.config.para['line_bot_api_token'])
handler             = WebhookHandler(control.config.para['handler_key'])
api_client          = ApiClient(configuration=config)
messaging_api       = MessagingApi(api_client)
messaging_api_blob  = MessagingApiBlob(api_client)


########
# log
########
log_format = "%(asctime)s %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S",
                    handlers=[
                            logging.FileHandler("line_api_server.log"),     # 寫入本地 .log 檔案
                            logging.StreamHandler()                         # 同時也印出來（WSGI Server 可接收）
                            ]       
                    )


###################
#
# LINE rich menu
#
###################
### 建立 Rich Menu
def create_rich_menu(messaging_api):
    try:
        rich_menu = RichMenuRequest(
            size=RichMenuSize(width=2500, height=843),
            selected=True,
            name="Main Menu",
            chat_bar_text="開啟選單",
            areas=[
                RichMenuArea(
                    bounds=RichMenuBounds(x=0, y=0, width=1250, height=843),
                    action=URIAction(uri=control.config.para['api_add_url'])
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=1250, y=0, width=1250, height=843),
                    action=URIAction(uri=control.config.para['api_statistics_url'])
                )

            ]
        )
        response = messaging_api.create_rich_menu(rich_menu)
        rich_menu_id = response.rich_menu_id
        print(f"[成功] Rich Menu Created, ID: {rich_menu_id}")
        return rich_menu_id
    except Exception as e:
        print("[錯誤] 建立 Rich Menu 失敗，錯誤訊息：", str(e))
        traceback.print_exc()
        return None

### 上傳 Rich Menu 圖片
def upload_rich_menu_image(rich_menu_id, image_path, channel_access_token):
    headers = {
        "Authorization": f"Bearer {channel_access_token}",
    }

    if image_path.lower().endswith((".jpg", ".jpeg")):
        content_type = "image/jpeg"
    elif image_path.lower().endswith(".png"):
        content_type = "image/png"
    else:
        raise ValueError("圖片必須是 .jpg 或 .png 格式")

    headers["Content-Type"] = content_type

    with open(image_path, 'rb') as f:
        image_data = f.read()

    url = f"https://api-data.line.me/v2/bot/richmenu/{rich_menu_id}/content"  # 注意 domain
    response = requests.post(url, headers=headers, data=image_data)

    if response.status_code == 200:
        print(f"[成功] 圖片成功上傳到 Rich Menu: {rich_menu_id}")
        return True
    else:
        print(f"[錯誤] 上傳失敗，狀態碼 {response.status_code}, 回傳訊息: {response.text}")
        return False


### 設為預設
def set_default_rich_menu(messaging_api, rich_menu_id):
    try:
        messaging_api.set_default_rich_menu(rich_menu_id)
        print(f"[成功] 設定 Rich Menu {rich_menu_id} 為預設選單")
    except Exception as e:
        print("[錯誤] 設定預設 Rich Menu 失敗")
        traceback.print_exc()

### 主流程
def setup_rich_menu(image_path, channel_access_token):
    configuration = Configuration(access_token=channel_access_token)
    
    with ApiClient(configuration) as api_client:
        messaging_api = MessagingApi(api_client)

        rich_menu_id = create_rich_menu(messaging_api)
        if not rich_menu_id:
            print("[錯誤] 建立 Rich Menu 失敗，停止流程")
            return

        success = upload_rich_menu_image(rich_menu_id, image_path, channel_access_token)
        if success:
            set_default_rich_menu(messaging_api, rich_menu_id)
        else:
            print("[錯誤] 上傳圖片失敗，停止流程")
                


channel_access_token = control.config.para['line_bot_api_token']
image_path           = control.config.para['menu_img_path']  # 你的圖片路徑

####################################
#
# 設定 rich menu ( 需要換圖再開啟 )
#
####################################
#setup_rich_menu(image_path, channel_access_token)


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


#################
# /favicon.ico
#################
@app.route('/favicon.ico')
def favicon():
    return '', 204  # 回傳「無內容」的狀態碼


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
        r_a_id      = request.form.get('r_a_id')
        r_a_company = request.form.get('r_a_company')
        p_msg       = request.form.get('p_msg')

        check_uid = dao.is_valid_uid(r_a_id)

        ### receiver User profile 
        r_a_name  = dao.get_line_account_profile(r_a_id , 'user_name') or "unknow line username"
        r_name    = dao.res_line_uid_data2(r_a_id, r_a_company, 'name') or "unknow UID "
        r_company = dao.res_line_uid_data2(r_a_id, r_a_company, 'company') or "unknow company name"

        if check_uid == False:
            
                r_j_msg = {
                            "line_api": "active push message",
                            "status": "failed",
                            "e_msg": "wrong UID format"
                    }
                    
                logging.warning(json.dumps(r_j_msg, ensure_ascii=False, indent=2))
                return jsonify(r_j_msg), 500
        
        elif r_name == "fail":
           
            r_j_msg = {
                            "line_api": "active push message",
                            "status": "failed",
                            "e_msg": "unknow UID"
                    }
                    
            logging.info(json.dumps(r_j_msg, ensure_ascii=False, indent=2))
            return jsonify(r_j_msg), 500

        elif r_company == 'fail':
                
            r_j_msg = {
                    "line_api": "active push message",
                    "status": "failed",
                    "e_msg": "unknow company name"
            }
                
            logging.warning(json.dumps(r_j_msg, ensure_ascii=False, indent=2))
            return jsonify(r_j_msg), 500
        
        else:
            
            ### response json 
            r_j_msg = { 
                        "line_api":'active push message',
                        "r_company":r_company,
                        "r_a_name":r_a_name, 
                        "r_a_id":r_a_id,  
                        "p_msg":p_msg,
                        "status":"successfully"
                    }

            ### active push mesage
            if dao.push_message_v2(r_a_id, p_msg) == True:
            
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


#####################
# /test
#####################
@app.route("/test", methods=["POST"])
def test():
    
    q_company = request.form.get('company')
    q_year    = request.form.get('year')
    q_month   = request.form.get('month')

    res_dict = dao.res_total_line_api_uid_by_company(q_company)

    res_json = json.dumps(res_dict , ensure_ascii=False , indent=2)

    logging.info(res_json)
            
    return render_template('ajax/a_test.html', q_company=q_company, q_year=q_year, q_month=q_month)


#####################
# /add
#####################
@app.route("/add")
def add():
    
    title           = f"{control.config.para['company']}"
    server_name     = control.config.para['server_name']
    copyright       = control.config.para['copyright']

    return render_template('add.html', title=title, server_name=server_name, copyright=copyright)


########################
# /a_login_statistics
########################
@app.route("/a_login_statistics", methods=["POST"])
def a_login_statistics():
    
    title           = f"{control.config.para['company']}"
    server_name     = control.config.para['server_name']
    copyright       = control.config.para['copyright']

    e_msg = "登入密碼更新完成 , 下次請用新密碼登入 , 感謝您"

    l_company = request.form.get('l_company')
    l_pwd     = request.form.get('l_pwd')

    res_company = dao.total_line_user_company_sonbor_db()
    res = dao.alter_login_line_user_company_sonbor_db(l_company, l_pwd)

    if res == 'ok':

        # push msg total amount
        query_total_line_push_msg_by_company_amount  = dao.query_total_line_push_msg_by_company_amount(l_company)
        query_total_line_push_msg_by_company_amount2 = dao.query_total_line_push_msg_by_company_amount2(l_company)

        # UID total amount
        query_total_line_uid_by_company  = dao.query_total_line_uid_by_company(l_company)
        query_total_line_uid_by_company2 = dao.query_total_line_uid_by_company2(l_company)

        return render_template('ajax/a_login_statistics.html', title=title, server_name=server_name, copyright=copyright, 
                               l_company=l_company, query_total_line_push_msg_by_company_amount=query_total_line_push_msg_by_company_amount,
                               query_total_line_push_msg_by_company_amount2=query_total_line_push_msg_by_company_amount2,
                               query_total_line_uid_by_company=query_total_line_uid_by_company,
                               query_total_line_uid_by_company2=query_total_line_uid_by_company2, e_msg=e_msg
                               )
    else:
        return render_template('statistics.html', title=title, server_name=server_name, copyright=copyright, e_msg=e_msg, 
                               res_company=res_company)

#####################
# /login_statistics
#####################
@app.route("/login_statistics", methods=["POST"])
def login_statistics():
    
    title           = f"{control.config.para['company']}"
    server_name     = control.config.para['server_name']
    copyright       = control.config.para['copyright']

    e_msg = "抱歉 , 目前沒有此公司資料 , 請先加入再使用 ! 感謝您"

    l_company = request.form.get('l_company')
    l_pwd     = request.form.get('l_pwd')

    res_company = dao.total_line_user_company_sonbor_db()
    res = dao.login_line_user_company_sonbor_db(l_company, l_pwd)

    if res:

        # push msg total amount
        query_total_line_push_msg_by_company_amount  = dao.query_total_line_push_msg_by_company_amount(l_company)
        query_total_line_push_msg_by_company_amount2 = dao.query_total_line_push_msg_by_company_amount2(l_company)

        # UID total amount
        query_total_line_uid_by_company  = dao.query_total_line_uid_by_company(l_company)
        query_total_line_uid_by_company2 = dao.query_total_line_uid_by_company2(l_company)

        return render_template('ajax/a_login_statistics.html', title=title, server_name=server_name, copyright=copyright, 
                               l_company=l_company, query_total_line_push_msg_by_company_amount=query_total_line_push_msg_by_company_amount,
                               query_total_line_push_msg_by_company_amount2=query_total_line_push_msg_by_company_amount2,
                               query_total_line_uid_by_company=query_total_line_uid_by_company,
                               query_total_line_uid_by_company2=query_total_line_uid_by_company2
                               )
    else:
        return render_template('statistics.html', title=title, server_name=server_name, copyright=copyright, e_msg=e_msg, 
                               res_company=res_company)

#####################
# /statistics
#####################
@app.route("/statistics")
def statistics():
    
    title           = f"{control.config.para['company']}"
    server_name     = control.config.para['server_name']
    copyright       = control.config.para['copyright']

    res_company = dao.total_line_user_company_sonbor_db()
            
    return render_template('statistics.html', title=title, server_name=server_name, copyright=copyright, res_company=res_company)


#####################
# /query_uid
#####################
@app.route("/query_uid", methods=["POST"])
def query_uid():
    
    q_company = request.form.get('q_company')

    res_dict = dao.res_total_line_api_uid_by_company(q_company)

    res_json = json.dumps(res_dict , ensure_ascii=False , indent=2)

    logging.info(res_json)
            
    return render_template('ajax/a_query_uid.html', res_uid=res_json)

#####################
# /del_uid_statistics
#####################
@app.route("/del_uid_statistics", methods=["POST"])
def del_uid_statistics():
    
    title   = control.config.para['company']
    company = request.form.get('company')
    id      = request.form.get('id')
    uid     = request.form.get('uid')


    res_uid = dao.del_line_uid(company, id, uid)

    return res_uid

###########################
# /reload_uid_statistics2
###########################
@app.route("/reload_uid_statistics2", methods=["POST"])
def reload_uid_statistics2():
    
    company = request.form.get('company')
    
    uid_data          = dao.res_server_line_uid_data2(company)
    query_total_line_uid_by_company2 = dao.query_total_line_uid_by_company2(company)

    return render_template('ajax/a_reload_uid_statistics2.html', uid_data=uid_data, query_total_line_uid_by_company2=query_total_line_uid_by_company2) 


###########################
# /reload_uid_statistics
###########################
@app.route("/reload_uid_statistics", methods=["POST"])
def reload_uid_statistics():
    
    uid_data          = dao.res_server_line_uid_data()

    return render_template('ajax/a_reload_uid_statistics.html', uid_data=uid_data)  


#####################
# /uid_statistics
#####################
@app.route("/uid_statistics", methods=["POST"])
def uid_statistics():
    
    title   = control.config.para['company']
    company = request.form.get('company')

    res_uid = dao.total_line_api_uid_by_company(company)

    return render_template('ajax/a_uid_statistics.html', company=company, res_uid=res_uid)    


#####################
# /push_statistics3
#####################
@app.route("/push_statistics3", methods=["POST"])
def push_statistics3():
    
    title   = control.config.para['company']
    company = request.form.get('company')
    year    = request.form.get('year')
    month   = request.form.get('month')

    by_month_push_sum2      = dao.res_total_line_api_usage_by_month2(company, year, month)
    by_month_name_push_sum2 = dao.res_total_line_api_usage_by_month3(company, year, month)


    return render_template('ajax/a_push_statistics3.html', company=company, year=year, month=month, by_month_push_sum2=by_month_push_sum2, by_month_name_push_sum2=by_month_name_push_sum2)

########################
# /push_statistics3_1
########################
@app.route("/push_statistics3_1", methods=["POST"])
def push_statistics3_1():
    
    title   = control.config.para['company']
    company = request.form.get('company')
    year    = request.form.get('year')
    month   = request.form.get('month')
    name    = request.form.get('name')

    by_year_name_push_sum3_1 = dao.res_total_line_api_usage_by_year3_1(company, year, month, name)


    return render_template('ajax/a_push_statistics3_1.html', company=company, year=year, month=month, by_year_name_push_sum3_1=by_year_name_push_sum3_1, name=name)


########################
# /push_statistics2_1
########################
@app.route("/push_statistics2_1", methods=["POST"])
def push_statistics2_1():
    
    title   = control.config.para['company']
    company = request.form.get('company')
    year    = request.form.get('year')
    name    = request.form.get('name')

    by_year_name_push_sum2_1 = dao.res_total_line_api_usage_by_year2_1(company, year , name)


    return render_template('ajax/a_push_statistics2_1.html', company=company, year=year, by_year_name_push_sum2_1=by_year_name_push_sum2_1, name=name)


#####################
# /push_statistics2
#####################
@app.route("/push_statistics2", methods=["POST"])
def push_statistics2():
    
    title   = control.config.para['company']
    company = request.form.get('company')
    year    = request.form.get('year')
    total   = request.form.get('total')

    by_year_push_sum2      = dao.res_total_line_api_usage_by_year2(company, year)
    by_year_name_push_sum2 = dao.res_total_line_api_usage_by_year3(company, year)


    return render_template('ajax/a_push_statistics2.html', company=company, year=year, by_year_push_sum2=by_year_push_sum2, by_year_name_push_sum2=by_year_name_push_sum2)

#####################
# /push_statistics
#####################
@app.route("/push_statistics", methods=["POST"])
def push_statistics():
    
    title   = control.config.para['company']
    company = request.form.get('company')

    by_year_push_sum  = dao.res_total_line_api_usage_by_year(company)
    by_month_push_sum = dao.res_total_line_api_usage_by_month(company)

    return render_template('ajax/a_push_statistics.html', company=company, by_year_push_sum=by_year_push_sum, by_month_push_sum=by_month_push_sum)


##############
# /
##############
@app.route("/")
def index():
    
    title           = f"{control.config.para['company']}"
    server_name     = control.config.para['server_name']
    copyright       = control.config.para['copyright']
    
    api_push_msg_url         = control.config.para['api_push_msg_url']
    api_push_msg_http_method = control.config.para['api_push_msg_http_method']
    api_push_msg_http_para   = control.config.para['api_push_msg_http_para']

    api_query_uid_url         = control.config.para['api_query_uid_url']
    api_query_uid_http_method = control.config.para['api_query_uid_http_method']
    api_query_uid_http_para   = control.config.para['api_query_uid_http_para']

    paras             = json.dumps(control.config.para , ensure_ascii=False , indent=2)
    uid_data          = dao.res_server_line_uid_data()
    company_api_usage = dao.res_total_line_api_company()
    push_msg_usage    = dao.res_server_line_push_msg_usage()


    # API Server log
    a_s_log = dao.tail(control.config.para['server_log_path'])
    r_a_s_log = "<pre>" + "".join(a_s_log) + "</pre>"

    # push msg total amount
    total_line_push_msg = dao.total_line_push_msg()
    total_line_push_msg_by_company = dao.total_line_push_msg_by_company()

    # UID total amount
    total_line_uid = dao.total_line_uid()
    total_line_uid_by_company = dao.total_line_uid_by_company()

    
    return render_template('index.html', 
                           title=title, paras=json.loads(paras), uid_data=uid_data,  push_msg_usage=push_msg_usage,
                           company_api_usage=company_api_usage, copyright=copyright, server_name=server_name, 
                           api_push_msg_url=api_push_msg_url,   api_push_msg_http_method=api_push_msg_http_method,   api_push_msg_http_para=api_push_msg_http_para,
                           api_query_uid_url=api_query_uid_url, api_query_uid_http_method=api_query_uid_http_method, api_query_uid_http_para=api_query_uid_http_para,
                           total_line_push_msg=total_line_push_msg, total_line_push_msg_by_company=total_line_push_msg_by_company, 
                           total_line_uid=total_line_uid, total_line_uid_by_company=total_line_uid_by_company, r_a_s_log=r_a_s_log
                           )

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

        ### 判斷是否包含 sbi
        if "sbi" in text:
            # 分割字串，抓取 sbi 後面的公司名稱
            company_name = text.split('sbi', 1)[1].strip()
                
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
            dao.save_line_user_company_sonbor_db(company_name)
        
            ### LINE reply text
            reply_text = f"您好 , \U0001F464 {user_name} , \u2705 歡迎使用 {company_name} 推播系統 "
            
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
                    reply_text = f"您好 , {user_name} \n📢 新加入的好友 , 請先輸入廠商名稱格式如下 ==> sbi松柏資訊"

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
                dao.save_line_user_company_sonbor_db(company_name)

                ### LINE reply text
                reply_text = f"您好 , \U0001F464 {user_name} , \u2705 歡迎使用 {company_name} 推播系統 "
                
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
                reply_text = f"您好 , {user_name} \n📢 新加入的好友 , 請先輸入廠商名稱格式如下 ==> sbi松柏資訊"

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
            dao.save_line_user_company_sonbor_db(company_name)
        
            ### LINE reply text
            reply_text = f"您好 , \U0001F464 {user_name} , \u2705 歡迎使用 {company_name} 推播系統 "
            
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
                reply_text = f"您好 , {user_name} \n📢 新加入的好友 , 請先輸入廠商名稱格式如下 ==> sbi松柏資訊"

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
            dao.save_line_user_company_sonbor_db(company_name)
        
            ### LINE reply text
            reply_text = f"您好 , \U0001F464 {user_name} , \u2705 歡迎使用 {company_name} 推播系統 "
            
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
                reply_text = f"您好 , {user_name} \n📢 新加入的好友 , 請先輸入廠商名稱格式如下 ==> sbi松柏資訊"

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
            dao.save_line_user_company_sonbor_db(company_name)
        
            ### line reply message
            reply_text = f"您好 , \U0001F464 {user_name} , \u2705 歡迎使用 {company_name} 推播系統 "

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



#####################
# error 404 page
#####################
@app.errorhandler(404)
def page_not_found(e):

    title           = f"{control.config.para['company']}"
    server_name     = control.config.para['server_name']
    copyright       = control.config.para['copyright']

    return render_template('404.html', title=title, server_name=server_name, copyright=copyright) , 404

#####################
# error 500 page
#####################
@app.errorhandler(500)
def page_not_found(e):

    title           = f"{control.config.para['company']}"
    server_name     = control.config.para['server_name']
    copyright       = control.config.para['copyright']

    return render_template('500.html', title=title, server_name=server_name, copyright=copyright) , 500

#####################
# error 502 page
#####################
@app.errorhandler(502)
def page_not_found(e):

    title           = f"{control.config.para['company']}"
    server_name     = control.config.para['server_name']
    copyright       = control.config.para['copyright']

    return render_template('502.html', title=title, server_name=server_name, copyright=copyright) , 502



#####################################################################################################################################################################################################################
#
# Main
#
#####################################################################################################################################################################################################################
if __name__ == "__main__":
    pass
    ### windows 使用 waitress
    #app.run(port=5000, host="0.0.0.0")


