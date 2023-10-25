# urls.py
from django.urls import path
from apps.cves.views import ErrorTableView, error_table_api_view

urlpatterns = [
    path('', ErrorTableView.as_view(), name='error_table'),
    path('api/error-table/', error_table_api_view, name='error_table_api'),
]