import helpers.billing
from django.db import models
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.conf import settings

User = settings.AUTH_USER_MODEL # "auth.User"

ALLOW_CUSTOM_GROUPS = True
SUBSCRIPTION_PERMISSIONS = [
            ("advanced", "Advance Perm"), # subscriptions.advance
            ("pro", "Pro Perm"), # subcriptions.pro
            ("basic", "Basic Perm"), # subscriptions.basic
            ("basic_ai", "Basic AI Perm") 
        ]

class Subscription(models.Model):
    """
    Subscription Plan = Stripe Product
    """    
    name = models.CharField(max_length=120)
    active = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group)
    permissions = models.ManyToManyField(Permission, limit_choices_to={"content_type__app_label": "subscriptions", "codename__in":[x[0] for x in SUBSCRIPTION_PERMISSIONS]}) # list comprehension technique
    stripe_id = models.CharField(max_length=120, null=True, blank=True)
    
    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        permissions = SUBSCRIPTION_PERMISSIONS
        
        
    def save(self, *args, **kwargs):
        if not self.stripe_id:
            stripe_id = helpers.billing.create_product(name=self.name, metadata={
                        "subscription_plan_id": self.id}, raw=False)
            self.stripe_id = stripe_id
            super().save(*args, **kwargs)
                     
        
        
class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)
    
def user_sub_post_save(sender, instance, *args, **kwargs):
    user_sub_instance = instance
    user = user_sub_instance.user
    subscription_obj = user_sub_instance.subscription
    groups_ids = []
    if subscription_obj is not None:
        groups = subscription_obj.groups.all()
        groups_ids = groups.values_list('id', flat=True)
    if not ALLOW_CUSTOM_GROUPS:
        user.groups.set(groups_ids)
    else:
        subs_qs = Subscription.objects.filter(active=True)
        if subscription_obj is not None:
            subs_qs = subs_qs.exclude(id=subscription_obj.id)
        subs_groups = subs_qs.values_list("groups__id", flat=True)
        subs_groups_set = set(subs_groups) 
        # groups_ids = groups.values_list('id', flat=True) # [1, 2, 3]
        current_groups = user.groups.all().values_list('id', flat=True)
        groups_ids_set = set(groups_ids)
        current_groups_set = set(current_groups) - subs_groups_set 
        final_group_ids = list(groups_ids_set | current_groups_set)
        user.groups.set(final_group_ids)
        
post_save.connect(user_sub_post_save, sender=UserSubscription)