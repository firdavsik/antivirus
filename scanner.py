import os
import sys
import django
import time
import clamd
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'antivirus.settings')
django.setup()

from holder.models import Queue


def scann_file(item: Queue):
    cd = clamd.ClamdUnixSocket(path='/tmp/clamd.socket')

    try:
        if item.file_url:
            content = requests.get(item.file_url)
            open("/home/scanning_file", 'wb').write(content.content)
            res = cd.scan("/home/scanning_file")
        else:
            res = cd.scan(item.file_data.path)
    except:
        item.has_error = True
        res = {}

    item.response = res
    item.is_scanned = True

    item.save()
    print(res)


while True:
    item = Queue.objects.filter(is_scanned=False).first()

    if item is None:
        print("Sleep for 2 secs")
        time.sleep(2)
    else:
        scann_file(item)
