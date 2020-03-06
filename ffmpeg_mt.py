# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import ffmpeg, argparse, os, sys, json, threading, time
from colorama import init
from termcolor import colored

init()

extensions = [
    '.mp4',
    '.mpeg',
    '.mpg',
    '.avi',
    '.mkv',
]

queue = []

event = threading.Event()

def convert(item, listitem):
    try:
        print("[INFO] Converting: %s" % listitem)
        ffmpeg.input(listItem).output(
        item,
        vcodec='h264',
        acodec='aac',
        format='mp4',
        strict='-2').run(
            capture_stdout=True,
            capture_stderr=True)
        print(colored("[DONE] Converted: %s" % listitem, "grey", "on_green"))
        event.set()
    except:
        print(colored("[ERROR] Error occured with: %s" % listitem, "white", "on_red"))

def check_codec(string):
    if string == "aac" or string == "h264":
        return True
    else:
        return False

def dir_path(string):
    if os.path.isdir(string):
        return True
    else:
        return False

parser = argparse.ArgumentParser(description='ffmpeg multithreaded utility')
parser._action_groups.pop()
required = parser.add_argument_group('Required arguments')
optional = parser.add_argument_group('Optional arguments')
required.add_argument('-d','--directory', help='Starting directory',required=True)
required.add_argument('-o','--output',help='Output directory', required=True)
required.add_argument('-O','--overwrite',help='Overwrite converted files', choices=['yes', 'no'], default="no")
optional.add_argument('-s','--silent', help='Show only QUEUES during scan - Default: no', choices=['yes', 'no'], default="no")
optional.add_argument('-t','--threads',help='Max parallel convertions - Default: 1', type=int, default=1)
args = parser.parse_args()

if args.threads <= 0:
    sys.exit(colored("[ERROR] Threads have to be bigger than zero.", "red"))

if dir_path(args.directory) == False or dir_path(args.output) == False:
    sys.exit(colored("[ERROR] Check your starting and ending directories and retry.", "red"))

for dirpath, dirnames, files in os.walk(args.directory):
    for name in files:
        if os.path.splitext(name.lower())[1] in extensions:
            finalFile = os.path.join(dirpath, name)
            try:
                fileInfo = ffmpeg.probe(finalFile, cmd='ffprobe')
                codecOne = fileInfo["streams"][0]["codec_name"]
                codecTwo = fileInfo["streams"][1]["codec_name"]
                if check_codec(codecOne) == False or check_codec(codecTwo) == False:
                    queue.append(finalFile)
                    print(colored("[QUEUED] %s" % finalFile, "grey", "on_green"))
                else:
                    if args.silent == "no":
                        print(colored("[OK-SKIP] %s" % finalFile, "grey", "on_yellow"))
            except:
                if args.silent == "no":
                    print(colored("[MISSING-CODEC-SKIP] %s" % finalFile, "white", "on_red"))

print("\n"+colored("[INFO] Scan finished. Starting convertions...", "yellow"))

for listItem in queue:
    time.sleep(1)
    destination = args.output
    if destination.endswith("\\") or destination.endswith("/"):
        item = "%s.mp4" % os.path.splitext(os.path.split(listItem)[1])[0]
    else:
        if sys.platform.startswith('win'):
            item = "%s\\%s.mp4" % (destination, os.path.splitext(os.path.split(listItem)[1])[0])
        else:
            item = "%s/%s.mp4" % (destination, os.path.splitext(os.path.split(listItem)[1])[0])
    
    if args.overwrite == "yes":
        if os.path.exists(item):
            print(colored("[INFO] Deleting %s ..." % item, "yellow"))
            try:
                os.remove(item)
                print(colored("[INFO] Deleted %s" % item, "green"))
            except:
                print(colored("[ERROR] An ERROR occured while deleting %s" % item, "red"))
    else:
        if os.path.exists(item):
            print(colored("[INFO] Skipping %s ..." % item, "yellow"))
            continue

    thread = threading.Thread(target = convert, args = (item, listItem,))
    thread.start()
    if threading.active_count() == int(args.threads) + 1:
        thread.join()
