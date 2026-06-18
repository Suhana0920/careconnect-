from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # Django admin panel
    path('admin/', admin.site.urls),

    # All app URLs
    path('', include('user_accounts.urls')),
]