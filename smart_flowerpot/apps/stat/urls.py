from django.urls import path
from .views import (
    DashboardView,
    FlowerpotView,
    FlowerpotCreatorView,
    set_threshold,
)

urlpatterns = [
    path("", DashboardView.as_view(), name="flowerpot.list"),
    path("home/", DashboardView.as_view(), name="home"),
    path('flowerpot/<int:pk>/', FlowerpotView.as_view(), name='flowerpot.detail'),
    path('flowerpot-creator', FlowerpotCreatorView.as_view(), name='flowerpot-creator'),
    path('flowerpot/<int:id>/set-threshold/', set_threshold, name='set-threshold'),
]