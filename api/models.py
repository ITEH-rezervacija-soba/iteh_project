import django
from django.db import models


class WishModel(models.Model):
    user = models.ForeignKey(django.contrib.auth.get_user_model(), null=True, on_delete=models.CASCADE)
    wish_name = models.CharField(max_length=256)
    completed = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.wish_name

