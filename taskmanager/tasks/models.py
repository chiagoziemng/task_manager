from django.db import models
from django.contrib.auth.models import User

class Epic(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User,
    related_name='created_epics', on_delete=models.CASCADE)


class Sprint(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User,
    related_name='created_sprints', on_delete=models.CASCADE)
    tasks = models.ManyToManyField('Task',
    related_name='sprints', blank=True)

class VersionMixing:
    version = models.IntegerField(default=0)

class Task(VersionMixing, models.Model):
    STATUS_CHOICES = [
    ("UNASSIGNED", "Unassigned"),
    ("IN_PROGRESS", "In Progress"),
    ("DONE", "Completed"),
    ("ARCHIVED", "Archived"),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=False, default="")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="UNASSIGNED", 
                              db_comment="Can be UNASSIGNED, IN_PROGRESS, DONE, or ARCHIVED.",)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, related_name="created_tasks", on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name="owned_tasks", on_delete=models.SET_NULL, 
                              null=True, db_comment="Foreign Key to the User who currently owns the task.",)
    class Meta:
        db_table_comment = "Holds information about tasks"




