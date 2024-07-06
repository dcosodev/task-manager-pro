from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from .models import Task
from .services import sync_todoist_tasks, sync_trello_tasks, assign_priorities

# Vistas de Tareas

class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'


class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'


class TaskCreateView(CreateView):
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['title', 'description', 'due_date', 'priority', 'completed']


class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['title', 'description', 'due_date', 'priority', 'completed']


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = '/'


# Vistas de Sincronización

class SyncTodoistTasksView(View):
    def get(self, request, *args, **kwargs):
        sync_todoist_tasks()
        assign_priorities()
        return redirect('task-list')


class SyncTrelloTasksView(View):
    def get(self, request, *args, **kwargs):
        sync_trello_tasks()
        assign_priorities()
        return redirect('task-list')
