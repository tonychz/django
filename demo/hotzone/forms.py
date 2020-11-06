from django import forms
from .models import Location
class recordForm(forms.Form):

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


class geodataForm(forms.Form):
    #geodata location search box
    search_location = forms.CharField()
    def result(self):
        return search_location