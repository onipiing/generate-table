# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import TableRow, TableHeader

# Register your models here.
@admin.register(TableRow)
class TableRowAdmin(admin.ModelAdmin):
    list_display = ("guid", "title", "body",)


@admin.register(TableHeader)
class TableRowAdmin(admin.ModelAdmin):
    list_display = ("content",)