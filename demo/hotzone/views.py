from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, ListView, FormView

from .models import Location, Case, Patient
from .forms import recordForm, geodataForm
import requests, json
from django.contrib import messages
from django.db import models

class recordView(ListView):
    model = Location
    template_name="locationList.html"
    list_name="locationList.html"

    def get_context_data (self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['case'] = Case.objects.filter(case__pk = caseNumber)
        #context['patient'] = Patient.objects.get(pk = name)
        return context

# Create your views here.
def hotzoneView(request):
    #return HttpResponse('code thate does somehng')
    return render(request, "hotzone.html")

def createRecordFinishedView(request):
    #return HttpResponse('code thate does somehng')
    return render(request, "createRecordFinished.html")
    
class findLocationView(TemplateView):
    template_name = 'createRecord.html'

def deleteRecordView(request):
    error_alert = False
    if request.method=='POST':
        delete = request.POST.get('delete')
        if Location.objects.filter(name=delete).exists():
            delete_location = Location.objects.get(name=delete)
            delete_location.delete()
        else:
            error_alert = True
            pass
    return render(request, "deleteRecord.html",{'alert_flag': error_alert})




def createRecordView(request):
    if request.method == 'POST':
        form = recordForm(request.POST)
        if form.is_valid():
            #form.save()

            loc = form.cleaned_data['location_visited']
            address = form.cleaned_data['address']
            x = form.cleaned_data['x_coordinate']
            y = form.cleaned_data['y_coordinate']
            starting = form.cleaned_data['starting_date_of_patient_present_on_the_location']
            ending = form.cleaned_data['ending_date_of_patient_present_on_the_location']

            l = Location.objects.create(name = loc, address = address, x_coordinate = x, y_coordinate = y, startingDate=starting,endingDate=ending)
            l.save()
            #instance=form.save(commit=False)
            #instance.save()
            return HttpResponseRedirect("/createRecordFinished")
    
    elif request.method == 'GET':
        
        form = recordForm()
        location = request.GET.get('search_location')
        #form = requests.post("/createRecord")
        #return HttpResponse(data)
        error_alert = False
        if location!=None and location!='':
            PARAMS = {'q':location} 
            geodata_result = requests.get(url='https://geodata.gov.hk/gs/api/v1.0.0/locationSearch', params=PARAMS)
            if(geodata_result.status_code != 200 or location==''):
                error_alert=True
            
            geodata = geodata_result.json()

            form = recordForm({'location_visited': geodata[0]['nameEN'],
            'address': geodata[0]['addressEN'],
            'x_coordinate': geodata[0]['x'],
            'y_coordinate': geodata[0]['y']})

            #form.autofill(geodata[0]['addressEN'],geodata[0]['nameEN'],geodata[0]['x'],geodata[0]['y'])
            return render(request, 'createRecord.html', 
            {'form': form, 
            'addressEN': geodata[0]['addressEN'],
            'nameEN': geodata[0]['nameEN'],
            'x_coor': geodata[0]['x'],
            'y_coor': geodata[0]['y'],
            'alert_flag': error_alert})
        else:
            return render(request, 'createRecord.html', {'form': form, 'alert_flag': error_alert} )
    else:
        form = recordForm()
        form2 = geodataForm()

    return render(request, 'createRecord.html', {'form': form})




def get_queryset(self):
    response = requests.get('https://geodata.gov.hk/gs/api/v1.0.0/locationSearch' % q)
    
    geodata = response.json()
    return render(request, '/hotzone/createRecord.html', {
    'addressZH': geodata['addressZH'],
    'nameZH': geodata['nameZH'],
    'x': geodata['x':],
    'y': geodata['y'],
    'nameEN': geodata['nameEN'],
    'addressEN' : geodata['addressEN']}
    )

    form = recordForm({'location_visited': geodata[0]['addressEN'],
    'address': geodata[0]['nameEN'],
    'x_coordinate': geodata[0]['x'],
    'y_coordinate': geodata[0]['y']})

