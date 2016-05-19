# -*- coding: utf-8 -*-

'''''
Filename: "utildate.py"
author:   "binpo"
date  :   "2014-03-24"
version:  "1.00"
'''

def datetime_format(format='%Y-%m-%d %H:%M:%S',input_time=None):
    import datetime
    if not input_time:
        input_time=datetime.datetime.now()
    return datetime.datetime.strftime(input_time,format)

#print date_time_format()