from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from tasks.tasks import send_email_task
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.views.decorators.csrf import csrf_exempt

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@csrf_exempt
def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.two_factor_enabled:
                otp_code = get_random_string(length=4, allowed_chars='0123456789')
                user.otp_code = otp_code
                user.save()
                subject = 'Your OTP Code'
                body = f'Your OTP code is {otp_code}'
                send_email_task.delay(user.email, subject, body)  
                request.session['temp_user_id'] = user.id
                return redirect('verify_otp')
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'accounts/login.html')

User = get_user_model()
def verify_otp_view(request):
    if request.method == 'POST':
        otp_code = request.POST.get('otp_code')
        user_id = request.session.get('temp_user_id')
        if not user_id:
            messages.error(request, "Session expired. Please log in again.")
            return redirect('login')
        user = User.objects.get(id=user_id)
        if user.otp_code == otp_code:
            login(request, user)
            del request.session['temp_user_id']
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid OTP code.")
    return render(request, 'accounts/verify_otp.html')


@login_required
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html', {'user': request.user})

@login_required
def enable_2fa_view(request):
    if request.method == 'POST':
        request.user.two_factor_enabled = True
        request.user.save()
        return redirect('dashboard')    
    return render(request, 'accounts/enable_2fa.html')

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
