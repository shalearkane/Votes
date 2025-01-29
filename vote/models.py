from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class UserVote(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="vote_profile"
    )
    voted_option = models.CharField(
        max_length=1,
        blank=True,
        null=True,
        choices=[
            ("A", "Option A"),
            ("B", "Option B"),
            ("C", "Option C"),
            ("D", "Option D"),
        ],
    )

    def __str__(self):
        return f"Vote profile for {self.user.username}"
