from django.urls import path
from .views import DashboardListView, DashboardDetailView, GenerateDashboardView

urlpatterns = [
    path('dashboards/', DashboardListView.as_view(), name='dashboard-list'),
    path('dashboards/<int:dashboard_id>/', DashboardDetailView.as_view(), name='dashboard-detail'),
    path('generate_dashboard/', GenerateDashboardView.as_view(), name='generate-dashboard'),
] 