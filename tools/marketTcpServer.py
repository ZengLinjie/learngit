#! /usr/bin/env python
# coding=utf-8
import json
import datetime
import traceback
import time
import tornado
from tornado.iostream import StreamClosedError
from tornado.tcpserver import TCPServer
from tornado.ioloop import IOLoop

from configs.config_default import configs_default
from configs.config_error import config_error
from dal.dal_user import Dal_User
from model.market import Market
from model.user import User
from tools.mainTimerManager import MainTimerManager
from tools.utils import Utils
from dal.dal_market import Dal_Market
from logic.marker import Marker
from dal.dal_guester import Dal_Guester
from model.guester import Guester
from tornado.gen import coroutine


TCP_MAX_LENGTH = 1024


class TCPConnection(object):

     def __init__(self, stream, address):
        self._stream = stream
        self._address = address
        self.read_message()

     @tornado.gen.coroutine
     def read_message(self):
         while True:
            try:
              # data =  yield self._stream.read_bytes(TCP_MAX_LENGTH,partial=True)
              data = yield self._stream.read_until(b'\n')
              self.on_data(data)
            except StreamClosedError:
                    self.on_close()
                    break
            except Exception as e:
                msg = traceback.format_exc()  # 方式1
                Utils().logMainDebug(msg)

     @tornado.gen.coroutine
     def on_data(self, data):
         try:
                 bJson = Utils().is_json(data)
                 if bJson == False:
                     return

                 jsonData = json.loads(data)
                 if 'msg' not in jsonData:
                     return

                 msg = jsonData['msg']
                 if msg == 'init_mk':
                     mkid = jsonData['mkid']
                     self.on_init_mk(mkid)
                 elif msg == 'beat_heart':
                     self.on_beat_heart(jsonData)

         except StreamClosedError:
                self.on_close()
         except Exception as e:
             msg = traceback.format_exc()  # 方式1
             Utils().logMainDebug(msg)


     def send_message(self, data):
        data = str(data).encode('utf-8')
        self._stream.write(data)

     def on_close(self):
          Utils().logMainDebug('mk connect closed' + str(self.mkid))
          MarketTcpServer.del_market(self.mkid)


##message handle
     def on_init_mk(self,mkid):
        try:
            self.mkid = mkid
            MarketTcpServer.add_market(mkid, self)
            msg = {'errorcode': config_error['success']}
            encodeMsg = json.dumps(msg)
            self.send_message(encodeMsg)
        except Exception as e:
            msg = traceback.format_exc()  # 方式1
            Utils().logMainDebug(msg)

     def on_beat_heart(self, jsonData):
        try:
            msg = {'errorcode': config_error['success'],'mkid':self.mkid}
            encodeMsg = json.dumps(msg)
            self.send_message(encodeMsg)
        except Exception as e:
            msg = traceback.format_exc()  # 方式1
            Utils().logMainDebug(msg)


class MarketTcpServer(TCPServer):
    markets = dict()
    m_timerMgr = MainTimerManager()  ##超时处理队列
    lastOpenDoorUser = None
    light_state = dict()

    @tornado.gen.coroutine
    def handle_stream(self, stream, address):
        TCPConnection(stream, address)


