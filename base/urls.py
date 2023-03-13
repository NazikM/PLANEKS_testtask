from django.contrib import admin
from django.urls import path, include

from base.views import signin, signout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', signin, name='login'),
    path('signout/', signout, name='signout'),
    path('', include('csv_generator.urls'))
]
