from django.db import models

# Create your models here.
class Patient(models.Model):
    name = models.CharField(max_length=200)
    identityDocumentNumber = models.PositiveIntegerField()
    dateOfBirth = models.DateTimeField()
    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    x_coordinate = models.BigIntegerField()
    y_coordinate = models.BigIntegerField()
    startingDate = models.DateField()
    endingDate = models.DateField()
    def __str__(self):
        return self.name

class Case(models.Model):
    caseNumber = models.PositiveIntegerField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    infectingVirus = models.CharField(max_length=200)
    date = models.DateField()
    isLocal = models.BooleanField()
    location = models.ManyToManyField(Location)
    def __str__(self):
        return str(self.caseNumber)+'  '+self.patient.name




