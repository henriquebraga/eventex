from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from eventex.core.models import Speaker, Talk, CourseOld


def home(request):
    speakers = Speaker.objects.all()

    return render(request, 'index.html', context={'speakers': speakers })


def speaker_detail(request, slug):
    speaker = get_object_or_404(Speaker, slug=slug)
    return render(request, 'core/speaker_detail.html',{'speaker': speaker})

def talk_list(request):
    at_morning = list(Talk.objects.morning()) + list(CourseOld.objects.morning())
    at_morning.sort(key=lambda o : o.start)

    at_afternoon = list(Talk.objects.afternoon()) + list(CourseOld.objects.afternoon())
    at_afternoon.sort(key=lambda o : o.start)

    context = {
            'morning_talks': at_morning,
            'afternoon_talks': at_afternoon,
    }


    return render(request, 'core/talk_list.html', context)