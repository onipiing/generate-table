# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import TableRow

# Register your models here.
@admin.register(TableRow)
class TableRowAdmin(admin.ModelAdmin):

    list_display = ("guid",
                    "title",
                    "body",)