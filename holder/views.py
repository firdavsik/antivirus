from django.shortcuts import render
from django.views import View

# Create your views here.
from holder.models import Queue


class IndexPage(View):
    def get(self, request):
        return render(request, 'holder/index.html')

    def post(self, request):
        print(request.FILES)
        file_data = request.FILES['file_data']
        print(file_data)
        new_queue = Queue(file_data=file_data)
        new_queue.save()
        return render(request, 'holder/index.html')
