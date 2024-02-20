from django import forms
from .models import Workspace, WorkspaceImage


class Workspace_Form(forms.ModelForm):
    class Meta:
        model = Workspace
        exclude = ["user"]


class SpaceImage(forms.ModelForm):
    class Meta:
        model = WorkspaceImage
        fields = ["images","category"]
