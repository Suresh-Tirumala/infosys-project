from django.urls import path
from ..views.documents import upload_document, list_documents, document_detail, ask_about_document

urlpatterns = [
    path('upload/', upload_document, name='upload-document'),
    path('', list_documents, name='list-documents'),
    path('<int:doc_id>/', document_detail, name='document-detail'),
    path('<int:doc_id>/ask/', ask_about_document, name='ask-about-document'),
]
