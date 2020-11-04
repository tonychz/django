from django.urls import path
from . import views
from .views import hotzoneView, createRecordView, createRecordFinishedView, recordView, deleteRecordView

urlpatterns = [
    path('', hotzoneView, name='home'),
    path('hotzone', hotzoneView, name='home'),
    path('createRecord', createRecordView, name='createRecord'),
    path('createRecordFinished', createRecordFinishedView, name='createRecordFinished'),
    path('caselist', recordView.as_view(), name='caselist'),
    path('deleteRecord', deleteRecordView, name='deleteRecord')
    #path('results', resultsView, name='results')
]
