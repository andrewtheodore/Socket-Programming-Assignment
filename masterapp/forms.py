from django import forms
from .models import Job, Worker

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = {'name', 'job_type', 'parameters'}
        labels = {
            'name'          : 'Enter job name',
            'job_type'      : 'Enter job type',
	    'parameters'    : 'Enter parameters for the job',
        }
        
        
class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = {'ip', 'port'}
        labels = {
            'ip'    : "Enter the worker's Private IP",
            'port'  : "Enter the accepting port",
        }
