import requests
from datetime import datetime
from .models import Task
from django.conf import settings

# Funciones para la sincronización de Todoist
def get_todoist_tasks():
    headers = {
        "Authorization": f"Bearer {settings.TODOIST_API_KEY}"
    }
    response = requests.get("https://api.todoist.com/rest/v1/tasks", headers=headers)
    return response.json()

def parse_todoist_task(task_data):
    return {
        'title': task_data['content'],
        'description': task_data.get('description', ''),
        'due_date': datetime.strptime(task_data['due']['date'], '%Y-%m-%dT%H:%M:%SZ') if task_data.get('due') else None,
        'priority': task_data['priority'],
        'completed': task_data['completed']
    }

def sync_todoist_tasks():
    tasks = get_todoist_tasks()
    
    for task_data in tasks:
        task_info = parse_todoist_task(task_data)
        Task.objects.update_or_create(
            title=task_info['title'],
            defaults=task_info
        )

# Funciones para la sincronización de Trello
def get_trello_boards():
    url = f"https://api.trello.com/1/members/me/boards?key={settings.TRELLO_API_KEY}&token={settings.TRELLO_TOKEN}"
    response = requests.get(url)
    return response.json()

def get_trello_cards(board_id):
    url = f"https://api.trello.com/1/boards/{board_id}/cards?key={settings.TRELLO_API_KEY}&token={settings.TRELLO_TOKEN}"
    response = requests.get(url)
    return response.json()

def parse_trello_card(card):
    return {
        'title': card['name'],
        'description': card.get('desc', ''),
        'due_date': datetime.strptime(card['due'], '%Y-%m-%dT%H:%M:%SZ') if card.get('due') else None,
        'priority': 1,  # Trello doesn't have priority levels by default
        'completed': card['dueComplete']
    }

def sync_trello_tasks():
    boards = get_trello_boards()
    
    for board in boards:
        cards = get_trello_cards(board['id'])
        
        for card in cards:
            task_info = parse_trello_card(card)
            Task.objects.update_or_create(
                title=task_info['title'],
                defaults=task_info
            )

# Funciones para calcular y asignar prioridades
def calculate_priority(task):
    priority = 1
    if task.due_date:
        days_left = (task.due_date - datetime.now()).days
        if days_left <= 1:
            priority = 3
        elif days_left <= 3:
            priority = 2
    return priority

def assign_priorities():
    tasks = Task.objects.all()
    for task in tasks:
        task.priority = calculate_priority(task)
        task.save()
