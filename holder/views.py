from django.shortcuts import render, redirect
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
        print(file_data.name)
        new_queue = Queue(file_data=file_data, file_name=file_data.name)
        new_queue.save()
        return redirect('result', result_id=new_queue.uniq_id)


class ResultPage(View):
    def get(self, request, result_id):
        queue = Queue.objects.filter(uniq_id=result_id).first()
        context = {'queue': queue}

        if queue.is_scanned:
            files = []
            is_infected = False
            for key, val in queue.response.items():
                files.append(
                    [
                        key[::-1][0:key[::-1].find('/')][::-1],
                        val[0],
                        val[1]
                    ]
                )
                if val[0] == 'FOUND':
                    is_infected = True

            context['files'] = files
            context['is_infected'] = is_infected

        return render(request, 'holder/result.html', context=context)
