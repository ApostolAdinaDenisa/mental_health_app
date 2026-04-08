# mental_health_app

MindWell is a Streamlit mental health companion app.

How to run:

1. Create a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run the app:

```powershell
streamlit run app.py
```

## Account and password reset

- New users must provide an email address at registration.
- On the Login tab, use `Forgot password? Reset by email`.
- The app sends a 6-digit reset code by email (valid for 10 minutes), then lets the user set a new password.

## Password reset by email (SMTP)

For the reset-password email to work, configure these values in Streamlit secrets
(`.streamlit/secrets.toml`) or as environment variables:

- `SMTP_HOST`
- `SMTP_PORT` (default: `587`)
- `SMTP_USER`
- `SMTP_PASSWORD`
- `SMTP_FROM`
- `SMTP_USE_TLS` (`true`/`false`, default: `true`)

Example `.streamlit/secrets.toml`:

```toml
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "your_email@gmail.com"
SMTP_PASSWORD = "your_app_password"
SMTP_FROM = "your_email@gmail.com"
SMTP_USE_TLS = true
```

## Phone reminders by SMS (Twilio)

To send reminders to phone numbers, configure these values in `.streamlit/secrets.toml`
or environment variables:

- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_FROM_NUMBER` (must be E.164 format, for example `+15551234567`)

Example:

```toml
TWILIO_ACCOUNT_SID = "your_twilio_sid"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_FROM_NUMBER = "+15551234567"
```

In the app, set your account phone in `Settings` using E.164 format
(for example `+40700111222`).
