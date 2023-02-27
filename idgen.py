#!/usr/bin/python3

import random
import sys
import wget
import os

def mkId(region, system, pub, game=''):
    ch = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"

    tmp = []
    tmp = list("      ")

    tmp[0] = system
    if game == '':
        tmp[1] = random.choice(ch)
        tmp[2] = random.choice(ch)
    else:
        tmp[1] = game[0]
        tmp[2] = game[1]

    tmp[3] = region
    tmp[4] = pub[0]
    tmp[5] = pub[1]

    return "".join(tmp)

version = 0.2
url = "https://www.gametdb.com/wiitdb.txt"
db = "wiitdb.txt"
prompt = False
count = -1
h = "usage: idgen.py [-pcd]\n"\
    "     --help      print this help\n"\
    "     --version   print version info\n"\
    " -p, --prompt    prompt user for id codes\n"\
    " -c, --count     how many ids to make\n"\
    " -d, --database  title database file"

regions = [{'A': "all"}, {'B': "virtual"}, {'C': "china emu"},
           {'D': "german"}, {'E': "NTSC"}, {'F': "french"},
           {'I': "italian"}, {'J': "japan"}, {'K': "korea"},
           {'L': "japan2pal"}, {'M': "NTSC2pal"}, {'N': "japan2NTSC"},
           {'P': "pal"}, {'Q': "koreajapan"}, {'S': "spain"},
           {'T': "koreaNTSC"}, {'U': "wiiware"}, {'W': "taiwan"},
           {'X': "homebrew"}]
regions_str = "ABCDEFIJKLMNPQSTUWX"

systems = [{'C': "commodore"}, {'D': "demo"}, {'E': "virtual"},
           {'F': "nes"}, {'G': "gc"}, {'H': "channel"},
           {'J': "snes"}, {'L': "master"}, {'M': "megadrive"},
           {'N': "n64"}, {'P': "turbografx"}, {'Q': "turbografx cd"},
           {'R': "old wii"}, {'S': "new wii"}, {'W': "wiiware"},
           {'X': "msx"}]
systems_str = "CDEFGHJLMNPQRSWX"

pubs = [{"00": "Nintendo"}, {"01": "Nintendo"}, {"08": "Capcom"},
            {"AF": "Namco Bandai Games"}, {"ZZ": "Nintendo"}]
pubs_str = ["00", "01", "08", "ZZ", "AF"]


#if len(sys.argv) < 2:
    #print(h)
    #exit(1)

for i in range(len(sys.argv)):
    if sys.argv[i] == "-p" or sys.argv[i] == "--prompt":
        prompt = True
    if sys.argv[i] == "--version":
        print(f"idgen-{str(version)}")
        exit()
    if sys.argv[i] == "-c" or sys.argv[i] == "--count":
        if len(sys.argv) - 2 >= i:
            count = int(sys.argv[i + 1])
        else:
            print(f"{sys.argv[i]} requires 1 argument")
            exit(1)
    if sys.argv[i] == "-d" or sys.argv[i] == "--database":
        if len(sys.argv) - 2 >= i:
            db = sys.argv[i + 1]
        else:
            print(f"{sys.argv[i]} requires 1 argument")
            exit(1)

    if sys.argv[i] == "--help":
        print(h)
        exit()

if os.path.exists(db) == False:
    print(f"file {db} not found")
    if os.path.exists("wiitdb.txt") == False:
        print("downloading wiitdb.txt")
        wget.download(url)
        db = "wiitdb.txt"
    else:
        print("db = wiitdb.txt")
        db = "wiitdb.txt"
    print("\n")

print("idgen - A shitty Wii custom game ID generator\nby lvlrk\n")

if prompt:
    for i in regions:
        print(i)
    print("\nWhich region (default: {'E': 'NTSC'}): ")
    sregion = input()
    if(sregion == '' or sregion not in regions_str):
        sregion = 'E'

    print()

    for i in systems:
        print(i)
    print("\nWhich system (default: {'S': 'new wii'}): ")
    ssystem = input()
    if(ssystem == '' or ssystem not in systems_str):
        ssystem = 'S'

    print()

    for i in pubs:
        print(i)
    print("note: publisher list isnt complete yet")
    print("\nWhich publisher (default: {'00': 'Nintendo'}): ")
    spub = input()
    if(spub == '' or spub not in pubs_str):
        spub = "00"

    print()

    print("\nWhich game (optional): ")
    sgame = input()
    if sgame == '':
        custom = False
    else:
        custom = True

    print()
else:
    sregion = 'E'
    ssystem = 'S'
    spub = "AF"

with open(db, "r") as f:
    dat = f.read()
    f.close()

ids = []

for line in dat.split("\n"):
    ids.append(line.split(" ")[0])

ch = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
tid = ""
tidl = []

nids = []

lc = count
bbb = 0

if count == -1:
    while True:
        tid = mkId(sregion, ssystem, spub, sgame)

        if tid not in ids:
            print(tid)

elif count > 0:
    if sgame != '':
        lc = 1
    
    while bbb < lc:
        tid =  mkId(sregion, ssystem, spub, sgame)
        if tid not in ids:
            print(tid)
        else:
            print(f"{tid} found in database")
            print("\ntry for another id [y/n]: ")
            choice = input()

            if choice == 'y':
                print()
                sgame = "".join(random.choices(ch, k=2))
                bbb -= 1
            else:
                exit(0)

        bbb += 1
