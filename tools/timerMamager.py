# #-*-coding:utf-8-*-
#
# #定时任务管理类
# import time
# from datetime import datetime
# from apscheduler.schedulers.tornado  import TornadoScheduler
# class TimerManager:
#     def __init__(self):##牌类型，牌字
#        self.m_scheduler = TornadoScheduler()
#        self.start()
#
#     def start(self):##
#        return self.m_scheduler.start()
#
#     def stop(self):##
#        return self.m_scheduler.shutdown()
#
#     def getTimer(self,id):##
#        return self.m_scheduler.get_job(str(id))
#
#
#     def addLoopTimer(self, tid,tick,time,arg):  ##
#         try:
#             job = self.getTimer(tid)
#             if job == None:
#                self.m_scheduler.add_job(tick, 'interval', seconds=int(time), args=arg,id=str(tid),replace_existing = True)  # 间隔3秒钟执行一次
#         except Exception as e:
#            print str(Exception)
#
#     def addOnceTimer(self, tid, tick, tm,arg):  ##
#         try:
#                job = self.getTimer(tid)
#                if job == None:
#                    doTime = time.time() + int(tm)
#                    doTime = datetime.fromtimestamp(doTime)
#                    self.m_scheduler.add_job(tick, 'date', next_run_time= doTime,args=arg, id=str(tid))  # 执行一次
#
#         except Exception as e:
#            print str(Exception)
#
#     def delTimer(self, id):  ##
#         try:
#             id = str(id)
#             job = self.getTimer(id)
#             if job:
#                self.m_scheduler.remove_job(id)
#         except Exception as e:
#            print str(Exception)
#
#     def pauseTimer(self, id):  ##暂停
#         try:
#             id = str(id)
#             job = self.getTimer(id)
#             if job:self.m_scheduler.pause_job(id)
#         except Exception as e:
#             print str(Exception)
#
#     def resumeTimer(self, id):  ##暂停
#         try:
#             id = str(id)
#             job = self.getTimer(id)
#             if job: self.m_scheduler.resume_job(id)
#         except Exception as e:
#             print str(Exception)
#
#     def pauseAllTimer(self):  ##
#         self.m_scheduler.pause()
#
#     def resumeAllTimer(self):  ##
#         self.m_scheduler.resume()
#
#     def delAllTimer(self):  ##
#         self.m_scheduler.remove_all_jobs()