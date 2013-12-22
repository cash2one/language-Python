from django.db import models

# Create your models here.
class Cates(models.Model):
    catename = models.CharField(max_length=200)
    parentcate = models.IntegerField(default=0)

    def __unicode__(self):
        return self.catename

class Posts(models.Model):
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=204800)
    pubdate = models.DateTimeField()
    visits = models.IntegerField(default=0)
    cateid = models.ForeignKey(Cates)
    digg = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

class Comms(models.Model):
    postid = models.ForeignKey(Posts)
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=204800)
    comdate = models.DateTimeField()
    author = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    website = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title

