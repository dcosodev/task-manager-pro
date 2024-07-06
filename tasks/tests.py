from django.test import TestCase, Client
from django.urls import reverse
from .models import Task
from .services import calculate_priority, sync_todoist_tasks, sync_trello_tasks, assign_priorities
from datetime import datetime, timedelta
from unittest.mock import patch

class TaskModelTests(TestCase):

    def setUp(self):
        self.task = Task.objects.create(
            title='Test Task',
            description='This is a test task',
            due_date=datetime.now() + timedelta(days=2),
            priority=1,
            completed=False
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.description, 'This is a test task')
        self.assertFalse(self.task.completed)

class TaskViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.task = Task.objects.create(
            title='Test Task',
            description='This is a test task',
            due_date=datetime.now() + timedelta(days=2),
            priority=1,
            completed=False
        )

    def test_task_list_view(self):
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')

    def test_task_detail_view(self):
        response = self.client.get(reverse('task-detail', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')

    def test_task_create_view(self):
        response = self.client.post(reverse('task-create'), {
            'title': 'New Task',
            'description': 'New task description',
            'due_date': datetime.now() + timedelta(days=3),
            'priority': 2,
            'completed': False
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.last().title, 'New Task')

    def test_task_update_view(self):
        response = self.client.post(reverse('task-edit', args=[self.task.id]), {
            'title': 'Updated Task',
            'description': 'Updated task description',
            'due_date': self.task.due_date,
            'priority': self.task.priority,
            'completed': self.task.completed
        })
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')

    def test_task_delete_view(self):
        response = self.client.post(reverse('task-delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

class TaskServiceTests(TestCase):

    @patch('tasks.services.requests.get')
    def test_sync_todoist_tasks(self, mock_get):
        mock_get.return_value.json.return_value = [
            {
                'content': 'Test Todoist Task',
                'description': 'This is a test todoist task',
                'due': {'date': (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%dT%H:%M:%SZ')},
                'priority': 1,
                'completed': False
            }
        ]
        sync_todoist_tasks()
        self.assertTrue(Task.objects.filter(title='Test Todoist Task').exists())

    @patch('tasks.services.requests.get')
    def test_sync_trello_tasks(self, mock_get):
        mock_get.side_effect = [
            {'json.return_value': [{'id': '1', 'name': 'Test Board'}]},  # Mocking boards response
            {'json.return_value': [
                {
                    'name': 'Test Trello Card',
                    'desc': 'This is a test trello card',
                    'due': (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%dT%H:%M:%SZ'),
                    'dueComplete': False
                }
            ]}  # Mocking cards response
        ]
        sync_trello_tasks()
        self.assertTrue(Task.objects.filter(title='Test Trello Card').exists())

    def test_calculate_priority(self):
        task = Task.objects.create(
            title='Priority Test Task',
            description='This is a priority test task',
            due_date=datetime.now() + timedelta(days=1),
            priority=1,
            completed=False
        )
        priority = calculate_priority(task)
        self.assertEqual(priority, 3)

    def test_assign_priorities(self):
        task = Task.objects.create(
            title='Assign Priority Test Task',
            description='This is an assign priority test task',
            due_date=datetime.now() + timedelta(days=1),
            priority=1,
            completed=False
        )
        assign_priorities()
        task.refresh_from_db()
        self.assertEqual(task.priority, 3)
