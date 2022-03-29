from django.shortcuts import render
from .models import Richiesta, Componente, UfficioCompetente


# Create your views here.
def index(request):

    num_richieste = Richiesta.objects.all().count()
    num_componenti = Componente.objects.all().count()

    context = {
        'num_richieste': num_richieste,
        'num_componenti': num_componenti,
    }

    return render(request, 'index.html', context=context)
