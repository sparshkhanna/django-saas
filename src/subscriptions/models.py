from django.db import models

# Create your models here.

class Subscription(models.Model):
    name = models.CharField(max_length=120)

    class Meta:
        permissions = [
            ("advanced", "Advance Perm"), # subscriptions.advance
            ("pro", "Pro Perm"), # subcriptions.pro
            ("basic", "Basic Perm"), # subscriptions.basic
            ("basic_ai", "Basic AI Perm") 
        ]