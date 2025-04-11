#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Date        : 20250407
# update      : 20250410
# Author      : Jason Hung
# Version     : v1.0
# Description : v1.0 SonBor Line Messaging API parameters 

from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage ,ImageSendMessage
from linebot.exceptions import InvalidSignatureError , LineBotApiError
from flask import Flask , json , jsonify , request
import pymysql , pyodbc , logging , requests

#####################################################################################################################################################################################################################
#
# parameter
#
#####################################################################################################################################################################################################################
para = {
        ### line token 1 - sonbor 
        #'line_bot_api_token':'/Cnorb4qfJULKMlvrO9RPPhWNk/jrlArOm0T6I3P/B5Er5x+bwUJ4A8vdOzUFM+cDnZF/GPdGEZx5lHnVM180363k15zOedERjYFz5f0itcIxADCquDM/o1hjKAWCLm/l5m0+G5/wCgEJ9to8LivHwdB04t89/1O/w1cDnyilFU=' ,
        #'handler_key'       :'cf22f3a7026c0643b5e6aa4891ed761d',
        #'admin_uid'         :'Udc1fafeaa808c292cbed3f1542ec15b3',
        #'user_uid'          :'U6c62b506b6a6eb52427be571dfdf2b5d',
        
        ### line token 2 - jason hung
        'line_bot_api_token':'hgIwbe7Su3xEmaFBhqCG47fJ9C3AoZKjKqKP0qrDI14V8k46q9/3wN0UqidBXj6dgxIjwsEfKCA0cfeAziGl0Xl/FaB7YdsckgNXcYxTYDj97qtRGtNB6pU5vP4Cu10WTFnqKU3ZLqSTA3bLNUKhbAdB04t89/1O/w1cDnyilFU=',
        'handler_key'       :'a2344147e30cd6278dddb46cbf877b23',
        'admin_uid'         :'Ucb1af50b59c28c5200fdfde33c10bcf2',
        'user_uid'          :'Ucb1af50b59c28c5200fdfde33c10bcf2',

        ### line para
        'warning_threshold':10,  # 當剩餘訊息低於這數字時提醒
        
        ### MSSQL
        'mssql_driver':'ODBC Driver 17 for SQL Server',
        'mssql_host'  :'192.168.1.199',
        'mssql_db'    :'test_wnsh_2008',
        'mssql_uid'   :'sbi',
        'mssql_pwd'   :'22643364',
        
        ### MySQL
        'mysql_host'   :'localhost',
        'mysql_port'   :3306,
        'mysql_db'     :'sonbor_erp',
        'mysql_uid'    :'root',
        'mysql_pwd'    :'sbin3364',
        'mysql_charset':'utf8mb4'
        }


#####################################################################################################################################################################################################################

