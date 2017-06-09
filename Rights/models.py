# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User)
    # student_id = models.CharField(max_length=10, primary_key=True)
    nickname = models.CharField(max_length=10)
    academy = models.CharField(max_length=10)
    classes = models.CharField(max_length=15)
    mobile = models.CharField(max_length=11)

    class Meta:
        ordering = ['classes']

    def __unicode__(self):
        return self.user.username

class Arcitle(models.Model):
    title = models.CharField(max_length=25)
    body = models.TextField()
    # comment = models.CharField(max_length=250)

    author = models.ForeignKey(User,default=None)
    slug = models.SlugField(max_length=250, unique_for_date='publishtime')
    publishtime = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-publishtime']

    def __unicode__(self):
        return self.title