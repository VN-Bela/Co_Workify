from django.contrib import admin
from space.models import User
from accounts.models import BuyerOrganization

# Register your models here.

admin.site.register(User)


@admin.register(BuyerOrganization)
class BuyerOrganizationAdmin(admin.ModelAdmin):
    list_display = ["pk", "user", "status", "order_id", "is_paid", "create_date"]
