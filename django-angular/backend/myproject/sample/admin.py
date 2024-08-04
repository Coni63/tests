from django.contrib import admin
from .models import A, B, C, AtoB, Status

from adminsortable2.admin import SortableAdminMixin
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase
from orderable.admin import OrderableAdmin, OrderableTabularInline

# class AtoBInline(SortableInlineAdminMixin, admin.TabularInline):
class AtoBInline(OrderableTabularInline):
    model = AtoB
    extra = 0

class AAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [AtoBInline]

# class BAdmin(admin.ModelAdmin):
#     pass

admin.site.register(A, AAdmin)
# admin.site.register(B, BAdmin)
admin.site.register(Status)