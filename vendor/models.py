from django.db import models
from account.models import User , userprofile

# Create your models here.

class vendor(models.Model):
    user = models.OneToOneField(User , related_name = 'user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(userprofile , related_name='userprofile' , on_delete=models.CASCADE)
    vandor_name = models.CharField(max_length=50)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.vandor_name