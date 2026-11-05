import os
import smtplib
from email.message import EmailMessage
from pathlib import Path
from re import fullmatch


def send_invoice_email(
    recipient: str,
    invoice_number: str,
    attachment_path: str | Path,
) -> bool:
    """
    Send an invoice as an HTML email attachment.

    EMAIL_MODE=local prints a test confirmation without sending.
    EMAIL_MODE=smtp uses configured SMTP credentials.
    """

    if not isinstance(recipient, str):
        raise ValueError("Recipient email must be text.")

    recipient = recipient.strip()

    if not fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", recipient):
        raise ValueError("Enter a valid customer email address.")

    path = Path(attachment_path)

    if not path.is_file():
        raise FileNotFoundError("Invoice attachment does not exist.")

    mode = os.getenv("EMAIL_MODE", "local").strip().lower()

    if mode == "local":
        print(
            f"[LOCAL EMAIL TEST] Invoice {invoice_number} "
            f"would be sent to {recipient}."
        )
        return True

    if mode != "smtp":
        raise ValueError("EMAIL_MODE must be 'local' or 'smtp'.")

    host = os.getenv("SMTP_HOST")
    port = os.getenv("SMTP_PORT", "587")
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")
    sender = os.getenv("SMTP_SENDER", username or "")

    if not all([host, username, password, sender]):
        raise ValueError("SMTP configuration is incomplete.")

    try:
        port_number = int(port)
    except ValueError as exc:
        raise ValueError("SMTP_PORT must be a valid number.") from exc

    message = EmailMessage()
    message["Subject"] = f"Your PMS Invoice - {invoice_number}"
    message["From"] = sender
    message["To"] = recipient

    message.set_content(
        f"Thank you for shopping with us.\n"
        f"Your invoice number is {invoice_number}.\n"
        f"Please find your invoice attached."
    )

    message.add_attachment(
        path.read_bytes(),
        maintype="text",
        subtype="html",
        filename=path.name,
    )

    try:
        with smtplib.SMTP(host, port_number, timeout=15) as server:
            server.starttls()
            server.login(username, password)
            server.send_message(message)
    except (OSError, smtplib.SMTPException) as exc:
        raise RuntimeError(f"Invoice email delivery failed: {exc}") from exc

    return True