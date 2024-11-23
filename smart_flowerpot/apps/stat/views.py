from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView
from .models import Flowerpot, EnvironmentData
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardView(ListView):
  ''' Main dashboard page displaying all connected flowerpots '''

  template_name = "dashboard.html"
  model = Flowerpot
  context_object_name = 'flowerpots'

class FlowerpotView(DetailView):
  ''' Detail page displaying the environment data for a specific flowerpot '''

  template_name = "flowerpot.html"
  model = Flowerpot
  context_object_name = 'flowerpot'


  def get_queryset(self):
    return super().get_queryset().prefetch_related('environment_data')



