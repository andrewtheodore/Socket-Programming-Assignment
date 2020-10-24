# This script should be run whenever a new worker node is registered
# It creates a new socket instance that listens to port 80 (HTTP)
# Worker node will then send his own IP to the master node


from threading import Thread
import socket
import urllib.request
import json

from time import sleep


def parse_job(job_str):
	job = json.loads(job_str)
	return job


def perform_job(job_type, job_params):
	if job_type == '1':
		sleep(5)
		# Performs a summation of several integers
		result = 0
		for i in job_params:
			result += int(i)

		return result

	elif job_type == '2':
		# Return the product of several integers
		sleep(10)
		result = job_params[0]
		for i in job_params[1:]:
			result *= int(i)

		return result

	elif job_type == '3':
		# Return (((((a[0]^a[1])^a[2])^a[3])^...)^a[n])
		sleep(20)
		result = job_params[0]
		for i in job_params[1:]:
			result = (result**int(i))

		return result

	else:
		# Invalid job type
		raise Exception()


def check_data(job):
	if not(('id' in job) and ('type' in job) and (int(job['type']) in range(1, 4))):
		raise Exception()


def wait_response(sock):
	while True:
		response = sock.recv(1024)
		if response:
			break


def update_job_status(sock, id, status):
	resp = {
		'id': id,
		'status': status
	}
	sock.send(json.dumps(resp).encode('utf-8'))
	wait_response(sock)


def send_job_result(sock, id, result):
	resp = {
		'id': id,
		'status': 'SUCCESS',
		'result': result
	}
	sock.send(json.dumps(resp).encode('utf-8'))
	wait_response(sock)


def handle_job(sock):
	# Receive all of the data first
	whole_data = sock.recv(1024).decode('utf-8')

	print("Here is the full request:", whole_data)
	# Parse the message
	job = parse_job(whole_data)
	try:
		check_data(job)
		# Update job status
		update_job_status(sock, job['id'], 'WORKING')
		try:
			result = perform_job(job['type'], job['params'])
			send_job_result(sock, job['id'], result)
		except:
			update_job_status(sock, job['id'], 'FAILED')
	except:
		update_job_status(sock, job['id'], 'BAD_JOB')

	sock.close()


listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = int(input("Enter port number: "))

listener.bind(('', port))
print("socket binded to {}".format(port))

listener.listen(3)

print("socket is listening")

# Return this instance's private IP address
sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

PRIVATE_IP = "127.0.0.1"  # urllib.request.urlopen("http://169.254.169.254/latest/meta-data/local-ipv4").read()

while True:
	c, addr = listener.accept()
	print("Job request from", addr)

	handle_job(c)

listener.close()