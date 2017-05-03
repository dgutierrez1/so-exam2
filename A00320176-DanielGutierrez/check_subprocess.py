import time, psutil



def run():

	while True:
	
		check.cpu = get_cpu_pecentage()
		print(check)
		print(check.cpu)


		time.sleep(2)



def get_cpu_percentage():
	return "CPU PERCENTAGE: " + str(psutil.cpu_pencentage()*100) + "%"
