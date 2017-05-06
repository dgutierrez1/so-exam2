import time, psutil, json, os
from subprocess import Popen, PIPE
from database import db, Check
import threading
from datetime import datetime

active = threading.Event()
thr = threading.Thread()

def run_process():
	db.create_all()
	active.clear()
	thr = threading.Thread(target=check_loop)
	thr.daemon = True
	thr.start()
	time.sleep(2)

def check_loop():

	max = 100

	while not active.isSet():

		checks = Check.query.all()
		db_size = len(checks) -1

		if(db_size > 99):
			db.session.delete(cheks[0])


		cpu = get_cpu_percent()
		memory = get_memory()
		disk = get_disk_usage()
		httpd = get_service()

		check = Check(cpu, memory, disk, httpd)
		db.session.add(check)
		db.session.commit()
		print("cpu: "+cpu+"| memory: "+memory+" | disk: "+disk+" | httpd service: "+httpd+" | time: "+str(datetime.now()))
		time.sleep(60)


def stop_process():
	active.set()
	#thr._stop()

def get_process_status():
	return not active.isSet()

def all_checks_query():
	db.create_all()
	checks = Check.query.all()
	checks_json = []

	for check in checks:
		obj_json = {"cpu":check.cpu, "memory": check.memory, "disk": check.disk, "httpd": check.httpd  }
		check_json = json.dumps(obj_json)
		checks_json.append(check_json)

	return checks_json

def cpu_query(param):
	db.create_all()
	checks = Check.query.all()
	cpu_check_list = []

	for x in range(0, param):
		check = checks[x]
		obj_json = {"cpu":check.cpu}
		check_json = json.dumps(obj_json)
		cpu_check_list.append(check_json)

	return cpu_check_list

def activate_httpd():
	Popen(["service","httpd","start"], stdout=PIPE, stderr=PIPE)

def inactivate_httpd():
	Popen(["service","httpd","stop"], stdout=PIPE, stderr=PIPE)

def get_status_httpd():
	return  Popen(["service","httpd","status", "|" , "grep", "Active:"], stdout=PIPE, stderr=PIPE).communicate()[0].split('\n')[2]

def get_cpu_percent():
	cpu = psutil.cpu_percent()
	str_cpu = str(cpu)
	return "CPU PERCENTAGE( " + str_cpu + "% )"

def get_memory():
	memory = psutil.virtual_memory()
	str_memory = str(memory)
	return "MEMORY USAGE( "+ str_memory +")"

def get_disk_usage():
	st = os.statvfs('/')
	free = str(st.f_bavail * st.f_frsize)
	total = str(st.f_blocks * st.f_frsize)
	used = str((st.f_blocks - st.f_bfree) * st.f_frsize)
	return "DISK USAGE( Total: " + total + " , Free: " + free +" , Used: "+ used +" )"

def get_service():
	service_status = get_status_httpd()
	return "HTTPD SERVICE STATUS( "+ service_status +" )"
