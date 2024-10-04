import uuid
from django.db import models
from company.models import CustomUser

class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    emails = models.EmailField()
    names = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['emails', 'user'], name='unique_email_per_user')
        ]

    def __str__(self):
        return f"Client of {self.user.email}"
