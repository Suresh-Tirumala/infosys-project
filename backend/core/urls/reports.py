from django.urls import path
from ..views.reports import generate_report, list_reports, report_detail

urlpatterns = [
    path('generate/<int:conversation_id>/', generate_report, name='generate-report'),
    path('', list_reports, name='list-reports'),
    path('<int:report_id>/', report_detail, name='report-detail'),
]
