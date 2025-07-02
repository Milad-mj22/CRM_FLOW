from django.contrib import admin

# Register your models here.
# Register your models here.

from .models import CoopStateHistory, coops , CarModel





class CoopStateHistoryInline(admin.TabularInline):
    model = CoopStateHistory
    extra = 0
    readonly_fields = ['previous_state', 'new_state', 'changed_by', 'changed_at']

class CoopAdmin(admin.ModelAdmin):
    inlines = [CoopStateHistoryInline]

admin.site.register(coops, CoopAdmin)
admin.site.register(CoopStateHistory)
admin.site.register(CarModel)