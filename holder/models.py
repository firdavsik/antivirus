import time
import uuid

import pytz
from django.db import models
from django.utils import timezone


def generate_uniq_id():
    return f"{int(time.time())}-{str(uuid.uuid4())}"


class User(models.Model):
    uniq_uuid = models.CharField(max_length=100, default=generate_uniq_id)


# Create your models here.
class Queue(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    uniq_id = models.CharField(max_length=100, default=generate_uniq_id)
    file_url = models.CharField(max_length=2048, null=True, blank=True)
    file_data = models.FileField(upload_to='uploaded_files')
    file_name = models.CharField(max_length=1024, null=True)

    response = models.JSONField(null=True)
    is_scanned = models.BooleanField(default=False)
    has_error = models.BooleanField(default=False)

    def created_at_loc(self):

        return timezone.localtime(self.created_at, pytz.timezone('Asia/Tashkent')).strftime("%m/%d/%Y, %H:%M:%S")

    def is_infected(self):
        files = []
        is_infected = False
        for key, val in self.response.items():
            files.append(
                [
                    key[::-1][0:key[::-1].find('/')][::-1],
                    val[0],
                    val[1]
                ]
            )
            if val[0] == 'FOUND':
                is_infected = True

        return is_infected
