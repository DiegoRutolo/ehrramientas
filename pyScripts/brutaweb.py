#!/usr/bin/env python3

'''
	uso: brutaweb.py [-o file] TARGET 
'''

import argparse
import requests
import sys
import itertools
from time import sleep
from threading import Thread


CHARSET_COMPLETO = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~:/?#[]@!$&\'()*+,;='
CHARSET_SIMPLE = 'abcdefghijklmnopqrstuvwxyz.-_'
STATUS = (200, 401, 403)


parser = argparse.ArgumentParser(description='Buscador de URLs por fuerza bruta.')
parser.add_argument('-o', '--output', action='append', dest='out_file', help='Archivo de salida')
parser.add_argument('-n', '--min', type=int, default=2, dest='min', help='Número mínimo de caracteres')
parser.add_argument('-m', '--max', type=int, default=10, dest='max', help='Número máximo de caracteres')
parser.add_argument('-d', '--delay', type=int, default=1, dest='delay', help='milisegundos de espera entre cada petición')
parser.add_argument('-v', '--verbose', action='count', default=0, help='Cantidad de información a mostrar')
parser.add_argument('target', help='Url objetivo', metavar='TARGET')

args = parser.parse_args()

target = args.target if args.target.startswith('http') else 'http://' + args.target
if not target.endswith("/"):
	target += "/"

try:
	print("Probando conexión a " + target)
	resp = requests.get(target)
	if not resp.status_code in STATUS:
		print("Error de conexión: " + str(resp.status_code))
		sys.exit()
except:
	print("Error al conectarse a " + target)
	sys.exit()

print("Conexión correcta")
print()

# Aquí empieza la fiesta
def log(url, status):
	if args.verbose >= 1:
		linea = url + " " + str(status)
		if status in STATUS:
			linea += " *** EXITO *** "
		print(linea)
	else:
		if status in STATUS:
			print(url)
	
	if args.out_file != None and status in STATUS:
		with open(args.out_file[0], 'a') as file:
			file.write(url + "\n")

def prueba(url):
	try:
		resp = requests.get(url)
	except KeyboardInterrupt:
		raise
	except:
		pass

	log(target+pal, resp.status_code)

for n in range(args.min, args.max+1):
	for p in itertools.combinations_with_replacement(CHARSET_SIMPLE, n):
		try:
			sleep(args.delay/1000)
			pal = ""
			for l in p:
				pal += l
			
			hilo = Thread(target=prueba, args=(target+pal,))
			hilo.start()
		except (KeyboardInterrupt, SystemExit):
			print("Interrumpiendo...")
			sys.exit()
		
