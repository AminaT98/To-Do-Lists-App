from django.shortcuts import render, redirect, get_object_or_404
from .forms import ListForm, LoginForm, SignupForm, TaskForm
from .models import List, Task, Profile
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .permissions import IsObjectOwner
from rest_framework.response import Response
from .serializers import ProfileSerializer, RegisterSerializer, TaskSerializer, ListSerializer
from rest_framework import viewsets, status
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages



# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "bio": profile.bio,
        "location": profile.location,
        "avatar": profile.avatar
    })

@login_required
def index(request):
    lists = List.objects.filter(owner=request.user.profile)
    context = {
        'lists': lists,
    }
    return render(request, 'index.html', context)

@login_required
def list_detail(request, list_id):
    todo_list = get_object_or_404(List, id=list_id, owner=request.user.profile)
    tasks = Task.objects.filter(list=todo_list)
    
       # Check if an edit request exists
    edit_task_id = request.GET.get('edit')
    edit_task = None
    if edit_task_id:
        edit_task = get_object_or_404(Task, id=edit_task_id, list__owner=request.user.profile)
    
    context = {
        'todo_list': todo_list,
        'tasks': tasks,
        'edit_task': edit_task, # pass this to the template
    }
    return render(request, 'list_detail.html', context)

@login_required
def create_task(request, list_id):
    if request.method == 'POST':
        todo_list = get_object_or_404(List, id=list_id, owner=request.user.profile)
        form = TaskForm(request.POST)
        if form.is_valid():
            form.instance.list = todo_list
            form.save()
    return redirect('list_detail', list_id=list_id)

@login_required
def create_list(request):
    if request.method != 'POST':
        return render(request, 'new_list.html')
    else:
        form = ListForm(request.POST)
        if not form.is_valid():
            return render(request, 'new_list.html', {'form': form})
        
        form.instance.owner = request.user.profile
        form.save()
    return redirect('list_detail', list_id=form.instance.id)

@login_required
def toggle_task(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id, list__owner=request.user.profile)
        task.completed = not task.completed
        task.save()

        return redirect('list_detail', list_id=task.list.id)

@login_required
def delete_list(request, list_id):
    if request.method == "POST":
        todo_list = get_object_or_404(List, id=list_id, owner=request.user.profile)
        todo_list.delete()
        return redirect('index')
    

@login_required
def delete_task(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id, list__owner=request.user.profile)
        list_id = task.list.id
        task.delete()
        return redirect('list_detail', list_id=list_id)

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, list__owner=request.user.profile)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect('list_detail', list_id=task.list.id)

    else:
        form = TaskForm(instance=task)

    return render(request, 'edit_task.html', {
        'form': form,
        'task': task
    })

def signup_page(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if not form.is_valid():
            return render(request, "signup.html", {"form": form})

        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, "signup.html")

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect("login")

    return render(request, "signup.html")

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(request, "login.html", {"form": form})
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('index')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

class RegisterViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User created successfully",
                "user": RegisterSerializer(user).data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsObjectOwner]
    
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsObjectOwner]

class ListViewSet(viewsets.ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer
    permission_classes = [IsAuthenticated, IsObjectOwner]