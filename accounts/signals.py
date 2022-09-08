from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, UserProfile


@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    print(created)
    if created:
        UserProfile.objects.create(user=instance)
        # print("User profile Created")
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            # Create the userprofile if not exist
            UserProfile.objects.create(user=instance)
            # print("Didn't Exist. User profile Created")
        # print("user Updated")


@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    # print(instance.username , " user is being Created")
    pass
