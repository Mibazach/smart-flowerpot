from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import Flowerpot, EnvironmentData
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.core.management import call_command
import json

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
  fields = ['slug', 'name', 'description', 'location']

  success_url = reverse_lazy('home')

  def form_valid(self, form):
      return super().form_valid(form)
  
def delete_flowerpot(request, id):
    if request.method == "POST":
        flowerpot = get_object_or_404(Flowerpot, id=id)
        flowerpot.delete()
        return redirect('home')

@csrf_exempt
@require_http_methods(["PATCH"])
def set_threshold(request, id):
    try:
        flowerpot = get_object_or_404(Flowerpot, id=id)

        print(f"Flowerpot fetched: {flowerpot}")
        print(f"Flowerpot fetched: {flowerpot.id}")

        data = json.loads(request.body)

        print(f"Received data: {data}")

        threshold = data.get("threshold")
        
        print(f"Threshold received: {threshold}")

        if threshold is None or not isinstance(threshold, int) or not (0 <= threshold <= 100):
            return JsonResponse({"error": "Threshold must be an integer between 0 and 100"}, status=400)

        flowerpot.threshold = threshold
        flowerpot.save()
        print(f"Flowerpot threshold updated: {flowerpot.threshold}")

        moisture_thresh = -27 * threshold + 4095
        flowerpot_esp = f"flowerpot-{flowerpot.id}"

        call_command('publish_mqtt', flowerpot_esp, moisture_thresh)

        print("MQTT Publisher command executed successfully.")

        return JsonResponse({"message": "Threshold updated successfully", "threshold": flowerpot.threshold}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        print(e)
        return JsonResponse({"error": str(e)}, status=500)