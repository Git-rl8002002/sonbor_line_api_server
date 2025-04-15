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
import pymysql , pyodbc , logging , requests , time , json

#####################################################################################################################################################################################################################
#
#
# dao          
#
#####################################################################################################################################################################################################################
class dao:
        
        ##############
        # parameters
        ##############
        para = {
                ### line token 1 - sonbor 
                'company'           :'松柏資訊 - LINE messaging API Aerver',
                'push_msg_api_url'  :'https://97b5-211-75-138-129.ngrok-free.app/push_msg', # push LINE message api url 
                'warning_threshold' : 10, # 當剩餘訊息低於這數字時提醒
                'line_bot_api_token':'/Cnorb4qfJULKMlvrO9RPPhWNk/jrlArOm0T6I3P/B5Er5x+bwUJ4A8vdOzUFM+cDnZF/GPdGEZx5lHnVM180363k15zOedERjYFz5f0itcIxADCquDM/o1hjKAWCLm/l5m0+G5/wCgEJ9to8LivHwdB04t89/1O/w1cDnyilFU=' ,
                'handler_key'       :'cf22f3a7026c0643b5e6aa4891ed761d',
                'admin_uid'         :'Udc1fafeaa808c292cbed3f1542ec15b3',
                'user1_uid'         :'U6c62b506b6a6eb52427be571dfdf2b5d', # for test use  (is jasonhung UID)
               
                ### customer - MSSQL
                'mssql_driver_old':'SQL Server Native Client 10.0',
                'mssql_driver'    :'ODBC Driver 17 for SQL Server',
                'mssql_host'      :'192.168.1.12',
                'mssql_db'        :'柏豐new1',
                'mssql_uid'       :'sbi',
                'mssql_pwd'       :'22643364',

                ### sonbor - MSSQL
                'sb_mssql_driver_old':'SQL Server Native Client 10.0',
                'sb_mssql_driver'    :'ODBC Driver 17 for SQL Server',
                'sb_mssql_host'      :r'192.168.1.12\sql2008',
                'sb_mssql_db'        :'公司用進銷存',
                'sb_mssql_uid'       :'sbi',
                'sb_mssql_pwd'       :'22643364',
                'sb_mssql_tb1'       :'line_user',      # 紀錄 各公司及UID
                'sb_mssql_tb2'       :'line_api_usage',  # 紀錄 各公司 push LINE message usage

                ### sonbor - MSSQL
                #'mssql_driver_old':'SQL Server Native Client 10.0',
                #'mssql_driver'    :'ODBC Driver 17 for SQL Server',
                #'mssql_host'      :'192.168.1.12',
                #'mssql_db'        :'柏豐new1',
                #'mssql_uid'       :'sbi',
                #'mssql_pwd'       :'22643364',
                
                ### sonbor - MySQL
                'sb_mysql_host'   :'localhost',
                'sb_mysql_port'   :3306,
                'sb_mysql_db'     :'sonbor_erp',
                'sb_mysql_uid'    :'root',
                'sb_mysql_pwd'    :'sbin3364',
                'sb_mysql_charset':'utf8mb4'
                }
        
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
                        self.line_bot_api = LineBotApi(self.para['line_bot_api_token'])
                        self.handler      = WebhookHandler(self.para['handler_key'])
                
                except Exception as e:
                        logging.info(f"\n[ Error ]  __init__ : \n\t{str(e)}\n")

                finally:
                       pass

        
        ##################
        # show_dao_para
        ##################
        def show_dao_para(self):

                try:
                        logging.info(json.dumps(self.para , ensure_ascii=False , indent=2))

                except Exception as e:
                        logging.error(f"[Error] show_dao_para : {str(e)}")
                
                finally:
                        pass

        ##################
        # test_push_msg
        ##################
        def test_push_msg(self):
                
                url = dao.para['push_msg_api_url']
                
                self.__connect_mssql_sonbor__()

                try:
                        sql = """
                                SELECT c_uid FROM [公司用進銷存].[dbo].[line_user]
                        """
                        self.curr_mssql_sonbor.execute(sql)
                        res = self.curr_mssql_sonbor.fetchall()

                        for i , v in enumerate(res , start=1):

                                try:
                                        payload = {
                                                        'r_a_id': v[0],                    
                                                        'p_msg': f'(測試訊息) 訂單編號 {range(0,1000)} , 已於 {self.time_response('datetime')} 出貨完成'
                                        }
                                        
                                        p_res = requests.post(url , data=payload)
                                        
                                        logging.info(f" [回應] {p_res.status_code} , {p_res.text}")

                                except requests.exceptions.RequestException as e:
                                        error_log = {
                                                "index":i,
                                                "uid":v[0],
                                                "status":"failed",
                                                "error":str(e)
                                        } 

                                        logging.error(f"[Error] {json.dumps(error_log , ensure_ascii=False , indent=2)}")

                except Exception as e:
                        logging.error(f"\n[ Error ]  test_push_msg : \n\t{str(e)}\n")

                finally:
                        self.__disconnect_mssql_sonbor__()
        
        #############################
        # get_line_account_profile
        #############################
        def get_line_account_profile(self , r_a_id , item):
                
                try:
                        ### user profile
                        user_profile = self.line_bot_api.get_profile(r_a_id)

                        return {
                                "user_name":user_profile.display_name,
                                "user_id":user_profile.user_id,
                                "user_icon":user_profile.picture_url,
                                "user_status":user_profile.status_message
                        }.get(item)
                        
                except LineBotApiError as e:
                        logging.error(f"[LINE API Error] get_line_account_profile failed for user {r_a_id}")
                        logging.error(f"Status: {e.status_code}, Message: {e.error.message}, Request ID: {e.request_id}")
                        return None

                except Exception as e:
                        logging.error(f"[Unexpected Error] get_line_account_profile: {str(e)}")
                        return None

        ########################################
        # push_message_v2 - line bot sdk v2.0
        ########################################
        def push_message_v2(self , r_a_id , p_message):

                ### variables
                admin_user_id = dao.para['admin_uid']
                user_user_id  = r_a_id
                push_msg      = p_message 
                
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
                        if remaining < self.para['warning_threshold']:
                                
                                self.line_bot_api.push_message(
                                        admin_user_id,
                                        TextSendMessage(text=f"⚠️ 訊息剩餘 {remaining} 則，請注意！")
                                )

                        else:
                                ### update line user data
                                #self.save_line_data_db(user_name , user_id)
                                
                                ### update LINE user data
                                company_name = self.res_line_uid_data(user_id)
                                self.save_line_user_sonbor_db(user_name , user_id , company_name)

                                ### save push LINE message data to sonbor mssql
                                self.save_line_push_msg_db(company_name , user_name , user_id , push_msg) 


                                ### push message to user
                                if user_user_id == "U6c62b506b6a6eb52427be571dfdf2b5d":
                                        
                                        p_t_msg =f"⚠️ 訊息剩餘 {total_quota} - {used_quota} = {remaining}\n您好 , {user_name}\n📢{push_msg}"

                                        self.line_bot_api.push_message(
                                                user_user_id,
                                                messages=[
                                                                #ImageSendMessage(
                                                                #                original_content_url=user_icon,
                                                                #                preview_image_url=user_icon
                                                                #),
                                                                TextSendMessage(text=p_t_msg)
                                                ]
                                        )

                                        return True
                                else:

                                        p_t_msg =f"您好 , {user_name}\n📢{push_msg}"

                                        self.line_bot_api.push_message(
                                                user_user_id,
                                                messages=[
                                                                #ImageSendMessage(
                                                                #                original_content_url=user_icon,
                                                                #                preview_image_url=user_icon
                                                                #),
                                                                TextSendMessage(text=p_t_msg)
                                                ]
                                        )

                                        return True

                except LineBotApiError as e:
                        logging.error(f"\n[Error] Line Bot api : \n\t{e.status_code}, {str(e.error.message)}")
                        logging.error(f"\n[Error] Line Bot api Detail : \n\t{str(e.error.details)}")

                finally:
                       pass

        ###################
        # get_mssql_data
        ###################
        def get_mssql_data(self):

                self.__connect_mssql__()

                try:
                        sql = """
                                SELECT * FROM [柏豐new1].[dbo].[LINE]
                        """
                        self.curr_mssql.execute(sql)
                        res = self.curr_mssql.fetchall()

                        # 取回結果
                        for val in res:
                                print(val)

                except Exception as e:
                     logging.error(f"\n[ Error ]  get_mssql_data : \n\t{str(e)}\n")

                finally:
                        self.__connect_mssql__()


        #########################
        # res_line_uid_data
        #########################
        def res_line_uid_data(self , uid):
                
                
                ### customer - mssql
                self.__connect_mssql_sonbor__()

                try:    
                        #####################
                        # customer - mssql
                        #####################
                        sql2 = """
                                SELECT c_company FROM [公司用進銷存].[dbo].[line_user] WHERE c_uid = ?
                        """
                        
                        self.curr_mssql_sonbor.execute(sql2 , (uid,))
                        res = self.curr_mssql_sonbor.fetchone()

                        return res[0]

                except Exception as e:
                       logging.error(f"\n[ Error ]  res_line_uid_data : \n\t{str(e)}\n")

                finally:
                        ### customer mssql
                        self.__disconnect_mssql_sonbor__()

        #########################
        # save_line_push_msg_db
        #########################
        def save_line_push_msg_db(self , company , uname , uid , p_msg):
                
                
                ### customer - mssql
                self.__connect_mssql_sonbor__()

                try:    
                        #####################
                        # customer - mssql
                        #####################
                        sql2 = """
                                INSERT INTO [公司用進銷存].[dbo].[line_api_usage] (r_datetime , r_year , r_month , r_day , r_time ,  c_name , c_uid , c_company , c_p_msg) 
                                                                          VALUES (? , ? , ? , ? , ? , ? , ? , ? , ?)
                        """
                        
                        self.curr_mssql_sonbor.execute(sql2 , (self.time_response('datetime'),self.time_response('year'),self.time_response('month'),self.time_response('day'),self.time_response('time'), uname , uid , company , p_msg,))
                        self.conn_mssql_sonbor.commit()
                        return 1

                except Exception as e:
                       logging.error(f"\n[ Error ]  save_line_push_msg_db : \n\t{str(e)}\n")

                finally:
                        ### customer mssql
                        self.__disconnect_mssql_sonbor__()

        #############################
        # save_line_user_sonbor_db
        #############################
        def save_line_user_sonbor_db(self , uname , uid , company):
              
                ### customer - mssql
                self.__connect_mssql_sonbor__()

                try:
                      
                        #####################
                        # customer - mssql
                        #####################
                        sql = """
                                SELECT * FROM line_user WHERE c_uid=?
                        """
                        self.curr_mssql_sonbor.execute(sql , (uid,))
                        res = self.curr_mssql_sonbor.fetchone()

                        if res is None:
                                
                                #####################
                                # customer - mssql
                                #####################
                                sql2 = """
                                        INSERT INTO line_user (c_name , c_uid , c_company) VALUES (? , ? , ?)
                                """
                                
                                self.curr_mssql_sonbor.execute(sql2 , (uname, uid, company,))
                                self.conn_mssql_sonbor.commit()
                                return 1
                        
                        else:
                                #####################
                                # customer - mssql
                                #####################
                                sql3 = """
                                        UPDATE line_user SET c_name=? , c_company=? WHERE c_uid=?
                                """

                                self.curr_mssql_sonbor.execute(sql3 , (uname, company, uid,))
                                self.conn_mssql_sonbor.commit()
                                return 1

                except Exception as e:
                       logging.error(f"\n[ Error ]  save_line_user_sonbor_db : \n\t{str(e)}\n")

                finally:
                        ### customer mssql
                        self.__disconnect_mssql_sonbor__()


        #########################
        # save_line_data_db
        #########################
        def save_line_data_db(self , uname , uid):
                
                ### save to test database - MySQL
                #self.__connect_mysql__()
                
                ### customer - mssql
                self.__connect_mssql__()

                try:
                        ########################
                        # sonbor test - mysql
                        ########################
                        #sql = "SELECT * FROM line_message_api WHERE c_uid = %s"
                        #self.curr_mysql.execute(sql, (uid,))
                        #res = self.curr_mysql.fetchone()

                        #####################
                        # customer - mssql
                        #####################
                        sql = """
                                SELECT * FROM LINE WHERE UID = ?
                        """
                        self.curr_mssql.execute(sql , (uid,))
                        res = self.curr_mssql.fetchone()

                        if res is None:
                                
                                #####################
                                # customer - mssql
                                #####################
                                sql2 = """
                                        INSERT INTO LINE (NAME , UID) VALUES (? , ?)
                                """
                                
                                self.curr_mssql.execute(sql2 , (uname , uid,))
                                self.conn_mssql.commit()
                                return 1

                                ########################
                                # sonbor test - mysql
                                ########################
                                #sql2 =  """
                                #        INSERT INTO line_message_api (r_datetime, c_user, c_uid, c_status) VALUES (%s, %s, %s, 'ok')
                                #        """
                                #self.curr_mysql.execute(sql2, (self.time_response('datetime'),uname,uid))
                                #self.conn_mysql.commit()
                                #return 1
                        
                        else:
                                #####################
                                # customer - mssql
                                #####################
                                sql3 = """
                                        UPDATE LINE SET NAME=? WHERE UID=?
                                """

                                self.curr_mssql.execute(sql3 , (uname , uid,))
                                self.conn_mssql.commit()
                                return 1

                                ########################
                                # sonbor test - mysql
                                ########################
                                #sql3 = """
                                #        update line_message_api set c_user=%s where c_uid=%s
                                #        """
                                #self.curr_mysql.execute(sql3, (uname , uid))
                                #self.conn_mysql.commit()

                                #return 1
        
                except Exception as e:
                       logging.error(f"\n[ Error ]  save_line_data_db : \n\t{str(e)}\n")

                finally:
                        ### sonbor test - mysql
                        #self.__disconnect_mysql__()

                        ### customer mssql
                        self.__disconnect_mssql__()


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
                        logging.info(f"\n[ Error ]  get_mysql_data : \n\t{str(e)}\n")

                finally:
                        self.__disconnect_mysql__()
        

        #########################
        # time_response
        #########################
        def time_response(self , item):
                
                try:
                        return {
                                "date":     time.strftime("%Y-%m-%d", time.localtime()),
                                "datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                "year":     time.strftime("%Y", time.localtime()),
                                "month":    time.strftime("%m", time.localtime()),
                                "day":      time.strftime("%d", time.localtime()),
                                "time":     time.strftime("%H:%M:%S", time.localtime())
                        }.get(item)
                
                except Exception as e:
                        logging.error(f"\n[ Error ] time_response : \n\t{str(e)}\n")
                

        #########################
        # connect mssql sonbor
        #########################
        def __connect_mssql_sonbor__(self):
                
                try:
                        conn_mssql = (
                                f"DRIVER={self.para['sb_mssql_driver_old']};"
                                f"SERVER={self.para['sb_mssql_host']};"
                                f"DATABASE={self.para['sb_mssql_db']};"
                                f"UID={self.para['sb_mssql_uid']};"
                                f"PWD={self.para['sb_mssql_pwd']}"
                        )

                        self.conn_mssql_sonbor = pyodbc.connect(conn_mssql)
                        self.curr_mssql_sonbor = self.conn_mssql_sonbor.cursor()

                except Exception as e:
                        logging.info(f"\n[ Error ]  __connect_mssql_sonbor__ : \n\t{str(e)}\n")

                finally:
                        pass

        ############################
        # disconnect mssql sonbor  
        ############################
        def __disconnect_mssql_sonbor__(self):
                
                try:
                        self.curr_mssql_sonbor.close()
                        self.conn_mssql_sonbor.close()
                
                except Exception as e:
                        logging.error(f"\n[ Error ]  __disconnect_mssql_sonbor__ : \n\t{str(e)}\n")

                finally:
                        pass

        ##################
        # connect mssql
        ##################
        def __connect_mssql__(self):
                
                try:
                        conn_mssql = f"DRIVER={self.para['mssql_driver_old']};SERVER={self.para['mssql_host']};DATABASE={self.para['mssql_db']};UID={self.para['mssql_uid']};PWD={self.para['mssql_pwd']}"  
                        self.conn_mssql = pyodbc.connect(conn_mssql)
                        self.curr_mssql = self.conn_mssql.cursor()

                except Exception as e:
                        logging.error(f"\n[ Error ]  __connect_mssql__ : \n\t{str(e)}\n")

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
                        logging.info(f"\n[ Error ]  __disconnect_mssql__ : \n\t{str(e)}\n")

                finally:
                        pass

        ##################
        # connect mysql
        ##################
        def __connect_mysql__(self):
                
                try:
                        self.conn_mysql = pymysql.connect(host=self.para['sb_mysql_host'],port=self.para['sb_mysql_port'],user=self.para['sb_mysql_uid'],password=self.para['sb_mysql_pwd'],database=self.para['sb_mysql_db'],charset=self.para['sb_mysql_charset'])
                        self.curr_mysql = self.conn_mysql.cursor()

                except Exception as e:
                 logging.error(f"\n[ Error ]  __connect_mysql__ : \n\t{str(e)}\n")

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
                        logging.error(f"\n[ Error ]  __disconnect_mysql__ : \n\t{str(e)}\n")

                finally:
                        pass

                
    





