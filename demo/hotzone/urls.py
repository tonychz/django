from django.urls import path
from . import views
from .views import hotzoneView, createRecordView, createRecordFinishedView, recordView, deleteRecordView, deleteRecordFinishedView

urlpatterns = [
    path('', hotzoneView, name='home'),
    path('hotzone', hotzoneView, name='home'),
    path('createRecord', createRecordView, name='createRecord'),
    path('createRecordFinished', createRecordFinishedView, name='createRecordFinished'),
    path('locationList', recordView.as_view(), name='locationList'),
    path('deleteRecord', deleteRecordView, name='deleteRecord'),
    path('deleteRecordFinished', deleteRecordFinishedView, name='deleteRecordFinished')
    #path('results', resultsView, name='results')
]
