import smtplib
import uuid
from datetime import datetime
from datetime import timezone
from email.message import EmailMessage

from app.core.logger import logger
from app.models import EmailTracking
from app.settings import config


class EmailService:
    @classmethod
    def send_email_smtp(cls, subject: str, body: str, to_emails: list[str]):
        smtp_server = config.SMTP_SERVER
        smtp_port = config.SMTP_PORT
        smtp_user = config.SMTP_SENDER

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = smtp_user
        msg["To"] = ", ".join(to_emails)
        msg.set_content(body)

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # server.starttls()  # not needed for mailhog
            # server.login(smtp_user, smtp_pass)  # not needed for Mailhog
            server.send_message(msg)

    @classmethod
    def send_email_to_users(cls, users: list[dict], subject: str, body: str, utm_source: str):
        batch_id = uuid.uuid4().hex
        user_emails = [user["email"] for user in users]
        status = "sent"

        try:
            cls.send_email_smtp(subject, body, user_emails)
        except Exception as e:
            status = "failed"
            logger.error(e)

        now = datetime.now(timezone.utc).isoformat()
        EmailTracking(
            PK=f"EMAIL#{batch_id}",
            SK="Tracking",
            batch_id=batch_id,
            emails=user_emails,
            status=status,
            utm_source=utm_source,
            created_at=now,
            updated_at=now,
        ).save()

        return {
            "batch_id": batch_id,
            "sent": len(users) if status == "sent" else 0,
            "failed": len(users) if status == "failed" else 0,
        }
