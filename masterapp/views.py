from django.shortcuts import render
from .models import Job
from .forms import JobForm
from .thread import add_job

def home(request):
	#  TODO: Call add_job when user click 'Submit'
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
	job_list = Job.objects.all()
	return render(request, 'index.html', {'form' : form, 'job_list' : job_list})