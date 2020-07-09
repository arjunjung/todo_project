from django.db import IntegrityError
from django.shortcuts import render, redirect ,get_object_or_404
# for signup form
from django.contrib.auth.forms import UserCreationForm
# for login form
from django.contrib.auth.forms import AuthenticationForm
# for user creation
from django.contrib.auth.models import User
# for user login
from django.contrib.auth import login
# for logout
from django.contrib.auth import logout
# for checking password and username is true or not
from django.contrib.auth import authenticate
# for todos form
from .forms import TodoFrom
#Importing model Todo
from .models import Todo
#Importing Timezone
from django.utils import timezone
# For only verified user show some pages
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'todo/home.html')


def loginuser(request):
    if request.method == 'GET':
        return render(request, './todo/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        # If username and password are not matched then...
        if user is None:
            return render(request, './todo/loginuser.html',
                          {'form': AuthenticationForm(), 'error': "Username or Password didn't matched."})
        else:
            login(request, user)
            return redirect('current_todos')


def signupuser(request):
    if request.method == 'GET':
        return render(request, './todo/signupuser.html', {'form': UserCreationForm()})
    else:
        # This else block is called by signup button automatically
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                login(request, user)
                return redirect('current_todos')

            except IntegrityError:
                return render(request, './todo/signupuser.html',
                              {'form': UserCreationForm(), 'error': "Username already existed."})
        else:
            return render(request, './todo/signupuser.html',
                          {'form': UserCreationForm(), 'error': "Password didn't match"})


@login_required()
def current_todos(request):
    todos = Todo.objects.filter(user = request.user, dateCompleted__isnull=True)
    return render(request, 'todo/current_todos.html',{'todos':todos})


@login_required()
def completed_todos(request):
    todos = Todo.objects.filter(user = request.user, dateCompleted__isnull=False).order_by('-dateCompleted')
    return render(request, 'todo/completed_todos.html',{'todos':todos})


@login_required()
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required()
def create_todo(request):
    if request.method == 'GET':
        return render(request, 'todo/create_todo.html', {'form': TodoFrom()})
    else:
        try:
            # getting all data from FORM
            form = TodoFrom(request.POST)
            # getting user who made Todo
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            # pushing to the database
            newtodo.save()

        except ValueError:
            return render(request, 'todo/create_todo.html', {'form': TodoFrom(),'error':"Invalid input. Try Again"})

        return redirect('current_todos')


@login_required()
def view_todo(request,todo_pk):
    # To get object of single todos using primary key
    todo = get_object_or_404(Todo,pk=todo_pk,user=request.user)
    if request.method == 'GET':
        # To through Todos form with filed data which are previously written.
        form = TodoFrom(instance=todo)
        return render(request, 'todo/view_todo.html', {'todo': todo, 'form': form})
    else:
        try:
            # getting all data from FORM
            form = TodoFrom(request.POST, instance=todo)
            form.save()
            return redirect('current_todos')

        except ValueError:
            return render(request, 'todo/view_todo.html', {'todo': todo,'form':TodoFrom(instance=todo),'error':"Invalid input. Try Again"})


@login_required()
def complete_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.dateCompleted = timezone.now()
        todo.save()
        return redirect('current_todos')


@login_required()
def delete_todo(request,todo_pk):
    todo = get_object_or_404(Todo,pk= todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('current_todos')