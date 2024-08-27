# FastAPI Task Manager with Celery, PostgreSQL, and Redis

This is a FastAPI-based task management application that includes asynchronous task handling using Celery, PostgreSQL for data storage, and Redis as the message broker. The application is containerized using Docker to ensure consistency across different environments.

## Features

- RESTful API (CRUD Operations) for managing tasks
- Asynchronous background tasks with Celery
- Email notifications via SendGrid
- Containerized environment with Docker

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Environment Variables

The application uses the following environment variables:

- **DATABASE_URL**: The connection string for the cloud PostgreSQL database.
- **CELERY_BROKER_URL**: The URL for the Redis instance (default: `redis://localhost:6379/0`).
- **CELERY_RESULT_BACKEND**: The backend URL for Celery results (default: `redis://localhost:6379/0`).
- **SENDGRID_API_KEY**: The SendGrid API key for sending emails.
- **SENDGRID_TEMPLATE_ID**: The ID of the SendGrid email template.
- **SENDGRID_FROM_EMAIL**: The email address from which emails will be sent.
- **SENDGRID_TO_EMAIL**: The recipient email address.

These variables are set directly in the `.env` file.

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Tanmay1903/task-manager.git
cd task-manager
```

### 2. Set Up Environment Variables

Copy the provided `.env` file in the root folder (task-manager). Please replace the value in `SENDGRID_TO_EMAIL` key to `your_own_email_address` in the `.env` file, in order to test the email notification.

### 3. Build and Run the Containers

```bash
docker-compose up --build
```

### 4. Access the Application

```bash
http://127.0.0.1:8081/docs#/
```

### 5. Stopping the Containers

```bash
docker-compose down
```

## Testing and Functionality

### 1. Testing the Code
To ensure the quality and reliability of the application, I have written and run tests using a testing framework like pytest.

#### Setting Up Pytest
- Install pytest: Ensure pytest is installed in your environment.
- Write Tests: Created a tests/ directory in the root of the project, and added test files to it. For example, tests/test_main.py includes tests for the FastAPI endpoints.
- Run the Tests Inside the Docker Container:
```bash
docker-compose up --build test
```

### 2. Core Functionalities
The application offers the following core functionalities:

1. Creating Tasks:
   - Endpoint: `POST /tasks/`
   - Functionality: Allows users to create a new task by providing a title and description.
   - Example Request:
     ```bash
      curl -X POST "http://localhost:8081/tasks/" -H "Content-Type: application/json" -d '{"title": "New Task", "description": "This is a new task"}'
     ```
   - Example Response:
     ```
      {
          "id": 1,
          "title": "New Task",
          "description": "This is a new task"
      }
     ```
2. Listing Tasks:
   - Endpoint: `GET /tasks/`
   - Functionality: Lists all existing tasks
   - Example Request:
     ```bash
      curl -X GET "http://localhost:8081/tasks/"
     ```
   - Example Response:
     ```
      [
        {
            "id": 1,
            "title": "New Task",
            "description": "This is a new task"
        }
      ]
     ```
3. Retrieving a Specific Task:
   - Endpoint: `GET /tasks/{task_id}`
   - Functionality: Retrieves a specific task by its ID.
   - Example Request:
     ```bash
      curl -X GET "http://localhost:8081/tasks/1"
     ```
   - Example Response:
     ```
      {
          "id": 1,
          "title": "New Task",
          "description": "This is a new task"
      }
     ```
4. Updating a Task:
   - Endpoint: `PUT /tasks/{task_id}`
   - Functionality: Updates an existing task's title and description.
   - Example Request:
     ```bash
      curl -X PUT "http://localhost:8081/tasks/1" -H "Content-Type: application/json" -d '{"title": "Updated Task", "description": "This is an updated task"}'
     ```
   - Example Response:
     ```
      {
          "id": 1,
          "title": "Updated Task",
          "description": "This is an updated task"
      }
     ```
5. Deleting a Task:
   - Endpoint: `DELETE /tasks/{task_id}`
   - Functionality: Deletes a task by its ID.
   - Example Request:
     ```bash
      curl -X DELETE "http://localhost:8081/tasks/1"
     ```
   - Example Response:
     ```
      {
          "id": 1,
          "title": "Updated Task",
          "description": "This is an updated task"
      }
     ```

You can also find Swagger documentation of API's on the link `http://127.0.0.1:8081/docs#/`, after running the application.

### 3. Background Tasks with Celery and Email Notifications
The application uses Celery for handling background tasks, such as sending email notifications when a new task is created.

#### How It Works:
1. Task Creation and Notification:
   - When a new task is created via the `POST /tasks/` endpoint, an asynchronous Celery task (`send_email_task`) is triggered to send an email notification.
2. Celery Task Implementation:
   - The `send_email_task` function is defined in `app.celery_worker` and is decorated with `@celery_app.task`, making it a Celery task. This task is responsible for sending an email using the SendGrid API.
3. Email Notification:
   - When the task is created, the `send_email_task` function is called asynchronously, ensuring that the API request is not blocked by the time-consuming email-sending operation. This enhances the user experience by providing faster responses.
4. Running the Celery Worker:
   - The Celery worker is run as a separate service in Docker. It listens for tasks and executes them in the background.
5. Verifying Email Delivery:
   - To test the email notification feature, create a task via the `POST /tasks/` endpoint and check the inbox of the `SENDGRID_TO_EMAIL` address. You should receive an email notification about the new task.
     `Note: Sometimes the notification Email goes to Spam folder. Please check the spam folder.`

### 4. Optimizations Implemented
- Asynchronous Task Execution: By using Celery, the application can handle long-running tasks, like sending emails, in the background without blocking the main application thread.
- Efficient Resource Utilization: Redis is used as a message broker and result backend, providing fast and reliable messaging between the application and Celery worker.
- Containerization: Docker ensures that the environment is consistent across different machines, making it easier to develop, test, and deploy the application.

     
