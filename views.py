from decimal import Decimal

from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import *
from hashlib import sha256
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# for email otp verification
import math, random
from django.core.mail import send_mail

# Create your views here.
def orphanagehome(request):
    # request.session.flush()
    return render(request, 'orphanage_index.html')
    
def index(request):
    request.session.flush()
    return render(request, 'index.html')

# Donor Login Function
def login(request):
    request.session.flush()
    if 'email' in request.session:
        return redirect(donorhome)

    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        print(email,password)
        password2=sha256(password.encode()).hexdigest()
        print(password2)
        donor=all_logins.objects.filter(email=email,password=password2,status=1)
        if donor:
            donor_details=all_logins.objects.get(email=email,password=password2)
            email=donor_details.email
            request.session['email']=email
            return redirect('donorhome')
        else:
            print("invalid")
            messages.success(request,"Invalid login Credentials")
            return redirect(login)
    return render(request, 'login.html')

# Function for OTP Generation
def generateOTP() :
     digits = "0123456789"
     OTP = ""
     for i in range(4) :
         OTP += digits[math.floor(random.random() * 10)]
         a=OTP
     print("swdfghjk",a)
     return OTP

# Donor Registration
def reg(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        place=request.POST.get('place')
        aadhar=request.POST.get('aadhar') 
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        passwords=sha256(pass2.encode()).hexdigest()
        if all_logins.objects.filter(email=email,status=True).exists():
            messages.success(request,'Email already Exist....!')
            return redirect('login')
        elif all_logins.objects.filter(email=email,status=False).exists():
            user=all_logins.objects.get(email=email) 
            o=generateOTP()
            htmlgen = '<p>Your OTP is:'+o+'</p>'
            send_mail('OTP request',o,'orphanage management',[email], fail_silently=False, html_message=htmlgen)
            user.otp=o;
            user.save()
            messages.success(request, 'Email already exist..Please Verify Email!!!!')
            request.session['email']=email 
            return redirect('verify_otp') 
        else:
            o=generateOTP()
            htmlgen = '<p>Your OTP is:'+o+'</p>'
            send_mail('OTP request',o,'orphanage management',[email], fail_silently=False, html_message=htmlgen)
            all_logins(email=email,password=passwords,otp=o).save()
            new_donor(donorname=name,donoremail=email,donorphone=phone,donorplace=place,donoraadhar=aadhar).save()
            # messages.success(request,"registered successfully")
            request.session['email']=email 
            return redirect(verify_otp)
    return render(request, 'reg.html')


# Otp Verification
def verify_otp(request):
    if 'email' in request.session:
        if request.method=='POST':
            otps = request.POST.get('otp');
            email = request.POST.get('email');
            session=request.session['email']
            if all_logins.objects.filter(email=email,otp=otps): 
                user=all_logins.objects.get(email=email)
                user.status=True;
                user.save()
                messages.success(request, 'Email is verified')
                return redirect('login')
            else:
                messages.success(request, 'Invalid Otp!!')
                return redirect('verify_otp')
        session=request.session['email']
        return render(request, 'otp.html',{'session':session})
    else:
        return redirect(login)


def donorhome(request):
    if 'email' in request.session:
        # id=request.session['id']
        email=request.session['email']
        return render(request, 'donorhome.html',{'id':id,'email':email})
    return redirect(login)

def logout(request):
    if 'email' in request.session:
        request.session.flush()
    return redirect(login)

def selectdistrict(request):
    district= District.objects.all()
    email=request.session['email']
    d = {'district': district,'name':email}
    return render(request,'selectdistrict.html',d)

def load_orphanages(request):
    district_id = request.GET.get('district')
    orphanages = Orphanage.objects.filter(district_id=district_id).order_by('name')
    return render(request, 'orphanage_dropdown_list_options.html', {'orphanages': orphanages})

def vieworphanage(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        district=request.POST.get('district')
        result=Orphanage.objects.filter(id=name,district_id=district)
        print(name,district)
        if result:
            result_details=Orphanage.objects.get(id=name,district_id=district)
            print(result)
            print("orphanage")
            name=result_details.name
            id=result_details.id
            request.session['id']=id
            vieworphanage=Orphanage.objects.all()
            district=District.objects.all()
            email=request.session['email']
            return render(request,'vieworphanage.html',{'name':name,'id':id,'district':district,'vieworphanage':vieworphanage,'email':email})      
        else:
            return redirect(selectdistrict)


    

def donatehome(request):
    if request.method == 'POST':
        opid=request.POST.get('opid')
        item=request.POST.get('item') 
        other=request.POST.get('other') 
        date=request.POST.get('date')
        address=request.POST.get('radio')
        print(address)
        print(date)
        print("**************************")
        if 'email' in request.session:
            user=request.session['email']
            donation=userdonate(user_id=user,item=item,otherdonations=other,date=date,orphanage_id=opid,address_id=address)
            donation.save()
            messages.success(request,"Donated successfully")
            return redirect(viewdonations)
    # district=District.objects.all()
    # items=donationtype.objects.all()
    # messages.success(request,"registered successfully")
    # return render(request, 'donatehome.html',{'district':district,'items':items})


def donate(request,id):
    district=District.objects.all()
    items=donationtype.objects.all()
    orphanage=Orphanage.objects.filter(id=id)
    email=request.session['email']
    address=Address.objects.filter(user_id=email)
    id=Address.objects.all()
    # info=Donorprofiles.objects.filter(user_id=email)
    return render(request, 'donatehome.html',{'district':district,'items':items,'name':email,'orphanage':orphanage,'address':address,'id':id})

#Doner Profile
def profile(request):
    if 'email' in request.session:
        district=District.objects.all()
        email = request.session['email']
        profile=new_donor.objects.all()
        address=Address.objects.filter(user_id=email)
        id=Address.objects.all()
        return render(request,"profile.html",{'email':email,'profile':profile,'district':district,'address':address,'id':id})
    messages.success(request, 'Sign in..!!')
    return redirect(login)




def change_password(request):
    if 'email' in request.session:
        email=request.session['email']
        user=all_logins.objects.get(email=email)
        if request.method =="POST":
            old_password=request.POST.get('oldpass')
            new_password=request.POST.get('pass');
            new_pswd=sha256(new_password.encode()).hexdigest()
            pswd=sha256(old_password.encode()).hexdigest()
          
            if pswd == user.password:
                user.password=new_pswd
                user.save()
                print("Password updated Successfully")
                messages.success(request, 'Password updated Successfully...')
                return redirect('profile')
            else:
                messages.success(request, 'Incorrect Password ...')
                print("Incorrect Password")
                return redirect('profile')
        return redirect('login')


def volunteerhome(request):
    if 'email' in request.session:
        email=request.session['email']
        return render(request, 'volunteerhome.html',{'name':email})
    return redirect(volunteer_login)

def volunteerreg(request):
    if request.method == 'POST':
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        hname=request.POST.get('hname')
        dist=request.POST.get('district')
        city=request.POST.get('city')
        pin=request.POST.get('pin')
        aadhar=request.POST.get('aadhar') 
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        passwords=sha256(pass2.encode()).hexdigest()
       

        if volunteers_login.objects.filter(user=email).exists():
            messages.success(request, 'Email already exist....!!!!')
            return redirect('volunteerreg')    
        else:
            log=volunteers_login(user=email,password=passwords)
            log.save()
            
            userid=volunteers_login.objects.get(user=email)
            reg=volunteer_reg(fname=fname,lname=lname,phone=phone,hname=hname,district_id=dist,user_id=userid.user,city=city,pin=pin,aadhar=aadhar,password=passwords)
            reg.save()
            return redirect('volunteer_login')
    district=District.objects.all()
    return render(request,'volunteerreg.html',{'district':district})


def volunteer_login(request):
    request.session.flush()
    if 'email' in request.session:
        return redirect(volunteerhome)

    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        print(email,password)
        password2=sha256(password.encode()).hexdigest()
        print(password2)
        vol=volunteers_login.objects.filter(user=email,password=password2,type=1)
        if vol:
            vol_details=volunteers_login.objects.get(user=email,password=password2)
            email=vol_details.user
            request.session['email']=email
            return redirect('volunteerhome')
        else:
            print("invalid")
            messages.success(request,"Invalid login Credentials")
            return redirect(volunteer_login)
    return render(request, 'volunteer_login.html')


def viewdonations(request):
    
    if 'email' in request.session:
        
        email=request.session['email']
        print(email)
        view=userdonate.objects.all()
        pay=Payment.objects.filter(user_id=email)
        return render(request, 'viewdonations.html',{'email':email,'view':view,'pay':pay})

def volunteer_logout(request):
    if 'email' in request.session:
        request.session.flush()
    return redirect(volunteer_login)


def address(request):
    if request.method == 'POST':
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        hname=request.POST.get('hname')
        city=request.POST.get('city') 
        district=request.POST.get('district')
        pin=request.POST.get('pin')
        if 'email' in request.session:
            user=request.session['email']
            reg=Address(fname=fname,email=email,phone=phone,hname=hname,city=city,district_id=district,pin=pin,user_id=user,lname=lname)
            reg.save()
            print(fname)
            return redirect('profile')
    # district=District.objects.all()
    # return render(request,,{'district':district})
    return redirect('profile')


def deleteaddress(request,id):
    Address.objects.get(id=id).delete()
    return redirect(profile)


def vol_chooseorphan(request):
    district= District.objects.all()
    email=request.session['email']
    d = {'district': district,'name':email}
    return render(request,'Vol_chooseorphan.html',d)

def vol_load_orphanages(request):
    district_id = request.GET.get('district')
    # name=request.POST.get('name')
    orphanages = Orphanage.objects.filter(district_id=district_id)
    return render(request, 'Vol_Orphanagelist.html', {'orphanages': orphanages})


def donate_approve(request,id):
    if 'email' in request.session:
        value=userdonate.objects.get(id=id)
        value.status=1
        value.save()
        return redirect(vol_chooseorphan)
    return redirect(login)


def vol_viewdonations(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        district=request.POST.get('district')
        result=userdonate.objects.filter(orphanage_id=name)
        if 'email' in request.session:
            email=request.session['email']
            return render(request, 'vol_viewdonation.html',{'email':email,'result':result})
        return redirect(login)


# Forgot Password
def forgotpassword(request):
    if request.method =="POST":
        email=request.POST.get('email')
        if all_logins.objects.filter(email=email).exists():
            user=all_logins.objects.get(email=email) 
            o=generateOTP()
            htmlgen = '<p>Your OTP is:'+o+'</p>'
            send_mail('OTP request',o,'Orphanage Management',[email], fail_silently=False, html_message=htmlgen)
            user.otp=o;
            user.save()
            request.session['email']=email 
            messages.success(request, 'OTP is send to ..'+email+'...Please Verify')
            return redirect('verify_forgot_otp')
        else:
            messages.success(request, 'Email Not Exist ...')
            return redirect(login)
    return render(request,'forgot_email.html')

# Verify forgot password OTP
def verify_forgot_otp(request):
    if 'email' in request.session:
        if request.method=='POST':
            otps = request.POST.get('otp');
            email = request.POST.get('email');
            if all_logins.objects.filter(email=email,otp=otps):
                messages.success(request, 'OTP is Verified..Please Enter New Password...')
                return redirect(new_password)
            else:
                 messages.success(request, 'Incorrcect OTP...')
    session=request.session['email']
    return render(request,'verify_forgot_otp.html',{'session':session}) 

# New Password via Forgot Password
def new_password(request):
    if 'email' in request.session:
        if request.method=='POST':
            password = request.POST.get('pswd');
            pswd=sha256(password.encode()).hexdigest()
            email = request.POST.get('email');
            user=all_logins.objects.get(email=email)
            user.password=pswd
            user.save()
            messages.success(request, 'Password Updated Successfully ...')
            return redirect(login)
    session=request.session['email']
    return render(request,'newpassword.html',{'session':session})


# For Donate Money
def Donate_Money(request,id):
    if 'email' in request.session:
        email=request.session['email']
        home=Orphanage.objects.get(id=id)
        id=home.id
        return render(request,"Donate_Amount.html",{'id':id,'email':email})
    else:
        return redirect(login)

def pay_money(request,id):
    if 'email' in request.session:
        email=request.session['email']
        user=all_logins.objects.get(email=email)
        home=Orphanage.objects.get(id=id)
        if request.method =="POST":
            Amounts=request.POST.get('Amount');
            result=Payment(user=user,amount=Amounts,orphanage=home)
            result.save()
            total=Decimal(Amounts)
            total_amount=tbl_amounts.objects.get(id=1)
            total_amount.amounts= total_amount.amounts - total
            total_amount.save()
        messages.success(request, 'Donated Successfully...')
        return redirect(viewdonations)
    else:
        return redirect(login)