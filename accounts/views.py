from typing import Any
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView
from space.models import User, Workspace, WorkspaceImage
from accounts.models import BuyerOrganization,SellerOrganization
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from accounts.forms import LoginForm
from space.forms import Workspace_Form
from accounts.forms import UserRegistration
import razorpay
from django.contrib.auth.views import LoginView



class SignUpView(CreateView):
    template_name="registration/signup.html"
    form_class=UserRegistration
    success_url = "login/"
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        pass1=form.cleaned_data["password"]
        pass2=form.cleaned_data["confirm_password"]
        if pass1!=pass2:
            return HttpResponse("Passowrd and confirm password should be match")
        form.instance.password=make_password(pass1)

        return super().form_valid(form)


def custom_logout(request):
    logout(request)
    return redirect("/")


class confrim_Registration(View):
    def get(self, request, *args, **kwargs):
        seller_email = kwargs.get("seller_email")
        image_pk = kwargs.get("image_pk")
        image_obj = get_object_or_404(WorkspaceImage, pk=image_pk)
        buyer_subject = "Co-Working Space Rental Agreement Confirmation"
        seller_subject = "Confirmation of Co-Working Space Rental Agreement"
        buyer_message = """Dear [Buyer/Seller],

                I'm pleased to confirm the successful execution of our Co-Working Space Rental Agreement. Your designated space at [address] will be available from [start date].

                Payment of [amount] per [day/week/month] is due on [payment schedule].

                If you have any questions, feel free to reach out.

                Best regards,
                [Your Name]
                [Co-Working Space Provider Name]"""
        seller_message = """
         Dear [Buyer/Seller],

        I'm writing to confirm that our Co-Working Space Rental Agreement has been finalized. Your designated space at [address] will be available for your use starting from [start date].

        Please note that payment of [amount] per [day/week/month] is due on [payment schedule].

        Should you have any questions or require further assistance, don't hesitate to reach out.

        Best regards,
        [Your Name]
        [Co-Working Space Provider Name]        
    """
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
    model = BuyerOrganization
    template_name = "registration/buyer.html"
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().order_by("-pk")


class SellerView(ListView):
    template_name = "registration/seller.html"

    def get_queryset(self) -> QuerySet[Any]:
        user = self.request.user
        workspaces = Workspace.objects.filter(user=user)
        workspace_images = WorkspaceImage.objects.filter(workspace_name__in=workspaces)
        applied_org = BuyerOrganization.objects.filter(space__in=workspace_images)
        return applied_org


class OrderView(View):
    def get(self, request, pk):
        order = BuyerOrganization.objects.filter(pk=pk).first()

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        data = {
            "amount": int(order.space.get_amount()) * 100,
            "currency": "INR",
            "receipt": "order_rcptid_11",
        }
        payment = client.order.create(data=data)
        print(payment)
        order.order_id = payment["id"]  
        order.save()
        context = {"payment": payment}

        return render(request, "registration/Order.html", context=context)


class PaymentVerificationView(View):
    def get(self, request):
        payment_id = request.GET.get("order_id")
        user = request.user
        obj = BuyerOrganization.objects.filter(user=user, order_id=payment_id).first()
        if obj:
            obj.status = "allocated"
            obj.is_paid = True
            obj.save()
        else:
            return HttpResponse("Payment Failed")
        return HttpResponse("Payment Success")


class CustomLoginView(LoginView):
    template_name="registration/login.html"
    form_class=LoginForm
    model=User

    def form_valid(self, form) :
        username=form.cleaned_data.get("username")
        password=form.cleaned_data.get("password")
        user=authenticate(username=username,password=password)
        if user is not None:
            login(self.request,user)
            if user.role=="buyer":
                
                return redirect("buyer")
            elif user.role=="seller":
              
                return redirect("seller")

            return super().form_valid(form)
        else:
            form.add_error(None,"Invalid username and password")
            return self.form_invalid(form)   
        
class SellerProfileView(TemplateView):
    model=SellerOrganization
    template_name="registration/seller_profile.html"
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        user=self.request.user
        seller_org=SellerOrganization.objects.filter(user=user).first()
        context["seller_org"]=seller_org
        return context