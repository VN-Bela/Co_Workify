from django.db import models
from space.models import User, WorkspaceImage,Workspace

# Create your models here.


STATUS_CHOICES = (
    ("in_progress", "InProgress"),
    ("approve", "Approve"),
    ("reject", "Reject"),
    ("allocated", "Allocated"),
)


class BuyerOrganization(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    space = models.ForeignKey(
        WorkspaceImage, on_delete=models.CASCADE, related_name="workspace_image"
    )
    status = models.CharField(
        choices=STATUS_CHOICES, max_length=50, default="in_progress"
    )
    order_id = models.CharField(max_length=100, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    create_date=models.DateTimeField(auto_now_add=True)

class SellerOrganization(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller_user")
    space = models.ForeignKey(  
        WorkspaceImage, on_delete=models.CASCADE, related_name="seller_workspace_image"
    )
    Workspace_detail = models.ForeignKey(  
        Workspace, on_delete=models.CASCADE, related_name="seller_workspace"
    )
    status = models.CharField(
        choices=STATUS_CHOICES, max_length=50, default="in_progress"
    )
    create_date=models.DateTimeField(auto_now_add=True)
