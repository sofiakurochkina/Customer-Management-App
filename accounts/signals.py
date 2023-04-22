from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.dispatch import receiver
from .models import Customer
import os

# For signals to work override 'ready' method in apps.py  OR  in __init__.py add: default_app_config = 'accounts.apps.AccountsConfig')

# Create (Customer) profile for newly created user .
@receiver(post_save,sender=User)

def customer_profile(sender, instance, created, **kwargs):
    # send when user is created (created == False - works only on update)
	if created:
			# Add 'admin' group to superuser created via shell or fixtures(called to populate db). Groups must be created in admin panel,shell or  fixtures
		if instance.is_staff:
			group = Group.objects.get(name='admin')
			instance.groups.add(group)
		else:
			# Add 'customer' group to each user that doesn't have 'staff' status (look django user in admin panel) and isn't assigned to 'admin' group.
			group = Group.objects.get(name='customer')
			instance.groups.add(group)
			# Link current created user(instance) with this new Customer object (only users assigned to 'customer' group)
			Customer.objects.create(
				user=instance,
				name=instance.username,
				email=instance.email,
				)


