from django.db import models
from django.conf import settings

import gensokyo.config as config


class Post(models.Model):
    """docstring for Post"""
    hid = models.IntegerField(editable=False, db_index=True)
    thread = models.ForeignKey('Thread', related_name='posts', on_delete=models.CASCADE, editable=False, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False, db_index=True)

    text = models.TextField(max_length=2048, blank=True)

    title = models.CharField(max_length=64, blank=True)
    author = models.CharField(max_length=32, blank=True)
    email = models.CharField(max_length=32, blank=True)
    password = models.CharField(max_length=16, blank=True)

    is_op = models.BooleanField(editable=False)

    user_was_warned = models.BooleanField(default=False)
    user_was_banned = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False, db_index=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, editable=False)

    replies = models.ManyToManyField('self', editable=False, db_index=True, symmetrical=False)

    ip_address = models.CharField(max_length=16, editable=False, db_index=True)

    class Meta:
        unique_together = ['thread', 'hid']
        indexes = []

    def hid2hex(self):
        return config.POST_HID_FORMAT.format(hid=self.hid)