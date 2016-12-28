from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.list import ListView

from eventex.core.models import Speaker, Talk, CourseOld


#TemplateResponseMixin: Acumula a responsabilidade de renderizar uma página a partir de um contexto.
#MultipleObjectMixin: Pega uma coleção de objetos e coloca no contexto. (Deve vir antes do TemplateView)

#ListView: Trabalha como MultipleObjectMixin e Template View

home = ListView.as_view(template_name='index.html', model=Speaker)
speaker_detail = DetailView.as_view(model=Speaker)

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


#talk_list = ListView.as_view(model=Talk)