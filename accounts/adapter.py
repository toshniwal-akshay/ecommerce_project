# from allauth.account.adapter import DefaultAccountAdapter
# from django.contrib.sites.shortcuts import get_current_site
# from .models import User

# class CustomAccountAdapter(DefaultAccountAdapter):

#     def send_confirmation_mail(self, request, emailconfirmation, signup):
#         current_site = get_current_site(request)
#         activate_url = self.get_email_confirmation_url(request, emailconfirmation)
#         ctx = {
#             "user":emailconfirmation.email_address.user,
#             "activate_url": activate_url,
#             "current_site": current_site,
#             "key": emailconfirmation.key,
#         }
#         if signup:
#             email_template = "account/email/email_confirmation_signup"
#         else:
#             email_template = "account/email/email_confirmation"
        
#         user = User.objects.get(email=emailconfirmation.email_address.user)
#         if user.is_staff == True:    
                
#             self.send_mail(email_template, "admin@admin.com", ctx)
#         else:
#             self.send_mail(email_template, emailconfirmation.email_address.email, ctx)
            