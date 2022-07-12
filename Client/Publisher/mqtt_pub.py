#!usr/bin/env python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt		# MQTTのライブラリをインポート
from time import sleep				# ウェイトのために使う
import random						# ランダム数作成
import datetime

# ブローカーに接続できたときの処理
def on_connect(client, userdata, flag, rc):
	print("Connected with result code " + str(rc))

# ブローカーが切断したときの処理
def on_disconnect(client, userdata, flag, rc):
	if rc != 0:
		print("Unexpected disconnection.")

# publishが完了したときの処理
def on_publish(client, userdata, mid):
	print("publish: {0}".format(mid))

def main():
	topic = "topic_test01"
	cnt = 1
	client = mqtt.Client()							# クラスのインスタンス(実体)の作成
	client.on_connect = on_connect					# 接続時のコールバック関数を登録
	client.on_disconnect = on_disconnect	 		# 切断時のコールバックを登録
	client.on_publish = on_publish					# メッセージ送信時のコールバック

	client.connect("fast-fjord-64260.herokuapp.com")			# 接続先はローカルのMQTTブローカー

	# 通信処理スタート
	# subscriberはloop_forever()だが，publishはloop_start()で起動だけさせる
	client.loop_start()

	while True:
		#############ここだけ青沼が改変
		dt_now = datetime.datetime.now()
		td = datetime.timedelta(seconds=random.randrange(59), minutes=random.randrange(59))
		dt_now_td = dt_now + td

		send_msg = '{"interested":%d,"age":%d,"gender":%d,"start_time":"%s","end_time":"%s"}' % \
			(random.randrange(100), random.randrange(65),random.randrange(2),dt_now, dt_now_td)
		#idは自動インクリメントなので、idは送らなくてよい
		###############

		print(send_msg)					# メッセージを表示

		client.publish(topic,send_msg)	# トピック名とメッセージを決めて送信
		sleep(1)	 					# 1秒待つ

if __name__ == '__main__':
	main()			