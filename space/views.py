from typing import Any
from django.forms import BaseModelForm
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from .models import WorkspaceImage, Workspace
from .forms import Workspace_Form, SpaceImage

# Create your views here.


class Home(TemplateView):
    template_name = "space/index.html"


class AboutView(TemplateView):
    template_name = "space/about.html"


class ContactView(TemplateView):
    template_name = "space/contact.html"


class PriceView(TemplateView):
    template_name = "space/price.html"


class GallaryView(TemplateView):
    template_name = "space/gallary.html"


class SellerView(CreateView):
    model = Workspace
    form_class = Workspace_Form
    template_name = "space/seller.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.role == "seller":
            workspaces = Workspace.objects.filter(user=request.user)
            form = Workspace_Form()
            context = {"form": form, "workspaces": workspaces}
            return render(request, self.template_name, context=context)
        return redirect("/")

    def post(self, request, *args, **kwargs):
        form = Workspace_Form(request.POST or None)
        if form.is_valid():
            workspace = form.save(commit=False)
            workspace.user = request.user
            workspace.save()
        return redirect(request.path)


class RetriveWorkspace(DetailView):
    model = Workspace
    template_name = "space/workspace.html"
    form = SpaceImage()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = self.form
        images = WorkspaceImage.objects.filter(workspace_name=self.object)
        context["images"] = images
        return context


class SpaceImageView(CreateView):
    model = WorkspaceImage
    template_name = "space/index.html"
    form_class = SpaceImage

    def form_valid(self, form):
        self.pk = self.kwargs.get("pk")  # Retrieve pk from URL kwargs
        workspace_obj = Workspace.objects.get(pk=self.pk)
        form.instance.workspace_name = workspace_obj
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return self.request.META.get("HTTP_REFERER")
