from django.db import models
from datetime import datetime

JOB_TYPE = {
    ('1', 'Summation'),
    ('2', 'Given N. Count how many possibility of a * b = c * d'),
    ('3', 'Exponentiation'),
    ('4', 'Levenshtein\'s Distance')
}

class Job(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=50)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE, default='0')
    worker = models.CharField(max_length=30, default='N/A')
    request_timestamp = models.DateTimeField(auto_now_add=True)
    job_work_time = models.DateTimeField(default=None, blank=True, null=True)
    status = models.CharField(max_length=20, default='CREATED')
    parameters = models.CharField(max_length=255, default='')
    
    
class Worker(models.Model):
    id = models.AutoField(primary_key = True)
    ip = models.CharField(max_length=15)
    port = models.IntegerField(default=1337)
