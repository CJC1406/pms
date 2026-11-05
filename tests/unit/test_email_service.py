
import smtplib

import pytest

from src.services.email_service import send_invoice_email


def test_local_email_mode_succeeds(tmp_path, monkeypatch, capsys):
    attachment = tmp_path / "invoice.html"
    attachment.write_text("<html>Invoice</html>", encoding="utf-8")

    monkeypatch.setenv("EMAIL_MODE", "local")

    result = send_invoice_email(
        "customer@example.com",
        "INV-001",
        attachment,
    )

    output = capsys.readouterr().out

    assert result is True
    assert "INV-001" in output
    assert "customer@example.com" in output


def test_invalid_email_address_is_rejected(tmp_path, monkeypatch):
    attachment = tmp_path / "invoice.html"
    attachment.write_text("<html>Invoice</html>", encoding="utf-8")

    monkeypatch.setenv("EMAIL_MODE", "local")

    with pytest.raises(ValueError, match="valid customer email"):
        send_invoice_email(
            "invalid-email",
            "INV-001",
            attachment,
        )


def test_missing_attachment_is_rejected(monkeypatch, tmp_path):
    monkeypatch.setenv("EMAIL_MODE", "local")

    missing_file = tmp_path / "missing.html"

    with pytest.raises(FileNotFoundError):
        send_invoice_email(
            "customer@example.com",
            "INV-001",
            missing_file,
        )


def test_invalid_email_mode_is_rejected(tmp_path, monkeypatch):
    attachment = tmp_path / "invoice.html"
    attachment.write_text("<html>Invoice</html>", encoding="utf-8")

    monkeypatch.setenv("EMAIL_MODE", "invalid")

    with pytest.raises(ValueError, match="EMAIL_MODE"):
        send_invoice_email(
            "customer@example.com",
            "INV-001",
            attachment,
        )


def test_smtp_requires_configuration(tmp_path, monkeypatch):
    attachment = tmp_path / "invoice.html"
    attachment.write_text("<html>Invoice</html>", encoding="utf-8")

    monkeypatch.setenv("EMAIL_MODE", "smtp")
    monkeypatch.delenv("SMTP_HOST", raising=False)
    monkeypatch.delenv("SMTP_USERNAME", raising=False)
    monkeypatch.delenv("SMTP_PASSWORD", raising=False)
    monkeypatch.delenv("SMTP_SENDER", raising=False)

    with pytest.raises(ValueError, match="SMTP configuration"):
        send_invoice_email(
            "customer@example.com",
            "INV-001",
            attachment,
        )


def test_smtp_email_is_sent_successfully(tmp_path, monkeypatch):
    attachment = tmp_path / "invoice.html"
    attachment.write_text("<html>Invoice</html>", encoding="utf-8")

    monkeypatch.setenv("EMAIL_MODE", "smtp")
    monkeypatch.setenv("SMTP_HOST", "smtp.example.com")
    monkeypatch.setenv("SMTP_PORT", "587")
    monkeypatch.setenv("SMTP_USERNAME", "sender@example.com")
    monkeypatch.setenv("SMTP_PASSWORD", "test-password")
    monkeypatch.setenv("SMTP_SENDER", "sender@example.com")

    sent_messages = []

    class FakeSMTP:
        def __init__(self, host, port, timeout):
            assert host == "smtp.example.com"
            assert port == 587
            assert timeout == 15

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            return False

        def starttls(self):
            pass

        def login(self, username, password):
            assert username == "sender@example.com"
            assert password == "test-password"

        def send_message(self, message):
            sent_messages.append(message)

    monkeypatch.setattr(
        "src.services.email_service.smtplib.SMTP",
        FakeSMTP,
    )

    result = send_invoice_email(
        "customer@example.com",
        "INV-001",
        attachment,
    )

    assert result is True
    assert len(sent_messages) == 1
    assert sent_messages[0]["To"] == "customer@example.com"
    assert "INV-001" in sent_messages[0]["Subject"]


def test_smtp_failure_is_reported(tmp_path, monkeypatch):
    attachment = tmp_path / "invoice.html"
    attachment.write_text("<html>Invoice</html>", encoding="utf-8")

    monkeypatch.setenv("EMAIL_MODE", "smtp")
    monkeypatch.setenv("SMTP_HOST", "smtp.example.com")
    monkeypatch.setenv("SMTP_PORT", "587")
    monkeypatch.setenv("SMTP_USERNAME", "sender@example.com")
    monkeypatch.setenv("SMTP_PASSWORD", "test-password")
    monkeypatch.setenv("SMTP_SENDER", "sender@example.com")

    class FailingSMTP:
        def __init__(self, host, port, timeout):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            return False

        def starttls(self):
            raise smtplib.SMTPException("Test SMTP failure")

    monkeypatch.setattr(
        "src.services.email_service.smtplib.SMTP",
        FailingSMTP,
    )

    with pytest.raises(RuntimeError, match="email delivery failed"):
        send_invoice_email(
            "customer@example.com",
            "INV-001",
            attachment,
        )
