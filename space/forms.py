from django import forms
from .models import Workspace, WorkspaceImage


class Workspace_Form(forms.ModelForm):
    class Meta:
        model = Workspace
        exclude = ["user"]
        widgets={
            'address':forms.Textarea(attrs={"rows":2,"cols":20})
        }


class SpaceImage(forms.ModelForm):
    class Meta:
        model = WorkspaceImage
        fields = ["images","category"]
