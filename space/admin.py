from django.contrib import admin
from .models import Workspace, WorkspaceImage, SpaceCategory

# Register your models here.
admin.site.register(Workspace)
admin.site.register(WorkspaceImage)
admin.site.register(SpaceCategory)
