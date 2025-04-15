#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Date        : 20250407
# update      : 202504010
# Author      : Jason Hung
# Version     : v1.1
# Description : v1.0 SonBor Line Messaging API - LINE SDK v2 寫法
#               v1.1 package api for VB  

from control.dao import dao
dao = dao()

#####################################################################################################################################################################################################################
#
# Main
#
#####################################################################################################################################################################################################################
if __name__ == "__main__":
   
    ###################################################################################################
    #
    # funcion : push message(p1,p2,p3)
    # usage :    
    #           p1 : push message admin's UID
    #           p2 : receiver message user's UID
    #           p3 : push message content
    #
    ###################################################################################################
    #dao.push_message_v2(dao.para['admin_uid'] , dao.para['user1_uid'] , '訂單編號 1024578 , 已於 2025/04/10 出貨完成')
    #dao.push_message_v2(dao.para['user2_uid'] , '(測試訊息) 訂單編號 1024848 , 已於 2025/04/10 出貨完成')

    ### test push message
    #dao.test_push_msg()

    ### test mssql
    #dao.get_mssql_data()

    ### show dao parameters
    dao.show_dao_para()