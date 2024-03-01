from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect,get_object_or_404
from django.views import View
from django.views.generic import TemplateView,CreateView,ListView
from space.models import User,Workspace,WorkspaceImage
from accounts.models import BuyerOrganization
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from space.forms import Workspace_Form


# Create your views here.
class loginView(View):
    template_name = "accounts/login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST["email"]
        password = request.POST["password"]
        user = User.objects.filter(email=email)
        if not user.exists():
            return HttpResponse("Account not found!!")

        user_obj = authenticate(email=email, password=password)
        if user_obj:
            login(request, user_obj)
            if user_obj.role == "seller":
                return redirect("seller")
            elif user_obj.role == "buyer":
                return redirect("price")
            else:
                return redirect("/")
        return HttpResponse("Invalid Credentials")


class SignUpView(View):
    def get(self, request):
        return render(request, "accounts/signup.html")

    def post(self, request):
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        role = request.POST["role"]
        if password == confirm_password:
            User.objects.create(
                email=email, password=make_password(password), role=role
            )
        else:
            return HttpResponse("Password does not match.")
        return redirect("login")


def custom_logout(request):
    logout(request)
    return redirect("/")


class confrim_Registration(View):
     def get(self, request, *args, **kwargs):
        seller_email = kwargs.get('seller_email')
        image_pk = kwargs.get('image_pk')
        image_obj= get_object_or_404(WorkspaceImage, pk=image_pk)
        buyer_subject = "Co-Working Space Rental Agreement Confirmation"
        seller_subject = "Confirmation of Co-Working Space Rental Agreement"
        buyer_message = """Dear [Buyer/Seller],

                I'm pleased to confirm the successful execution of our Co-Working Space Rental Agreement. Your designated space at [address] will be available from [start date].

                Payment of [amount] per [day/week/month] is due on [payment schedule].

                If you have any questions, feel free to reach out.

                Best regards,
                [Your Name]
                [Co-Working Space Provider Name]"""
        seller_message='''
         Dear [Buyer/Seller],

        I'm writing to confirm that our Co-Working Space Rental Agreement has been finalized. Your designated space at [address] will be available for your use starting from [start date].

        Please note that payment of [amount] per [day/week/month] is due on [payment schedule].

        Should you have any questions or require further assistance, don't hesitate to reach out.

        Best regards,
        [Your Name]
        [Co-Working Space Provider Name]        
    '''
        send_mail(
            subject=buyer_subject,
            message=buyer_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[request.user.email],
        )
        send_mail(
            subject=seller_subject,
            message=seller_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[seller_email],
        )
        BuyerOrganization.objects.create(user=request.user, space=image_obj)


        return redirect("/")

class AddWorkspaceView(CreateView):
    model = Workspace
    form_class = Workspace_Form
    template_name = "space/seller1.html"

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

class BuyerView(ListView):
    model=BuyerOrganization
    template_name="accounts/buyer.html"
    
    
class SellerView(ListView):
    template_name="accounts/seller.html"

    def get_queryset(self) -> QuerySet[Any]:
        user = self.request.user
        workspaces = Workspace.objects.filter(user=user)
        workspace_images = WorkspaceImage.objects.filter(workspace_name__in=workspaces)
        applied_org = BuyerOrganization.objects.filter(space__in=workspace_images)
        return applied_org