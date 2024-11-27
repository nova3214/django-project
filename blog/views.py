from django.shortcuts import render, get_object_or_404, redirect
from .forms import ApplicationForm
from .models import Application
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from .forms import UserRegisterForm, ApplicationForm
from django.contrib.auth.forms import AuthenticationForm
from .forms import ProfileForm
from .models import Profile



def home(request):
    return render(request, 'blog/univer.html')

def history(request):
    return render(request, 'blog/history.html')

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')
@login_required
def application_status(request):
    try:
        application = Application.objects.get(user=request.user)
        if application.status == 'approved':
            schedule = {
                "Математика": "Понедельник, 10:00",
                "Физика": "Вторник, 12:00",
                "Химия": "Среда, 14:00"
            }
            teachers = ["Иван Иванов", "Петр Петров", "Алексей Алексеев"]
        else:
            schedule = None
            teachers = None
    except Application.DoesNotExist:
        application = None
        schedule = None
        teachers = None

    return render(request, 'blog/application_status.html', {
        'application': application,
        'schedule': schedule,
        'teachers': teachers
    })

@login_required
def apply(request):
    try:
        application = Application.objects.get(user=request.user)
    except Application.DoesNotExist:
        application = None
    if application and application.status == 'rejected':
        application.delete()
        application = None
    if application:
        return render(request, 'blog/apply.html', {'application': application})
    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            new_application = form.save(commit=False)
            new_application.user = request.user
            new_application.save()
            return redirect('apply')  
    else:
        form = ApplicationForm()

    return render(request, 'blog/apply.html', {'form': form, 'application': application})
def application_list(request):
    applications = Application.objects.all()
    return render(request, 'blog/application_list.html', {'applications': applications})
def approve_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    application.status = 'approved'
    application.save()
    return redirect('application_list')
def reject_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    application.status = 'rejected'
    application.save()
    return redirect('application_list')
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'blog/login.html'

class CustomLogoutView(LogoutView):
    template_name = 'blog/logout.html'
def dashboard(request):
    if request.method == "POST":
        if "login" in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('dashboard')
        elif "register" in request.POST:
            register_form = UserRegisterForm(request.POST)
            if register_form.is_valid():
                register_form.save()
                return redirect('dashboard')
    else:
        login_form = AuthenticationForm()
        register_form = UserRegisterForm()

    application = None
    application_form = None
    if request.user.is_authenticated:
        try:
            application = Application.objects.get(user=request.user)
        except Application.DoesNotExist:
            application_form = ApplicationForm()

    return render(request, 'blog/dashboard.html', {
        'login_form': login_form,
        'register_form': register_form,
        'application': application,
        'application_form': application_form,
    })
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('dashboard')
    else:
        profile_form = ProfileForm(instance=profile)

    return render(request, 'blog/dashboard.html', {
        'profile_form': profile_form,
        'profile': profile,
    })

