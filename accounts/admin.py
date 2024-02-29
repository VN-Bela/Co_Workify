from django.contrib import admin
from space.models import User
from accounts.models import BuyerOrganization

# Register your models here.

admin.site.register(User)
admin.site.register(BuyerOrganization)