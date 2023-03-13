from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from csv_generator.views import schema_list, SchemaCreateView, schema_detail, schema_update

urlpatterns = [
    path('', schema_list, name='schema_list'),
    path('create/', SchemaCreateView.as_view(), name='schema_create'),
    path('update/<int:pk>/', schema_update, name='schema_update'),
    path('<int:pk>/', SchemaCreateView.as_view(), name='schema_detail'),
    path('generate/<int:pk>/', schema_detail, name='generate_dataset')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
