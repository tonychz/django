from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, ListView, FormView

from .models import Location, Case, Patient
from .forms import recordForm, geodataForm
import requests, json
from django.contrib import messages
from django.db import models

class recordView(ListView):
    model = Case
    template_name="caselist.html"
    list_name="caselist.html"

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
        if Case.objects.filter(caseNumber=delete).exists():
            delete_case = Case.objects.get(caseNumber=delete)
            delete_case.delete()
        else:
            error_alert = True
            pass
    return render(request, "deleteRecord.html",{'alert_flag': error_alert})




def createRecordView(request):
    if request.method == 'POST':
        form = recordForm(request.POST)
        if form.is_valid():
            #form.save()

            case_number = form.cleaned_data['case_number']
            name = form.cleaned_data['patient_name']
            virus = form.cleaned_data['infecting_virus']
            date = form.cleaned_data['date_of_confirm']
            local = form.cleaned_data['local_or_imported']

            idn = form.cleaned_data['identity_document_number']
            birth = form.cleaned_data['date_of_birth']


            loc = form.cleaned_data['location_visited']
            address = form.cleaned_data['address']
            x = form.cleaned_data['x_coordinate']
            y = form.cleaned_data['y_coordinate']
            starting = form.cleaned_data['starting_date_of_patient_present_on_the_location']
            ending = form.cleaned_data['ending_date_of_patient_present_on_the_location']

            p = Patient.objects.create(name=name, identityDocumentNumber= idn, dateOfBirth=birth)
            l = Location.objects.create(name = loc, address = address, x_coordinate = x, y_coordinate = y, startingDate=starting,endingDate=ending)
            c = Case.objects.create(caseNumber=case_number, patient=p, infectingVirus=virus, date=date, isLocal=local)
            c.location.add(l)
            c.save()
            #instance=form.save(commit=False)
            #instance.save()
            return HttpResponseRedirect("/createRecordFinished")
    
    elif request.method == 'GET':
        
        form = recordForm()
        location = request.GET.get('search_location')
        form = requests.post("http://127.0.0.1:8000/createRecord")
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

