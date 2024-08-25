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
- **CELERY_BROKER_URL**: The URL for your Redis instance (default: `redis://localhost:6379/0`).
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

Copy the provided .env file in the root folder (task-manager).

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
