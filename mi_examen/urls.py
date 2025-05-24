from django.contrib import admin
from django.urls import path, include
from turismo_app.views import AdvancedTourSummaryAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/tour-summary/', AdvancedTourSummaryAPIView.as_view(), name='tour-summary-api'),
    # path('api/', include('turismo_app.urls')), # Si tuvieras más APIs en turismo_app
]