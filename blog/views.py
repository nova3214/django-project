from django.shortcuts import render, get_object_or_404, redirect
from .forms import ApplicationForm
from .models import Application
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from .forms import UserRegisterForm



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
    # Проверка, есть ли уже заявка от пользователя
    try:
        application = Application.objects.get(user=request.user)
    except Application.DoesNotExist:
        application = None

    # Если заявка отклонена, даём пользователю возможность подать заявку снова
    if application and application.status == 'rejected':
        application.delete()
        application = None

    # Если заявка уже существует, показываем её статус
    if application:
        return render(request, 'blog/apply.html', {'application': application})
    
    # Если заявка еще не отправлена, показываем форму
    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            new_application = form.save(commit=False)
            new_application.user = request.user
            new_application.save()
            return redirect('apply')  # Перезагружаем страницу для отображения статуса
    else:
        form = ApplicationForm()

    return render(request, 'blog/apply.html', {'form': form, 'application': application})


def application_list(request):
    applications = Application.objects.all()
    return render(request, 'blog/application_list.html', {'applications': applications})

# Функция для одобрения заявки
def approve_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    application.status = 'approved'
    application.save()
    return redirect('application_list')

# Функция для отклонения заявки
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
            login(request, user)  # автоматический вход после регистрации
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'blog/login.html'

class CustomLogoutView(LogoutView):
    template_name = 'blog/logout.html'

