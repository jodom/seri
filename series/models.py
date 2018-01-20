from django.db import models

# Create your models here.
class Serie(models.Model):
    # author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    limit = models.IntegerField(default=100)
    public = models.BooleanField(default=True)

    # def notes(self)
    def publish(self):
        self.save()

    def __str__(self):
        return self.title

class Note(models.Model):
    serie = models.ForeignKey('Serie')
    content = models.TextField(blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def publish(self):
        self.save()

    def __str__(self):
        return self.content
