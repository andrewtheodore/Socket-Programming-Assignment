# This script should be run whenever a new worker node is registered
# It creates a new socket instance that listens to port 80 (HTTP)
# Worker node will then send his own IP to the master node


from threading import Thread
import socket
import urllib.request
import json
import random
import string

from time import sleep


letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
passwd = ''.join(random.choice(letters) for i in range(12))

def parse_job(job_str):
	job = json.loads(job_str)
	return job

def levenshtein_distance(i, j, string_1, string_2):
    if min(i, j) == 0:
        return max(i, j)
    lev_3_int = 0 if string_1[i - 1] == string_2[j - 1] else 1
    lev_1 = levenshtein_distance(i - 1, j, string_1, string_2) + 1
    lev_2 = levenshtein_distance(i, j - 1, string_1, string_2) + 1
    lev_3 = levenshtein_distance(i - 1, j - 1, string_1, string_2) + lev_3_int
    return min(lev_1, lev_2, lev_3)

def perform_job(job_type, job_params):
	if job_type == '0':
		# Accept registration from master node
		return passwd
		
	elif job_type == '1':
		# Performs a summation of several integers
		result = 0
		for i in job_params:
			result += int(i)

		return result

	elif job_type == '2':
		# Return how many possibilty of a * b = c * d when 0 < a, b, c, d < n. Complexity O(n^4)
		n = job_params[0]
		result = 0
		for a in range(1, n):
			for b in range(1, n):
				for c in range(1,n):
					for d in range(1, n):
						if a * b == c * d:
							result = result + 1
		return result

	elif job_type == '3':
		# Return (((((a[0]^a[1])^a[2])^a[3])^...)^a[n]). Complexity O(a[0] + a[1] + ... + a[n])
		result = job_params[0]
		for i in job_params[1:]:
			result = (result**int(i))

		return result
	elif job_type == '4':
		#Return how many minimum number to change stringA to string B. Complextiy O(3^N)
		return levenshtein_distance(len(job_params[0]), len(job_params[1]), job_params[0], jobs_params[1])
	else:
		# Invalid job type
		raise Exception()


def check_data(job):
	if not(('id' in job) and ('type' in job) and (int(job['type']) in range(4))):
		raise Exception()
	if (int(job['type']) != 0) and not (('key' in job) and (job['key'] == passwd)):
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
			result = perform_job(str(job['type']), job['params'])
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
