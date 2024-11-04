from django.http import HttpResponse

def index(request):
  return HttpResponse("To jest strona ze statystykami")