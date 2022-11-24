from django.urls import path

from .views import (
    CreateJournalView,
    GetPaperGradebookView,
    JournalDetailView,
    SymbolAnalyzerView,
    UploadBlankImageView
)

app_name = 'symbols_analyzer'

urlpatterns = [
    path(
        '',
        CreateJournalView.as_view(),
        name='create_journal'
    ),
    path(
        'journal/<int:pk>/',
        JournalDetailView.as_view(),
        name='journal'
    ),
    path(
        'journal/<int:pk>/get_paper_gradebook/',
        GetPaperGradebookView.as_view(),
        name='get_paper_gradebook'
    ),
    path(
        'uploadblank/',
        UploadBlankImageView.as_view(),
        name='uploadblank'
    ),
    path(
        'symbolanalyzer/',
        SymbolAnalyzerView.as_view(),
        name='symbolanalyzer'
    )
]
