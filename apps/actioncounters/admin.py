from django.contrib import admin

from .models import Action, ActionCounter, ActionHit

class ActionAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'max_per_unique', )
admin.site.register(Action, ActionAdmin)

class ActionCounterAdmin(admin.ModelAdmin):
    list_display = ( 'action', 'content_object', 'total', )
admin.site.register(ActionCounter, ActionCounterAdmin)

class ActionHitAdmin(admin.ModelAdmin):
    list_display = ( 'counter', 'total', 'user', 'ip', )
admin.site.register(ActionHit, ActionHitAdmin)
