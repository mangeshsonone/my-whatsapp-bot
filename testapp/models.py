from django.db import models

class PersonsData(models.Model):
    AGE_CHOICES = [(i, str(i)) for i in range(1, 121)]  # Age choices from 1 to 120
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    MARITAL_STATUS_CHOICES = [
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed'),
    ]
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    age = models.IntegerField(choices=AGE_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_CHOICES)
    qualification = models.CharField(max_length=100)
    job_profile = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100) 
    exact_nature_of_duties = models.TextField()
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    permanent_address = models.TextField()
    landline_no = models.CharField(max_length=15, blank=True, null=True)
    phone_no = models.CharField(max_length=15)
    alternative_no = models.CharField(max_length=15, blank=True, null=True)
    email_id = models.EmailField()
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    photo_upload = models.ImageField(upload_to='photos/')

    class Meta:
        abstract = True  

class Samaj(models.Model):
    samaj_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.samaj_name

class Family(models.Model):
    samaj = models.ForeignKey(Samaj, on_delete=models.CASCADE)
    surname = models.CharField(max_length=255)

    def __str__(self):
        return self.surname

class FamilyHead(PersonsData):
    name_of_head = models.CharField(max_length=255)
    family = models.ForeignKey(Family, on_delete=models.CASCADE)

    def __str__(self):
        return self.name_of_head

class Member(PersonsData):
    family_head = models.ForeignKey(FamilyHead, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name