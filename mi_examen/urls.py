from django.contrib import admin
from django.urls import path
from turismo_app.views import tour_summary_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/tour-summary/', tour_summary_api),
]
