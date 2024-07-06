# TaskManagerPro

A smart task management application with automated priority assignment and seamless synchronization with Todoist and Trello.

## Features

- Sync tasks from Todoist and Trello
- Automated priority assignment based on deadlines and importance
- Task management with create, read, update, and delete functionality
- Productivity analytics

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/dcosodev/taskmanagerpro.git
   cd TaskManagerPro
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables for Todoist and Trello API keys in `settings.py`.

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

- Access the admin panel at `/admin` to manage tasks and synchronize with Todoist and Trello.
- Use the task list, detail, create, update, and delete views to manage your tasks.

## API Integration

### Todoist Integration

To sync tasks from Todoist, ensure you have your Todoist API key set up in the `settings.py` file:

```python
TODOIST_API_KEY = 'your_todoist_api_key'
```

### Trello Integration

To sync tasks from Trello, ensure you have your Trello API key, API secret, and token set up in the `settings.py` file:

```python
TRELLO_API_KEY = 'your_trello_api_key'
TRELLO_API_SECRET = 'your_trello_api_secret'
TRELLO_TOKEN = 'your_trello_token'
```

## Synchronization

To synchronize tasks, you can use the following URLs:

- Sync tasks from Todoist: `http://127.0.0.1:8000/tasks/sync_todoist/`
- Sync tasks from Trello: `http://127.0.0.1:8000/tasks/sync_trello/`

These endpoints will fetch tasks from Todoist and Trello, respectively, and update your local task list with the latest information.

## Running Tests

To run the tests for this project, use the following command:

```bash
python manage.py test tasks
```

This will execute the test suite for the `tasks` app, ensuring that all functionalities are working as expected.

## Contributing

Contributions are welcome! If you have any suggestions or improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
