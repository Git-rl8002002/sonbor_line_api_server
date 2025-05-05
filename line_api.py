#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Date        : 20250407
# update      : 202504010
# Author      : Jason Hung
# Version     : v1.1
# Description : v1.0 SonBor Line Messaging API - LINE SDK v2 寫法
#               v1.1 package api for VB  

import random
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
    
    ### test add push message
    for i in range(random.randint(0,100)):
        
        dao.test_save_line_push_msg_db('2025-04-12 11:45:12' , '2025' , '04' , '12' , '11:45:12' ,'測試資訊', '測試哥' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2025-03-12 11:45:12' , '2025' , '03' , '12' , '11:45:12' ,'測試資訊', '測試哥' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2025-02-12 11:45:12' , '2025' , '02' , '12' , '11:45:12' ,'測試資訊', '測試哥' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2025-01-12 11:45:12' , '2025' , '01' , '12' , '11:45:12' ,'測試資訊', '測試哥' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')


        dao.test_save_line_push_msg_db('2025-04-12 11:45:12' , '2025' , '04' , '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2025-03-12 11:45:12' , '2025' , '03' , '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2025-02-12 11:45:12' , '2025' , '02' , '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2025-01-12 11:45:12' , '2025' , '01' , '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        

        dao.test_save_line_push_msg_db('2024-12-12 11:45:12' , '2024' , '12', '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2024-11-12 11:45:12' , '2024' , '11', '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2024-10-11 11:45:12' , '2024' , '10', '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2024-09-12 11:45:12' , '2024' , '09' , '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2024-08-12 11:45:12' , '2024' , '08' , '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2024-07-12 11:45:12' , '2024' , '07' , '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2024-06-12 11:45:12' , '2024' , '06' , '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2024-05-12 11:45:12' , '2024' , '05' , '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2024-04-12 11:45:12' , '2024' , '04' , '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2024-03-12 11:45:12' , '2024' , '03' , '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')

        dao.test_save_line_push_msg_db('2023-12-12 11:45:12' , '2023' , '12', '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2023-11-12 11:45:12' , '2023' , '11', '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2023-10-11 11:45:12' , '2023' , '10', '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2023-09-12 11:45:12' , '2023' , '09' , '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2023-08-12 11:45:12' , '2023' , '08' , '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2023-07-12 11:45:12' , '2023' , '07' , '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2023-06-12 11:45:12' , '2023' , '06' , '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2023-05-12 11:45:12' , '2023' , '05' , '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2023-04-12 11:45:12' , '2023' , '04' , '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2023-03-12 11:45:12' , '2023' , '03' , '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')

        dao.test_save_line_push_msg_db('2022-12-12 11:45:12' , '2022' , '12', '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2022-11-12 11:45:12' , '2022' , '11', '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2022-10-11 11:45:12' , '2022' , '10', '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2022-09-12 11:45:12' , '2022' , '09' , '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2022-08-12 11:45:12' , '2022' , '08' , '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2022-07-12 11:45:12' , '2022' , '07' , '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2022-06-12 11:45:12' , '2022' , '06' , '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2022-05-12 11:45:12' , '2022' , '05' , '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2022-04-12 11:45:12' , '2022' , '04' , '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2022-03-12 11:45:12' , '2022' , '03' , '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')

        dao.test_save_line_push_msg_db('2021-12-12 11:45:12' , '2021' , '12', '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2021-11-12 11:45:12' , '2021' , '11', '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2021-10-11 11:45:12' , '2021' , '10', '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2021-09-12 11:45:12' , '2021' , '09' , '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2021-08-12 11:45:12' , '2021' , '08' , '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2021-07-12 11:45:12' , '2021' , '07' , '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2021-06-12 11:45:12' , '2021' , '06' , '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2021-05-12 11:45:12' , '2021' , '05' , '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2021-04-12 11:45:12' , '2021' , '04' , '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2021-03-12 11:45:12' , '2021' , '03' , '12' , '11:45:12' ,'松柏資訊', '測試男' , 'U6c62b506b6a6eb52427be571dfdgg88w' , '(測試) test test test test')

        dao.test_save_line_push_msg_db('2021-12-12 11:45:12' , '2021' , '12', '12' , '11:45:12' ,'松柏資訊', '洪毅明' , 'U6c62b506b6a6eb52427be571dfdf2b5d' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2021-11-12 11:45:12' , '2021' , '11', '12' , '11:45:12' ,'松柏資訊', '洪毅明' , 'U6c62b506b6a6eb52427be571dfdf2b5d' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2021-10-11 11:45:12' , '2021' , '10', '12' , '11:45:12' ,'松柏資訊', '洪毅明' , 'U6c62b506b6a6eb52427be571dfdf2b5d' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2021-09-12 11:45:12' , '2021' , '09' , '12' , '11:45:12' ,'松柏資訊', '洪毅明' , 'U6c62b506b6a6eb52427be571dfdf2b5d' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2021-08-12 11:45:12' , '2021' , '08' , '12' , '11:45:12' ,'松柏資訊', '洪毅明' , 'U6c62b506b6a6eb52427be571dfdf2b5d' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2021-07-12 11:45:12' , '2021' , '07' , '12' , '11:45:12' ,'松柏資訊', '洪毅明' , 'U6c62b506b6a6eb52427be571dfdf2b5d' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2021-06-12 11:45:12' , '2021' , '06' , '12' , '11:45:12' ,'松柏資訊', '洪毅明' , 'U6c62b506b6a6eb52427be571dfdf2b5d' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2021-05-12 11:45:12' , '2021' , '05' , '12' , '11:45:12' ,'松柏資訊', '洪毅明' , 'U6c62b506b6a6eb52427be571dfdf2b5d' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2021-04-12 11:45:12' , '2021' , '04' , '12' , '11:45:12' ,'松柏資訊', '洪毅明' , 'U6c62b506b6a6eb52427be571dfdf2b5d' , '(測試) test test test test')
        dao.test_save_line_push_msg_db('2021-03-12 11:45:12' , '2021' , '03' , '12' , '11:45:12' ,'松柏資訊', '洪毅明' , 'U6c62b506b6a6eb52427be571dfdf2b5d' , '(測試) test test test test')




    print('ok')
    ### show dao parameters
    #dao.show_dao_para()