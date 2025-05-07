#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Date        : 20250407
# update      : 20250410
# Author      : Jason Hung
# Version     : v1.0
# Description : v1.0 SonBor Line Messaging API parameters 

##############
# parameters
##############
ngrok_api_server_url = "https://8125-211-75-138-129.ngrok-free.app"

para = {
        ### line token 1 - sonbor 
        'company'              :'松柏資訊推播系統',
        'server_name'          :'LINE API Server',
        'copyright'            :'© 2025 松柏資訊版權所有',
        'line_id'              :'@099icqmh',
        'line_id2'             :'@268ecgfo',

        'api_server_url'           :ngrok_api_server_url,
        'api_add_url'              :f"{ngrok_api_server_url}/add",
        'api_statistics_url'       :f"{ngrok_api_server_url}/statistics",
        'api_push_msg_url'         :f'{ngrok_api_server_url}/push_msg', # push LINE message api url 
        'api_push_msg_http_method' :'POST', 
        'api_push_msg_http_para'   :'( 使用者 ID ) r_a_id , ( 傳送的訊息內容 ) p_msg , ( 公司 ) r_a_company',   

        'api_query_uid_url'         :f'{ngrok_api_server_url}/query_uid', # query LINE user ID api url 
        'api_query_uid_http_method' :'POST', 
        'api_query_uid_http_para'   :'( 公司 ) q_company ', 
        'menu_img_path'             :'D:\\w_project\\api_server\\static\\img\\line\\menu.jpg',
        'server_log_path'           :'D:\\w_project\\api_server\\line_api_server.log',


        'warning_threshold'    : 10, # 當剩餘訊息低於這數字時提醒
        'line_bot_api_token'   :'/Cnorb4qfJULKMlvrO9RPPhWNk/jrlArOm0T6I3P/B5Er5x+bwUJ4A8vdOzUFM+cDnZF/GPdGEZx5lHnVM180363k15zOedERjYFz5f0itcIxADCquDM/o1hjKAWCLm/l5m0+G5/wCgEJ9to8LivHwdB04t89/1O/w1cDnyilFU=',
        'line_bot_api_token2'  :'LZLjUoG38MHxzaMRpG4V16H0Ab9S/1VYPH1Fovg/sJehOAQP6EFsoYzTYn5WA0NRVH37CKkSTqJFXiopXAXpmDtiXqUFXfIWeyyacV6pJwJLSi/l/xeRMn0bASBAZ+KO/TPubwC+E6hEbwsKGQxOVAdB04t89/1O/w1cDnyilFU=',
        'handler_key'          :'cf22f3a7026c0643b5e6aa4891ed761d',
        'handler_key2'         :'007d1ea925f70b907bf72f32bb51008a',
        'admin_uid'            :'Udc1fafeaa808c292cbed3f1542ec15b3',
        'user1_uid'            :'U6c62b506b6a6eb52427be571dfdf2b5d', # for test use  (is jasonhung UID)
        
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
        'sb_mssql_db'        :'line_notify',
        'sb_mssql_uid'       :'sbi',
        'sb_mssql_pwd'       :'22643364',
        'sb_mssql_tb1'       :'line_user',       # 紀錄 各公司及UID
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