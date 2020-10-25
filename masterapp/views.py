from django.shortcuts import render, redirect
from .models import Job, Worker
from .forms import JobForm, WorkerForm
from .thread import add_job, add_worker
import socket
import json

def home(request):
	if request.method == 'POST':
		form = JobForm(request.POST)
		if form.is_valid():
			saved_job = form.save()
			job_pack = {
				'id': saved_job.id,
				'type': saved_job.job_type,
				'params': [2, 2, 2]
			}
			print(job_pack)
			add_job(job_pack)
	
	form = JobForm()
	w_form = WorkerForm()
	job_list = Job.objects.all()
	return render(request, 'index.html', {'form' : form, 'w_form': w_form, 'job_list' : job_list})
	
	
def register_worker(request):
	if request.method == 'POST':
		form = WorkerForm(request.POST)
		if form.is_valid():
			# Try to connect to the worker first
			s = socket.socket()
			s.connect((form.data['ip'], int(form.data['port'])))
			conn_pack = {
				'id': 0,
				'type': 0,
				'params': []
			}
			s.send(json.dumps(conn_pack).encode('utf-8'))
			while True:
				result = json.loads(s.recv(1024).decode('utf-8'))
				s.send("Got it".encode('utf-8'))
				print(result)
				if 'result' in result:
					break
			password = result['result']
			s.close()
			
			# Add worker to queue
			worker_pack = {
				'dest': (form.data['ip'], int(form.data['port'])),
				'password': password
			}
			add_worker(worker_pack)
			
	return redirect('home')
