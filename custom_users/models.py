from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    profile_name = models.CharField(max_length=250)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    contact_no = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)

    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.user.username



class Answers(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    vil = models.FloatField()
    aul = models.FloatField()
    kl = models.FloatField()
    vel = models.FloatField()
    anl = models.FloatField()
    sl = models.FloatField()
    sol = models.FloatField()
    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = "Answers"
    def __str__(self):
       return self.id
    
class Response(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    Q1 = models.CharField(max_length = 20)
    Q2 = models.CharField(max_length = 20)
    Q3 = models.CharField(max_length = 20)
    Q4 = models.CharField(max_length = 20)
    Q5 = models.CharField(max_length = 20)
    Q6 = models.CharField(max_length = 20)
    Q7 = models.CharField(max_length = 20)
    Q8 = models.CharField(max_length = 20)
    Q9 = models.CharField(max_length = 20)
    Q10 = models.CharField(max_length = 20)
    class Meta:
        verbose_name = 'Response'
        verbose_name_plural = "Responses"
    
    def __str__(self):
       return self.id 