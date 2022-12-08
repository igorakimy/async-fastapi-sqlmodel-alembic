import ssl
import os
import smtplib
import logging
from jinja2 import Template
from typing import Optional, Dict, Any

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings


def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Optional[Dict[str, Any]] = None
) -> None:
    assert settings.EMAILS_ENABLED, "No provided configuration for email variables"
    if environment is None:
        environment = {}

    message = MIMEMultipart("alternative")
    message["Subject"] = subject_template
    message["From"] = settings.EMAILS_FROM_EMAIL
    message["To"] = email_to

    content = MIMEText(Template(html_template).render(**environment), "html")
    message.attach(content)

    context = ssl.create_default_context()

    if settings.SMTP_TLS:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            response = server.sendmail(
                settings.EMAILS_FROM_EMAIL,
                email_to,
                message.as_string())
    else:
        with smtplib.SMTP_SSL(settings.SMTP_HOST, 465, context=context) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            response = server.sendmail(
                settings.EMAILS_FROM_EMAIL,
                email_to,
                message.as_string())

    logging.info(f"Send email response: {response}")


def send_password_reset_mail(
    email_to: str,
    email: str,
    token: str
) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Восстановление пароля для пользователя {email}"
    path = os.path.join(os.path.dirname(__file__), '..')
    with open(path + settings.EMAILS_TEMPLATES_DIR + "/reset_password.html") as f:
        template_str = f.read()

    link = f"{settings.SERVER_HOST}/reset-password?token={token}"
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAILS_RESET_TOKEN_EXPIRE_HOURS,
            "link": link
        }
    )


