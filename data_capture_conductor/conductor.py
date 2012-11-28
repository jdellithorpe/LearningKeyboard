import time
import subprocess
import sys

# get path to images
images_path = sys.argv[1]

# get path to keylogs
keylogs_path = sys.argv[2]

localtime = time.localtime()
timestamp = "%04d%02d%02d_%02d%02d_%02d" % (localtime.tm_year, localtime.tm_mon, localtime.tm_mday, localtime.tm_hour, localtime.tm_min, localtime.tm_sec)

devnull = open("/dev/null", "w")
p_record = subprocess.Popen(["record", images_path + timestamp], stdout=devnull)

key_logfile = open(keylogs_path + timestamp + "_keylog.txt", "wb")
p_keylog = subprocess.Popen(["python", "../keylogger/keylogger.py"], stdout=key_logfile)

p_keylog.wait()
p_record.terminate()
