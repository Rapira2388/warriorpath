from django.db import models
from django.conf import settings

import gensokyo.config as config


class Thread(models.Model):
    """docstring for Thread"""
    hid = models.IntegerField(editable=False, db_index=True)
    board = models.ForeignKey('Board', related_name='threads', on_delete=models.CASCADE, db_index=True)

    op = models.ForeignKey('Post', on_delete=models.CASCADE, db_index=True, related_name='+', null=True)
    # NOTE: 'plus' sign for 'related_name' disables reverse lookup, we don't need it here.
    # see: https://docs.djangoproject.com/en/2.0/ref/models/fields/#django.db.models.ForeignKey.related_name

    is_sticky = models.BooleanField(default=False, db_index=True)
    is_locked = models.BooleanField(default=False, db_index=True)
    is_deleted = models.BooleanField(default=False, db_index=True)

    max_posts_num = models.IntegerField()

    last_post_hid = models.IntegerField(null=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False, db_index=True)

    class Meta:
        unique_together = ['board', 'hid']
        indexes = []

    def posts_count(self):
        return self.posts.count()

    def hid2hex(self):
        return config.THREAD_HID_FORMAT.format(hid=self.hid)