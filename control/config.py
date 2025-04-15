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