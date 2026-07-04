# 1. handle views and redirect
from django.shortcuts import render,redirect
# 2. Import an authentication form
from django.contrib.auth import authenticate,login,logout
# 3. Protect views
from django.contrib.auth.decorators import login_required
# 4. Provide base 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
# 5. Call registrationform form forms.py
from .forms import RegisterForm
# 6. The user models
from django.contrib.auth.models import User

# home page view
@login_required
def home_view(request):
    return render(request,'auth_1/home.html')

# Login view
def login_view(request):
    error_message = None
    
    if request.method=="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username,password=password)

        if user is not None:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'home'
            return redirect(next_url)
        
        else:
            error_message = "Invalid Credentials!"

    context = {'error': error_message}
    return render(request, 'accounts/login.html', context)

# Protected view
class ProtectedView(LoginRequiredMixin, View):
    login_url = '/login/'
    # 'next' - to redirect URL
    redirect_field_name = 'redirect_to'

    def get(self, request):
        return render(request, 'registration/protected.html')


#Logout view page  
def logout_view(request):
    if request.method=="POST":
        logout(request)
        return redirect('login')
    
    else:
        return redirect('home')




# Registration view page
def register_view(request):
    if request.method=="POST":
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            username= form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user = User.objects.create_user(username=username, password=password)
            login(request,user)
            return redirect('home')
    else:
        form = RegisterForm()

    context = {'form':form}
    return render(request, 'accounts/register.html', context)
    