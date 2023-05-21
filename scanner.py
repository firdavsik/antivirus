import os
import sys
import django
import time
import clamd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'antivirus.settings')
django.setup()

from holder.models import Queue


def scann_file(item:Queue):
    cd = clamd.ClamdUnixSocket(path='/tmp/clamd.socket')
    res = cd.scan(item.file_data.path)

    item.response = res
    item.is_scanned = True
    
    item.save()
    print(res)


while True:
    item = Queue.objects.filter(is_scanned=False).first()
    print(item)
    if item is None:
        print("Sleep for 2 secs")
        time.sleep(2)
    else:
        scann_file(item)
