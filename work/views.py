from django.shortcuts import render,redirect
from django.views.generic import View
from work.forms import Register,LoginForm,TaskForm
from work.models import User,Taskmodel
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils.decorators import method_decorator

# Create your views here.
# CRUD
# decorator--koreperil oral egilum login aanel mathram todonte home pagell keran pattollu--cls based viewill mathram decnte aavsyollu
def signin_required(fn):
    def wrapper(request,**kwargs):      #getllum postllum varunna argu nammal wrapperill kodukkuney but self kodukkula only in cls not in fun
        if not request.user.is_authenticated:    #login cheytha aal authenticated allegil login allegil redirect cheya login llot
            return redirect("log")
        else:
            return fn(request,**kwargs)         #login aanegil ee argu ellam fn llot paranjuvida
    return wrapper


#oralde idll kerit matte aalude idll olla data delete aakan paadilla so next dec call  cheyanu
def mylogin(fn):
    def wrapper(request,**kwargs):
        id=kwargs.get("pk")
        obj=Taskmodel.objects.get(id=id)      #idnne eduthat modellil poyi objnne eduth verify cheyanam
        if obj.user!=request.user:
            return redirect("log")
        else:
            return fn(request,**kwargs)
    return wrapper


class Registration(View):
    def get(self,request,**kwargs):
        form=Register()
        return render(request,"register.html",{"form":form})

    def post(self,request,**kwargs):
        form=Register(request.POST)
        if form.is_valid():
            # form.save()
            User.objects.create_user(**form.cleaned_data)     #create_user=to encrypet the passwd kodutha  password encrypt aayit kanikyum pswd okke django decrypt cheyan pattum
            form=Register()
            return redirect("log")   #to connect to signin form we need to use a name that we have given in url
        


class Update_user(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        data=User.objects.get(id=id)
        form=Register(instance=data)
        return render(request,"register.html",{"form":form})
    

    def post(self,request,*args,**kwargs):
        id=User.objects.get(id=id)
        data=User.objects.get(id=id)
        form=Register(request.POST,instance=data)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            return redirect("log")

        
# agane oru user name and pswd endonnu nokkunu
class Signin(View):
    def get(self,request,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    

    def post(self,request,**kwargs):

        form=LoginForm(request.POST)

        if form.is_valid():         #username pswd
            print(form.cleaned_data)

            u_name=form.cleaned_data.get("username")
            # getting userame and pswd from cleaned_data
            pwd=form.cleaned_data.get("password")
            user_obj=authenticate(username=u_name,password=pwd)
            # checking if the username and pswd are valid in the table auth_user

            if user_obj:
                print("valid credentials")
                # if true passing the user_obj to the login function
                login(request,user_obj)
                return redirect("index")   #name="index"
            
            else:
                form=LoginForm()
                print("incorrect credentials")
                return render(request,"login.html",{"form":form})
            
    
@method_decorator(signin_required,name='dispatch')    #decoratorname,ooro clsnnu akath 1ll kooduthal methods varum so decorator aplly cheyumbo chelapo onill kooduthal methodsll act cheyendivarum so nama dispatch kodukkunu(name matti kodukan pattum aneram chelapo error varum chelodath dispatch already files kodukum)
class Add_task(View):
    def get(self,request,**kwargs):
        form=TaskForm()
        # data=Taskmodel.objects.all().order_by('completed')   
        data=Taskmodel.objects.filter(user=request.user).order_by('completed')   #.filter(user=re.user) aa aal kodutha task mathram kanikyum ellardeyum kanikilla posillum kodukanam
        return render(request,"index.html",{"form":form,"data":data})
    

    def post(self,request,**kwargs):
        form=TaskForm(request.POST)
        # task_name,task_description
        if form.is_valid():
            form.instance.user=request.user
            # request.user=get the authenticated user(login)
            form.save()
            messages.success(request,"task added successfully")
        form=TaskForm()
         # data=Taskmodel.objects.all().order_by('completed')   
        data=Taskmodel.objects.filter(user=request.user).order_by('completed')     #read
        return render(request,"index.html",{"form":form,"data":data})
        
# oral already login aanegil aalude task mathram del aakan paadoluu allathe bakhi ollorude cheyan paadilla
# delete
@method_decorator(signin_required,name="dispatch")
@method_decorator(mylogin,name="dispatch")
class Delete_task(View):
    def get(self,request,**kwargs):
        id=kwargs.get("pk")
        Taskmodel.objects.get(id=id).delete()
        return redirect("index")
    

# update completed=false to true 

class Task_edit(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")

        obj=Taskmodel.objects.get(id=id)
        if obj.completed==False:
            obj.completed=True
            obj.save()
        return redirect("index")
    

class Signout(View):
    def get(self,request):
        logout(request)
        return redirect("log")
    


class User_del(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        User.objects.get(id=id).delete()
        return redirect('reg')
    

