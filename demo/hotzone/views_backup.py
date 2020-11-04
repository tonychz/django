from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, FormView

from .models import Location, Case, Patient
from .forms import recordForm, geodataForm
import requests, json


# Create your views here.
def hotzoneView(request):
    #return HttpResponse('code thate does somehng')
    return render(request, "hotzone.html")

def createRecordView2(request):
    return render(request, "createRecord.html") 
    
class findLocationView(TemplateView):
    template_name = 'createRecord.html'


def createRecordView(request):
    if request.method == 'POST':
        #if request.POST['action'] == 'Submit':
        if request.POST.get('action', 'Submit'):
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
                return HttpResponse("successfully added case record.")
    
        elif request.POST.get('action', 'Search'):
            #if request.method == 'GET':
            form = recordForm()
            #location = request.GET.get('search_location')
            #location = request.POST.get('search_location')
            location = request.POST.get('search_location')
            #form = requests.post("http://127.0.0.1:8000/createRecord")
            #return HttpResponse(data)
            
            if location!=None and location!='':
                PARAMS = {'q':location} 
                geodata_result = requests.get(url='https://geodata.gov.hk/gs/api/v1.0.0/locationSearch', params=PARAMS)
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
                'y_coor': geodata[0]['y']})
            else:
                return render(request, 'createRecord.html', {'form': form})
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

