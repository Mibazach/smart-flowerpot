from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from .models import Flowerpot, EnvironmentData
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardView(LoginRequiredMixin, ListView):
  ''' Main dashboard page displaying all connected flowerpots '''

  template_name = "dashboard.html"
  model = Flowerpot
  context_object_name = 'flowerpots'

class FlowerpotView(LoginRequiredMixin, DetailView):
  ''' Detail page displaying the environment data for a specific flowerpot '''

  template_name = "flowerpot.html"
  model = Flowerpot
  context_object_name = 'flowerpot'


  def get_queryset(self):
    return super().get_queryset().prefetch_related('environment_data')

class FlowerpotCreatorView(LoginRequiredMixin, CreateView):
  ''' Form page for creating a new flowerpot '''

  template_name = "flowerpot_creator.html"
  model = Flowerpot
  fields = ['name', 'description', 'location']

  success_url = reverse_lazy('home')

  def form_valid(self, form):
      return super().form_valid(form)