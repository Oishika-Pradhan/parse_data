from django.urls import path

from . import views

app_name = "myapp"

urlpatterns = [
    path('upload/', views.index, name='index'),
    path('compounds3/', views.compound, name='compound'),
    path('retention_roundoff/', views.retention, name='retention'),
    path('mean/', views.mean, name='mean'),
    path('downloadexcel/',views.downloadexcel ,name="downloadexcel"),
]
