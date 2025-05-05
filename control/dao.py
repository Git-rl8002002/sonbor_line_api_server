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
import pymysql , pyodbc , logging , requests , time , json , control.config , random
 

#####################################################################################################################################################################################################################
#
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
                        self.line_bot_api = LineBotApi(control.config.para['line_bot_api_token'])
                        self.handler      = WebhookHandler(control.config.para['handler_key'])
                
                except Exception as e:
                        logging.info(f"\n[ Error ]  __init__ : \n\t{str(e)}\n")

                finally:
                       pass

        
        ##################
        # show_dao_para
        ##################
        def show_dao_para(self):

                try:
                        logging.info(json.dumps(control.config.para , ensure_ascii=False , indent=2))

                except Exception as e:
                        logging.error(f"[Error] show_dao_para : {str(e)}")
                
                finally:
                        pass

        ##################
        # test_push_msg
        ##################
        def test_push_msg(self):
                
                url = control.config.para['push_msg_api_url']
                
                self.__connect_mssql_sonbor__()

                try:
                        sql = """
                                SELECT c_uid FROM [line_notify].[dbo].[line_api_user]
                        """
                        self.curr_mssql_sonbor.execute(sql)
                        res = self.curr_mssql_sonbor.fetchall()

                        for i , v in enumerate(res , start=1):

                                try:
                                        payload = {
                                                        'r_a_id': v[0],                    
                                                        'p_msg': f'(測試訊息) 訂單編號 {random.randint(0,10000)} , 已於 {self.time_response('datetime')} 出貨完成'
                                        }
                                        
                                        p_res   = requests.post(url , data=payload)
                                        r_j_res = p_res.json()
                                        
                                        logging.info(f" [回應] {p_res.status_code}\n{json.dumps(r_j_res , ensure_ascii=False , indent=2)}")

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
                admin_user_id = control.config.para['admin_uid']
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
                        if remaining < control.config.para['warning_threshold']:
                                
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
                                #self.save_line_push_msg_db(company_name , user_name , user_id , push_msg) 


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

        #################
        # del_line_uid
        #################
        def del_line_uid(self, company, id, uid):
                
                
                ### customer - mssql
                self.__connect_mssql_sonbor__()

                try:    
                        #####################
                        # customer - mssql
                        #####################
                        sql2 = """
                                delete from [line_notify].[dbo].[line_api_user] where c_company=? and c_name=? and c_uid=?
                        """
                        
                        res = self.curr_mssql_sonbor.execute(sql2, (company, id, uid,))
                        self.curr_mssql_sonbor.commit()

                        if res.rowcount > 0:
                        
                                return 'ok'
                        else:
                                return 'no'
                        
                except Exception as e:
                       logging.error(f"\n[ Error ]  del_line_uid : \n\t{str(e)}\n")

                finally:
                        ### customer mssql
                        self.__disconnect_mssql_sonbor__()


        ########################################
        # res_total_line_api_uid_by_company
        ########################################
        def res_total_line_api_uid_by_company(self, company):
                
                
                ### customer - mssql
                self.__connect_mssql_sonbor__()

                try:    
                        #####################
                        # customer - mssql
                        #####################
                        sql2 = """
                                select c_name, c_uid from [line_notify].[dbo].[line_api_user] where c_company=?
                        """
                        
                        self.curr_mssql_sonbor.execute(sql2, (company,))
                        res = self.curr_mssql_sonbor.fetchall()

                        # 抓欄位名稱
                        columns = [col[0] for col in self.curr_mssql_sonbor.description]

                        # 將每筆資料轉成 dict
                        res_dict = [dict(zip(columns, row)) for row in res]
                        
                        return res_dict

                except Exception as e:
                       logging.error(f"\n[ Error ]  res_total_line_api_uid_by_company : \n\t{str(e)}\n")

                finally:
                        ### customer mssql
                        self.__disconnect_mssql_sonbor__()

        ########################################
        # total_line_api_uid_by_company
        ########################################
        def total_line_api_uid_by_company(self, company):
                
                
                ### customer - mssql
                self.__connect_mssql_sonbor__()

                try:    
                        #####################
                        # customer - mssql
                        #####################
                        sql2 = """
                                SELECT c_name, c_uid FROM [line_notify].[dbo].[line_api_user] where c_company=?
                        """
                        
                        self.curr_mssql_sonbor.execute(sql2, (company,))
                        res = self.curr_mssql_sonbor.fetchall() 

                        return res

                except Exception as e:
                       logging.error(f"\n[ Error ]  total_line_api_usage_by_company : \n\t{str(e)}\n")

                finally:
                        ### customer mssql
                        self.__disconnect_mssql_sonbor__()

        
        ########################################
        # res_total_line_api_usage_by_month3
        ########################################
        def res_total_line_api_usage_by_month3(self, company, year, month):
                
                
                ### customer - mssql
                self.__connect_mssql_sonbor__()

                try:    
                        #####################
                        # customer - mssql
                        #####################
                        sql2 = """
                                SELECT c_name, count(*)  FROM [line_notify].[dbo].[line_api_usage] where c_company=? and r_year=? and r_month=? group by c_name order by c_name asc;
                        """
                        
                        self.curr_mssql_sonbor.execute(sql2, (company, year, month))
                        res = self.curr_mssql_sonbor.fetchall() 

                        return res

                except Exception as e:
                       logging.error(f"\n[ Error ]  res_total_line_api_usage_by_month3 : \n\t{str(e)}\n")

                finally:
                        ### customer mssql
                        self.__disconnect_mssql_sonbor__()
        
        ########################################
        # res_total_line_api_usage_by_month2
        ########################################
        def res_total_line_api_usage_by_month2(self, company, year, month):
                
                
                ### customer - mssql
                self.__connect_mssql_sonbor__()

                try:    
                        #####################
                        # customer - mssql
                        #####################
                        sql2 = """
                                SELECT r_datetime, c_name, c_uid, c_p_msg  FROM [line_notify].[dbo].[line_api_usage] where c_company=? and r_year=? and r_month=? order by r_datetime asc;
                        """
                        
                        self.curr_mssql_sonbor.execute(sql2, (company, year, month))
                        res = self.curr_mssql_sonbor.fetchall() 

                        return res

                except Exception as e:
                       logging.error(f"\n[ Error ]  res_total_line_api_usage_by_month2 : \n\t{str(e)}\n")

                finally:
                        ### customer mssql
                        self.__disconnect_mssql_sonbor__()

        ########################################
        # res_total_line_api_usage_by_month
        ########################################
        def res_total_line_api_usage_by_month(self, company):
                
                
                ### customer - mssql
                self.__connect_mssql_sonbor__()

                try:    
                        #####################
                        # customer - mssql
                        #####################
                        sql = """
                                SELECT r_year , count(*)  FROM [line_notify].[dbo].[line_api_usage] where c_company=? group by r_year order by r_year asc;
                        """
                        
                        self.curr_mssql_sonbor.execute(sql, (company,))
                        res = self.curr_mssql_sonbor.fetchall() 

                        res_month = []

                        for val in res:
                                sql2 = """
                                        SELECT r_month , count(*)  FROM [line_notify].[dbo].[line_api_usage] where c_company=? and r_year=? group by r_month order by r_month asc;
                                """

                                self.curr_mssql_sonbor.execute(sql2, (company, val[0],))
                                res2 = self.curr_mssql_sonbor.fetchall()

                                for val2 in res2:
                                        res_month.append({'year':val[0], 'month':val2[0], 'total':val2[1]})

                        return res_month

                except Exception as e:
                       logging.error(f"\n[ Error ]  res_total_line_api_usage_by_month : \n\t{str(e)}\n")

                finally:
                        ### customer mssql
                        self.__disconnect_mssql_sonbor__()

        ########################################
        # res_total_line_api_usage_by_year3_1
        ########################################
        def res_total_line_api_usage_by_year3_1(self, company, year, month, name):
                
                
                ### customer - mssql
                self.__connect_mssql_sonbor__()

                try:    
                        #####################
                        # customer - mssql
                        #####################
                        sql2 = """
                                SELECT r_datetime, c_name, c_uid, c_p_msg  FROM [line_notify].[dbo].[line_api_usage] 
                                where c_company=? and r_year=? and r_month=? and c_name=?  order by r_datetime asc
                        """
                        
                        self.curr_mssql_sonbor.execute(sql2, (company, year, month, name,))
                        res = self.curr_mssql_sonbor.fetchall() 

                        return res

                except Exception as e:
                       logging.error(f"\n[ Error ]  res_total_line_api_usage_by_year3_1: \n\t{str(e)}\n")

                finally:
                        ### customer mssql
                        self.__disconnect_mssql_sonbor__()


        ########################################
        # res_total_line_api_usage_by_year2_1
        ########################################
        def res_total_line_api_usage_by_year2_1(self, company, year, name):
                
                
                ### customer - mssql
                self.__connect_mssql_sonbor__()

                try:    
                        #####################
                        # customer - mssql
                        #####################
                        sql2 = """
                                SELECT r_datetime, c_name, c_uid, c_p_msg  FROM [line_notify].[dbo].[line_api_usage] where c_company=? and r_year=? and c_name=?  order by r_datetime asc
                        """
                        
                        self.curr_mssql_sonbor.execute(sql2, (company, year, name,))
                        res = self.curr_mssql_sonbor.fetchall() 

                        return res

                except Exception as e:
                       logging.error(f"\n[ Error ]  res_total_line_api_usage_by_year2_1: \n\t{str(e)}\n")

                finally:
                        ### customer mssql
                        self.__disconnect_mssql_sonbor__()

        ########################################
        # res_total_line_api_usage_by_year3
        ########################################
        def res_total_line_api_usage_by_year3(self, company, year):
                
                
                ### customer - mssql
                self.__connect_mssql_sonbor__()

                try:    
                        #####################
                        # customer - mssql
                        #####################
                        sql2 = """
                                SELECT c_name, count(*)  FROM [line_notify].[dbo].[line_api_usage] where c_company=? and r_year=? group by c_name order by c_name asc;
                        """
                        
                        self.curr_mssql_sonbor.execute(sql2, (company, year))
                        res = self.curr_mssql_sonbor.fetchall() 

                        return res

                except Exception as e:
                       logging.error(f"\n[ Error ]  res_total_line_api_usage_by_year3 : \n\t{str(e)}\n")

                finally:
                        ### customer mssql
                        self.__disconnect_mssql_sonbor__()


        ########################################
        # res_total_line_api_usage_by_year2
        ########################################
        def res_total_line_api_usage_by_year2(self, company, year):
                
                
                ### customer - mssql
                self.__connect_mssql_sonbor__()

                try:    
                        #####################
                        # customer - mssql
                        #####################
                        sql2 = """
                                SELECT r_datetime, c_name, c_uid, c_p_msg  FROM [line_notify].[dbo].[line_api_usage] where c_company=? and r_year=? order by r_datetime asc;
                        """
                        
                        self.curr_mssql_sonbor.execute(sql2, (company, year))
                        res = self.curr_mssql_sonbor.fetchall() 

                        return res

                except Exception as e:
                       logging.error(f"\n[ Error ]  res_total_line_api_usage_by_year2 : \n\t{str(e)}\n")

                finally:
                        ### customer mssql
                        self.__disconnect_mssql_sonbor__()

        ########################################
        # res_total_line_api_usage_by_year
        ########################################
        def res_total_line_api_usage_by_year(self, company):
                
                
                ### customer - mssql
                self.__connect_mssql_sonbor__()

                try:    
                        #####################
                        # customer - mssql
                        #####################
                        sql2 = """
                                SELECT r_year , count(*)  FROM [line_notify].[dbo].[line_api_usage] where c_company=? group by r_year order by r_year asc;
                        """
                        
                        self.curr_mssql_sonbor.execute(sql2, (company,))
                        res = self.curr_mssql_sonbor.fetchall() 

                        return res

                except Exception as e:
                       logging.error(f"\n[ Error ]  res_total_line_api_usage_by_year : \n\t{str(e)}\n")

                finally:
                        ### customer mssql
                        self.__disconnect_mssql_sonbor__()

        ###############################
        # res_total_line_api_company
        ###############################
        def res_total_line_api_company(self):
                
                
                ### customer - mssql
                self.__connect_mssql_sonbor__()

                try:    
                        #####################
                        # customer - mssql
                        #####################
                        sql2 = """
                                SELECT c_company , count(*) FROM [line_notify].[dbo].[line_api_usage] group by c_company
                        """
                        
                        self.curr_mssql_sonbor.execute(sql2)
                        res = self.curr_mssql_sonbor.fetchall() 

                        return res

                except Exception as e:
                       logging.error(f"\n[ Error ]  res_total_line_api_company : \n\t{str(e)}\n")

                finally:
                        ### customer mssql
                        self.__disconnect_mssql_sonbor__()


        #####################################
        # query_total_line_uid_by_company2
        #####################################
        def query_total_line_uid_by_company2(self, company):
                
                
                ### customer - mssql
                self.__connect_mssql_sonbor__()

                try:    
                        #####################
                        # customer - mssql
                        #####################
                        sql2 = """
                                SELECT c_name, c_uid FROM [line_notify].[dbo].[line_api_user] where c_company=? order by  r_datetime asc
                        """
                        
                        self.curr_mssql_sonbor.execute(sql2, (company))
                        res = self.curr_mssql_sonbor.fetchall() 

                        return res

                except Exception as e:
                       logging.error(f"\n[ Error ]  query_total_line_uid_by_company2 : \n\t{str(e)}\n")

                finally:
                        ### customer mssql
                        self.__disconnect_mssql_sonbor__()

        ##############################
        # total_line_uid_by_company
        ##############################
        def total_line_uid_by_company(self):
                
                
                ### customer - mssql
                self.__connect_mssql_sonbor__()

                try:    
                        #####################
                        # customer - mssql
                        #####################
                        sql2 = """
                                SELECT c_company, count(*) FROM [line_notify].[dbo].[line_api_user] group by c_company
                        """
                        
                        self.curr_mssql_sonbor.execute(sql2)
                        res = self.curr_mssql_sonbor.fetchall() 

                        return res

                except Exception as e:
                       logging.error(f"\n[ Error ]  total_line_uid_by_company : \n\t{str(e)}\n")

                finally:
                        ### customer mssql
                        self.__disconnect_mssql_sonbor__()

        ####################################
        # query_total_line_uid_by_company
        ####################################
        def query_total_line_uid_by_company(self, company):
                
                
                ### customer - mssql
                self.__connect_mssql_sonbor__()

                try:    
                        #####################
                        # customer - mssql
                        #####################
                        sql2 = """
                                SELECT count(*) FROM [line_notify].[dbo].[line_api_user] where c_company=?
                        """
                        
                        self.curr_mssql_sonbor.execute(sql2, (company,))
                        res = self.curr_mssql_sonbor.fetchone() 

                        return res[0]

                except Exception as e:
                       logging.error(f"\n[ Error ]  query_total_line_uid_by_company : \n\t{str(e)}\n")

                finally:
                        ### customer mssql
                        self.__disconnect_mssql_sonbor__()

        ###################
        # total_line_uid
        ###################
        def total_line_uid(self):
                
                
                ### customer - mssql
                self.__connect_mssql_sonbor__()

                try:    
                        #####################
                        # customer - mssql
                        #####################
                        sql2 = """
                                SELECT count(*) FROM [line_notify].[dbo].[line_api_user]
                        """
                        
                        self.curr_mssql_sonbor.execute(sql2)
                        res = self.curr_mssql_sonbor.fetchone() 

                        return res[0]

                except Exception as e:
                       logging.error(f"\n[ Error ]  total_line_uid : \n\t{str(e)}\n")

                finally:
                        ### customer mssql
                        self.__disconnect_mssql_sonbor__()


        #############################
        # res_server_line_uid_data2
        #############################
        def res_server_line_uid_data2(self, company):
                
                
                ### customer - mssql
                self.__connect_mssql_sonbor__()

                try:    
                        #####################
                        # customer - mssql
                        #####################
                        sql2 = """
                                SELECT c_name , c_uid FROM [line_notify].[dbo].[line_api_user] where c_company=?
                        """
                        
                        self.curr_mssql_sonbor.execute(sql2, (company,))
                        res = self.curr_mssql_sonbor.fetchall() 

                        return res

                except Exception as e:
                       logging.error(f"\n[ Error ]  res_server_line_uid_data2 : \n\t{str(e)}\n")

                finally:
                        ### customer mssql
                        self.__disconnect_mssql_sonbor__()


        #############################
        # res_server_line_uid_data
        #############################
        def res_server_line_uid_data(self):
                
                
                ### customer - mssql
                self.__connect_mssql_sonbor__()

                try:    
                        #####################
                        # customer - mssql
                        #####################
                        sql2 = """
                                SELECT c_company , count(*) FROM [line_notify].[dbo].[line_api_user] group by c_company
                        """
                        
                        self.curr_mssql_sonbor.execute(sql2)
                        res = self.curr_mssql_sonbor.fetchall() 

                        return res

                except Exception as e:
                       logging.error(f"\n[ Error ]  res_server_line_uid_data : \n\t{str(e)}\n")

                finally:
                        ### customer mssql
                        self.__disconnect_mssql_sonbor__()


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
                                SELECT c_company FROM [line_notify].[dbo].[line_api_user] WHERE c_uid = ?
                        """
                        
                        self.curr_mssql_sonbor.execute(sql2 , (uid,))
                        res = self.curr_mssql_sonbor.fetchone()

                        return res[0]

                except Exception as e:
                       logging.error(f"\n[ Error ]  res_line_uid_data : \n\t{str(e)}\n")

                finally:
                        ### customer mssql
                        self.__disconnect_mssql_sonbor__()


        #################################################
        # query_total_line_push_msg_by_company_amount2
        #################################################
        def query_total_line_push_msg_by_company_amount2(self, company):
                
                
                ### customer - mssql
                self.__connect_mssql_sonbor__()

                try:    
                        #####################
                        # customer - mssql
                        #####################
                        sql2 = """
                                SELECT c_company, COUNT(*) AS usage_count FROM [line_notify].[dbo].[line_api_usage] where c_company=? group by c_company
                        """
                        
                        self.curr_mssql_sonbor.execute(sql2, (company,))
                        res = self.curr_mssql_sonbor.fetchall()

                        return res

                except Exception as e:
                       logging.error(f"\n[ Error ]  query_total_line_push_msg_by_company_amount2 : \n\t{str(e)}\n")

                finally:
                        ### customer mssql
                        self.__disconnect_mssql_sonbor__()


        ###################################
        # total_line_push_msg_by_company
        ###################################
        def total_line_push_msg_by_company(self):
                
                
                ### customer - mssql
                self.__connect_mssql_sonbor__()

                try:    
                        #####################
                        # customer - mssql
                        #####################
                        sql2 = """
                                SELECT c_company, COUNT(*) AS usage_count FROM [line_notify].[dbo].[line_api_usage] group by c_company
                        """
                        
                        self.curr_mssql_sonbor.execute(sql2)
                        res = self.curr_mssql_sonbor.fetchall()

                        return res

                except Exception as e:
                       logging.error(f"\n[ Error ]  total_line_push_msg_by_company : \n\t{str(e)}\n")

                finally:
                        ### customer mssql
                        self.__disconnect_mssql_sonbor__()


        ################################################
        # query_total_line_push_msg_by_company_amount
        ################################################
        def query_total_line_push_msg_by_company_amount(self, company):
                
                
                ### customer - mssql
                self.__connect_mssql_sonbor__()

                try:    
                        #####################
                        # customer - mssql
                        #####################
                        sql2 = """
                                SELECT COUNT(*) AS usage_count FROM [line_notify].[dbo].[line_api_usage] where c_company=?
                        """
                        
                        self.curr_mssql_sonbor.execute(sql2, (company,))
                        res = self.curr_mssql_sonbor.fetchone()

                        return res[0]

                except Exception as e:
                       logging.error(f"\n[ Error ]  query_total_line_push_msg_by_company_amount : \n\t{str(e)}\n")

                finally:
                        ### customer mssql
                        self.__disconnect_mssql_sonbor__()

        ###################################
        # total_line_push_msg
        ###################################
        def total_line_push_msg(self):
                
                
                ### customer - mssql
                self.__connect_mssql_sonbor__()

                try:    
                        #####################
                        # customer - mssql
                        #####################
                        sql2 = """
                                SELECT COUNT(*) AS usage_count FROM [line_notify].[dbo].[line_api_usage]
                        """
                        
                        self.curr_mssql_sonbor.execute(sql2)
                        res = self.curr_mssql_sonbor.fetchone()

                        return res[0]

                except Exception as e:
                       logging.error(f"\n[ Error ]  total_line_push_msg : \n\t{str(e)}\n")

                finally:
                        ### customer mssql
                        self.__disconnect_mssql_sonbor__()

        ###################################
        # res_server_line_push_msg_usage
        ###################################
        def res_server_line_push_msg_usage(self):
                
                
                ### customer - mssql
                self.__connect_mssql_sonbor__()

                try:    
                        #####################
                        # customer - mssql
                        #####################
                        sql2 = """
                                SELECT r_year , r_month , c_company , COUNT(*) AS usage_count FROM [line_notify].[dbo].[line_api_usage]
                                GROUP BY r_year,r_month,c_company ORDER BY c_company , r_year , r_month;
                        """
                        
                        self.curr_mssql_sonbor.execute(sql2)
                        res = self.curr_mssql_sonbor.fetchall()

                        return res

                except Exception as e:
                       logging.error(f"\n[ Error ]  res_server_line_push_msg_usage : \n\t{str(e)}\n")

                finally:
                        ### customer mssql
                        self.__disconnect_mssql_sonbor__()


        ###############################
        # test_save_line_push_msg_db
        ###############################
        def test_save_line_push_msg_db(self , r_datetime , r_year , r_month , r_day , r_time , company , uname , uid , p_msg):
                
                
                ### customer - mssql
                self.__connect_mssql_sonbor__()

                try:    
                        #####################
                        # customer - mssql
                        #####################
                        sql2 = """
                                INSERT INTO [line_notify].[dbo].[line_api_usage] (r_datetime , r_year , r_month , r_day , r_time ,  c_name , c_uid , c_company , c_p_msg) 
                                                                          VALUES (? , ? , ? , ? , ? , ? , ? , ? , ?)
                        """
                        
                        self.curr_mssql_sonbor.execute(sql2 , (r_datetime, r_year, r_month, r_day, r_time, uname , uid , company , p_msg,))
                        self.conn_mssql_sonbor.commit()
                        return 1

                except Exception as e:
                       logging.error(f"\n[ Error ]  save_line_push_msg_db : \n\t{str(e)}\n")

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
                                INSERT INTO [line_notify].[dbo].[line_api_usage] (r_datetime , r_year , r_month , r_day , r_time ,  c_name , c_uid , c_company , c_p_msg) 
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


        #####################################
        # total_line_user_company_sonbor_db
        #####################################
        def total_line_user_company_sonbor_db(self):
              
                ### customer - mssql
                self.__connect_mssql_sonbor__()

                try:
                      
                        #####################
                        # customer - mssql
                        #####################
                        sql = """
                                SELECT c_company FROM line_api_user_company order by no asc
                        """
                        self.curr_mssql_sonbor.execute(sql)
                        res = self.curr_mssql_sonbor.fetchall()

                        
                        return res
                                
                                
                        
                except Exception as e:
                       logging.error(f"\n[ Error ]  total_line_user_company_sonbor_db : \n\t{str(e)}\n")

                finally:
                        ### customer mssql
                        self.__disconnect_mssql_sonbor__()

        ############################################
        # alter_login_line_user_company_sonbor_db
        ############################################
        def alter_login_line_user_company_sonbor_db(self, company, pwd):
              
                ### customer - mssql
                self.__connect_mssql_sonbor__()

                try:
                      
                        #####################
                        # customer - mssql
                        #####################
                        sql = """
                                update line_api_user_company set c_c_pwd=? WHERE c_company=? 
                        """
                        res = self.curr_mssql_sonbor.execute(sql , (pwd, company,))
                        self.conn_mssql_sonbor.commit()

                        if res:
                                return 'ok'
                                
                        
                except Exception as e:
                       logging.error(f"\n[ Error ]  alter_login_line_user_company_sonbor_db : \n\t{str(e)}\n")

                finally:
                        ### customer mssql
                        self.__disconnect_mssql_sonbor__()

        
        #####################################
        # login_line_user_company_sonbor_db
        #####################################
        def login_line_user_company_sonbor_db(self, company, pwd):
              
                ### customer - mssql
                self.__connect_mssql_sonbor__()

                try:
                      
                        #####################
                        # customer - mssql
                        #####################
                        sql = """
                                SELECT * FROM line_api_user_company WHERE c_company=? and c_c_pwd=?
                        """
                        self.curr_mssql_sonbor.execute(sql , (company, pwd,))
                        res = self.curr_mssql_sonbor.fetchone()

                        if res:
                                return res
                                
                        
                except Exception as e:
                       logging.error(f"\n[ Error ]  login_line_user_company_sonbor_db : \n\t{str(e)}\n")

                finally:
                        ### customer mssql
                        self.__disconnect_mssql_sonbor__()

        #####################################
        # save_line_user_company_sonbor_db
        #####################################
        def save_line_user_company_sonbor_db(self, company):
              
                ### customer - mssql
                self.__connect_mssql_sonbor__()

                try:
                      
                        #####################
                        # customer - mssql
                        #####################
                        sql = """
                                SELECT * FROM line_api_user_company WHERE c_company=?
                        """
                        self.curr_mssql_sonbor.execute(sql , (company,))
                        res = self.curr_mssql_sonbor.fetchone()

                        if res is None:
                                
                                #####################
                                # customer - mssql
                                #####################
                                sql2 = """
                                        INSERT INTO line_api_user_company (c_company, c_c_pwd) VALUES (?, 'sbin123')
                                """

                                res1 = self.curr_mssql_sonbor.execute(sql2 , (company,))
                                self.conn_mssql_sonbor.commit()

                                
                                if res1:
                                        return True
                                else:
                                        return False
                        
                        
                except Exception as e:
                       logging.error(f"\n[ Error ]  save_line_user_company_sonbor_db : \n\t{str(e)}\n")

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
                                SELECT * FROM line_api_user WHERE c_uid=? and c_company=?
                        """
                        self.curr_mssql_sonbor.execute(sql , (uid, company,))
                        res = self.curr_mssql_sonbor.fetchone()

                        if res is None:
                                
                                #####################
                                # customer - mssql
                                #####################
                                sql2 = """
                                        INSERT INTO line_api_user (c_name , c_uid , c_company) VALUES (? , ? , ?)
                                """

                                res1 = self.curr_mssql_sonbor.execute(sql2 , (uname, uid, company,))
                                self.conn_mssql_sonbor.commit()

                                
                                if res1:
                                        return True
                                else:
                                        return False
                        
                        else:
                                #####################
                                # customer - mssql
                                #####################
                                sql3 = """
                                        UPDATE line_api_user SET c_name=? WHERE c_uid=? and c_company=?
                                """

                                self.curr_mssql_sonbor.execute(sql3 , (uname, uid, company,))
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
                                f"DRIVER={control.config.para['sb_mssql_driver_old']};"
                                f"SERVER={control.config.para['sb_mssql_host']};"
                                f"DATABASE={control.config.para['sb_mssql_db']};"
                                f"UID={control.config.para['sb_mssql_uid']};"
                                f"PWD={control.config.para['sb_mssql_pwd']}"
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
                        conn_mssql = f"DRIVER={control.config.para['mssql_driver_old']};SERVER={control.config.para['mssql_host']};DATABASE={control.config.para['mssql_db']};UID={control.config.para['mssql_uid']};PWD={control.config.para['mssql_pwd']}"  
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
                        self.conn_mysql = pymysql.connect(host=control.config.para['sb_mysql_host'],port=control.config.para['sb_mysql_port'],user=control.config.para['sb_mysql_uid'],password=control.config.para['sb_mysql_pwd'],database=control.config.para['sb_mysql_db'],charset=control.config.para['sb_mysql_charset'])
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

                
    





