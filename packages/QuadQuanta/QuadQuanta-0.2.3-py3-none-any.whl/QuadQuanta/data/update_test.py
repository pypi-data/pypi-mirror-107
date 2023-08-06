#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   update.py
@Time    :   2021/05/08
@Author  :   levonwoo
@Version :   0.1
@Contact :   
@License :   (C)Copyright 2020-2021
@Desc    :   日线数据测试模块
'''

# here put the import lib
import datetime
import time

from QuadQuanta.config import config
from QuadQuanta.data import save_bars

if __name__ == '__main__':
    # while True:
    today = datetime.date.today()
    hour = datetime.datetime.now().hour
    start_time = config.start_date + ' 09:00:00'
    end_time = str(today) + ' 17:00:00'
    save_bars(start_time, end_time, frequency='daily', database='jqdata')
    # try:
    #     if hour < 17 and hour >= 6:
    #         save_all_jqdata('2014-01-01',
    #                         '2014-07-01',
    #                         frequency='minute',
    #                         database='jqdata')
    # except Exception as e:
    #     print(e)
    #     break
    # time.sleep(60)

# TODO 第一次存分钟数据注意关注聚宽流量，所取分钟数据大于剩余流量可能会发生未知错误
# start_time = config.start_date + ' 09:00:00'
# # end_time = str(today) + ' 17:00:00'
#
# end_time = str(datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(days=15, hours=8))
# save_all_jqdata(start_time,
#                 end_time,
#                 frequency='minute',
#                 database='jqdata')
