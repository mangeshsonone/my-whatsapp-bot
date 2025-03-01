from django.db import models

class Samaj(models.Model):
    samaj_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.samaj_name


class Family(models.Model):
    samaj = models.ForeignKey(Samaj, on_delete=models.CASCADE)
    surname = models.CharField(max_length=255)

    def __str__(self):
        return self.surname


class Member(models.Model):
    GENDER_CHOICES = [("M", "Male"), ("F", "Female"), ("O", "Other")]
    
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.IntegerField()
    blood_group = models.CharField(max_length=5)
    mobile1 = models.CharField(max_length=15)
    mobile2 = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.name
