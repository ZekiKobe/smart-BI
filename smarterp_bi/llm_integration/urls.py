from django.urls import path
from . import views
from .api import api


urlpatterns = [
    path('generate-sql/',views.generate_sql,name="generate-sql"),
    path('api/', api.urls),
]