#
# dao
#
#####################################################################################################################################################################################################################
class dao:

        ########
        # log
        ########
        log_format = "%(asctime)s %(message)s"
        logging.basicConfig(format=log_format , level=logging.INFO , datefmt="%Y-%m-%d %H:%M:%S")
        #logging.disable(logging.INFO)


       
        #############
        # __init__
        #############
        def __init__(self):  
                
                try:    
                        ### line bot - token / secret
                        self.line_bot_api = LineBotApi(para['line_bot_api_token'])
                        self.handler      = WebhookHandler(para['handler_key'])
                
                except Exception as e:
                        logging.info(f"\n< ERROR > __init__ : \n\t{str(e)}\n")

                finally:
                       pass
                

        #################
        # push_message
        #################
        def push_message(self , p_a_id , r_a_id):

                ### variables
                admin_user_id = p_a_id
                user_user_id  = r_a_id
                
                ### user profile
                user_profile = self.line_bot_api.get_profile(user_user_id)
                user_name    = user_profile.display_name
                user_id      = user_profile.user_id
                user_icon    = user_profile.picture_url
                user_status  = user_profile.status_message

                # check total quote and used quote by month
                total_quota = self.line_bot_api.get_message_quota().value
                used_quota  = self.line_bot_api.get_message_quota_consumption().total_usage
                remaining   = total_quota - used_quota

                try:   
                        print(f"目前已使用 {used_quota} 則，剩餘 {remaining} 則")

                        if remaining < para['warning_threshold']:
                                
                                self.line_bot_api.push_message(
                                        admin_user_id,
                                        TextSendMessage(text=f"⚠️ 訊息剩餘 {remaining} 則，請注意！")
                                )

                        else:
                                print(f" Hi , {user_name} \n uid = {user_id} \n status_msg = {user_status} \n 訊息剩餘 {total_quota} / {remaining}。")

                                self.line_bot_api.push_message(
                                        user_user_id,
                                        messages=[
                                                        ImageSendMessage(
                                                                        original_content_url=user_icon,
                                                                        preview_image_url=user_icon
                                                        ),
                                                        TextSendMessage(text=f"Hi , {user_name} \n uid = {user_id} \n status_msg = {user_status} \n 📢 訊息剩餘 {total_quota} / {remaining}。")
                                        ]
                                )

                except LineBotApiError as e:
                        logging.info(f"\n< Error - Line Bot api > : \n\t{e.status_code}, {str(e.error.message)}")
                        logging.info(f"\n< Error - Line Bot api Detail > : \n\t{str(e.error.details)}")

                finally:
                       pass

        ###################
        # get_mssql_data
        ###################
        def get_mssql_data(self):

                self.__connect_mssql__()

                try:
                        sql = f"SELECT * FROM  [test_wnsh_2008].[dbo].[訂單作業] where 訂單單號='107010001'"
                        self.curr_mssql.execute(sql)
                        res = self.curr_mssql.fetchall()

                        # 取回結果
                        for val in res:
                                print(val)

                except Exception as e:
                     logging.info(f"\n< ERROR > get_mssql_data : \n\t{str(e)}\n")

                finally:
                        self.__connect_mssql__()

        ###################
        # get_mysql_data
        ###################
        def get_mysql_data(self):
                
                self.__connect_mysql__()

                try:
                        sql = f"SELECT c_status FROM line_message_api where c_user='U6c62b506b6a6eb52427be571dfdf2b5d'"
                        self.curr_mysql.execute(sql)
                        res = self.curr_mysql.fetchall()

                        for val in res:
                                print(val)
                
                except Exception as e:
                        logging.info(f"\n< ERROR > get_mysql_data : \n\t{str(e)}\n")

                finally:
                        self.__disconnect_mysql__()

        ##################
        # connect mssql
        ##################
        def __connect_mssql__(self):
                
                try:
                        conn_mssql = f"DRIVER={para['mssql_driver']};SERVER={para['mssql_host']};DATABASE={para['mssql_db']};UID={para['mssql_uid']};PWD={para['mssql_pwd']}"  
                        self.conn_mssql = pyodbc.connect(conn_mssql)
                        self.curr_mssql = self.conn_mssql.cursor()

                except Exception as e:
                 logging.info(f"\n< ERROR > __connect_mssql__ : \n\t{str(e)}\n")

                finally:
                        pass

        #####################
        # disconnect mssql   
        #####################
        def __disconnect_mssql__(self):
                
                try:
                        self.curr_mssql.close()
                        self.conn_mssql.close()
                
                except Exception as e:
                        logging.info(f"\n< ERROR > __disconnect_mssql__ : \n\t{str(e)}\n")

                finally:
                        pass

        ##################
        # connect mysql
        ##################
        def __connect_mysql__(self):
                
                try:
                        self.conn_mysql = pymysql.connect(host=para['mysql_host'],port=para['mysql_port'],user=para['mysql_uid'],password=para['mysql_pwd'],database=para['mysql_db'],charset=para['mysql_charset'])
                        self.curr_mysql = self.conn_mysql.cursor()

                except Exception as e:
                 logging.info(f"\n< ERROR > __connect_mysql__ : \n\t{str(e)}\n")

                finally:
                        pass

        ##################
        # disconnect mysql   
        ##################
        def __disconnect_mysql__(self):
                
                try:
                        self.curr_mysql.close()
                        self.conn_mysql.close()
                
                except Exception as e:
                        logging.info(f"\n< ERROR > __disconnect_mysql__ : \n\t{str(e)}\n")

                finally:
                        pass

                
    





