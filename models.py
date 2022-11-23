from distutils.command.upload import upload
import email
from email.policy import default
from django.db import models
from django.core.validators import RegexValidator
import datetime
from django.core.validators import MinValueValidator


# Create your models here.




class new_donor(models.Model):
    donorname = models.CharField(max_length=200)
    donoremail = models.CharField(max_length=200, unique=True)
    donorphone = models.CharField(max_length=200)
    donorplace = models.CharField(max_length=200)
    donoraadhar=models.CharField(max_length=200,null=True)
    password = models.CharField(max_length=100,default=1)

    class Meta:
        verbose_name_plural = "Donor Details"



class all_logins(models.Model):
    email = models.CharField(max_length=200, unique=True, primary_key=True)
    password = models.CharField(max_length=100)
    otp = models.IntegerField(default=1)
    status=models.BooleanField(default=False)


class volunteers_login(models.Model):
    user = models.EmailField(max_length=200, unique=True, primary_key=True,default=1)
    password = models.CharField(max_length=100)
    type=models.BooleanField(max_length=100,default=False)

class District(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name




class Orphanage(models.Model):
    name = models.CharField(max_length=124)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.CharField(max_length=250)
    pin= models.CharField(max_length=12, blank=True)
    image = models.ImageField(upload_to='pics')
    phone = models.CharField(max_length=12, blank=True)
    email=models.EmailField()
    no_of_persons=models.IntegerField()
    

class donationtype(models.Model):
    name = models.CharField(max_length=200,unique=True)
    description = models.TextField(max_length=200,blank=True)
    def __str__(self):
        return self.name


class Address(models.Model):
    user=models.ForeignKey(all_logins,on_delete=models.CASCADE)
    fname = models.CharField(max_length=200)
    lname=models.CharField(max_length=200,null=True)
    email = models.EmailField(max_length=200,default=True)
    phone = models.CharField(max_length=200,null=True)
    hname = models.CharField(max_length=200)
    city=models.CharField(max_length=200)
    district=models.ForeignKey(District,on_delete=models.CASCADE,default=1) 
    pin = models.IntegerField()

class userdonate(models.Model):
    user=models.ForeignKey(all_logins,on_delete=models.CASCADE)    
    item=models.CharField(max_length=400,null=True)
    orphanage=models.ForeignKey(Orphanage,on_delete=models.CASCADE,null=True)   
    address=models.ForeignKey(Address,on_delete=models.CASCADE,null=True)   
    otherdonations=models.CharField(max_length=200,null=True)
    date=models.DateField(validators=[MinValueValidator(datetime.date.today)],null=True)
    status=models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = "Donations Details"

class Payment(models.Model):
    amount=models.DecimalField(max_digits=20,decimal_places=2) 
    user=models.ForeignKey(all_logins,on_delete=models.CASCADE)    
    orphanage=models.ForeignKey(Orphanage,on_delete=models.CASCADE,null=True)   
    Donation_date=models.DateTimeField(auto_now_add=True,null=True)



# class Donorprofile(models.Model):
#     user=models.ForeignKey(all_logins,on_delete=models.CASCADE)
#     fname = models.CharField(max_length=200)
#     email = models.EmailField(max_length=200,default=True)
#     phone = models.CharField(max_length=200,null=True)
#     hname = models.CharField(max_length=200)
#     city=models.CharField(max_length=200)
#     district=models.ForeignKey(District,on_delete=models.CASCADE,default=1) 
#     pin = models.IntegerField()


    

class volunteer(models.Model):
    fname = models.CharField(max_length=200)
    lname = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    hname = models.CharField(max_length=200)
    email = models.CharField(max_length=200,null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, blank=True, null=True)
    city=models.CharField(max_length=200)
    pin=models.CharField(max_length=200)
    aadhar=models.CharField(max_length=200)
    password = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "Volunteers Details"

class volunteer_reg(models.Model):
    fname = models.CharField(max_length=200)
    lname = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    hname = models.CharField(max_length=200)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(volunteers_login, on_delete=models.SET_NULL, blank=True, null=True)
    city=models.CharField(max_length=200)
    pin=models.CharField(max_length=200)
    aadhar=models.CharField(max_length=200)
    password = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "Volunteers Details"

class tbl_amounts(models.Model):
    amounts=models.DecimalField(max_digits=20,decimal_places=2) 