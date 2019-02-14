# Create your models here.
import datetime

from django.db import models
from django.utils import timezone
from django.forms import ModelForm
# Create your models here.

class Activity(models.Model):
    activity_id = models.AutoField(primary_key=True)
    activity_title = models.CharField(max_length=200)
    activity_content = models.TextField(null=True, blank =True)

    # STATUS_CHOICES = (
    #     (1, 'Open'),
    #     (2, 'Closed'),
    #     (3, 'On-going'),
    #     (4, 'Cancel'),
    #     (5, 'Pending'),
    # )
    # status = models.IntegerField(choices=STATUS_CHOICES, default=1)

    owner = models.CharField(max_length=200, null=True, blank =True)
    numberofmem = models.PositiveSmallIntegerField(null=True, blank =True)
    budget = models.PositiveSmallIntegerField(null=True, blank =True)
    # pub_date = models.DateTimeField(auto_now_add=True, 'date published')
    pub_date = models.DateTimeField(auto_now_add=True)
    now = timezone.now()
    start_time = models.DateTimeField('start time', default=now,blank=True)
    duration = models.TimeField('duration', null = True)
    location = models.TextField(null = True, blank = True)
    def publish(self):
        self.pub_date = timezone.now()
        self.save()
    def __str__(self):
        return self.activity_title
    # def was_published_recently(self):
    #     now = timezone.now()
    #     return now - datetime.timedelta(days = 1) <= self.pub_date <= now

class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        now = timezone.now()
        fields = ['activity_title', 'activity_content', 'owner', 'numberofmem', 'start_time', 'duration', 'location']
        #start_time = forms.DateTimeField(initial=now, required=False)