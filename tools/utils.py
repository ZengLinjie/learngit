#coding:utf-8
import json
import os
import uuid
from random import random
import tornado.httpclient
from configs.config_default import configs_default
from tools.singleton import Singleton
import time
import datetime
import logging
import tornado.gen
from configs import operation_rule

#工具类
class Utils(metaclass = Singleton):
    # __metaclass__ = Singleton
    ##工具中包含有 截取字符串的    编码的 解码的  是否为空的  获取文件路径的
#prama: ,,,;,,, return dict
    def decodeMutilFormat(self,inputstring,char1,char2):## 输入的字符串"1:30;2:20;3:90;4;90"
        outResult = {}
        outlist = inputstring.split(char1);

        for substr in outlist:
            arrStr = substr.split(char2)
            outResult[arrStr[0]] = arrStr[1]
        return outResult

    def encodeMutilFormat(self,inputDict,char1,char2):
        outResult = '' ##{‘name’:"blx","age":20,"sex":"nan"}
        i = 0
        dlen = len(inputDict)
        for k, v in inputDict.items():
            outResult = outResult + str(k) + char2 + str(v)
            i = i + 1
            if i < dlen:
                outResult = outResult + char1

        return outResult

#prama: ;;;; [] return str
    def encodeIDFormat(self,inputList,char = ';'):  ## 列表转化为字符串
        outResult = ''
        index = 0
        listlen = len(inputList)
        for substr in inputList:
            index = index + 1
            if index < listlen:
                outResult = outResult +str(substr)+ char
            else:
                outResult = outResult + str(substr)
        return outResult
    ## decodeIDFromat() 解码 就是分割字符串 分隔符 传入一个字符串和分隔符 输出一个列表
    def decodeIDFormat(self,inputstring,char = ';'):  ## 字符串转化为列表"1;2;3;4;5" ==> [1,2,3,4]
        outResult = []
        outlist = inputstring.split(char)
        for substr in outlist:
            outResult.append(substr)
        return outResult
    ## 判断某个元素是否在一个字符串（可以分割成列表）中
    def isValueInIDFormat(self,v,inputstring):
        if self.isNull(inputstring):
            return False
        outlist = self.decodeIDFormat(inputstring)
        return (str(v) in outlist)   ##返回的值是False  和 True
    ## 判断是否为空
    def isNull(self,v):
        return (v == None or v == '');

    def getFileCountInPath(self,path):
        count = 0
        for root, dirs, files in os.walk(path):
        #print files
            fileLength = len(files)
            if fileLength != 0:
               count = count + fileLength
        return count


    def logMainDebug(self, msg):
        loger = logging.getLogger("ingenia")
        loger.info(msg)
       # self.logErrorSend(msg)

    def is_json(self,myjson):
        try:
            json_object = json.loads(myjson)
        except Exception as e:
             return False
        return True

    def dbTime2Client(self, timeDB):
        timeArre = time.strptime(timeDB, "%Y-%m-%d %H:%M:%S")
        timestrap = int(time.mktime(timeArre))
        v1 = datetime.datetime.utcfromtimestamp(timestrap)
        return v1

    def dateTime2String(self, dt):
        return dt.strftime("%Y-%m-%d-%H")

    def dateTime3String(self, dt):
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    def String2dateTime(self, str):
        return datetime.datetime.strptime(str, "%Y-%m-%d %H:%M:%S")

    def dbTimeCreate(self):
        return time.strftime('%Y-%m-%d %H:%M:%S')

    def dbTime2Number(self, timeDB):
        if not isinstance(timeDB, datetime.datetime):
            timeDB = datetime.datetime.strptime(timeDB, "%Y-%m-%d %H:%M:%S")
        timestrap = int(time.mktime(timeDB.timetuple()))
        return timestrap

    def string2Number(self, str_time):
        str_time = "%s" % str_time
        return self.dbTime2Number(self.String2dateTime(str_time))

    def time2now(self, time):
        timeA = self.dbTime2Number(time)
        timeN = self.dbTime2Number(self.dbTimeCreate())
        return timeN - timeA

    def random_range(self, min, max):
        return random.randint(min, max)

    def random_index(self, rate):
        """随机变量的概率函数"""
        #
        # 参数rate为list<int>
        #
        start = 0
        randnum = random.randint(1, sum(rate))

        for index, item in enumerate(rate):
            start += item
            if randnum <= start:
                break
        return index

    def DateTime2Float(self, dt):
        return time.mktime(dt.timetuple())

        # 获取某天0点的时间戳

    def DayBeginTime(self, timeD):
        # t = time.localtime(time.time()) 当天
        t = time.localtime(timeD)
        time1 = time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00', t), '%Y-%m-%d %H:%M:%S'))
        return float(time1)

        # 获取某天24点的时间戳

    def DayEndTime(self, timeD):
        z_time = self.DayBeginTime(timeD)
        return z_time + 86400

        # 获取现在到当天24点的时间戳

    def TodayDeltaTime(self):
        cur_time = time.time()
        end_time = self.DayEndTime(cur_time)
        return end_time - cur_time

        # 获取昨天0点的时间戳

    def LastDayBeginTime(self):
        z_time = self.DayBeginTime(time.time())
        return z_time - 86400

        # 获取昨天24点的时间戳

    def LastDayEndTime(self):
        return self.DayBeginTime(time.time())

        # 获取上周第一天的时间戳

    def LastWeekBeginTime(self):
        now = datetime.datetime.now()
        last_week_start = now - datetime.timedelta(days=now.weekday() + 7)
        last_week_start = self.DateTime2Float(last_week_start)
        last_week_start = self.DayBeginTime(last_week_start)
        return last_week_start

        # 获取上周最后一天的时间戳

    def LastWeekEndTime(self):
        now = datetime.datetime.now()
        last_week_end = now - datetime.timedelta(days=now.weekday() + 1)
        last_week_end = self.DateTime2Float(last_week_end)
        last_week_end = self.DayEndTime(last_week_end)
        return last_week_end

        # 获取本周最后一天的时间戳

    def WeekEndTime(self):
        now = datetime.datetime.now()
        this_week_end = now + datetime.timedelta(days=6 - now.weekday())
        this_week_end = self.DateTime2Float(this_week_end)
        this_week_end = self.DayEndTime(this_week_end)
        return this_week_end

        # 获取现在到周末24点的时间戳

    def WeekDeltaTime(self):
        cur_time = time.time()
        end_time = self.WeekEndTime()
        return end_time - cur_time

        # 获取上月第一天的时间戳

    def LastMonthBeginTime(self):
        now = datetime.datetime.now()
        this_month_start = datetime.datetime(now.year, now.month, 1)
        last_month_end = this_month_start - datetime.timedelta(days=1)
        last_month_start = datetime.datetime(last_month_end.year, last_month_end.month, 1)
        last_month_start = self.DateTime2Float(last_month_start)
        last_month_start = self.DayBeginTime(last_month_start)
        return last_month_start

        # 获取上月最后一天的时间戳

    def LastMonthEndTime(self):
        now = datetime.datetime.now()
        this_month_start = datetime.datetime(now.year, now.month, 1)
        last_month_end = this_month_start - datetime.timedelta(days=1)
        last_month_end = self.DateTime2Float(last_month_end)
        last_month_end = self.DayEndTime(last_month_end)
        return last_month_end

        # 获取本月最后一天的时间戳

    def MonthEndTime(self):
        now = datetime.datetime.now()
        nextYear = now.year
        nextMonth = now.month + 1
        if (now.month + 1) > 12:
            nextYear = now.year + 1
            nextMonth = 0
        this_month_end = datetime.datetime(nextYear, nextMonth + 1, 1) - datetime.timedelta(days=1)
        this_month_end = self.DateTime2Float(this_month_end)
        this_month_end = self.DayEndTime(this_month_end)
        return this_month_end

        # 获取现在到月末24点的时间戳

    def MonthDeltaTime(self):
        cur_time = time.time()
        end_time = self.MonthEndTime()
        return end_time - cur_time

        # 获取去年第一天的时间戳

    def LastYearBeginTime(self):
        now = datetime.datetime.now()
        this_year_start = datetime.datetime(now.year, 1, 1)
        last_year_end = this_year_start - datetime.timedelta(days=1)
        last_year_start = datetime.datetime(last_year_end.year, 1, 1)
        last_year_start = self.DateTime2Float(last_year_start)
        last_year_start = self.DayBeginTime(last_year_start)
        return last_year_start

        # 获取去年最后一天的时间戳

    def LastYearEndTime(self):
        now = datetime.datetime.now()
        this_year_start = datetime.datetime(now.year, 1, 1)
        last_year_end = this_year_start - datetime.timedelta(days=1)
        last_year_end = self.DateTime2Float(last_year_end)
        last_year_end = self.DayEndTime(last_year_end)
        return last_year_end

        # 获取本年最后一天的时间戳

    def YearEndTime(self):
        now = datetime.datetime.now()
        this_year_end = datetime.datetime(now.year + 1, 1, 1) - datetime.timedelta(days=1)
        this_year_end = self.DateTime2Float(this_year_end)
        this_year_end = self.DayEndTime(this_year_end)
        return this_year_end

        # 获取现在到年末24点的时间戳

    def YearDeltaTime(self):
        cur_time = time.time()
        end_time = self.YearEndTime()
        return end_time - cur_time


    def gen_virtual_payment(self,pid,goods):
        if goods == None or goods == '':return

        url = configs_default['server_map']['admin_url']+ 'genvp'
        data = {}
        data['pID'] = pid
        data['goods'] = goods
        self.send_post_asyn_request(url,data)

    def gen_uuid(self):
        return str(uuid.uuid1())

    def page_generate(self, pageid):
        pageid = int(pageid)
        return ((pageid-1)*operation_rule.PAGE_NUM, (pageid-1)*operation_rule.PAGE_NUM+(operation_rule.PAGE_NUM-1))


    def send_post_asyn_request(self,url,data,callback=None):
        try:
            client = tornado.httpclient.AsyncHTTPClient()
            req_obj = tornado.httpclient.HTTPRequest(
                url=url,
                method="POST",
                body=json.dumps(data),
            )
            client.fetch(req_obj,callback)
        except Exception as e:
            print("Error: " + str(e))


    @tornado.gen.coroutine
    def send_post_asyn_request_resp(self,url,data):
        client = tornado.httpclient.AsyncHTTPClient()
        req_obj = tornado.httpclient.HTTPRequest(
            url=url,
            method="POST",
            body=json.dumps(data)
        )
        resp = yield client.fetch(req_obj)
        resp_dict = json.loads(resp.body)
        raise tornado.gen.Return(resp_dict)

#发送错误日志
    def logErrorSend(self, msg):
        url = configs_default['server_map']['admin_url'] + 'errorlog'
        msg = configs_default['server_id'] + msg
        Utils().send_post_asyn_request(url,msg)

    def any2unicode(self, s, encoding=None):
            return str(s)

    def any2int(self, s):
        if isinstance(s, str):
            s = s.split('.')[0]

        s = int(s)
        return s