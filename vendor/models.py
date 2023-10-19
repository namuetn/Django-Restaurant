from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification

class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approval = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.vendor_name

    def save(self, *args, **kwargs):
        if self.pk is not None:
            origin = Vendor.objects.get(pk=self.pk)
            if origin.is_approval != self.is_approval:
                email_template = 'accounts/emails/adminApprovalEmail.html'
                context = {
                    'user': self.user,
                    'is_approval': self.is_approval,
                }
                if self.is_approval == True:
                    mail_subject = 'Congratulations! Your restaurant has been approved'
                else:
                    mail_subject = "We're sorry! You are not eligible for publishing your food menu on our marketplace"

                send_notification(mail_subject, email_template, context)
        return super(Vendor, self).save(*args, **kwargs)
