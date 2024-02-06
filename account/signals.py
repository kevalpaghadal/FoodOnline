from django.db.models.signals import post_save , pre_save
from django.dispatch import receiver
from .models import user , userprofile

# 2 way
@receiver(post_save , sender=user)
def post_save_create_profile_reciver(sender , instance, created , **kwargs):
    print(created)
    if created:
        # print('create th  e user profile')
        userprofile.objects.create(user=instance)
        print('user profile is created')
    else:
        try:
            profile = userprofile.objects.get(user=instance)
            profile.save()
        except:
            # create the userprofile if not exist
            userprofile.objects.create(user=instance)
            print('profile was not exits , but I created one')

        print('user is updated')

# 1 way
# post_save.connect(post_save_create_profile_reciver , sender=user)
        

@receiver(pre_save , sender=user)
def pre_save_profile_reciver(sender , instance , **kwargs):
    print(instance.username, 'this user is being saved')