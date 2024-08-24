import os
from celery import Celery
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To

load_dotenv()

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")

celery_app = Celery(
    "worker",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND
)

celery_app.conf.update(task_serializer="json", accept_content=["json"], result_serializer="json")

from_email = os.environ.get('SENDGRID_FROM_EMAIL')
to_email = os.environ.get('SENDGRID_TO_EMAIL')
template_id = os.environ.get('SENDGRID_TEMPLATE_ID')

@celery_app.task
def send_email_task(task_title: str, task_description: str):
    # Simulate sending an email
    print(f"Sending email notification for task: {task_title}")
    message = Mail(
    from_email=(from_email, 'Task Manager'),
    to_emails=to_email)
    message.dynamic_template_data = {
     "title": task_title,
     "description": task_description
    }
    message.subject = 'New Task Added'
    message.template_id = template_id
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
