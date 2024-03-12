from django.shortcuts import render ,redirect
from django.http import HttpResponse
from django.template import loader
from .models import Items,ItemDetails,Cart
from .forms import CreatUserForm,LoginUserForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
 templates=loader.get_template('index.html')
 return HttpResponse(templates.render())

def VF_product(request):
 templates=loader.get_template('VF_product.html')
 VF=ItemDetails.objects.select_related('itemsid')
 print(VF.query)
 return HttpResponse(templates.render({'VF':VF}))


@csrf_exempt
def auth_login(request):
 form=LoginUserForm()
 if request.method=='POST':
        form=LoginUserForm(data=request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            
            user=authenticate(username=username,password=password)
            if user:
                if user.is_active:
                    login(request,user)
                    return render(request,"index.html")
                        
 context={"form":form}
 return render(request,'auth_login.html',context)


@csrf_exempt
def auth_register(request):
 templates=loader.get_template('auth_register.html')
 form=CreatUserForm()
 if request.method=='POST':
        form=CreatUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('auth_login')
 context={'registerform':form}
 return HttpResponse(templates.render(context=context))

@csrf_exempt
def auth_logout(request):
     if request.method=='POST':
         logout(request)
         return redirect('/')


@login_required(login_url='/auth_login/')
def checkout(request):
 templates=loader.get_template('checkout.html')
 return HttpResponse(templates.render())

def VF_details(request ,id):
 templates=loader.get_template('VF_details.html')
 currentuser=request.user

 VF=ItemDetails.objects.select_related('itemsid').filter(id=id)
 context={
    'VF':VF
 }
 return HttpResponse(templates.render(context))

def add_to_cart(request,id):
   currentuser=request.user
   discount=2
   status=False
   VF=ItemDetails.objects.select_related('itemsid').filter(id=id)
   for item in VF:
        net=item.total-discount
   cart = Cart(
      Id_product=item.id,
      Id_user=currentuser.id,
      price=item.price,
      qty=item.qty,
      tax=item.tax,
      total=item.total,
      discount=discount,
      net=net,
      status=status
    
   )

   cart.save()
   return redirect('/VF_product')



