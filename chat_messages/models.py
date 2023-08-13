from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    supervisor = models.CharField(max_length=50)
    student1 = models.CharField(max_length=50, default='')
    student2 = models.CharField(max_length=50, default='')
    student3 = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.CharField(max_length=100)
    sender = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.content}"
