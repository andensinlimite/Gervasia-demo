# -*- coding: utf-8 -*-
#!/usr/bin/env python
import wit
import json
import time
from gtts import gTTS
import os
from datetime import datetime

ACCESS_TOKEN="2ZUAK2RGAGEN3EAHE2SNQM37LBQCOQ26"

_keep = True

def detect_message(json_response, mensaje):
	for i in json_response[u'outcomes']:
		if i[u'intent'] == mensaje:
			return True
	return False

def gervi_dice(algo):
	#import pdb
	#pdb.set_trace()
	tts = gTTS(text=algo, lang='es')
	tts.save("out.mp3")
	os.system("mpg321 out.mp3 -quiet")
	pass

def callback(response):
	global _keep
	m = json.loads(response) if response else None
	if m and m['_text']:
		print(m)
		print("===						===")
		print(u"Gervi[Oye]: {}".format(m['_text']))
		print("===						===")

		ahora = datetime.now()
		h = ahora.hour

		_keep = not detect_message(m, u'adios')
		if detect_message(m, u'Saluda'):
			gervi_dice("Hola")
			if h > 6 and h < 12:
				gervi_dice("Buenos días")
			elif h > 12 and h < 20:
				gervi_dice("Buenas tardes")
			else:
				gervi_dice("muy buenas")
		elif detect_message(m, u'Que_tal'):
			gervi_dice("Yo muy bien, ¿y tu?")
		elif detect_message(m, u'Dame_la_hora'):
			horas = ahora.strftime("%I").lstrip('0')
			minutos = ahora.strftime("%M").lstrip('0')
			gervi_dice("Las "+horas+" y "+minutos)
		elif detect_message(m, u'Te_lo_agradecemos'):
			gervi_dice("De nada, muy amable")
		elif not _keep:
			gervi_dice("Adiós!")
			if h > 6 and h < 15:
				gervi_dice("Hasta luego")
			elif h >= 15 and h < 20:
				gervi_dice("Buenas tardes")
			else:
				gervi_dice("Buenas noches!")
	else:
		print("=== 					===")
		print(u"Gervasia no te entendió")
		gervi_dice("No te entiendo")
		print("=== 					===")

def listen_gervi():
	wit.init()
	response = wit.voice_query_auto(ACCESS_TOKEN)
	callback(response)
	wit.close()

if __name__ == "__main__":
	while _keep:
		print (".................")
		listen_gervi()