#辅助函数
    @classmethod
    def get_all_market_count(cls):
        return len(cls.markets)


    @classmethod
    def add_market(cls,id,conn):
        try:
            if (id in cls.markets) == False:
                newMt = Marker(id,conn)
                cls.markets[id] = newMt
            else:
                mk = cls.get_market(id)
                mk.m_conn = conn
        except Exception as e:
            msg = traceback.format_exc()  # 方式1
            Utils().logMainDebug(msg)

    @classmethod
    def del_market(cls,id):
        try:
            if id in cls.markets == True:
                mk = cls.get_market(id)
                mk.m_conn = None
        except Exception as e:
            msg = traceback.format_exc()  # 方式1
            Utils().logMainDebug(msg)

    @classmethod
    def get_market(cls,id):
        return cls.markets.get(id)

    @classmethod
    def send_message(cls, mkid,data):
       try:
            mk = cls.get_market(mkid)
            if mk:
                if mk.m_conn:
                    mk.m_conn.send_message(data)
       except Exception as e:
           msg = traceback.format_exc()  # 方式1
           Utils().logMainDebug(msg)


    @classmethod
    def open_door_inner(cls, mkid,uid = None):
        try:
            mk = cls.get_market(mkid)
            if mk == None:
                msg = {'errorcode': config_error['mkinvaild']}
                encodeMsg = json.dumps(msg)
                return encodeMsg

            return mk.open_door_inner(uid)
        except Exception as e:
            msg = traceback.format_exc()  # 方式1
            Utils().logMainDebug(msg)


    @classmethod
    def open_door(cls, mkid,uid = None):
        try:
            mk = cls.get_market(mkid)
            if mk == None:
                msg = {'errorcode': config_error['mkinvaild']}
                encodeMsg = json.dumps(msg)
                return encodeMsg

            return mk.open_door(uid)

        except Exception as e:
            msg = traceback.format_exc()  # 方式1
            Utils().logMainDebug(msg)

    # 后台暴力开门
    @classmethod
    def admin_opendoor(cls, mkid):
        try:
            mkid = mkid.decode(encoding='utf-8')
            mk = cls.get_market(mkid)
            if mk:
                return mk.admin_opendoor()
        except Exception as e:
            msg = traceback.format_exc()  # 方式1
            Utils().logMainDebug(msg)

    # 后台锁门
    @classmethod
    def admin_closedoor(cls, mkid):
        try:
            mkid = mkid.decode(encoding='utf-8')
            mk = cls.get_market(mkid)
            if mk:
                return mk.admin_closedoor()
        except Exception as e:
            msg = traceback.format_exc()  # 方式1
            Utils().logMainDebug(msg)

    # 开闸机
    @classmethod
    def open_gate(cls, mkid,uid, gate_num=1):
        try:
            mk = cls.get_market(mkid)
            if mk:
                return mk.open_gate(uid, gate_num)

            msg = {'errorcode': config_error['mkinvaild']}
            encodeMsg = json.dumps(msg)
            return encodeMsg

        except Exception as e:
            msg = traceback.format_exc()  # 方式1
            Utils().logMainDebug(msg)

    # 添加主动扫描商品
    @classmethod
    def on_zdAddGood(cls, mkid, uid, gid):
        try:
            mkid = str(mkid)
            mk = cls.get_market(mkid)
            if mk == None:
                msg = {'errorcode': config_error['mkinvaild']}
                encodeMsg = json.dumps(msg)
                return encodeMsg

            return mk.on_zdAddGood(uid,gid)

        except Exception as e:
            msg = traceback.format_exc()  # 方式1
            Utils().logMainDebug(msg)

    # 删除主动扫描商品
    @classmethod
    def on_zdDelGood(cls, mkid, uid, gid):
        try:
            mkid = str(mkid)
            mk = cls.get_market(mkid)
            if mk == None:
                msg = {'errorcode': config_error['mkinvaild']}
                encodeMsg = json.dumps(msg)
                return encodeMsg

            return mk.on_zdDelGood(uid,gid)

        except Exception as e:
            msg = traceback.format_exc()  # 方式1
            Utils().logMainDebug(msg)

    # 用户请求付款(主动)
    @classmethod
    def on_payZDReq(cls, mkid,uid):
        try:
            mkid = str(mkid)
            uid = str(uid)
            mk = cls.get_market(mkid)
            if mk == None:
                msg = {'errorcode': config_error['mkinvaild']}
                encodeMsg = json.dumps(msg)
                return encodeMsg

            return mk.on_payZDReq(uid)
        except Exception as e:
            msg = traceback.format_exc()  # 方式1
            Utils().logMainDebug(msg)


    @classmethod
    def handlePayResult(cls, mkid, uid, goods):
        try:
            mkid = str(mkid)
            uid = str(uid)
            goods = str(goods)

            mk = cls.get_market(mkid)
            if mk:
                  mk.handlePayResult(uid, goods)

        except Exception as e:
            msg = traceback.format_exc()  # 方式1
            Utils().logMainDebug(msg)

    @classmethod
    def check_user(cls, uid):
        try:
            user = Dal_User().getUser(uid)
            if user == None:#第一次自动创建用户
                user = User()
                user.id = uid
                user.state = configs_default['userstat']['out']
                user.paygoods = ''
                user.lastintime = Utils().dbTimeCreate()
                user.lastouttime = Utils().dbTimeCreate()
                Dal_User().addUser(user)
            return user

        except Exception as e:
            msg = traceback.format_exc()  # 方式1
            Utils().logMainDebug(msg)

    @classmethod
    def on_getUserState(cls, uid):
        try:
            if uid:
                cls.check_user(uid)

            user = Dal_User().getUser(uid)
            msg = {'errorcode': config_error['success'],'state': user.state}
            encodeMsg = json.dumps(msg)
            return encodeMsg

        except Exception as e:
            msg = traceback.format_exc()  # 方式1
            Utils().logMainDebug(msg)

#如果uid为空，则默认是最后一个人
    @classmethod
    def on_setUserState(cls, uid = None,state = configs_default['userstat']['out']):
        try:
            if uid == None: return

            user = Dal_User().getUser(uid)
            if user:
               user.state = state
               Dal_User().updateUserState(uid, state)

        except Exception as e:
            msg = traceback.format_exc()  # 方式1
            Utils().logMainDebug(msg)


    @classmethod
    def open_light(cls, mkid):
       try:
            mk = cls.get_market(mkid)
            if mk:
               mk.open_all_light()
       except Exception as e:
           msg = traceback.format_exc()  # 方式1
           Utils().logMainDebug(msg)

    @classmethod
    def close_light(cls, mkid):
        try:
            mk = cls.get_market(mkid)
            if mk:
               mk.close_all_light()
        except Exception as e:
            msg = traceback.format_exc()  # 方式1
            Utils().logMainDebug(msg)

#获取当前顾客购物车商品
    @classmethod
    def on_getGuesterGoods(cls,mkid, uid):
        try:
            mkid = str(mkid)
            mk = cls.get_market(mkid)
            if mk == None:
                msg = {'errorcode': config_error['mkinvaild']}
                encodeMsg = json.dumps(msg)
                return encodeMsg

            return mk.on_getGuesterGoods(uid)

        except Exception as e:
            msg = traceback.format_exc()  # 方式1
            Utils().logMainDebug(msg)




















