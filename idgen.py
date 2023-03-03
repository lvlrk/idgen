#!/nix/store/h4h5rxs0hzpzvz37yrwv1k2na1acgzww-python3-3.9.15/bin/python3

__name__ = "idgen"
__author__ = "lvlrk"
__version__ = 1.0

import sys
import urllib3
import codes
import os
import hashlib
import random
import string

http = urllib3.PoolManager()

generate = False
generatecount = 0
lookup = False
lookuptitle = ""

usage = f"""usage: {__name__} [-g]
     --help               display this help
     --version            print version information
 -g, --generate [COUNT]   generate [COUNT] game IDs
 -l, --lookup [TITLE]     lookup [TITLE]"""

if len(sys.argv) < 2:
	print(usage)
	exit(1)

for i in range(len(sys.argv)):
	if sys.argv[i] == "-g" or sys.argv[i] == "--generate":
		if len(sys.argv) >= i + 2:
			generate = True
			generatecount = int(sys.argv[i + 1])
		else:
			print(f"{sys.argv[i]}: requires an argument [COUNT]")
			print(usage)
			exit(1)
	elif sys.argv[i] == "-l" or sys.argv[i] == "--lookup":
		if len(sys.argv) >= i + 2:
			lookup = True
			lookuptitle = sys.argv[i + 1]
		else:
			print(f"{sys.argv[i]}: requires an argument [TITLE]")
			print(usage)
			exit(1)
	elif sys.argv[i] == "--help":
		print(usage)
		exit(0)
	elif sys.argv[i] == "--version":
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
rawdbhash = "f900c3fe8ac8d1ce5ec04ad8069bf5ec9ba35aba068b773844c5120a56b2dc56"

with open("wiitdb.txt", "r") as f:
	rawdb = f.read()
	f.close()

# print(hashlib.sha256(rawdb.encode("utf-8")).hexdigest())
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

#print("title_codes = [", end="")    
#for title in titles:
#    print("\t{" + f'"id": "{title["id"]}", "name": "{title["name"]}"' + "},")
#print("]")

if generate:
	code = ["", "", "", "", "", ""]
	
	systems = []
	for sys in codes.system_codes:
		systems.append(sys["id"])
	
	print(codes.system_codes)
	print(f"which system code (default {codes.system_codes[13]}):")
	system = input()
	if system == '' or system not in systems:
		system = codes.system_codes[13]["id"]

	print(f"which title code (default random):")
	title = input()
	if title == '':
		title = random.choices(codes.title_characters, k=2)

	regions = []
	for reg in codes.region_codes:
		regions.append(reg["id"])

	print(codes.region_codes)
	print(f"which region code (default {codes.region_codes[3]}):")
	region = input()
	if region == '' or region not in regions:
		region = codes.system_codes[2]["id"]
	
	for i in range(generatecount):
		code[0] = system
		code[1:2] = title
		code[3] = region
		print("".join(code))

if lookup:
	print(f"searching for '{lookuptitle}'")
	title_ids = []
	for title in codes.title_codes:
		title_ids.append(title["id"])

	lookupcount = 0

	for title in codes.title_codes:
		if lookuptitle.lower() in title["name"].lower():
			index = title["name"].lower().find(lookuptitle.lower())
			name = title["name"][:index] + "\033[1;32m" + lookuptitle.upper() + "\033[0m" + title["name"][(index + len(lookuptitle)):]
						
			print(str(title).replace(title["name"], name))
				
			lookupcount += 1

	print(f"found {lookupcount} matches")