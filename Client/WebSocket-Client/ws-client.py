    #!usr/bin/env python
# -*- coding: utf-8 -*-

import websocket
from time import sleep				
import random	
import datetime
import _thread as thread
import json

#クライアントクラスの定義
class ws_client():
    def __init__(self):
        host = "ws://fast-fjord-64260.herokuapp.com"
        websocket.enableTrace(True)
        #WbSocketの設定
        self.ws = websocket.WebSocketApp(host,
                            on_open=self.on_open,
                            on_message=self.on_message,
                            on_error=self.on_error,
                            on_close=self.on_close)

    def on_message(self, ws, message):
        print(message)

    def on_error(self, ws, error):
        print("Occur error")
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print("closed")

    def on_open(self, ws):
        print("connected")
        #接続完了後、スレッドを起動
        thread.start_new_thread(self.run, ())
        #self.test_run()

    #スレッド
    #ここでデータを送る
    def run(self, *args):
        while True:
            #############
            get_day = datetime.datetime(2022, 8, random.randrange(1,31), hour=random.randrange(8, 21), minute=random.randrange(59), second=random.randrange(59))
            td = datetime.timedelta(seconds=random.randrange(59), minutes=random.randrange(30))
            get_day_td = get_day + td
            send_msg = {"interested": random.randrange(100),"age": random.randrange(65),"gender": random.randrange(2),"start_time": str(get_day),"end_time": str(get_day_td)}
            send_msg = json.dumps(send_msg)
            #idは自動インクリメントなので、idは送らなくてよい
            ###############
            self.ws.send(send_msg)
            print(send_msg)					# メッセージを表示

            sleep(3)	 					# 5秒待つ
    
    #テスト通信用
    def test_run(self):
        send_msg = "test"
        self.ws.send(send_msg)
        self.ws.close()

    #永続接続
    def run_forever(self):
        self.ws.run_forever()

def main():
    client = ws_client()
    client.run_forever()

if __name__ == '__main__':
	main()			