from django.urls import path
from .views import (
    DashboardView,
    FlowerpotView,
    FlowerpotCreatorView
)

urlpatterns = [
    path("", DashboardView.as_view(), name="flowerpot.list"),
    path("home/", DashboardView.as_view(), name="home"),
    path('flowerpot/<int:pk>/', FlowerpotView.as_view(), name='flowerpot.detail'),
    path('flowerpot-creator', FlowerpotCreatorView.as_view(), name='flowerpot-creator')
]