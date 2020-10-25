from queue import Queue
from threading import Thread
import socket
import urllib.request
import json
from .models import Job

def supervise_jobs(job, worker, worker_queue):
	s = socket.socket()
	s.connect(worker['dest'])
	job['key'] = worker['password']
	s.send(json.dumps(job).encode('utf-8'))
	while True:
		whole_data = s.recv(1024).decode('utf-8')
		print("Worker sends his/her regards:", whole_data)
		s.send("Got it!".encode('utf-8'))
		upd = json.loads(whole_data)
		print("Status is now", upd['status'])  # TODO: Update the Django DB
		data = Job.objects.get(pk=int(upd['id']))
		data.status = upd['status']
		data.save()
		if upd['status'] == 'SUCCESS':
			print("Answer:", upd['result'])  # TODO: Update the Django DB
			data.result = upd['result']
			data.save()
		if not upd['status'] == 'WORKING':
			break
	s.close()
	worker_queue.put(worker)


def schedule_jobs(job_queue, worker_queue):
	while True:
		job = job_queue.get()
		worker = worker_queue.get()

		# Update the worker
		data = Job.objects.get(pk=job['id'])
		data.worker = str(worker['dest'])
		data.save()

		Thread(target = supervise_jobs, args = (job, worker, worker_queue)).start()


JOB_QUEUE = Queue()
WORKER_QUEUE = Queue()

sj = Thread(target = schedule_jobs, args = (JOB_QUEUE, WORKER_QUEUE))
sj.start()

def add_job(job):
	JOB_QUEUE.put(job)
	
def add_worker(worker):
	WORKER_QUEUE.put(worker)
