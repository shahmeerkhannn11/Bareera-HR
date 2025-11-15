from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Employee, EmployeeProfile


# Helper: generate username from name
def generate_username(name):
    name = name.lower().replace(" ", ".")
    base_username = name
    counter = 1

    # Ensure unique username
    while User.objects.filter(username=name).exists():
        name = f"{base_username}{counter}"
        counter += 1

    return name


@receiver(post_save, sender=Employee)
def create_user_and_profile(sender, instance, created, **kwargs):
    if created:
        # 👉 Generate username
        username = generate_username(instance.name)

        # 👉 Create a basic temporary password
        temp_password = "employee123"

        # 👉 Create User
        user = User.objects.create_user(
            username=username,
            email=instance.email,
            password=temp_password
        )

        # 👉 Link User to Employee (via EmployeeProfile)
        EmployeeProfile.objects.create(
            user=user,
            employee=instance
        )

        print(f"Created user '{username}' for employee {instance.name}")
