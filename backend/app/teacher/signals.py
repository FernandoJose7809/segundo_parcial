from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Teacher

@receiver(post_save, sender=Teacher)
def create_user_for_teacher(sender, instance, created, **kwargs):
    if created and instance.user is None:
        username = f"{instance.last_name[0].upper()}.{instance.ci}"
        base_username = username
        count = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{count}"
            count += 1

        user = User.objects.create_user(
            username=username,
            email=instance.email,
            password=f"{instance.last_name[0].upper()}.{instance.ci}"
        )
        instance.user = user
        instance.save()
