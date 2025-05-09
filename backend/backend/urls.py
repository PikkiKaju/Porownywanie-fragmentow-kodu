"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from app.views import TextView, FileListView, FileSingleView, FilePredictView
from backend import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('wel/', TextView.as_view(), name="upload-text"),
    path('wel/<int:pk>/', TextView.as_view(), name="delete-text"),
    path('file/', FileListView.as_view(), name="file"),
    path('file/<int:pk>/', FileSingleView.as_view(), name="file-by-id"),
    path('predict/<int:results_size>/', FilePredictView.as_view(), name="predict-file"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)