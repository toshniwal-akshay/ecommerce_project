from django.db import models

from accounts.models import User,UserProfile
from accounts.utils import send_notification
# Create your models here.

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE , related_name='user')
    user_profile = models.OneToOneField(UserProfile, on_delete= models.CASCADE , related_name='userprofile')
    shop_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)
 
 
    def __str__(self):
        return str(self.shop_name)
    

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # Update
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_template = 'accounts/emails/admin_approval_email.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved,
                    'to_email': self.user.email,
                }
                if self.is_approved == True:
                    # Send notification email
                    mail_subject = "Congratulations! Your Shop has been approved."
                    send_notification(mail_subject, mail_template, context)
                else:
                    # Send notification email
                    mail_subject = "We're sorry! You are not eligible for publishing your products on our marketplace."
                    send_notification(mail_subject, mail_template, context)
        return super(Vendor, self).save(*args, **kwargs)
           