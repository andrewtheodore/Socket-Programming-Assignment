from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = {'name', 'job_type', 'parameters'}
        labels = {
            'name'          : 'Enter job name',
            'job_type'      : 'Enter job type',
	    'parameters'    : 'Enter parameters for the job',
        }
