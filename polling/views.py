from django.shortcuts import render,HttpResponse,redirect
from .models import Contact,Candidate,extenduser
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

def index(request):
    # datas = extenduser.objects.filter(user = request.user)
    return render(request,'polling/index.html')


def loginhandle(request):
    if request.method == "POST":
        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request, user)
            messages.success(request,"Logged in")
            return redirect('index')
        else:
            messages.error(request,'Wrong credentials')
            return redirect('login')
        

    return render(request,'polling/login.html')

def register(request):
    usernamed = []
    aadhard = []
    voterd = []
    data = extenduser.objects.all()
    for i in data:
        usernamed.append(i.user.username)
        aadhard.append(i.aadhar)
        voterd.append(i.voterid)

    if request.method == "POST":
        
        username1 = request.POST['username1']
        # email1 = request.POST['email1']
        fname = request.POST['fname']
        lname = request.POST['lname']
        age = request.POST['age']
        phone = request.POST['phone']
        aadhar = request.POST['aadhar']
        voterid = request.POST['voterid']
        ward = request.POST['ward']
        pswd = request.POST['pswd']
        repswd = request.POST['repswd']
        if len(username1)<10:
            messages.error(request, " Your user name must be under 10 characters")
            return redirect('index')

        if not username1.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('index')
        if int(age)<18:
            messages.error(request,"You are not Eligible Age:Error ")
            return redirect('index')
        if username1 in usernamed:
            messages.error(request,'Username is already taken')
            return redirect('register')
        if aadhar in aadhard:
            messages.error(request,'Aadhar is already registered')
            return redirect('register')
        if voterid in voterd:
            messages.error(request,'Voterid is already registered')
            return redirect('register')
        if (pswd!=repswd):
             messages.error(request, " Passwords do not match")
             return redirect('index')
        if len(aadhar) != 12:
            messages.error(request,'Invalid Aadhar (Aadhar should be of 12 digits)')
            return redirect('register')
        if len(voterid) != 10:
            messages.error(request,'Invalid Voter ID')
            return redirect('register')
        if len(phone)<10 or len(phone)>13:
            messages.error(request,'Invalid phone number')
            return redirect('register')
        
        myuser = User.objects.create_user(username=username1,password=pswd)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        extend = extenduser(user=myuser,age=age,phone=phone,aadhar=aadhar,voterid=voterid,ward=ward)
        extend.save()
        messages.success(request, 'User successfully created')
        return redirect('index')
    return render(request,'polling/signup.html')

def logouthandle(request):
        logout(request)
        messages.success(request,'Successfull logged out')
        return redirect('login')

@login_required(login_url='login')
def results(request):
    data_C = Candidate.objects.filter(party='Congress')
    data_B = Candidate.objects.filter(party='BJP')
    data = extenduser.objects.filter(user=request.user).first()
    ward = data.ward
    candidate_l = Candidate.objects.filter(ward=ward).all()
    return render(request,'polling/result.html',{'data_C':data_C , 'data_B':data_B, 'data':candidate_l, 'U_data':data})

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        desc = request.POST['desc']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(desc)<2 :
            messages.error(request,'Please fill the form Correctly!')
        else:
            contact = Contact(name=name,email=email,phone=phone,desc=desc)
            contact.save()
            messages.success(request, 'Successfully Sent')
    return render(request,'polling/contact.html')

@login_required(login_url='login')    
def votingpanel(request):
    # if request.method == 'POST':
        data = extenduser.objects.filter(user=request.user).first()
        ward = data.ward
        cand_list = Candidate.objects.filter(ward=ward).all()

        return render(request,'polling/votingsection.html',{'cand_list':cand_list})

    # return render(request,'polling/votingsection.html')

def candidate(request):
    if request.method == 'POST':
        name = request.POST['name']
        party = request.POST['party']
        ward = request.POST['ward']
        city = request.POST['city']
        try:
            case = request.POST['case']
        except:
            case = False
        try:
            declare = request.POST['declare']
        except:
            declare = False
        if (case == 'on'):
            messages.error(request,'You are not Eligible')
            return redirect('candidate')
        elif (declare == False):
             messages.error(request,'You must agree to the terms!')
        else:
            cand = Candidate(name=name,party=party,ward=ward,city=city,criminal=False,declare=True )
            cand.save()
            # print(cand)
            messages.success(request,'Your application is under Verification')
            return redirect('candidate')
    return render(request,'polling/candidate.html')

@login_required(login_url='login')
def aadharverify(request):
    if request.method == 'POST':
        aadharv = request.POST['aadharv']
        voterv = request.POST['voterv']
        data = extenduser.objects.filter(user=request.user).first()
        if (aadharv == data.aadhar) and (voterv == data.voterid):
            messages.success(request,'Aadhar and Voter ID has been verified')
            return redirect('OTP')
        else:
            messages.error(request,'Invalid Aadhar or Voter ID Details, please try again')
            return redirect('verify')

    return render(request,'polling/aadharverification.html')

@login_required(login_url='login')
def otp(request):
    c_otp = '1234'
    if request.method == 'POST':
        otpv = request.POST['OTP']
        if (c_otp == otpv):
            messages.success(request,'Welcome to the Voting Section')
            return redirect('voting')
        else:
            messages.error(request,'Wrong OTP')
            return redirect('OTP') 

    return render(request,'polling/OTP.html')

def vote(request,sno):
    is_voted = extenduser.objects.filter(user=request.user).first()
    if (is_voted.voted == True):
        messages.error(request,'No Cheating, You have already VOTED!')
        return redirect('index')
    else:
        count = Candidate.objects.filter(sno=sno).first()
        count.vcount = count.vcount + 1
        count.save()
        is_voted.voted = True
        is_voted.save()
        messages.success(request,'Your response has been recorded')
        return redirect('index')
def show_results(request):
    if request.method == 'POST':
        try:
            globally = request.POST['globally']
        except:
            globally = False
        print(globally)
        if globally == 'on':
            voter_list = extenduser.objects.all()
            for voter in voter_list:
                if voter.show_results == False:
                    voter.show_results = True
                    voter.save()
            messages.success(request,'Changes applied successfully, Results are now Online')
            return redirect('index')
        elif globally == False:
            voter_list = extenduser.objects.all()
            for voter in voter_list:
                if voter.show_results == True:
                    voter.show_results = False
                    voter.save()
            messages.success(request,'Changes applied successfully, Results are now Offline')
            return redirect('index')

    return render(request,'polling/admin.html')    
    

