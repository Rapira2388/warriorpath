from django.contrib import admin
from django.db.models import Count
from django.conf import settings

from ..models import Board
import gensokyo.config as config


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):

    # List options
    # ==================================================================================================================
    list_display = (
        'id', 'hid',
        'name', 'url', 'threads_num', 'default_username',
        'default_max_posts_num', 'admin_last_thread_hid',
        'is_hidden', 'is_locked', 'is_deleted',
        'created_at', 'updated_at',
    )

    list_editable = (
        'is_hidden', 'is_locked', 'is_deleted',
    )

    # Editor options
    # ==================================================================================================================
    readonly_fields = (
        'id',
        'created_at',
        'updated_at',
        'admin_last_thread_hid',
        'threads_num',
    )

    save_on_top = True

    fieldsets = (
        (None, {
            'fields': (
                'id',
                'hid',
                'name',
                'url',
                ('created_at', 'updated_at',),
                ('threads_num', 'admin_last_thread_hid',),
            ),
        }),

        ('About board', {
            'fields': (
                ('description', 'rules',),
            ),
        }),

        ('Defaults', {
            'fields': (
                'default_username',
                'default_max_posts_num',
            ),
        }),

        ('Flags', {
            'fields': (
                ('is_hidden', 'is_locked', 'is_deleted',),
            ),
        }),
    )

    # Modified main queryset (prefetch some related stuff)
    # ==================================================================================================================
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(threads_num=Count('threads'))

    # Custom fields
    # ==================================================================================================================
    def threads_num(self, obj):
        return obj.threads_num
    threads_num.short_description = 'Threads'

    def admin_last_thread_hid(self, obj):
        return config.THREAD_HID_FORMAT.format(hid=obj.last_thread_hid) if obj.last_thread_hid else None
    admin_last_thread_hid.short_description = 'Last thread HID'