import time
import subprocess

localtime = time.localtime()
timestamp = "%04d%02d%02d_%02d%02d_%02d" % (localtime.tm_year, localtime.tm_mon, localtime.tm_mday, localtime.tm_hour, localtime.tm_min, localtime.tm_sec)

devnull = open("/dev/null", "w")
p_record = subprocess.Popen(["record", "../../image_data_capture/" + timestamp], stdout=devnull)

key_logfile = open("../../key_data_capture/" + timestamp + "_keylog.txt", "wb")
p_keylog = subprocess.Popen(["python", "../keylogger/keylogger.py"], stdout=key_logfile)

p_keylog.wait()
p_record.terminate()
