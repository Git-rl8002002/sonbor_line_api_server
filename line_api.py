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
dao = dao()


#####################################################################################################################################################################################################################
#
# Main
#
#####################################################################################################################################################################################################################
if __name__ == "__main__":
   
    ###################################################################################################
    #
    # funcion : push message(p1,r2)
    # usage :    
    #           p1 : push message line accoint handler secret key
    #           r2 : receiver message user id
    #
    ###################################################################################################
    dao.push_message(control.dao.para['admin_uid'] , control.dao.para['user_uid'])