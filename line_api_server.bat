@echo off
call d:\w_project\api_server\Scripts\activate.bat

::::::::::::
::  Flask 
::::::::::::
::python line_api_server.py 

:::::::::::::
:: waitress
:::::::::::::
python w_line_api_server.py

pause