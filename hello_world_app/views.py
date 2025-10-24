from django.shortcuts import render, redirect
from .models import Task
from django.db.models import Q

def home(request):
    # Add a new task
    if request.method == 'POST' and 'add_task' in request.POST:
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        Task.objects.create(title=title, description=description, due_date=due_date)
        return redirect('home')

    # Mark/unmark a task as completed
    if request.method == 'POST' and 'toggle_task' in request.POST:
        task_id = request.POST.get('task_id')
        task = Task.objects.get(id=task_id)
        task.completed = not task.completed
        task.save()
        return redirect('home')

    # Delete a task
    if request.method == 'POST' and 'delete_task' in request.POST:
        task_id = request.POST.get('task_id')
        Task.objects.get(id=task_id).delete()
        return redirect('home')

    # Search functionality
    query = request.GET.get('q')
    if query:
        tasks = Task.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    else:
        tasks = Task.objects.all()

    return render(request, 'home.html', {'tasks': tasks, 'query': query})

