#-*-coding:utf-8-*-

#定时任务管理类
import tornado
import tornado.ioloop
import time
from datetime import datetime

class MainTimerManager:
    def __init__(self):##
       self.m_scheduler = {}

    def start(self,id):##
        id = str(id)
        timer =  self.m_scheduler.get(id)
        if timer == None:return
        timer.start()

    def stop(self,id):##
        id = str(id)
        timer =  self.m_scheduler.get(id)
        if timer == None:return
        timer.stop()

    def getTimer(self,id):##
       return self.m_scheduler.get(str(id))


    def addTimer(self, id,callback,time,arg):  ##
            id = str(id)
            job = self.getTimer(id)
            if job:
                job.stop()
                self.m_scheduler.pop(id)
            job = tornado.ioloop.PeriodicCallback(lambda: callback(arg), time)
            self.m_scheduler[id] = job
            job.start()


    def delTimer(self, id):  ##
            id = str(id)
            job = self.getTimer(id)
            if job:
               job.stop()
               self.m_scheduler.pop(id)

    def pauseTimer(self, id):  ##暂停
        try:
            id = str(id)
            job = self.getTimer(id)
            if job:job.stop()
        except Exception as e:
            print(str(Exception))

    def resumeTimer(self, id):  ##暂停
        try:
            id = str(id)
            job = self.getTimer(id)
            if job:job.start()
        except Exception as e:
            print(str(Exception))

    def pauseAllTimer(self):  ##
        for k,v in self.m_scheduler.items():
            v.stop()

    def resumeAllTimer(self):  ##
        for k,v in self.m_scheduler.items():
            v.start()

    def delAllTimer(self):  ##
        self.pauseAllTimer()
        self.m_scheduler.clear()