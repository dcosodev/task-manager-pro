from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    priority = models.IntegerField(default=1)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
