from django.contrib import admin

from .models import LiveEvent


class LiveEventAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(LiveEvent, LiveEventAdmin)
