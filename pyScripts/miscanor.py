#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import socket
from datetime import datetime
import threading



def escanear(ip, puerto):
	s = socket.socket()
	socket.setdefaulttimeout(1)
	result = s.connect_ex((target, port))
	if result == 0:
		print("Puerto {} abierto".format(port))
	s.close()




if (len(sys.argv) == 1):
	print("p3 miscanor.py <IP> [[<PUERTO_INICIAL>] <PUERTO_FINAL>]")
	sys.exit()

target = socket.gethostbyname(sys.argv[1])
portIni = 1
portFin = 1000

if (len(sys.argv) == 3):
	portFin = int(sys.argv[-1])
if (len(sys.argv) == 4):
	portIni = int(sys.argv[-2])
	portFin = int(sys.argv[-1])


print("*" * 50)
print("Escaneando: " + target)
print("Puertos: " + str(portIni) + "-" + str(portFin))
print("Hora: " + str(datetime.now()))
print("*" * 50)
print()

try:
	hilos = {}
	for port in range(portIni, portFin):
		hilos[port] = threading.Thread(target=escanear, args=(target, port))
		hilos[port].start()
	
	for h in hilos.values():
		h.join()
except KeyboardInterrupt:
	print("\nInterrumpido")
	sys.exit()
except socket.gaierror:
	print("\nNo se pudo resolver el host")
	sys.exit()
except socket.error:
	print("\nError de conexion")
