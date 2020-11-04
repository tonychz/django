from django import forms
from .models import Location
class recordForm(forms.Form):


    case_number = forms.IntegerField()
    patient_name = forms.CharField()
    infecting_virus = forms.CharField()
    date_of_confirm = forms.DateField()
    CHOICES=[(True,'Local'),(False,'Imported')]
    local_or_imported = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    
    identity_document_number = forms.IntegerField()
    date_of_birth = forms.DateField()


    location_visited = forms.CharField(max_length=200)
    address = forms.CharField(max_length=300)
    x_coordinate = forms.IntegerField()
    y_coordinate = forms.IntegerField()
    starting_date_of_patient_present_on_the_location = forms.DateTimeField()
    ending_date_of_patient_present_on_the_location = forms.DateField()

    def autofill(self, nameEN, addressEN, x_coor, y_coor):
        
        location_visited = nameEN
        address = addressEN
        x_coordinate = x_coor
        y_coordinate = y_coor
        obj = super(recordForm, self)

    def result(self):   #not used
        c = Case(caseNumber=case_number, 
        patient=patient_name, 
        infectingVirus=infecting_virus, 
        date=date_of_confirm, 
        isLocal=local_or_imported, 
        location=location_visited,
        )
        c.save()
        return

class geodataForm(forms.Form):
    #geodata location search box
    search_location = forms.CharField()
    def result(self):
        return search_location