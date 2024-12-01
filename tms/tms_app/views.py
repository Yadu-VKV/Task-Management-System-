from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserForm, ProjectForm, TaskForm, TaskStatusForm
from .models import User, Project, Task

# Create your views here.

# ------------------ Authentication Views ------------------

# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect based on user role
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# ------------------ Dashboard Views ------------------

@login_required
def dashboard(request):
    if request.user.role == 'PM':
        return redirect('pm_dashboard')
    elif request.user.role == 'TL':
        return redirect('tl_dashboard')
    elif request.user.role == 'TM':
        return redirect('tm_dashboard')
    return render(request, 'access_denied.html')

@login_required
def pm_dashboard(request):
    projects = Project.objects.filter(created_by=request.user)
    return render(request, 'pm_dashboard.html', {'projects': projects})

@login_required
def tl_dashboard(request):
    projects = Project.objects.filter(team_lead=request.user)
    return render(request, 'tl_dashboard.html', {'projects': projects})

@login_required
def tm_dashboard(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, 'tm_dashboard.html', {'tasks': tasks})

# ------------------ Project Management Views ------------------

@login_required
def create_project(request):
    if request.user.role != 'PM':
        return render(request, 'access_denied.html')
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            return redirect('pm_dashboard')
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'form': form})

@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.user.role != 'PM' or project.created_by != request.user:
        return render(request, 'access_denied.html')
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('pm_dashboard')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'edit_project.html', {'form': form})

@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.user.role != 'PM' or project.created_by != request.user:
        return render(request, 'access_denied.html')
    if request.method == 'POST':
        project.delete()
        return redirect('pm_dashboard')
    return render(request, 'delete_project.html', {'project': project})

# ------------------ Task Management Views ------------------

@login_required
def create_task(request):
    if request.user.role != 'TL':
        return render(request, 'access_denied.html')
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            return redirect('tl_dashboard')
    else:
        form = TaskForm()
    return render(request, 'create_task.html', {'form': form})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.user.role not in ['PM', 'TL'] or (request.user.role == 'TL' and task.project.team_lead != request.user):
        return render(request, 'access_denied.html')
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tl_dashboard')
    else:
        form = TaskForm(instance=task)
    return render(request, 'edit_task.html', {'form': form})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.user.role not in ['PM', 'TL'] or (request.user.role == 'TL' and task.project.team_lead != request.user):
        return render(request, 'access_denied.html')
    if request.method == 'POST':
        task.delete()
        return redirect('tl_dashboard')
    return render(request, 'delete_task.html', {'task': task})

@login_required
def update_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.user.role != 'TM' or task.assigned_to != request.user:
        return render(request, 'access_denied.html')
    if request.method == 'POST':
        form = TaskStatusForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tm_dashboard')
    else:
        form = TaskStatusForm(instance=task)
    return render(request, 'update_task_status.html', {'form': form})

# ------------------ User Management Views ------------------

@login_required
def create_user(request):
    if request.user.role != 'PM':
        return render(request, 'access_denied.html')
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pm_dashboard')
    else:
        form = UserForm()
    return render(request, 'create_user.html', {'form': form})

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.user.role != 'PM':
        return render(request, 'access_denied.html')
    if request.method == 'POST':
        user.delete()
        return redirect('pm_dashboard')
    return render(request, 'delete_user.html', {'user': user})
