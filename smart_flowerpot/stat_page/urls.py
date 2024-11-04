from django.urls import path
from .views import (
    DashboardView,
    FlowerpotView,
)

urlpatterns = [
    path("", DashboardView.as_view(), name="flowerpot.list"),
    path('flowerpot/<int:pk>/', FlowerpotView.as_view(), name='flowerpot.detail'),
]