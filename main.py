from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from jinja2 import Template
import base64

def send_email_with_template(sender, to, subject, template_path, template_data):
    # Load the email template
    with open(template_path, 'r') as template_file:
        template_content = template_file.read()

    # Render the template with the provided data
    template = Template(template_content)
    rendered_template = template.render(**template_data)

    # Create the message with the rendered template
    message = create_message(sender, to, subject, rendered_template)

    # Send the message
    send_message(message)

def create_message(sender, to, subject, message_text):
    message = {
        'to': to,
        'from': sender,
        'subject': subject,
        'text': message_text
    }

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw_message}

def send_message(message):
    creds = Credentials.from_authorized_user_file('credentials.json')

    # If the credentials are expired or invalid, refresh them
    if creds.expired or not creds.valid:
        creds.refresh(Request())

    service = build('gmail', 'v1', credentials=creds)

    # Send the message using the Gmail API
    service.users().messages().send(userId='me', body=message).execute()

# Usage: Call the function with the necessary parameters
sender = 'your-email@gmail.com'
to = 'recipient-email@example.com'
subject = 'Hello from Google API'
template_path = 'email_template.html'
template_data = {
    'name': 'John Doe',
    'message': 'This is a sample email template'
}

send_email_with_template(sender, to, subject, template_path, template_data)
