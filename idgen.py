#!/usr/bin/python3

__name__ = "idgen"
__author__ = "lvlrk"
__version__ = 1.0

import sys
import urllib3
import codes
import os
import hashlib
import gameid

http = urllib3.PoolManager()

generate = False

usage = f"""usage: {__name__} [-g]
     --help      display this help
     --version   print version information
 -g, --generate  generate a game ID"""

if len(sys.argv) < 2:
	print(usage)
	exit(1)

for i in range(len(sys.argv)):
	if sys.argv[i] == "-g" or sys.argv[i] == "--generate":
		generate = True
	if sys.argv[i] == "--help":
		print(usage)
		exit(0)
	if sys.argv[i] == "--version":
		print(f"{__name__}-{__version__} {__author__}")
		exit(0)

if os.path.exists("wiitdb.txt") == False:
	print("warning: wiitdb.txt not found")
	print("download from gametdb.com? [y/n]")
	choice = input()
	if choice == "y":
		print("downloading database")
		resp = http.request("GET", "https://www.gametdb.com/wiitdb.txt")
		if resp.status != 200:
			print(f"error: bad http request {resp.status}")
			print(usage)
			exit(1)
		with open("wiitdb.txt", "w") as f:
			f.write(resp.data.decode("utf-8"))
			f.close()

		print("finished without error")
	else:
		print("error: cannot download database")
		exit(0)

titles = []

rawdb = ""
rawdbhash = "ac9e207cb21e7835bd8a5ec9484c2b2a904cf90e685c696248204f95417f5df8"

with open("wiitdb.txt", "r") as f:
	rawdb = f.read()
	f.close()

print(hashlib.sha256(rawdb.encode("utf-8")).hexdigest())
if hashlib.sha256(rawdb.encode("utf-8")).hexdigest() != rawdbhash:
	print("warning: outdated database")
	print("re-download database from gametdb.com? [y/n]")
	choice = input()
	if choice == "y":
		print("re-downloading database")
		resp = http.request("GET", "https://www.gametdb.com/wiitdb.txt")
		if resp.status != 200:
			print(f"error: bad http request {resp.status}")
			print(usage)
			exit(1)
		with open("wiitdb.txt", "w") as f:
			f.write(resp.data.decode("utf-8"))
			f.close()

		print("finished without error")
	else:
		print("error: cannot re-download database")
		exit(0)

for line in rawdb.split("\n"):
	entry = line.split(" = ")
	if entry[0] != "TITLES" and len(entry) >= 2:
		titles.append({"id": entry[0], "name": entry[1]})

print("title_codes = [", end="")
    
for title in titles:
    gid = gameid.gameid(title["id"])
    print("{" + f'"id": "{gid.title}", "name": "{title["name"]}"' + "}")
    
print("]")
