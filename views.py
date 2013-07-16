from django.views.generic.edit import CreateView, UpdateView, DeleteView
from models import Output
from forms import OutputForm

class OutputCreate(CreateView):
    context_object_name = 'output'
    queryset = Output.objects.all()
    form_class = OutputForm

