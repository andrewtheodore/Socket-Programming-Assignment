from queue import Queue
from threading import Thread
import socket
import urllib.request
import json

ID = 0

def supervise_jobs(job, worker, worker_queue):
	s = socket.socket()
	s.connect(worker)
	s.send(json.dumps(job).encode('utf-8'))
	while True:
		whole_data = s.recv(1024).decode('utf-8')
		print("Worker sends his/her regards:", whole_data)
		s.send("Got it!".encode('utf-8'))
		upd = json.loads(whole_data)
		print("Status is now", upd['status'])  # TODO: Update the Django DB
		if upd['status'] == 'SUCCESS':
			print("Answer:", upd['result'])  # TODO: Update the Django DB
		if not upd['status'] == 'WORKING':
			break
	s.close()
	worker_queue.put(worker)


def schedule_jobs(job_queue, worker_queue):
	while True:
		job = job_queue.get()
		worker = worker_queue.get()
		Thread(target = supervise_jobs, args = (job, worker, worker_queue)).start()


q = Queue()
vm = Queue()
vm.put(('127.0.0.1', 1337))
vm.put(('127.0.0.1', 1339))

sj = Thread(target = schedule_jobs, args = (q, vm))
sj.start()

while True:
	typ = input("Set a job: ")
	job = {
		'id': ID,
		'type': typ,
		'params': [2, 2, 2]
	}
	q.put(job)

	ID += 1