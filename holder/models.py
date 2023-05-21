import time
import uuid

from django.db import models


def generate_uniq_id():
    return f"{int(time.time())}-{str(uuid.uuid4())}"


# Create your models here.
class Queue(models.Model):
    uniq_id = models.CharField(max_length=100, default=generate_uniq_id)
    file_url = models.CharField(max_length=2048, null=True, blank=True)
    file_data = models.FileField(upload_to='uploaded_files')
    file_name = models.CharField(max_length=1024, null=True)

    response = models.JSONField(null=True)
    is_scanned = models.BooleanField(default=False)
    has_error = models.BooleanField(default=False)
