import streamlit as st
import sqlite3
import datetime
import pandas as pd
import random
import numpy as np
import smtplib
import ssl
from collections import Counter
import time
import os
import secrets
import json
import importlib
import re
import hashlib
import io
import wave
import struct
import math
from email.message import EmailMessage

try:
    px = importlib.import_module("plotly.express")
except Exception:
    px = None

try:
    go = importlib.import_module("plotly.graph_objects")
except Exception:
    go = None

# ===============================
# CONFIG
# ===============================
st.set_page_config(
    page_title="SereneMind - Mental Health Companion",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Theme configurations
THEMES = {
    "Ocean": {
        "primary": "#0288d1",
        "secondary": "#00838f",
        "success": "#00897b",
        "warning": "#f57c00",
        "danger": "#d32f2f",
        "bg_gradient": "linear-gradient(135deg, #0288d1 0%, #00838f 100%)",
        "app_bg": "linear-gradient(135deg, #e0f7fa 0%, #b2dfdb 100%)",
        "text_primary": "#004d73",
    },
    "Forest": {
        "primary": "#388e3c",
        "secondary": "#558b2f",
        "success": "#689f38",
        "warning": "#f57f17",
        "danger": "#c62828",
        "bg_gradient": "linear-gradient(135deg, #388e3c 0%, #558b2f 100%)",
        "app_bg": "linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%)",
        "text_primary": "#1b5e20",
    },
    "Sunset": {
        "primary": "#e64a19",
        "secondary": "#ff6f00",
        "success": "#ffb300",
        "warning": "#ff6d00",
        "danger": "#d32f2f",
        "bg_gradient": "linear-gradient(135deg, #ff6f00 0%, #e64a19 100%)",
        "app_bg": "linear-gradient(135deg, #ffe0b2 0%, #ffccbc 100%)",
        "text_primary": "#bf360c",
    },
    "Purple": {
        "primary": "#6366f1",
        "secondary": "#ec4899",
        "success": "#10b981",
        "warning": "#f59e0b",
        "danger": "#ef4444",
        "bg_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "app_bg": "linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)",
        "text_primary": "#4f46e5",
    },
    "Lavender": {
        "primary": "#7c3aed",
        "secondary": "#a855f7",
        "success": "#10b981",
        "warning": "#f59e0b",
        "danger": "#ef4444",
        "bg_gradient": "linear-gradient(135deg, #7c3aed 0%, #d946ef 100%)",
        "app_bg": "linear-gradient(135deg, #f3e8ff 0%, #ede9fe 100%)",
        "text_primary": "#5b21b6",
    },
    "Pink Blossom": {
        "primary": "#d81b60",
        "secondary": "#f06292",
        "success": "#2e7d32",
        "warning": "#ef6c00",
        "danger": "#c62828",
        "bg_gradient": "linear-gradient(135deg, #f06292 0%, #d81b60 100%)",
        "app_bg": "linear-gradient(135deg, #fff0f6 0%, #ffe4ef 100%)",
        "text_primary": "#880e4f",
    },
    "Accessibility High Contrast": {
        "primary": "#ffff00",
        "secondary": "#00e5ff",
        "success": "#00ff66",
        "warning": "#ffea00",
        "danger": "#ff1744",
        "bg_gradient": "linear-gradient(135deg, #000000 0%, #111111 100%)",
        "app_bg": "linear-gradient(135deg, #000000 0%, #1a1a1a 100%)",
        "text_primary": "#ffffff",
        "accessibility": True,
    }
}

# Initialize theme
if "theme" not in st.session_state:
    st.session_state.theme = "Purple"

def apply_theme(theme_name):
    theme = THEMES.get(theme_name, THEMES["Purple"])
    is_accessibility = bool(theme.get("accessibility", False))
    accessibility_css = ""

    if is_accessibility:
        accessibility_css = """
    * {
        letter-spacing: 0.01em;
    }

    .stApp, body {
        color: #ffffff !important;
    }

    .stMarkdown, .stText, p, li, label, span, div {
        color: #ffffff !important;
        font-size: 1.08rem;
    }

    .stButton > button {
        color: #000000 !important;
        border: 2px solid #ffffff !important;
    }

    .stTextInput input,
    .stTextArea textarea,
    .stSelectbox div[data-baseweb="select"],
    .stDateInput input,
    .stTimeInput input,
    .stNumberInput input {
        background: #000000 !important;
        color: #ffffff !important;
        border: 2px solid #00e5ff !important;
    }

    *:focus {
        outline: 3px solid #ffff00 !important;
        outline-offset: 2px !important;
    }
        """

    st.markdown(f"""
<style>
    :root {{
        --primary: {theme['primary']};
        --secondary: {theme['secondary']};
        --success: {theme['success']};
        --warning: {theme['warning']};
        --danger: {theme['danger']};
    }}
    
    body {{
        background: {theme['bg_gradient']};
        color: {theme['text_primary']};
    }}
    
    .stApp {{
        background: {theme['app_bg']};
    }}
    
    .main {{
        padding: 2.5rem 2rem;
    }}
    
    .stButton > button {{
        background: linear-gradient(90deg, {theme['primary']} 0%, {theme['secondary']} 100%);
        color: white;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 500;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        font-size: 0.95rem;
    }}
    
    .stButton > button:hover {{
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        transform: translateY(-1px);
    }}
    
    h1, h2, h3 {{
        color: {theme['primary']};
        font-weight: 600;
        letter-spacing: -0.01em;
    }}
    
    h1 {{
        font-size: 2.2rem;
        margin-bottom: 0.5rem;
    }}
    
    h2 {{
        font-size: 1.6rem;
    }}
    
    .metric-card {{
        background: white;
        padding: 24px;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 2px 6px rgba(0,0,0,0.04);
        margin: 12px 0;
        border: 1px solid rgba(0,0,0,0.05);
    }}
    
    .success-box {{
        background: rgba(16,185,129,0.04);
        border-left: 3px solid {theme['success']};
        padding: 16px;
        border-radius: 8px;
        font-size: 0.95rem;
    }}
    
    .info-box {{
        background: rgba(59,130,246,0.04);
        border-left: 3px solid {theme['primary']};
        padding: 16px;
        border-radius: 8px;
        font-size: 0.95rem;
    }}
    
    .warning-box {{
        background: rgba(245,158,11,0.04);
        border-left: 3px solid {theme['warning']};
        padding: 16px;
        border-radius: 8px;
        font-size: 0.95rem;
    }}

    {accessibility_css}
</style>
""", unsafe_allow_html=True)

# Apply theme at every page load
apply_theme(st.session_state.theme)

# ===============================
# DATABASE
# ===============================
conn = sqlite3.connect("serenemind.db", check_same_thread=False)
c = conn.cursor()

# Users table
c.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT PRIMARY KEY,
    password TEXT,
    created_date TEXT
)
""")

def ensure_users_schema_columns():
    c.execute("PRAGMA table_info(users)")
    existing_columns = {col[1] for col in c.fetchall()}

    if "phone" not in existing_columns:
        c.execute("ALTER TABLE users ADD COLUMN phone TEXT")

    c.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_users_phone ON users(phone)")

ensure_users_schema_columns()

# Mood tracking with more details
c.execute("""
CREATE TABLE IF NOT EXISTS mood_entries(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    mood TEXT,
    intensity INTEGER,
    triggers TEXT,
    notes TEXT,
    date TEXT,
    timestamp TEXT
)
""")

# Gratitude journal
c.execute("""
CREATE TABLE IF NOT EXISTS gratitude(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    entry TEXT,
    date TEXT,
    timestamp TEXT
)
""")

# Breathing sessions
c.execute("""
CREATE TABLE IF NOT EXISTS breathing_sessions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    duration INTEGER,
    cycles INTEGER,
    date TEXT,
    timestamp TEXT
)
""")

# Sleep tracking
c.execute("""
CREATE TABLE IF NOT EXISTS sleep_tracking(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    hours REAL,
    quality TEXT,
    notes TEXT,
    date TEXT,
    timestamp TEXT
)
""")

# Goals
c.execute("""
CREATE TABLE IF NOT EXISTS goals(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    goal TEXT,
    category TEXT,
    status TEXT,
    created_date TEXT,
    deadline TEXT
)
""")

def ensure_goals_schema_columns():
    c.execute("PRAGMA table_info(goals)")
    existing_columns = {col[1] for col in c.fetchall()}

    if "progress" not in existing_columns:
        c.execute("ALTER TABLE goals ADD COLUMN progress INTEGER DEFAULT 0")
    if "milestones" not in existing_columns:
        c.execute("ALTER TABLE goals ADD COLUMN milestones TEXT")

ensure_goals_schema_columns()

# Meditation sessions
c.execute("""
CREATE TABLE IF NOT EXISTS meditation_sessions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    duration INTEGER,
    type TEXT,
    date TEXT,
    timestamp TEXT
)
""")

# Activity sessions (games & psychology exercises)
c.execute("""
CREATE TABLE IF NOT EXISTS activity_sessions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    activity_name TEXT,
    details TEXT,
    duration_minutes INTEGER,
    date TEXT,
    timestamp TEXT
)
""")

# Daily habits
c.execute("""
CREATE TABLE IF NOT EXISTS habit_entries(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    habit_name TEXT,
    completed INTEGER,
    note TEXT,
    date TEXT,
    timestamp TEXT
)
""")

# Coping / safety plan
c.execute("""
CREATE TABLE IF NOT EXISTS coping_plans(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    warning_signs TEXT,
    coping_steps TEXT,
    support_contacts TEXT,
    safe_places TEXT,
    professional_help TEXT,
    updated_at TEXT
)
""")

# Smart reminders
c.execute("""
CREATE TABLE IF NOT EXISTS reminders(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    reminder_name TEXT,
    channel TEXT,
    hour INTEGER,
    minute INTEGER,
    active INTEGER,
    last_sent_date TEXT,
    created_at TEXT
)
""")

# Therapist sharing history
c.execute("""
CREATE TABLE IF NOT EXISTS shared_reports(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    therapist_email TEXT,
    subject TEXT,
    notes TEXT,
    payload_json TEXT,
    shared_at TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS notification_logs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    channel TEXT,
    recipient TEXT,
    subject TEXT,
    body TEXT,
    status TEXT,
    details TEXT,
    created_at TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS in_app_alarms(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    reminder_name TEXT,
    message TEXT,
    triggered_at TEXT,
    acknowledged INTEGER DEFAULT 0
)
""")

conn.commit()

# ===============================
# DATABASE FUNCTIONS
# ===============================
def register(username, password, phone):
    try:
        date = str(datetime.date.today())
        phone_clean = normalize_phone(phone)
        c.execute(
            "INSERT INTO users (username, password, phone, created_date) VALUES (?,?,?,?)",
            (username, password, phone_clean, date)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def login(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    return c.fetchone()

def _as_bool(value, default=True):
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    return str(value).strip().lower() in ["1", "true", "yes", "on"]

def get_secret_or_env(key, default_value=""):
    try:
        return st.secrets[key]
    except Exception:
        return os.getenv(key, default_value)

def _looks_like_placeholder(value):
    lowered = str(value).strip().lower()
    if not lowered:
        return False
    placeholder_tokens = ["paste_", "your_email", "your_app_password", "example", "changeme", "placeholder"]
    return any(token in lowered for token in placeholder_tokens)

def _get_smtp_config():
    host = str(get_secret_or_env("SMTP_HOST", "")).strip()
    port_raw = str(get_secret_or_env("SMTP_PORT", "587")).strip()
    user = str(get_secret_or_env("SMTP_USER", "")).strip()
    password = str(get_secret_or_env("SMTP_PASSWORD", "")).strip()
    sender = str(get_secret_or_env("SMTP_FROM", user)).strip()
    use_tls = _as_bool(get_secret_or_env("SMTP_USE_TLS", True), True)

    try:
        port = int(port_raw)
    except Exception:
        port = 587

    return {
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "from": sender,
        "use_tls": use_tls,
    }

def validate_smtp_config():
    cfg = _get_smtp_config()
    issues = []

    if not cfg["host"]:
        issues.append("SMTP_HOST is missing")
    if not cfg["port"]:
        issues.append("SMTP_PORT is missing")
    if not cfg["user"]:
        issues.append("SMTP_USER is missing")
    if not cfg["password"]:
        issues.append("SMTP_PASSWORD is missing")
    if not cfg["from"]:
        issues.append("SMTP_FROM is missing")

    for key in ["host", "user", "password", "from"]:
        if _looks_like_placeholder(cfg[key]):
            issues.append(f"SMTP_{key.upper()} looks like a placeholder")

    return issues

def send_email_notification(recipient, subject, body):
    cfg = _get_smtp_config()
    config_issues = validate_smtp_config()
    if config_issues:
        return False, "; ".join(config_issues)

    if not recipient or "@" not in recipient:
        return False, "Recipient email is invalid"

    try:
        msg = EmailMessage()
        msg["From"] = cfg["from"]
        msg["To"] = recipient.strip()
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP(cfg["host"], cfg["port"], timeout=20) as smtp:
            smtp.ehlo()
            if cfg["use_tls"]:
                smtp.starttls(context=ssl.create_default_context())
                smtp.ehlo()
            smtp.login(cfg["user"], cfg["password"])
            smtp.send_message(msg)
        return True, "Email sent"
    except Exception as exc:
        return False, str(exc)

def normalize_phone(phone):
    cleaned = re.sub(r"[^\d+]", "", str(phone).strip())
    if cleaned.startswith("00"):
        cleaned = "+" + cleaned[2:]
    return cleaned

def extract_phone_numbers(text):
    if not text:
        return []

    # Extract potential phone strings from free text and normalize them.
    raw_matches = re.findall(r"(?:\+|00)?\d[\d\s().-]{6,}\d", str(text))
    normalized = []
    for raw in raw_matches:
        phone = normalize_phone(raw)
        if len(phone.replace("+", "")) >= 8:
            normalized.append(phone)

    # Keep order while removing duplicates.
    unique_numbers = []
    seen = set()
    for phone in normalized:
        if phone not in seen:
            seen.add(phone)
            unique_numbers.append(phone)
    return unique_numbers



def save_shared_report(user, therapist_email, subject, notes, payload):
    shared_at = str(datetime.datetime.now())
    c.execute(
        "INSERT INTO shared_reports (username, therapist_email, subject, notes, payload_json, shared_at) VALUES (?,?,?,?,?,?)",
        (user, therapist_email.strip().lower(), subject, notes, json.dumps(payload, ensure_ascii=False), shared_at)
    )
    conn.commit()

def save_notification_log(username, channel, recipient, subject, body, status, details=""):
    created_at = str(datetime.datetime.now())
    c.execute(
        "INSERT INTO notification_logs (username, channel, recipient, subject, body, status, details, created_at) VALUES (?,?,?,?,?,?,?,?)",
        (username, channel, recipient, subject, body, status, details, created_at),
    )
    conn.commit()

def get_notification_logs(user, limit=50):
    c.execute(
        "SELECT id, channel, recipient, subject, status, details, created_at FROM notification_logs WHERE username=? ORDER BY id DESC LIMIT ?",
        (user, int(limit)),
    )
    return c.fetchall()

def save_in_app_alarm(user, reminder_name, message):
    triggered_at = str(datetime.datetime.now())
    c.execute(
        "INSERT INTO in_app_alarms (username, reminder_name, message, triggered_at, acknowledged) VALUES (?,?,?,?,0)",
        (user, reminder_name, message, triggered_at),
    )
    conn.commit()

def get_unacknowledged_in_app_alarms(user, limit=20):
    c.execute(
        "SELECT id, reminder_name, message, triggered_at FROM in_app_alarms WHERE username=? AND acknowledged=0 ORDER BY id DESC LIMIT ?",
        (user, int(limit)),
    )
    return c.fetchall()

def acknowledge_in_app_alarms(user):
    c.execute("UPDATE in_app_alarms SET acknowledged=1 WHERE username=? AND acknowledged=0", (user,))
    conn.commit()

def generate_alarm_sound_wav(duration_ms=700, frequency=880, volume=0.35, sample_rate=22050):
    frame_count = int(sample_rate * (duration_ms / 1000.0))
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        for i in range(frame_count):
            # Small fade-in/fade-out to avoid click artifacts.
            envelope = min(1.0, i / (sample_rate * 0.03), (frame_count - i) / (sample_rate * 0.03))
            sample = volume * envelope * math.sin(2 * math.pi * frequency * (i / sample_rate))
            wav_file.writeframesraw(struct.pack("<h", int(sample * 32767)))
    return buffer.getvalue()

def get_shared_reports(user):
    c.execute("SELECT * FROM shared_reports WHERE username=? ORDER BY shared_at DESC", (user,))
    return c.fetchall()

def upsert_reminder(user, reminder_name, channel, hour, minute, active):
    now_str = str(datetime.datetime.now())
    c.execute(
        "SELECT id FROM reminders WHERE username=? AND reminder_name=?",
        (user, reminder_name)
    )
    row = c.fetchone()
    if row:
        c.execute(
            "UPDATE reminders SET channel=?, hour=?, minute=?, active=? WHERE id=?",
            (channel, hour, minute, 1 if active else 0, row[0])
        )
    else:
        c.execute(
            "INSERT INTO reminders (username, reminder_name, channel, hour, minute, active, last_sent_date, created_at) VALUES (?,?,?,?,?,?,?,?)",
            (user, reminder_name, channel, hour, minute, 1 if active else 0, None, now_str)
        )
    conn.commit()

def get_reminders(user):
    c.execute("SELECT * FROM reminders WHERE username=? ORDER BY reminder_name ASC", (user,))
    return c.fetchall()

def process_due_reminders(user):
    # Email and SMS reminders removed; in-app alarms only
    pass

def get_user_phone(username):
    c.execute("SELECT phone FROM users WHERE username=?", (username,))
    row = c.fetchone()
    return row[0] if row and row[0] else ""

def save_mood(user, mood, intensity, triggers, notes):
    date = str(datetime.date.today())
    timestamp = str(datetime.datetime.now())
    c.execute(
        "INSERT INTO mood_entries (username, mood, intensity, triggers, notes, date, timestamp) VALUES (?,?,?,?,?,?,?)",
        (user, mood, intensity, triggers, notes, date, timestamp)
    )
    conn.commit()

def get_mood_history(user, days=30):
    date_limit = datetime.date.today() - datetime.timedelta(days=days)
    c.execute(
        "SELECT * FROM mood_entries WHERE username=? AND date>=? ORDER BY date DESC",
        (user, str(date_limit))
    )
    return c.fetchall()

def save_gratitude(user, entry):
    date = str(datetime.date.today())
    timestamp = str(datetime.datetime.now())
    c.execute(
        "INSERT INTO gratitude (username, entry, date, timestamp) VALUES (?,?,?,?)",
        (user, entry, date, timestamp)
    )
    conn.commit()

def get_gratitude(user):
    c.execute("SELECT * FROM gratitude WHERE username=? ORDER BY date DESC LIMIT 20", (user,))
    return c.fetchall()

def save_breathing(user, duration, cycles):
    date = str(datetime.date.today())
    timestamp = str(datetime.datetime.now())
    c.execute(
        "INSERT INTO breathing_sessions (username, duration, cycles, date, timestamp) VALUES (?,?,?,?,?)",
        (user, duration, cycles, date, timestamp)
    )
    conn.commit()

def save_sleep(user, hours, quality, notes):
    date = str(datetime.date.today())
    timestamp = str(datetime.datetime.now())
    c.execute(
        "INSERT INTO sleep_tracking (username, hours, quality, notes, date, timestamp) VALUES (?,?,?,?,?,?)",
        (user, hours, quality, notes, date, timestamp)
    )
    conn.commit()

def get_sleep_history(user, days=30):
    date_limit = datetime.date.today() - datetime.timedelta(days=days)
    c.execute(
        "SELECT * FROM sleep_tracking WHERE username=? AND date>=? ORDER BY date DESC",
        (user, str(date_limit))
    )
    return c.fetchall()

def save_meditation(user, duration, meditation_type):
    date = str(datetime.date.today())
    timestamp = str(datetime.datetime.now())
    c.execute(
        "INSERT INTO meditation_sessions (username, duration, type, date, timestamp) VALUES (?,?,?,?,?)",
        (user, duration, meditation_type, date, timestamp)
    )
    conn.commit()

def get_meditation_history(user, days=30):
    date_limit = datetime.date.today() - datetime.timedelta(days=days)
    c.execute(
        "SELECT * FROM meditation_sessions WHERE username=? AND date>=? ORDER BY date DESC",
        (user, str(date_limit))
    )
    return c.fetchall()

def save_activity_session(user, activity_name, details="", duration_minutes=0):
    date = str(datetime.date.today())
    timestamp = str(datetime.datetime.now())
    c.execute(
        "INSERT INTO activity_sessions (username, activity_name, details, duration_minutes, date, timestamp) VALUES (?,?,?,?,?,?)",
        (user, activity_name, details, duration_minutes, date, timestamp)
    )
    conn.commit()

def get_activity_history(user, days=30):
    date_limit = datetime.date.today() - datetime.timedelta(days=days)
    c.execute(
        "SELECT * FROM activity_sessions WHERE username=? AND date>=? ORDER BY timestamp DESC LIMIT 50",
        (user, str(date_limit))
    )
    return c.fetchall()

def save_habit_entry(user, habit_name, completed, note=""):
    date = str(datetime.date.today())
    timestamp = str(datetime.datetime.now())
    c.execute(
        "INSERT INTO habit_entries (username, habit_name, completed, note, date, timestamp) VALUES (?,?,?,?,?,?)",
        (user, habit_name, 1 if completed else 0, note, date, timestamp)
    )
    conn.commit()

def get_habit_history(user, days=30):
    date_limit = datetime.date.today() - datetime.timedelta(days=days)
    c.execute(
        "SELECT * FROM habit_entries WHERE username=? AND date>=? ORDER BY date DESC, timestamp DESC",
        (user, str(date_limit))
    )
    return c.fetchall()

def get_habit_streak(user):
    c.execute(
        "SELECT DISTINCT date FROM habit_entries WHERE username=? AND completed=1 ORDER BY date DESC",
        (user,)
    )
    rows = c.fetchall()
    if not rows:
        return 0

    completed_dates = {datetime.date.fromisoformat(row[0]) for row in rows}
    streak = 0
    current_day = datetime.date.today()

    while current_day in completed_dates:
        streak += 1
        current_day -= datetime.timedelta(days=1)

    return streak


MOOD_SCORE_MAP = {
    "Very Happy": 95,
    "Happy": 82,
    "Calm": 78,
    "Energetic": 80,
    "Neutral": 60,
    "Tired": 45,
    "Anxious": 35,
    "Stressed": 30,
    "Sad": 32,
    "Very Sad": 20,
}

SLEEP_QUALITY_MAP = {
    "Excellent": 95,
    "Good": 80,
    "Fair": 60,
    "Poor": 35,
}
SLEEP_QUALITY_ORDER = ["Poor", "Fair", "Good", "Excellent"]

LOW_MOOD_SET = {"Anxious", "Stressed", "Sad", "Very Sad"}


def _build_df(rows, columns):
    df = pd.DataFrame(rows, columns=columns) if rows else pd.DataFrame(columns=columns)
    if "Date" in df.columns and not df.empty:
        df["DateDT"] = pd.to_datetime(df["Date"], errors="coerce")
    return df


def _prepare_sleep_dashboard_df(sleep_df):
    if sleep_df is None or sleep_df.empty:
        return pd.DataFrame(columns=["Date", "DateDT", "Hours", "Quality", "QualityScore", "Notes"])

    df = sleep_df.copy()
    if "DateDT" not in df.columns:
        df["DateDT"] = pd.to_datetime(df["Date"], errors="coerce")

    df = df.dropna(subset=["DateDT"]).copy()
    if df.empty:
        return pd.DataFrame(columns=["Date", "DateDT", "Hours", "Quality", "QualityScore", "Notes"])

    df["QualityScore"] = df["Quality"].map(SLEEP_QUALITY_MAP).fillna(55).astype(float)
    df["Date"] = df["DateDT"].dt.strftime("%Y-%m-%d")
    df["Weekday"] = df["DateDT"].dt.day_name()
    df["Week"] = df["DateDT"].dt.strftime("%Y-W%W")
    return df.sort_values("DateDT")


def _sleep_dashboard_theme(accent_color):
    return {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(255,255,255,0.04)",
        "font": {"color": "#e5e7eb", "size": 12},
        "xaxis": {"showgrid": False, "zeroline": False},
        "yaxis": {"gridcolor": "rgba(148,163,184,0.22)", "zeroline": False},
        "hoverlabel": {"bgcolor": "#111827", "font": {"color": "#f9fafb"}},
        "accent": accent_color,
    }


def _render_sleep_kpi_cards(avg_hours, nights_target, target_ratio, avg_quality_score, label_text):
    st.markdown(
        f"""
        <div style=\"display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin:8px 0 16px 0;\">
            <div style=\"background:linear-gradient(135deg,#fff9fb,#ffe4ec);padding:18px;border-radius:12px;border:1px solid rgba(244,114,182,0.16);box-shadow:0 1px 3px rgba(0,0,0,0.04);\">
                <div style=\"color:#64748b;font-size:11px;font-weight:500;letter-spacing:0.02em;text-transform:uppercase;\">Average Sleep</div>
                <div style=\"color:#881337;font-size:28px;font-weight:600;line-height:1.2;margin:6px 0;\">{avg_hours:.1f}h</div>
                <div style=\"color:#be185d;font-size:11px;font-weight:500;\">{label_text}</div>
            </div>
            <div style=\"background:linear-gradient(135deg,#fffbf4,#ffedd5);padding:18px;border-radius:12px;border:1px solid rgba(251,146,60,0.16);box-shadow:0 1px 3px rgba(0,0,0,0.04);\">
                <div style=\"color:#64748b;font-size:11px;font-weight:500;letter-spacing:0.02em;text-transform:uppercase;\">Nights Above Target</div>
                <div style=\"color:#7c2d12;font-size:28px;font-weight:600;line-height:1.2;margin:6px 0;\">{nights_target}</div>
                <div style=\"color:#b45309;font-size:11px;font-weight:500;\">{target_ratio}% reached 7h+</div>
            </div>
            <div style=\"background:linear-gradient(135deg,#fdf8fb,#fce7f3);padding:18px;border-radius:12px;border:1px solid rgba(236,72,153,0.16);box-shadow:0 1px 3px rgba(0,0,0,0.04);\">
                <div style=\"color:#64748b;font-size:11px;font-weight:500;letter-spacing:0.02em;text-transform:uppercase;\">Sleep Quality Score</div>
                <div style=\"color:#831843;font-size:28px;font-weight:600;line-height:1.2;margin:6px 0;\">{avg_quality_score}/100</div>
                <div style=\"color:#db2777;font-size:11px;font-weight:500;\">Weighted by nightly quality</div>
            </div>
            <div style=\"background:linear-gradient(135deg,#fff9f9,#ffe4e6);padding:18px;border-radius:12px;border:1px solid rgba(244,63,94,0.16);box-shadow:0 1px 3px rgba(0,0,0,0.04);\">
                <div style=\"color:#64748b;font-size:11px;font-weight:500;letter-spacing:0.02em;text-transform:uppercase;\">Consistency</div>
                <div style=\"color:#9f1239;font-size:28px;font-weight:600;line-height:1.2;margin:6px 0;\">{max(0, min(100, int(100 - abs(avg_hours - 7.5) * 18)))}%</div>
                <div style=\"color:#e11d48;font-size:11px;font-weight:500;\">Closer to a stable sleep window</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _sleep_score_gauge(score, accent_color):
    if go is None:
        return None

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=max(0, min(100, score)),
            number={"suffix": "/100", "font": {"size": 28, "color": "#f8fafc"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#94a3b8"},
                "bar": {"color": accent_color, "thickness": 0.35},
                "bgcolor": "rgba(255,255,255,0.02)",
                "steps": [
                    {"range": [0, 40], "color": "rgba(239,68,68,0.32)"},
                    {"range": [40, 70], "color": "rgba(245,158,11,0.30)"},
                    {"range": [70, 100], "color": "rgba(16,185,129,0.30)"},
                ],
                "threshold": {"line": {"color": "#f8fafc", "width": 3}, "thickness": 0.7, "value": 75},
            },
            title={"text": "Sleep Recovery Index", "font": {"size": 15, "color": "#e2e8f0"}},
        )
    )
    fig.update_layout(height=300, margin=dict(l=16, r=16, t=42, b=16), paper_bgcolor="rgba(0,0,0,0)")
    return fig


def _sleep_hours_figure(sleep_df, accent_color):
    if px is None:
        return None

    theme = _sleep_dashboard_theme(accent_color)
    daily = sleep_df.groupby("DateDT", as_index=False)["Hours"].mean()
    fig = px.line(
        daily,
        x="DateDT",
        y="Hours",
        markers=True,
        labels={"DateDT": "Date", "Hours": "Sleep hours"},
        color_discrete_sequence=[accent_color],
    )
    fig.update_traces(line={"shape": "spline", "width": 3}, marker={"size": 8}, fill="tozeroy", fillcolor="rgba(59,130,246,0.12)")
    fig.add_hline(y=7, line_dash="dot", line_color="#f87171", annotation_text="Target: 7h", annotation_font_color="#fecaca")
    fig.add_hrect(y0=7, y1=9, fillcolor="rgba(16,185,129,0.08)", line_width=0)
    fig.update_layout(
        height=340,
        margin=dict(l=10, r=10, t=18, b=10),
        xaxis_title=None,
        yaxis_title="Hours",
        hovermode="x unified",
        paper_bgcolor=theme["paper_bgcolor"],
        plot_bgcolor=theme["plot_bgcolor"],
        font=theme["font"],
    )
    fig.update_xaxes(showgrid=theme["xaxis"]["showgrid"])
    fig.update_yaxes(gridcolor=theme["yaxis"]["gridcolor"])
    return fig


def _sleep_quality_figure(sleep_df):
    if px is None:
        return None

    quality_counts = sleep_df["Quality"].value_counts().reindex(SLEEP_QUALITY_ORDER, fill_value=0).reset_index()
    quality_counts.columns = ["Quality", "Nights"]

    fig = px.pie(
        quality_counts,
        names="Quality",
        values="Nights",
        color="Quality",
        category_orders={"Quality": SLEEP_QUALITY_ORDER},
        color_discrete_map={
            "Poor": "#ef4444",
            "Fair": "#f59e0b",
            "Good": "#3b82f6",
            "Excellent": "#10b981",
        },
        hole=0.58,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label", pull=[0.06, 0.02, 0.02, 0.02])
    fig.update_layout(
        height=340,
        margin=dict(l=10, r=10, t=18, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#e5e7eb", "size": 12},
        legend={"orientation": "h", "y": -0.12, "x": 0.05},
    )
    return fig


def _sleep_consistency_figure(sleep_df):
    if px is None:
        return None

    theme = _sleep_dashboard_theme("#38bdf8")
    fig = px.scatter(
        sleep_df,
        x="DateDT",
        y="Hours",
        color="Quality",
        size="QualityScore",
        size_max=18,
        category_orders={"Quality": SLEEP_QUALITY_ORDER},
        color_discrete_map={
            "Poor": "#ef4444",
            "Fair": "#f59e0b",
            "Good": "#3b82f6",
            "Excellent": "#10b981",
        },
        labels={"DateDT": "Date", "Hours": "Sleep hours", "Quality": "Sleep quality"},
        hover_data={"Date": True, "Hours": ":.1f", "Quality": True, "QualityScore": False},
    )
    fig.add_hline(y=7, line_dash="dot", line_color="#f87171")
    fig.update_traces(marker={"line": {"width": 1, "color": "rgba(255,255,255,0.35)"}, "opacity": 0.88})
    fig.update_layout(
        height=360,
        margin=dict(l=10, r=10, t=18, b=10),
        xaxis_title=None,
        yaxis_title="Hours",
        hovermode="closest",
        paper_bgcolor=theme["paper_bgcolor"],
        plot_bgcolor=theme["plot_bgcolor"],
        font=theme["font"],
    )
    fig.update_xaxes(showgrid=theme["xaxis"]["showgrid"])
    fig.update_yaxes(gridcolor=theme["yaxis"]["gridcolor"])
    return fig


def _sleep_heatmap_figure(sleep_df):
    if px is None:
        return None

    calendar = sleep_df.copy()
    if calendar.empty:
        return None

    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    heat_df = (
        calendar.groupby(["Week", "Weekday"], as_index=False)["Hours"].mean()
        .pivot(index="Weekday", columns="Week", values="Hours")
        .reindex(weekday_order)
    )

    fig = px.imshow(
        heat_df,
        labels={"x": "Week", "y": "Weekday", "color": "Hours"},
        color_continuous_scale=["#1e293b", "#2563eb", "#06b6d4", "#22c55e"],
        aspect="auto",
    )
    fig.update_layout(
        height=320,
        margin=dict(l=10, r=10, t=18, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#e5e7eb", "size": 12},
    )
    fig.update_coloraxes(colorbar_title="Hours")
    return fig


def _mood_dashboard_figure(mood_df, accent_color):
    if px is None or mood_df is None or mood_df.empty:
        return None

    mood_daily = mood_df.groupby("Date", as_index=False)["Intensity"].mean().sort_values("Date")
    fig = px.area(
        mood_daily,
        x="Date",
        y="Intensity",
        labels={"Date": "Date", "Intensity": "Mood intensity"},
        color_discrete_sequence=[accent_color],
    )
    fig.update_traces(line={"shape": "spline", "width": 3}, fillcolor="rgba(99,102,241,0.18)")
    fig.update_layout(
        height=320,
        margin=dict(l=10, r=10, t=16, b=10),
        hovermode="x unified",
        yaxis_title="Intensity",
        xaxis_title=None,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.04)",
        font={"color": "#e5e7eb", "size": 12},
    )
    fig.update_yaxes(gridcolor="rgba(148,163,184,0.22)")
    return fig


def _wellbeing_radar_figure(scores):
    if go is None:
        return None

    categories = ["Mood", "Mood Stability", "Sleep Quality", "Sleep Hours", "Meditation"]
    mood_stability = max(0, 100 - int(scores.get("intensity_score", 0)))
    values = [
        int(scores.get("mood_score", 0)),
        mood_stability,
        int(scores.get("sleep_score", 0)),
        int(scores.get("sleep_hours_score", 0)),
        int(scores.get("meditation_score", 0)),
    ]

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill="toself",
            line={"color": "#38bdf8", "width": 2.5},
            fillcolor="rgba(56,189,248,0.22)",
            name="Current",
        )
    )
    fig.update_layout(
        polar={
            "radialaxis": {"visible": True, "range": [0, 100], "gridcolor": "rgba(148,163,184,0.2)"},
            "angularaxis": {"gridcolor": "rgba(148,163,184,0.1)"},
            "bgcolor": "rgba(0,0,0,0)",
        },
        showlegend=False,
        height=320,
        margin=dict(l=12, r=12, t=18, b=14),
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "#e5e7eb", "size": 12},
    )
    return fig


def _render_dashboard_hero(user, wellbeing_score, tracking_consistency):
    tone = "Strong momentum"
    tone_color = "#22c55e"
    if wellbeing_score < 55:
        tone = "Stabilization needed"
        tone_color = "#ef4444"
    elif wellbeing_score < 75:
        tone = "Build consistency"
        tone_color = "#f59e0b"

    st.markdown(
        f"""
        <div style=\"background:linear-gradient(120deg,#fff9fb,#ffe4ec 40%,#fff3f8);padding:20px;border-radius:12px;border:1px solid rgba(244,114,182,0.14);margin-bottom:16px;box-shadow:0 1px 3px rgba(0,0,0,0.04);\">
            <div style=\"display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap;\">
                <div>
                    <div style=\"color:#be185d;font-size:11px;font-weight:500;letter-spacing:0.02em;text-transform:uppercase;\">Overview for {user}</div>
                    <div style=\"color:#831843;font-size:22px;font-weight:600;line-height:1.3;margin:4px 0 6px 0;\">Mental Wellbeing Command Center</div>
                    <div style=\"color:#be185d;font-size:13px;font-weight:400;\">Consistency today shapes resilience tomorrow.</div>
                </div>
                <div style=\"display:flex;gap:8px;flex-wrap:wrap;\">
                    <span style=\"background:rgba(244,114,182,0.08);border:1px solid rgba(244,114,182,0.24);color:#881337;padding:7px 12px;border-radius:8px;font-size:12px;font-weight:500;\">Wellbeing: {wellbeing_score}/100</span>
                    <span style=\"background:rgba(244,114,182,0.06);border:1px solid rgba(244,114,182,0.20);color:#9d174d;padding:7px 12px;border-radius:8px;font-size:12px;font-weight:500;\">Tracking: {tracking_consistency}%</span>
                    <span style=\"background:rgba(255,255,255,0.5);border:1px solid {tone_color};color:{tone_color};padding:7px 12px;border-radius:8px;font-size:12px;font-weight:500;\">{tone}</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_report_header_card(user, report_days, scores, metrics):
    st.markdown(
        f"""
        <div style=\"background:linear-gradient(125deg,#fff9fb,#ffe4ec 55%,#fff7fb);padding:20px;border-radius:12px;border:1px solid rgba(244,114,182,0.14);margin-bottom:16px;box-shadow:0 1px 3px rgba(0,0,0,0.04);\">
            <div style=\"display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap;\">
                <div>
                    <div style=\"color:#be185d;font-size:11px;font-weight:500;letter-spacing:0.02em;text-transform:uppercase;\">Clinical Summary</div>
                    <div style=\"color:#831843;font-size:20px;font-weight:600;line-height:1.3;margin:4px 0 6px 0;\">Wellbeing Report for {user}</div>
                    <div style=\"color:#9d174d;font-size:13px;font-weight:400;\">Window: last {report_days} days • Generated now</div>
                </div>
                <div style=\"display:flex;gap:8px;flex-wrap:wrap;\">
                    <span style=\"background:rgba(244,114,182,0.08);border:1px solid rgba(244,114,182,0.24);color:#881337;padding:7px 12px;border-radius:8px;font-size:12px;font-weight:500;\">Score {scores['wellbeing_score']}/100</span>
                    <span style=\"background:rgba(244,114,182,0.06);border:1px solid rgba(244,114,182,0.20);color:#9d174d;padding:7px 12px;border-radius:8px;font-size:12px;font-weight:500;\">Sleep {metrics['avg_sleep']:.1f}h</span>
                    <span style=\"background:rgba(244,63,94,0.08);border:1px solid rgba(244,63,94,0.22);color:#881337;padding:7px 12px;border-radius:8px;font-size:12px;font-weight:500;\">Habits {metrics['habit_completion_rate']}%</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def build_wellbeing_snapshot(user, report_days=30):
    history = get_mood_history(user, report_days)
    sleep_data = get_sleep_history(user, report_days)
    meditation_data = get_meditation_history(user, report_days)
    habit_data = get_habit_history(user, report_days)
    activity_data = get_activity_history(user, report_days)
    coping_plan = get_coping_plan(user)

    mood_df = _build_df(history, ["ID", "Username", "Mood", "Intensity", "Triggers", "Notes", "Date", "Timestamp"])
    sleep_df = _build_df(sleep_data, ["ID", "Username", "Hours", "Quality", "Notes", "Date", "Timestamp"])
    meditation_df = _build_df(meditation_data, ["ID", "Username", "Duration", "Type", "Date", "Timestamp"])
    habit_df = _build_df(habit_data, ["ID", "Username", "Habit", "Completed", "Note", "Date", "Timestamp"])
    activity_df = _build_df(activity_data, ["ID", "Username", "Activity", "Details", "Duration", "Date", "Timestamp"])

    mood_score = int(np.mean([MOOD_SCORE_MAP.get(row[2], 55) for row in history])) if history else 0
    intensity_score = int(np.mean([row[3] for row in history])) if history else 0
    sleep_score = int(np.mean([SLEEP_QUALITY_MAP.get(row[3], 55) for row in sleep_data])) if sleep_data else 0
    avg_sleep = float(np.mean([row[2] for row in sleep_data])) if sleep_data else 0.0
    meditation_minutes = int(sum([row[2] for row in meditation_data])) if meditation_data else 0

    completed_habits = len([row for row in habit_data if row[3] == 1])
    habit_total = len(habit_data)
    habit_completion_rate = int((completed_habits / habit_total) * 100) if habit_total else 0
    habit_streak = get_habit_streak(user)
    plan_ready = bool(coping_plan and any(coping_plan[:5]))

    mood_days_logged = mood_df["Date"].nunique() if not mood_df.empty else 0
    tracking_consistency = int((mood_days_logged / max(1, report_days)) * 100)

    low_mood_entries = len([row for row in history if row[2] in LOW_MOOD_SET]) if history else 0
    low_mood_ratio = int((low_mood_entries / max(1, len(history))) * 100) if history else 0

    sleep_target_nights = int((sleep_df["Hours"] >= 7).sum()) if not sleep_df.empty else 0
    sleep_target_ratio = int((sleep_target_nights / max(1, len(sleep_df))) * 100) if not sleep_df.empty else 0

    sleep_hours_score = min(100, int((avg_sleep / 8.0) * 100)) if avg_sleep else 0
    meditation_score = min(100, int((meditation_minutes / max(1, report_days * 10)) * 100))
    wellbeing_score = int(
        0.28 * mood_score
        + 0.18 * intensity_score
        + 0.20 * sleep_score
        + 0.12 * sleep_hours_score
        + 0.12 * habit_completion_rate
        + 0.10 * meditation_score
    )

    recommendations = []
    if tracking_consistency < 50:
        recommendations.append("Track mood at least 4 days per week for clearer patterns.")
    if avg_sleep and avg_sleep < 7:
        recommendations.append("Try a fixed sleep window and reduce screen time 60 minutes before bed.")
    if sleep_target_ratio < 60 and len(sleep_df):
        recommendations.append("Aim for at least 7h sleep on most nights to stabilize mood.")
    if habit_completion_rate < 60:
        recommendations.append("Reduce habits to 1-2 tiny actions daily to increase consistency.")
    if mood_score < 55 or low_mood_ratio > 45:
        recommendations.append("Schedule one social or outdoor activity this week for mood support.")
    if meditation_minutes < report_days * 5:
        recommendations.append("Aim for 5 minutes of breathing or meditation daily for the next 7 days.")
    if not plan_ready:
        recommendations.append("Complete your Coping Plan to prepare for difficult emotional moments.")
    if not recommendations:
        recommendations.append("Great trend overall. Keep your routine stable and review progress weekly.")

    focus_metrics = [
        {
            "Metric": "Mood tracking consistency",
            "Current": f"{tracking_consistency}%",
            "Target": ">= 60%",
            "Status": "On track" if tracking_consistency >= 60 else "Needs focus",
        },
        {
            "Metric": "Sleep nights >= 7h",
            "Current": f"{sleep_target_ratio}%",
            "Target": ">= 70%",
            "Status": "On track" if sleep_target_ratio >= 70 else "Needs focus",
        },
        {
            "Metric": "Habit completion",
            "Current": f"{habit_completion_rate}%",
            "Target": ">= 65%",
            "Status": "On track" if habit_completion_rate >= 65 else "Needs focus",
        },
        {
            "Metric": "Low mood share",
            "Current": f"{low_mood_ratio}%",
            "Target": "<= 35%",
            "Status": "On track" if low_mood_ratio <= 35 else "Needs focus",
        },
    ]

    pattern_insights = []
    if not mood_df.empty:
        mood_daily = mood_df.groupby("Date", as_index=False)["Intensity"].mean()
    else:
        mood_daily = pd.DataFrame(columns=["Date", "Intensity"])

    if not sleep_df.empty:
        sleep_daily = sleep_df.groupby("Date", as_index=False)["Hours"].mean()
    else:
        sleep_daily = pd.DataFrame(columns=["Date", "Hours"])

    if not mood_daily.empty and not sleep_daily.empty:
        merged = pd.merge(mood_daily, sleep_daily, on="Date", how="inner")
        if len(merged) >= 3:
            corr = merged["Intensity"].corr(merged["Hours"])
            if pd.notna(corr):
                pattern_insights.append(f"Mood intensity vs sleep correlation: {corr:.2f}")
                if corr < -0.25:
                    pattern_insights.append("Lower sleep appears associated with worse mood intensity.")

    if not habit_df.empty and not mood_df.empty:
        habit_done_days = habit_df[habit_df["Completed"] == 1]["Date"].nunique()
        mood_days = mood_df["Date"].nunique()
        if mood_days:
            adherence_ratio = habit_done_days / mood_days
            pattern_insights.append(f"Habit adherence on mood-tracked days: {adherence_ratio*100:.1f}%")

    if meditation_minutes and len(history):
        med_per_entry = meditation_minutes / max(1, len(history))
        pattern_insights.append(f"Meditation minutes per mood entry: {med_per_entry:.1f}")

    return {
        "history": history,
        "sleep_data": sleep_data,
        "meditation_data": meditation_data,
        "habit_data": habit_data,
        "activity_data": activity_data,
        "mood_df": mood_df,
        "sleep_df": sleep_df,
        "meditation_df": meditation_df,
        "habit_df": habit_df,
        "activity_df": activity_df,
        "scores": {
            "wellbeing_score": wellbeing_score,
            "mood_score": mood_score,
            "intensity_score": intensity_score,
            "sleep_score": sleep_score,
            "sleep_hours_score": sleep_hours_score,
            "meditation_score": meditation_score,
        },
        "metrics": {
            "avg_sleep": avg_sleep,
            "meditation_minutes": meditation_minutes,
            "habit_completion_rate": habit_completion_rate,
            "habit_streak": habit_streak,
            "plan_ready": plan_ready,
            "tracking_consistency": tracking_consistency,
            "sleep_target_ratio": sleep_target_ratio,
            "sleep_target_nights": sleep_target_nights,
            "low_mood_ratio": low_mood_ratio,
            "mood_days_logged": mood_days_logged,
        },
        "recommendations": recommendations,
        "focus_metrics": focus_metrics,
        "pattern_insights": pattern_insights,
    }

def upsert_coping_plan(user, warning_signs, coping_steps, support_contacts, safe_places, professional_help):
    updated_at = str(datetime.datetime.now())
    c.execute(
        """
        INSERT INTO coping_plans (username, warning_signs, coping_steps, support_contacts, safe_places, professional_help, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(username) DO UPDATE SET
            warning_signs=excluded.warning_signs,
            coping_steps=excluded.coping_steps,
            support_contacts=excluded.support_contacts,
            safe_places=excluded.safe_places,
            professional_help=excluded.professional_help,
            updated_at=excluded.updated_at
        """,
        (user, warning_signs, coping_steps, support_contacts, safe_places, professional_help, updated_at)
    )
    conn.commit()

def get_coping_plan(user):
    c.execute(
        "SELECT warning_signs, coping_steps, support_contacts, safe_places, professional_help, updated_at FROM coping_plans WHERE username=?",
        (user,)
    )
    return c.fetchone()

def add_goal(user, goal, category, deadline, milestones=""):
    created = str(datetime.date.today())
    c.execute(
        "INSERT INTO goals (username, goal, category, status, created_date, deadline, progress, milestones) VALUES (?,?,?,?,?,?,?,?)",
        (user, goal, category, "Active", created, deadline, 0, milestones)
    )
    conn.commit()

def get_goals(user):
    c.execute("SELECT * FROM goals WHERE username=? ORDER BY deadline ASC", (user,))
    return c.fetchall()

def update_goal_progress(goal_id, status, progress):
    c.execute("UPDATE goals SET status=?, progress=? WHERE id=?", (status, int(progress), goal_id))
    conn.commit()

def export_all_user_data(user):
    data_bundle = {}
    table_map = {
        "mood_entries": "SELECT * FROM mood_entries WHERE username=?",
        "gratitude": "SELECT * FROM gratitude WHERE username=?",
        "breathing_sessions": "SELECT * FROM breathing_sessions WHERE username=?",
        "sleep_tracking": "SELECT * FROM sleep_tracking WHERE username=?",
        "goals": "SELECT * FROM goals WHERE username=?",
        "meditation_sessions": "SELECT * FROM meditation_sessions WHERE username=?",
        "activity_sessions": "SELECT * FROM activity_sessions WHERE username=?",
        "habit_entries": "SELECT * FROM habit_entries WHERE username=?",
        "coping_plans": "SELECT * FROM coping_plans WHERE username=?",
        "reminders": "SELECT * FROM reminders WHERE username=?",
        "shared_reports": "SELECT * FROM shared_reports WHERE username=?",
    }

    for table_name, query in table_map.items():
        c.execute(query, (user,))
        rows = c.fetchall()
        column_names = [desc[0] for desc in c.description] if c.description else []
        data_bundle[table_name] = [dict(zip(column_names, row)) for row in rows]

    return {
        "user": user,
        "exported_at": str(datetime.datetime.now()),
        "data": data_bundle,
    }

def delete_user_account_and_data(user):
    table_delete_map = [
        "mood_entries",
        "gratitude",
        "breathing_sessions",
        "sleep_tracking",
        "goals",
        "meditation_sessions",
        "activity_sessions",
        "habit_entries",
        "coping_plans",
        "reminders",
        "shared_reports",
    ]

    for table in table_delete_map:
        c.execute(f"DELETE FROM {table} WHERE username=?", (user,))

    c.execute("DELETE FROM users WHERE username=?", (user,))
    conn.commit()

def generate_pdf_report(summary_text):
    try:
        fpdf_module = importlib.import_module("fpdf")
        FPDF = fpdf_module.FPDF
    except Exception:
        return None

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "SereneMind - Wellbeing Report", ln=True)
    pdf.ln(4)
    pdf.set_font("Arial", size=11)
    clean_text = summary_text.encode("latin-1", errors="replace").decode("latin-1")
    pdf.multi_cell(0, 7, clean_text)
    return bytes(pdf.output(dest="S"))

# ===============================
# SESSION STATE
# ===============================
if "user" not in st.session_state:
    st.session_state.user = None

# ===============================
# LOGIN / REGISTER PAGE
# ===============================
if st.session_state.user is None:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("# SereneMind")
        st.markdown("### Your Personal Mental Health Companion")
        
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            st.markdown("#### Login to Your Account")
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            
            if st.button("Login", use_container_width=True):
                user = login(username, password)
                if user:
                    st.session_state.user = username
                    st.success("Welcome back! 👋")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Invalid credentials!")
        
        with tab2:
            st.markdown("#### Create New Account")
            new_user = st.text_input("Choose Username", key="reg_user")
            new_phone = st.text_input("Phone (E.164, ex: +40700111222)", key="reg_phone")
            new_pass = st.text_input("Choose Password", type="password", key="reg_pass")
            new_pass_confirm = st.text_input("Confirm Password", type="password", key="reg_pass_conf")
            
            if st.button("Create Account", use_container_width=True):
                if not new_user or not new_phone or not new_pass:
                    st.error("Please fill all fields")
                elif not normalize_phone(new_phone).startswith("+"):
                    st.error("Please enter a valid phone in E.164 format (example: +40700111222)")
                elif new_pass != new_pass_confirm:
                    st.error("Passwords don't match")
                elif register(new_user, new_pass, new_phone):
                    st.success("Account created! Please login.")
                else:
                    st.error("Username or phone already exists!")

# ===============================
# MAIN APP
# ===============================
else:
    # Initialize navigation if not exists
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Dashboard"

    process_due_reminders(st.session_state.user)

    unacknowledged_alarms = get_unacknowledged_in_app_alarms(st.session_state.user)
    if unacknowledged_alarms:
        st.warning(f"🔔 You have {len(unacknowledged_alarms)} in-app alarm(s).")
        st.audio(generate_alarm_sound_wav(), format="audio/wav", autoplay=True)
        for alarm_row in unacknowledged_alarms[:3]:
            st.write(f"• {alarm_row[1]} ({alarm_row[3]})")
        if st.button("Mark Alarms As Seen", key="ack_in_app_alarms", use_container_width=True):
            acknowledge_in_app_alarms(st.session_state.user)
            st.rerun()

    nav_options = [
        "Dashboard", "Mood Tracking", "Games & Activities", "Sleep Tracking",
        "My Goals", "Habit Tracker", "Coping Plan", "Crisis Support", "Therapist Share", "Reminders", "Analytics", "Settings"
    ]
    if st.session_state.current_page not in nav_options:
        st.session_state.current_page = "Dashboard"
    
    with st.sidebar:
        st.markdown(f"### {st.session_state.user}")
        st.divider()
        
        option = st.radio(
            "Navigation",
            nav_options,
            index=nav_options.index(st.session_state.current_page)
        )
        
        # Update current page based on radio selection
        if option != st.session_state.current_page:
            st.session_state.current_page = option
            st.rerun()
        
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()

    # ===============================
    # DASHBOARD
    # ===============================
    if option == "Dashboard":
        st.title("Your Clarity Dashboard")
        st.caption("A quick view of what matters most right now and what to improve next.")

        dashboard_days = 30
        snapshot = build_wellbeing_snapshot(st.session_state.user, dashboard_days)
        metrics = snapshot["metrics"]
        scores = snapshot["scores"]

        _render_dashboard_hero(
            st.session_state.user,
            scores["wellbeing_score"],
            metrics["tracking_consistency"],
        )

        st.caption("Fixed view: last 30 days")

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Wellbeing Score", f"{scores['wellbeing_score']}/100", f"{dashboard_days} days")
        with col2:
            st.metric("Mood Logged", f"{metrics['mood_days_logged']} days", f"{metrics['tracking_consistency']}% consistency")
        with col3:
            st.metric("Average Sleep", f"{metrics['avg_sleep']:.1f}h", f"{metrics['sleep_target_nights']} nights >= 7h")
        with col4:
            st.metric("Habit Completion", f"{metrics['habit_completion_rate']}%", f"streak {metrics['habit_streak']} days")
        with col5:
            st.metric("Low Mood Share", f"{metrics['low_mood_ratio']}%", "Anxious/Stressed/Sad")

        st.divider()
        st.info("Dashboard overview only. Detailed charts live in Analytics.")

        st.divider()
        focus_col1, focus_col2 = st.columns([1.2, 1])

        with focus_col1:
            st.subheader("What to track this week")
            focus_df = pd.DataFrame(snapshot["focus_metrics"])
            st.dataframe(focus_df, use_container_width=True, hide_index=True)

        with focus_col2:
            st.subheader("Priority actions")
            for rec in snapshot["recommendations"][:4]:
                st.write(f"• {rec}")

            if scores["wellbeing_score"] >= 75:
                st.success("Strong baseline. Focus on consistency to keep momentum.")
            elif scores["wellbeing_score"] >= 55:
                st.warning("Moderate zone. Pick 1-2 habits and improve sleep regularity.")
            else:
                st.error("Risk zone. Track daily and consider reaching out for additional support.")

        st.divider()
        st.subheader("Quick Actions")
        quick1, quick2, quick3, quick4, quick5 = st.columns(5)

        with quick1:
            if st.button("Log Mood", use_container_width=True):
                st.session_state.current_page = "Mood Tracking"
                st.rerun()
        with quick2:
            if st.button("Play Activity", use_container_width=True):
                st.session_state.current_page = "Games & Activities"
                st.rerun()
        with quick3:
            if st.button("Log Sleep", use_container_width=True):
                st.session_state.current_page = "Sleep Tracking"
                st.rerun()
        with quick4:
            if st.button("Open Analytics", use_container_width=True):
                st.session_state.current_page = "Analytics"
                st.rerun()
        with quick5:
            if st.button("Log Habit", use_container_width=True):
                st.session_state.current_page = "Habit Tracker"
                st.rerun()

    # ===============================
    # MOOD TRACKING
    # ===============================
    elif option == "Mood Tracking":
        st.title("Mood Tracking")
        
        tab1, tab2, tab3 = st.tabs(["Log New Mood", "Emotion Wheel", "History"])
        
        with tab1:
            st.subheader("How are you feeling right now?")
            
            col1, col2 = st.columns(2)
            
            with col1:
                mood = st.selectbox(
                    "Select your mood:",
                    ["Very Happy", "Happy", "Calm", "Neutral", "Anxious", "Sad", "Very Sad", "Stressed", "Energetic", "Tired"]
                )
                
                mood_emojis = {
                    "Very Happy": "😄",
                    "Happy": "😊",
                    "Calm": "😌",
                    "Neutral": "😐",
                    "Anxious": "😰",
                    "Sad": "😢",
                    "Very Sad": "😢😢",
                    "Stressed": "😫",
                    "Energetic": "⚡",
                    "Tired": "😴"
                }
                
                st.markdown(f"### {mood}")
            
            with col2:
                intensity = st.slider("Intensity (0-100):", 0, 100, 50)
                st.markdown(f"### Intensity: {intensity}%")
            
            triggers = st.multiselect(
                "What triggered this mood? (Optional)",
                ["Work/School", "Relationships", "Health", "Money", "Family", "Lack of Sleep", "Exercise", "Social"]
            )
            
            notes = st.text_area("Add notes about your feeling:")
            
            if st.button("Save Mood Entry", use_container_width=True):
                save_mood(st.session_state.user, mood, intensity, ", ".join(triggers), notes)
                st.success("✅ Mood saved successfully!")
                st.balloons()
        
        with tab2:
            st.subheader("🎨 Emotion Wheel")
            st.markdown("""
            **Explore your emotions:**
            
            **Positive Emotions:**
            - 😊 Joy, Happiness, Excitement, Gratitude
            - 😌 Calm, Peaceful, Serene, Relaxed
            - 💪 Confident, Powerful, Strong, Capable
            
            **Negative Emotions:**
            - 😢 Sad, Disappointed, Despair, Grief
            - 😰 Anxious, Worried, Nervous, Tense
            - 😠 Angry, Frustrated, Irritated, Furious
            
            **Take a moment to identify which emotion resonates with you most.**
            """)
        
        with tab3:
            st.subheader("📖 Mood History")
            history = get_mood_history(st.session_state.user, 30)
            
            if history:
                mood_df = pd.DataFrame(history, columns=["ID", "Username", "Mood", "Intensity", "Triggers", "Notes", "Date", "Timestamp"])
                mood_df_display = mood_df[["Date", "Mood", "Intensity", "Triggers", "Notes"]]
                
                for idx, row in mood_df_display.iterrows():
                    with st.expander(f"📅 {row['Date']} - {row['Mood']} ({int(row['Intensity'])}%)"):
                        st.write(f"**Triggers:** {row['Triggers'] if row['Triggers'] else 'None'}")
                        st.write(f"**Notes:** {row['Notes']}")
                        st.progress(int(row['Intensity']) / 100.0)
            else:
                st.info("No mood entries yet. Start tracking!")

    # ===============================
    # GAMES & ACTIVITIES
    # ===============================
    elif option == "Games & Activities":
        st.title("Games & Mindfulness Activities")
        
        activity = st.selectbox(
            "Choose an activity:",
            [
                "Guided Breathing",
                "Meditation",
                "Gratitude Journal",
                "Affirmations",
                "Anxiety Relief",
                "Mindful Walking",
                "CBT Thought Reframe",
                "Self-Compassion Letter",
                "Values Compass",
                "Emotion Regulation Lab",
                "Behavioral Activation Quest"
            ]
        )

        if activity == "Guided Breathing":
            st.subheader("🫁 Guided Breathing Exercise")
            
            st.markdown("""
            Breathing exercises activate your parasympathetic nervous system, reducing stress and anxiety.
            """)
            
            technique = st.radio("Choose breathing technique:", 
                                ["4-7-8 Breathing", "Box Breathing", "Belly Breathing"])
            
            if technique == "4-7-8 Breathing":
                st.markdown("""
                **Instructions:**
                1. 🫁 **Inhale** through your nose for 4 seconds
                2. 🤐 **Hold** your breath for 7 seconds
                3. 😌 **Exhale** through your mouth for 8 seconds
                4. Repeat 4 times
                """)
                
            elif technique == "Box Breathing":
                st.markdown("""
                **Instructions:**
                1. 🫁 **Inhale** for 4 seconds
                2. 🤐 **Hold** for 4 seconds
                3. 😌 **Exhale** for 4 seconds
                4. ⏸️ **Hold** for 4 seconds
                5. Repeat 5 times
                """)
                
            elif technique == "Belly Breathing":
                st.markdown("""
                **Instructions:**
                1. Place one hand on chest, one on belly
                2. Breathe deeply through nose
                3. Feel belly rise, chest stays still
                4. Exhale slowly through mouth
                5. Practice for 5 minutes
                """)
            
            if st.button("Complete Breathing Exercise", use_container_width=True):
                duration = 4 if technique == "4-7-8 Breathing" else (5 if technique == "Box Breathing" else 5)
                cycles = 4 if technique == "4-7-8 Breathing" else 5
                save_breathing(st.session_state.user, duration * 20, cycles)
                save_activity_session(
                    st.session_state.user,
                    "Guided Breathing",
                    f"Technique: {technique}, cycles: {cycles}",
                    duration
                )
                st.success(f"✅ Great job! You completed {technique}!")
                st.balloons()

        elif activity == "Meditation":
            st.subheader("🧘 Guided Meditation")
            
            duration = st.slider("Meditation duration (minutes):", 1, 30, 5)
            meditation_type = st.selectbox("Meditation type:", 
                                          ["Body Scan", "Mindfulness", "Loving Kindness", "Visualization"])
            
            if meditation_type == "Body Scan":
                st.markdown("""
                **Body Scan Meditation:**
                - Lie down or sit comfortably
                - Start from your toes, notice any sensations
                - Slowly scan up through legs, torso, arms, head
                - Observe without judgment
                - Takes 5-15 minutes
                """)
            elif meditation_type == "Mindfulness":
                st.markdown("""
                **Mindfulness Meditation:**
                - Focus on your breath
                - Notice thoughts without judging
                - Gently return to breath when distracted
                - Stay present in this moment
                """)
            elif meditation_type == "Loving Kindness":
                st.markdown("""
                **Loving Kindness (Metta):**
                - Send love to yourself: "May I be happy"
                - Extend to loved ones
                - Include neutral people
                - Even difficult people
                - All beings everywhere
                """)
            elif meditation_type == "Visualization":
                st.markdown("""
                **Visualization Meditation:**
                - Imagine a peaceful place
                - Engage all senses - see, hear, smell, feel
                - Create vivid mental imagery
                - Find calm in this space
                """)
            
            st.info(f"⏱️ Set a timer for {duration} minutes and begin when ready.")
            
            if st.button("Mark Meditation Complete", use_container_width=True):
                save_meditation(st.session_state.user, duration, meditation_type)
                save_activity_session(
                    st.session_state.user,
                    "Meditation",
                    f"Type: {meditation_type}",
                    duration
                )
                st.success(f"✅ Congratulations! You completed {duration} minutes of {meditation_type} meditation!")
                st.balloons()

        elif activity == "Gratitude Journal":
            st.subheader("📝 Gratitude Journal")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Add a Gratitude Entry")
                gratitude_text = st.text_area("What are you grateful for today?", height=150)
                
                if st.button("Add to Journal", use_container_width=True):
                    if gratitude_text:
                        save_gratitude(st.session_state.user, gratitude_text)
                        save_activity_session(
                            st.session_state.user,
                            "Gratitude Journal",
                            f"Entry length: {len(gratitude_text)} chars",
                            5
                        )
                        st.success("✅ Gratitude entry saved!")
                        st.balloons()
                    else:
                        st.error("Please write something!")
            
            with col2:
                st.markdown("#### Recent Gratitude Entries")
                gratitude = get_gratitude(st.session_state.user)
                
                if gratitude:
                    for entry in gratitude[:5]:
                        with st.expander(f"📅 {entry[3]}"):
                            st.write(entry[2])
                else:
                    st.info("No entries yet. Start being grateful!")

        elif activity == "Affirmations":
            st.subheader("✨ Daily Affirmations")
            
            affirmations = {
                "Self-Love": [
                    "I am worthy of love and respect 💗",
                    "I am enough exactly as I am ✨",
                    "I deserve happiness and success 🌟",
                    "My potential is limitless 🚀",
                    "I choose to love myself unconditionally 💕"
                ],
                "Courage": [
                    "I am brave and strong 💪",
                    "I can overcome any challenge 🏔️",
                    "Fear is just an opportunity to grow 🌱",
                    "I am capable of amazing things 🌠",
                    "I choose courage over comfort 🔥"
                ],
                "Peace": [
                    "I am calm and at peace 😌",
                    "I let go of what I cannot control 🍃",
                    "This moment is all I need 🌅",
                    "I trust in the process of life 🌊",
                    "Peace flows through me 🕊️"
                ],
                "Success": [
                    "I am achieving my goals 🎯",
                    "Success flows to me naturally 💫",
                    "I am a magnet for abundance 💰",
                    "My hard work pays off 📈",
                    "I am becoming my best self 👑"
                ]
            }
            
            category = st.selectbox("Choose a category:", list(affirmations.keys()))
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Get Random Affirmation", use_container_width=True):
                    affirmation = random.choice(affirmations[category])
                    save_activity_session(
                        st.session_state.user,
                        "Affirmations",
                        f"Category: {category}",
                        2
                    )
                    st.balloons()
                    st.success(f"### {affirmation}")
            
            with col2:
                if st.button("Show All Affirmations", use_container_width=True):
                    for affirmation in affirmations[category]:
                        st.write(f"• {affirmation}")

        elif activity == "Anxiety Relief":
            st.subheader("🆘 Anxiety Relief Techniques")
            
            technique = st.selectbox("Choose a technique:",
                                    ["5-4-3-2-1 Grounding", "Progressive Muscle Relaxation", "Ice Water Shock"])
            
            if technique == "5-4-3-2-1 Grounding":
                st.markdown("""
                ### 5-4-3-2-1 Grounding Exercise
                This technique brings you back to the present moment.
                """)
                
                st.markdown("**5 things you can SEE:** Name 5 things around you")
                things_see = st.text_input("Example: wall, lamp, door...")
                
                st.markdown("**4 things you can TOUCH:** Name 4 things you can feel")
                things_touch = st.text_input("Example: floor, shirt, air...")
                
                st.markdown("**3 things you can HEAR:** Name 3 sounds around you")
                things_hear = st.text_input("Example: birds, wind, voices...")
                
                st.markdown("**2 things you can SMELL:** Name 2 things you smell")
                things_smell = st.text_input("Example: coffee, flowers...")
                
                st.markdown("**1 thing you can TASTE:** Name 1 thing you taste")
                things_taste = st.text_input("Example: mint, coffee...")
                
                if st.button("Complete Exercise", use_container_width=True):
                    if all([things_see, things_touch, things_hear, things_smell, things_taste]):
                        save_activity_session(
                            st.session_state.user,
                            "Anxiety Relief",
                            "5-4-3-2-1 Grounding completed",
                            5
                        )
                        st.success("✅ Great! You're grounded in the present moment. Your anxiety will pass.")
                    else:
                        st.warning("Please complete all fields")

        elif activity == "CBT Thought Reframe":
            st.subheader("🧠 CBT Thought Reframe")
            st.markdown("Turn an automatic negative thought into a more balanced, realistic one.")

            situation = st.text_area("1) Situation", placeholder="What happened?")
            auto_thought = st.text_area("2) Automatic Thought", placeholder="What was your first thought?")
            emotion = st.selectbox("3) Main Emotion", ["Anxiety", "Sadness", "Anger", "Shame", "Guilt", "Fear", "Frustration"])
            emotion_intensity = st.slider("4) Emotion Intensity (%)", 0, 100, 70)
            distortion = st.multiselect(
                "5) Cognitive Distortions (if any)",
                [
                    "Catastrophizing",
                    "All-or-Nothing Thinking",
                    "Mind Reading",
                    "Fortune Telling",
                    "Overgeneralization",
                    "Personalization",
                    "Should Statements"
                ]
            )
            evidence_for = st.text_area("6) Evidence FOR this thought", placeholder="Facts that support it")
            evidence_against = st.text_area("7) Evidence AGAINST this thought", placeholder="Facts that challenge it")
            balanced = st.text_area("8) Balanced Alternative Thought", placeholder="A realistic, kinder, evidence-based thought")
            new_intensity = st.slider("9) New Emotion Intensity (%)", 0, 100, 40)

            if st.button("Generate Reframe Summary", use_container_width=True):
                if situation and auto_thought and balanced:
                    shift = emotion_intensity - new_intensity
                    save_activity_session(
                        st.session_state.user,
                        "CBT Thought Reframe",
                        f"Emotion: {emotion}, shift: {shift:+d}, distortions: {len(distortion)}",
                        10
                    )
                    st.success("✅ Excellent cognitive work! You just practiced emotional flexibility.")
                    st.markdown(f"""
                    **CBT Snapshot**
                    - Emotion: **{emotion}**
                    - Intensity shift: **{emotion_intensity}% → {new_intensity}%** ({shift:+d} points)
                    - Distortions noticed: **{', '.join(distortion) if distortion else 'None selected'}**

                    **Balanced thought:**
                    _{balanced}_
                    """)
                else:
                    st.warning("Complete at least situation, automatic thought, and balanced thought.")

        elif activity == "Self-Compassion Letter":
            st.subheader("💌 Self-Compassion Letter")
            st.markdown("Write to yourself as if you were supporting a close friend.")

            hard_moment = st.text_area("Hard moment", placeholder="What are you struggling with right now?")
            self_critic = st.text_area("Inner critic says...", placeholder="Write the harsh inner dialogue")
            friend_voice = st.text_area("If a kind friend replied...", placeholder="What would they tell you?")
            need_now = st.text_input("What do you need right now?", placeholder="e.g., rest, boundaries, reassurance")

            tone = st.select_slider("Choose tone", options=["Gentle", "Warm", "Encouraging", "Strong and protective"], value="Warm")

            if st.button("Create My Letter", use_container_width=True):
                if hard_moment and friend_voice:
                    save_activity_session(
                        st.session_state.user,
                        "Self-Compassion Letter",
                        f"Tone: {tone}, need: {need_now if need_now else 'N/A'}",
                        12
                    )
                    intro = {
                        "Gentle": "Dear me, I'm here with you.",
                        "Warm": "Dear me, you deserve kindness in this moment.",
                        "Encouraging": "Dear me, this is hard, and you are still moving forward.",
                        "Strong and protective": "Dear me, I will stand by you and protect your peace."
                    }[tone]

                    st.info(f"""
{intro}

What happened hurts: {hard_moment}

Even if your inner critic says: "{self_critic if self_critic else 'I am not enough'}",
the kinder truth is: {friend_voice}

Right now, you need: {need_now if need_now else 'a small pause and a breath'}.
One next caring step: choose one tiny action in the next 10 minutes.

With compassion,
You
                    """)
                    st.success("✅ Letter generated. Read it slowly, out loud, once.")
                else:
                    st.warning("Please complete at least the hard moment and friend response.")

        elif activity == "Values Compass":
            st.subheader("🧭 Values Compass")
            st.markdown("Clarify what matters and take one small action in that direction.")

            domains = ["Health", "Relationships", "Growth", "Work/Study", "Fun", "Community"]
            importance_scores = {}
            action_scores = {}

            for domain in domains:
                col1, col2 = st.columns(2)
                with col1:
                    importance_scores[domain] = st.slider(f"{domain} importance (0-10)", 0, 10, 7, key=f"imp_{domain}")
                with col2:
                    action_scores[domain] = st.slider(f"{domain} current action (0-10)", 0, 10, 5, key=f"act_{domain}")

            chosen_domain = st.selectbox("Pick one domain for this week", domains)
            micro_action = st.text_input("Micro-action (under 15 minutes)", placeholder="e.g., 10-minute walk after lunch")

            if st.button("Build My Compass Plan", use_container_width=True):
                gaps = {d: importance_scores[d] - action_scores[d] for d in domains}
                top_gap = max(gaps, key=gaps.get)
                save_activity_session(
                    st.session_state.user,
                    "Values Compass",
                    f"Top gap: {top_gap}, focus: {chosen_domain}",
                    8
                )
                st.success("✅ Compass ready. Direction beats perfection.")
                st.markdown(f"""
                - Biggest values-action gap: **{top_gap}** (gap: **{gaps[top_gap]}**)
                - Focus domain this week: **{chosen_domain}**
                - Next tiny step: **{micro_action if micro_action else 'Define one 10-minute action now'}**
                """)

        elif activity == "Emotion Regulation Lab":
            st.subheader("🧪 Emotion Regulation Lab")
            st.markdown("Experiment with strategies and pick the one that lowers intensity best.")

            emotion_name = st.selectbox("Current emotion", ["Anxiety", "Sadness", "Anger", "Overwhelm", "Loneliness", "Shame"])
            before = st.slider("Intensity before strategy (%)", 0, 100, 75)
            strategies = st.multiselect(
                "Choose 2-3 strategies to try",
                [
                    "Paced breathing (2 min)",
                    "Name and normalize emotion",
                    "Opposite action",
                    "Cold water splash",
                    "Short body movement",
                    "Call/text a safe person",
                    "Self-soothing with senses"
                ],
                default=["Paced breathing (2 min)", "Name and normalize emotion"]
            )
            after = st.slider("Intensity after strategy (%)", 0, 100, 55)
            helpful = st.text_area("What helped most?", placeholder="Which strategy was most effective and why?")

            if st.button("Save Lab Result", use_container_width=True):
                if strategies:
                    delta = before - after
                    save_activity_session(
                        st.session_state.user,
                        "Emotion Regulation Lab",
                        f"Emotion: {emotion_name}, delta: {delta:+d}, strategies: {len(strategies)}",
                        7
                    )
                    st.success(f"✅ Session done. Intensity changed by {delta:+d} points.")
                    st.write(f"Best strategy set: {', '.join(strategies)}")
                    if helpful:
                        st.info(f"Insight: {helpful}")
                else:
                    st.warning("Select at least one strategy.")

        elif activity == "Behavioral Activation Quest":
            st.subheader("🎯 Behavioral Activation Quest")
            st.markdown("Low mood often improves after action, not before. Build your mini-quest.")

            energy = st.select_slider("Current energy", options=["Very Low", "Low", "Medium", "High"], value="Low")
            value_areas = st.multiselect(
                "Value areas to activate today",
                ["Body", "Mind", "Connection", "Environment", "Purpose", "Play"],
                default=["Body", "Connection"]
            )
            step_5_min = st.text_input("5-minute action", placeholder="e.g., stretch + drink water")
            step_20_min = st.text_input("20-minute action", placeholder="e.g., tidy desk + quick shower")
            reward = st.text_input("Healthy reward after completion", placeholder="e.g., tea + favorite song")

            if st.button("Launch Quest", use_container_width=True):
                if step_5_min and step_20_min:
                    difficulty_map = {"Very Low": "Easy", "Low": "Easy", "Medium": "Moderate", "High": "Stretch"}
                    save_activity_session(
                        st.session_state.user,
                        "Behavioral Activation Quest",
                        f"Energy: {energy}, values: {', '.join(value_areas) if value_areas else 'None'}",
                        25
                    )
                    st.success("✅ Quest generated. Start with the 5-minute action now.")
                    st.markdown(f"""
                    **Quest difficulty:** {difficulty_map[energy]}
                    
                    **Stage 1 (5 min):** {step_5_min}
                    
                    **Stage 2 (20 min):** {step_20_min}
                    
                    **Value links:** {', '.join(value_areas) if value_areas else 'Not selected'}
                    
                    **Reward:** {reward if reward else 'Short break + appreciation'}
                    """)
                else:
                    st.warning("Add both a 5-minute and a 20-minute action.")

        elif activity == "Mindful Walking":
            st.subheader("🚶 Mindful Walking Guide")
            
            st.markdown("""
            ### Mindful Walking Exercise
            
            1. **Find a quiet space** - Walk at a comfortable pace
            2. **Focus on sensations** - Feel your feet touching the ground
            3. **Observe surroundings** - Notice colors, shapes, movements
            4. **Listen carefully** - Hear all sounds around you
            5. **Breathe naturally** - Don't force anything
            6. **When mind wanders** - Gently bring it back to walking
            
            Duration: 10-20 minutes
            
            **Benefits:**
            - Reduces stress and anxiety
            - Improves focus and clarity
            - Connects you with nature
            - Boosts mood naturally
            """)
            
            if st.button("Start Mindful Walk", use_container_width=True):
                st.info("🚶 Go for a 15-minute walk. Come back when done or click below when finished.")
                if st.button("Walk Completed!", use_container_width=True):
                    save_activity_session(
                        st.session_state.user,
                        "Mindful Walking",
                        "15-minute mindful walk completed",
                        15
                    )
                    st.success("✅ Excellent! Mindful walking is a wonderful practice!")
                    st.balloons()

        st.divider()
        st.subheader("🗂️ Activity History")
        activity_history = get_activity_history(st.session_state.user, 30)

        if activity_history:
            for item in activity_history[:12]:
                with st.expander(f"📅 {item[5]} · {item[2]}"):
                    st.write(f"**Duration:** {item[4]} min")
                    st.write(f"**Details:** {item[3] if item[3] else 'No details'}")
        else:
            st.info("No activities logged yet. Complete an exercise to see history.")

    # ===============================
    # SLEEP TRACKING
    # ===============================
    elif option == "Sleep Tracking":
        st.title("Sleep Tracking")
        
        tab1, tab2 = st.tabs(["Log Sleep", "Sleep History"])
        
        with tab1:
            st.subheader("Track your sleep quality")
            
            sleep_date = st.date_input("Date:", datetime.date.today())
            sleep_hours = st.slider("Hours of sleep:", 0.0, 12.0, 7.5, 0.5)
            sleep_quality = st.selectbox("Sleep quality:", ["Poor", "Fair", "Good", "Excellent"])
            sleep_notes = st.text_area("Sleep notes (optional):", placeholder="e.g., Had bad dreams, woke up frequently...")
            
            if st.button("Save Sleep Data", use_container_width=True):
                save_sleep(st.session_state.user, sleep_hours, sleep_quality, sleep_notes)
                st.success("✅ Sleep data saved!")
        
        with tab2:
            st.subheader("Sleep Dashboard")
            sleep_history = get_sleep_history(st.session_state.user, 30)
            
            if sleep_history:
                sleep_df = _build_df(sleep_history, ["ID", "Username", "Hours", "Quality", "Notes", "Date", "Timestamp"])
                sleep_chart_df = _prepare_sleep_dashboard_df(sleep_df)

                filter_col1, filter_col2 = st.columns(2)
                with filter_col1:
                    dashboard_window = st.select_slider(
                        "Dashboard window",
                        options=[7, 14, 30],
                        value=30,
                        key="sleep_tracking_window",
                    )
                with filter_col2:
                    selected_quality = st.multiselect(
                        "Quality filter",
                        options=SLEEP_QUALITY_ORDER,
                        default=SLEEP_QUALITY_ORDER,
                        key="sleep_tracking_quality_filter",
                    )

                date_cutoff = pd.Timestamp(datetime.date.today() - datetime.timedelta(days=dashboard_window))
                filtered_sleep = sleep_chart_df[sleep_chart_df["DateDT"] >= date_cutoff]
                if selected_quality:
                    filtered_sleep = filtered_sleep[filtered_sleep["Quality"].isin(selected_quality)]

                if not filtered_sleep.empty:
                    avg_hours = float(filtered_sleep["Hours"].mean())
                    nights_target = int((filtered_sleep["Hours"] >= 7).sum())
                    target_ratio = int((nights_target / max(1, len(filtered_sleep))) * 100)
                    avg_quality_score = int(filtered_sleep["QualityScore"].mean())
                    sleep_recovery_index = int((avg_quality_score * 0.6) + (min(100, int((avg_hours / 8.0) * 100)) * 0.4))
                    _render_sleep_kpi_cards(avg_hours, nights_target, target_ratio, avg_quality_score, f"Last {dashboard_window} days")

                    accent = THEMES.get(st.session_state.theme, THEMES["Purple"])["primary"]
                    hours_fig = _sleep_hours_figure(filtered_sleep, accent)
                    quality_fig = _sleep_quality_figure(filtered_sleep)
                    consistency_fig = _sleep_consistency_figure(filtered_sleep)
                    heatmap_fig = _sleep_heatmap_figure(filtered_sleep)
                    gauge_fig = _sleep_score_gauge(sleep_recovery_index, accent)

                    chart_col1, chart_col2 = st.columns([1.45, 1])
                    with chart_col1:
                        if hours_fig is not None:
                            st.plotly_chart(
                                hours_fig,
                                use_container_width=True,
                                key="sleep_tracking_hours_chart",
                            )
                        else:
                            fallback_hours = filtered_sleep.groupby("Date", as_index=False)["Hours"].mean().sort_values("Date")
                            st.line_chart(fallback_hours.set_index("Date"))

                    with chart_col2:
                        if gauge_fig is not None:
                            st.plotly_chart(gauge_fig, use_container_width=True, key="sleep_tracking_recovery_gauge")
                        if quality_fig is not None:
                            st.plotly_chart(
                                quality_fig,
                                use_container_width=True,
                                key="sleep_tracking_quality_chart",
                            )
                        else:
                            fallback_quality = filtered_sleep["Quality"].value_counts().reindex(SLEEP_QUALITY_ORDER, fill_value=0)
                            st.bar_chart(fallback_quality)

                    if consistency_fig is not None:
                        st.plotly_chart(
                            consistency_fig,
                            use_container_width=True,
                            key="sleep_tracking_consistency_chart",
                        )

                    if heatmap_fig is not None:
                        st.plotly_chart(
                            heatmap_fig,
                            use_container_width=True,
                            key="sleep_tracking_heatmap_chart",
                        )

                    st.subheader("Sleep report (filtered)")
                    report_df = filtered_sleep[["Date", "Hours", "Quality", "Notes"]].sort_values("Date", ascending=False)
                    st.dataframe(report_df, use_container_width=True, hide_index=True)
                    st.download_button(
                        "Download sleep report (CSV)",
                        data=report_df.to_csv(index=False),
                        file_name=f"sleep_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        mime="text/csv",
                        use_container_width=True,
                    )
                else:
                    st.warning("No sleep entries match the selected filters.")

                st.divider()
                st.subheader("Sleep entries")
                for sleep in sleep_history:
                    with st.expander(f"📅 {sleep[5]} - {sleep[2]}h ({sleep[3]})"):
                        st.write(f"**Hours:** {sleep[2]}")
                        st.write(f"**Quality:** {sleep[3]}")
                        st.write(f"**Notes:** {sleep[4] if sleep[4] else 'None'}")
            else:
                st.info("No sleep data yet.")

    # ===============================
    # MY GOALS
    # ===============================
    elif option == "My Goals":
        st.title("My Goals")
        
        tab1, tab2 = st.tabs(["Add Goal", "My Goals"])
        
        with tab1:
            st.subheader("Set a new goal")
            
            goal_text = st.text_input("What's your goal?")
            category = st.selectbox("Category:", ["Health", "Mental Health", "Fitness", "Learning", "Relationships", "Work"])
            deadline = st.date_input("Deadline:")
            milestones = st.text_area("Milestones (optional)", placeholder="e.g., Week 1: baseline, Week 2: consistency")
            
            if st.button("Add Goal", use_container_width=True):
                if goal_text:
                    add_goal(st.session_state.user, goal_text, category, str(deadline), milestones)
                    st.success("✅ Goal added!")
                else:
                    st.error("Please enter a goal")
        
        with tab2:
            st.subheader("Your Goals")
            goals = get_goals(st.session_state.user)
            
            if goals:
                for goal in goals:
                    with st.expander(f"🎯 {goal[2]} ({goal[3]})"):
                        st.write(f"**Category:** {goal[3]}")
                        current_status = goal[4]
                        deadline_str = goal[6]
                        progress_value = int(goal[7]) if len(goal) > 7 and goal[7] is not None else 0
                        milestone_text = goal[8] if len(goal) > 8 and goal[8] else "No milestones"

                        st.write(f"**Current Status:** {current_status}")
                        st.write(f"**Deadline:** {deadline_str}")
                        st.write(f"**Milestones:** {milestone_text}")

                        days_left = None
                        try:
                            deadline_date = datetime.date.fromisoformat(deadline_str)
                            days_left = (deadline_date - datetime.date.today()).days
                        except Exception:
                            pass

                        if days_left is not None:
                            if days_left < 0 and progress_value < 100:
                                st.error("⚠️ Goal overdue and incomplete")
                            elif days_left <= 3 and progress_value < 80:
                                st.warning("⚠️ Goal at risk: near deadline with low progress")
                            else:
                                st.info(f"Days left: {days_left}")

                        st.progress(max(0, min(100, progress_value)) / 100)

                        new_progress = st.slider(
                            "Update progress (%)",
                            0,
                            100,
                            progress_value,
                            key=f"goal_progress_{goal[0]}"
                        )
                        new_status = st.selectbox(
                            "Update status",
                            ["Active", "In Progress", "Paused", "Completed"],
                            index=["Active", "In Progress", "Paused", "Completed"].index(current_status) if current_status in ["Active", "In Progress", "Paused", "Completed"] else 0,
                            key=f"goal_status_{goal[0]}"
                        )

                        if st.button("Save Goal Update", key=f"goal_save_{goal[0]}", use_container_width=True):
                            final_status = "Completed" if new_progress >= 100 else new_status
                            update_goal_progress(goal[0], final_status, new_progress)
                            st.success("Goal updated.")
            else:
                st.info("No goals yet. Set one to get started!")

    # ===============================
    # HABIT TRACKER
    # ===============================
    elif option == "Habit Tracker":
        st.title("Habit Tracker")

        default_habits = [
            "Drink water",
            "10-minute movement",
            "5-minute breathing",
            "No social media before sleep",
            "Journal check-in"
        ]

        tab1, tab2, tab3 = st.tabs(["Log Habit", "History", "Insights"])

        with tab1:
            st.subheader("Log your habit for today")
            habit_name = st.selectbox("Habit", default_habits + ["Custom"])
            custom_habit = ""
            if habit_name == "Custom":
                custom_habit = st.text_input("Custom habit name")

            completed = st.checkbox("Completed", value=True)
            note = st.text_area("Note (optional)", placeholder="How did it go?")

            if st.button("Save Habit Entry", use_container_width=True):
                final_habit = custom_habit.strip() if habit_name == "Custom" else habit_name
                if not final_habit:
                    st.error("Please enter a habit name.")
                else:
                    save_habit_entry(st.session_state.user, final_habit, completed, note)
                    st.success("✅ Habit entry saved!")

        with tab2:
            st.subheader("Last 30 days")
            habits = get_habit_history(st.session_state.user, 30)
            if habits:
                habit_df = pd.DataFrame(
                    habits,
                    columns=["ID", "Username", "Habit", "Completed", "Note", "Date", "Timestamp"]
                )
                habit_df["Completed"] = habit_df["Completed"].map({1: "Yes", 0: "No"})
                st.dataframe(habit_df[["Date", "Habit", "Completed", "Note"]], use_container_width=True)
            else:
                st.info("No habit entries yet.")

        with tab3:
            st.subheader("Habit insights")
            habits = get_habit_history(st.session_state.user, 30)
            streak = get_habit_streak(st.session_state.user)
            st.metric("Current streak", f"{streak} days")

            if habits:
                completed_rows = [row for row in habits if row[3] == 1]
                completion_rate = (len(completed_rows) / len(habits)) * 100
                st.metric("Completion rate (30 days)", f"{completion_rate:.1f}%")

                habit_counts = Counter([row[2] for row in completed_rows])
                if habit_counts:
                    chart_df = pd.DataFrame(list(habit_counts.items()), columns=["Habit", "Completions"])
                    st.bar_chart(chart_df.set_index("Habit"))
            else:
                st.info("Start logging habits to unlock insights.")

    # ===============================
    # COPING PLAN
    # ===============================
    elif option == "Coping Plan":
        st.title("Personal Coping Plan")
        st.caption("Build your personal plan for difficult emotional moments.")

        existing_plan = get_coping_plan(st.session_state.user)

        warning_default = existing_plan[0] if existing_plan else ""
        steps_default = existing_plan[1] if existing_plan else ""
        contacts_default = existing_plan[2] if existing_plan else ""
        places_default = existing_plan[3] if existing_plan else ""
        help_default = existing_plan[4] if existing_plan else ""

        warning_signs = st.text_area(
            "1) Warning signs",
            value=warning_default,
            placeholder="What signals tell you things are getting hard?"
        )
        coping_steps = st.text_area(
            "2) Coping steps",
            value=steps_default,
            placeholder="Step-by-step things you can do to regulate emotions"
        )
        support_contacts = st.text_area(
            "3) Support contacts",
            value=contacts_default,
            placeholder="Trusted people + phone numbers"
        )
        safe_places = st.text_area(
            "4) Safe places",
            value=places_default,
            placeholder="Places where you feel safer/calm"
        )
        professional_help = st.text_area(
            "5) Professional help",
            value=help_default,
            placeholder="Therapist, doctor, crisis line, local emergency contacts"
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save Coping Plan", use_container_width=True):
                upsert_coping_plan(
                    st.session_state.user,
                    warning_signs,
                    coping_steps,
                    support_contacts,
                    safe_places,
                    professional_help,
                )
                st.success("✅ Coping plan saved.")

        with col2:
            if existing_plan and existing_plan[5]:
                st.info(f"Last updated: {existing_plan[5]}")

        st.warning("If you are in immediate danger, call local emergency services now.")

    # ===============================
    # CRISIS SUPPORT
    # ===============================
    elif option == "Crisis Support":
        st.title("Crisis Support")
        st.markdown("Use this section when you need immediate grounding and clear support steps.")

        tab1, tab2 = st.tabs(["Immediate Actions", "My Emergency Contacts"])

        with tab1:
            st.subheader("What to do right now")
            st.markdown("""
            1. **Pause and breathe slowly** for 60 seconds.
            2. **Move to a safer space** (better light, quieter place, trusted person nearby).
            3. **Contact support now**: a trusted person, therapist, or emergency service.
            4. **Remove immediate risks** from your environment.
            """)
            st.warning("If you are in immediate danger, call local emergency services now.")

            quick_message = st.text_area(
                "Quick message to send a trusted person",
                value="Hi, I am having a difficult moment and I need support. Can you call me as soon as possible?"
            )
            st.code(quick_message)

        with tab2:
            plan = get_coping_plan(st.session_state.user)
            contacts = plan[2] if plan and plan[2] else ""
            if contacts:
                st.info("Contacts loaded from your Coping Plan:")
                st.write(contacts)

                phone_numbers = extract_phone_numbers(contacts)
                if phone_numbers:
                    st.markdown("### Tap to call")
                    for phone in phone_numbers:
                        st.markdown(f"- [📞 Call {phone}](tel:{phone})")
                    st.caption("On mobile, this opens the phone dialer directly.")
                else:
                    st.caption("No phone number detected in contacts text.")
            else:
                st.info("No emergency contacts found. Add them in Coping Plan.")

    # ===============================
    # THERAPIST SHARE
    # ===============================
    elif option == "Therapist Share":
        st.title("Therapist Share")
        st.caption("Send your therapy progress report by email.")

        smtp_issues = validate_smtp_config()
        if smtp_issues:
            st.warning("Email is not configured yet. Add SMTP settings in Streamlit secrets.")
            for issue in smtp_issues:
                st.write(f"- {issue}")
        else:
            st.success("SMTP configuration looks good.")

        therapist_email = st.text_input("Therapist email")
        report_days = st.slider("Include last N days", 7, 90, 30, key="therapist_report_days")
        clinician_notes = st.text_area("Message for therapist (optional)")

        history = get_mood_history(st.session_state.user, report_days)
        sleep_data = get_sleep_history(st.session_state.user, report_days)
        meditation_data = get_meditation_history(st.session_state.user, report_days)
        habit_data = get_habit_history(st.session_state.user, report_days)
        activity_data = get_activity_history(st.session_state.user, report_days)

        avg_sleep = float(np.mean([row[2] for row in sleep_data])) if sleep_data else 0.0
        mood_intensity = int(np.mean([row[3] for row in history])) if history else 0
        meditation_minutes = int(sum([row[2] for row in meditation_data])) if meditation_data else 0
        completed_habits = len([row for row in habit_data if row[3] == 1])

        report_payload = {
            "user": st.session_state.user,
            "generated_at": str(datetime.datetime.now()),
            "window_days": report_days,
            "summary": {
                "mood_entries": len(history),
                "avg_mood_intensity": mood_intensity,
                "avg_sleep_hours": round(avg_sleep, 2),
                "meditation_minutes": meditation_minutes,
                "completed_habits": completed_habits,
                "activity_sessions": len(activity_data),
            },
            "notes": clinician_notes,
        }

        preview = (
            f"SereneMind Clinical Summary\n"
            f"User: {st.session_state.user}\n"
            f"Window: last {report_days} days\n"
            f"Generated: {datetime.datetime.now()}\n\n"
            f"Mood entries: {len(history)}\n"
            f"Average mood intensity: {mood_intensity}%\n"
            f"Average sleep: {avg_sleep:.1f} hours\n"
            f"Meditation minutes: {meditation_minutes}\n"
            f"Completed habits: {completed_habits}\n"
            f"Activity sessions: {len(activity_data)}\n\n"
            f"User notes:\n{clinician_notes if clinician_notes else '-'}\n"
        )
        st.text_area("Report preview", value=preview, height=220)

        if st.button("Send Report by Email", use_container_width=True):
            if not therapist_email or "@" not in therapist_email:
                st.error("Please enter a valid therapist email.")
            elif smtp_issues:
                st.error("SMTP settings are missing or invalid.")
            else:
                subject = f"SereneMind Report - {st.session_state.user}"
                sent, msg = send_email_notification(therapist_email.strip(), subject, preview)
                if sent:
                    save_shared_report(st.session_state.user, therapist_email, subject, clinician_notes, report_payload)
                    save_notification_log(st.session_state.user, "email", therapist_email.strip(), subject, preview, "sent", "Therapist report")
                    st.success("✅ Report sent and saved in history.")
                else:
                    save_notification_log(st.session_state.user, "email", therapist_email.strip(), subject, preview, "failed", msg)
                    st.error(f"Could not send email: {msg}")

        st.divider()
        st.subheader("Share History")
        shared = get_shared_reports(st.session_state.user)
        if shared:
            for row in shared[:10]:
                with st.expander(f"📧 {row[2]} · {row[6]}"):
                    st.write(f"**Subject:** {row[3]}")
                    st.write(f"**Notes:** {row[4] if row[4] else '-'}")
        else:
            st.info("No shared reports yet.")

    # ===============================
    # REMINDERS
    # ===============================
    elif option == "Reminders":
        st.title("Smart Reminders")
        st.caption("Create daily reminders with in-app alarms.")

        tab1, tab2 = st.tabs(["Create / Update", "My Reminders"])

        with tab1:
            reminder_name = st.text_input("Reminder name", value="Evening check-in")
            channel = st.selectbox("Channel", ["In-App Alarm"])
            reminder_time = st.time_input("Reminder time", value=datetime.time(20, 0))
            active = st.checkbox("Active", value=True)

            if st.button("Save Reminder", use_container_width=True):
                if not reminder_name.strip():
                    st.error("Please enter a reminder name.")
                else:
                    upsert_reminder(
                        st.session_state.user,
                        reminder_name.strip(),
                        channel,
                        reminder_time.hour,
                        reminder_time.minute,
                        active,
                    )
                    st.success("✅ Reminder saved.")

            if st.button("Send Test Reminder Now", use_container_width=True):
                # Create in-app alarm test
                save_in_app_alarm(st.session_state.user, reminder_name, f"Test reminder: {reminder_name}")
                st.success(f"✅ In-app alarm triggered.")

        with tab2:
            reminders = get_reminders(st.session_state.user)
            if reminders:
                reminders_df = pd.DataFrame(
                    reminders,
                    columns=["ID", "Username", "Reminder", "Channel", "Hour", "Minute", "Active", "LastSent", "CreatedAt"]
                )
                reminders_df["Time"] = reminders_df["Hour"].astype(str).str.zfill(2) + ":" + reminders_df["Minute"].astype(str).str.zfill(2)
                reminders_df["Active"] = reminders_df["Active"].map({1: "Yes", 0: "No"})
                st.dataframe(reminders_df[["Reminder", "Channel", "Time", "Active", "LastSent"]], use_container_width=True)
            else:
                st.info("No reminders created yet.")

    # ===============================
    # ANALYTICS
    # ===============================
    elif option == "Analytics":
        st.title("Analytics & Reports")
        st.caption("Understand trends, detect risk early, and focus on the metrics that improve wellbeing.")

        report_days = st.slider("Reporting window (days)", 7, 90, 30, 1)
        snapshot = build_wellbeing_snapshot(st.session_state.user, report_days)

        history = snapshot["history"]
        mood_df = snapshot["mood_df"]
        sleep_df = snapshot["sleep_df"]
        meditation_df = snapshot["meditation_df"]
        habit_df = snapshot["habit_df"]
        activity_df = snapshot["activity_df"]
        scores = snapshot["scores"]
        metrics = snapshot["metrics"]
        recommendations = snapshot["recommendations"]

        tab_overview, tab_trends, tab_export = st.tabs(["Executive Overview", "Trend Explorer", "Reports & Export"])

        with tab_overview:
            st.markdown(f"### Wellbeing Score: **{scores['wellbeing_score']}/100**")
            st.progress(max(0, min(100, scores["wellbeing_score"])) / 100)

            kpi1, kpi2, kpi3, kpi4 = st.columns(4)
            with kpi1:
                st.metric("Mood tracking consistency", f"{metrics['tracking_consistency']}%", f"{metrics['mood_days_logged']} days logged")
            with kpi2:
                st.metric("Average sleep", f"{metrics['avg_sleep']:.1f}h", f"{metrics['sleep_target_nights']} nights >= 7h")
            with kpi3:
                st.metric("Habit completion", f"{metrics['habit_completion_rate']}%", f"streak {metrics['habit_streak']} days")
            with kpi4:
                st.metric("Low mood share", f"{metrics['low_mood_ratio']}%", "Anxious/Stressed/Sad")

            score_col1, score_col2, score_col3, score_col4 = st.columns(4)
            with score_col1:
                st.metric("Mood quality score", scores["mood_score"])
            with score_col2:
                st.metric("Sleep quality score", scores["sleep_score"])
            with score_col3:
                st.metric("Meditation minutes", metrics["meditation_minutes"])
            with score_col4:
                st.metric("Coping Plan", "Ready" if metrics["plan_ready"] else "Missing")

            st.divider()
            st.subheader("What to focus on next")
            st.dataframe(pd.DataFrame(snapshot["focus_metrics"]), use_container_width=True, hide_index=True)

            st.subheader("Recommended actions")
            for rec in recommendations:
                st.write(f"• {rec}")

        with tab_trends:
            dist1, dist2 = st.columns(2)

            with dist1:
                st.subheader("Mood distribution")
                if not mood_df.empty:
                    mood_counts = mood_df["Mood"].value_counts().reset_index()
                    mood_counts.columns = ["Mood", "Count"]
                    st.bar_chart(mood_counts.set_index("Mood"))
                else:
                    st.info("No mood data yet.")

            with dist2:
                st.subheader("Sleep dashboard")
                if not sleep_df.empty:
                    sleep_chart_df = _prepare_sleep_dashboard_df(sleep_df)
                    quality_filter = st.multiselect(
                        "Sleep quality filter",
                        options=SLEEP_QUALITY_ORDER,
                        default=SLEEP_QUALITY_ORDER,
                        key="analytics_sleep_quality_filter",
                    )

                    sleep_filtered = sleep_chart_df.copy()
                    if quality_filter:
                        sleep_filtered = sleep_filtered[sleep_filtered["Quality"].isin(quality_filter)]

                    if not sleep_filtered.empty:
                        avg_hours = float(sleep_filtered["Hours"].mean())
                        nights_target = int((sleep_filtered["Hours"] >= 7).sum())
                        target_ratio = int((nights_target / max(1, len(sleep_filtered))) * 100)
                        avg_quality_score = int(sleep_filtered["QualityScore"].mean())
                        _render_sleep_kpi_cards(
                            avg_hours,
                            nights_target,
                            target_ratio,
                            avg_quality_score,
                            f"Window: {report_days} days",
                        )

                        quality_fig = _sleep_quality_figure(sleep_filtered)
                        accent = THEMES.get(st.session_state.theme, THEMES["Purple"])["primary"]
                        gauge_fig = _sleep_score_gauge(
                            int((avg_quality_score * 0.6) + (min(100, int((avg_hours / 8.0) * 100)) * 0.4)),
                            accent,
                        )

                        if gauge_fig is not None:
                            st.plotly_chart(
                                gauge_fig,
                                use_container_width=True,
                                key="analytics_sleep_recovery_gauge",
                            )

                        if quality_fig is not None:
                            st.plotly_chart(
                                quality_fig,
                                use_container_width=True,
                                key="analytics_sleep_quality_chart",
                            )
                        else:
                            fallback_quality = sleep_filtered["Quality"].value_counts().reindex(SLEEP_QUALITY_ORDER, fill_value=0)
                            st.bar_chart(fallback_quality)
                    else:
                        st.warning("No sleep data for selected quality filter.")
                else:
                    st.info("No sleep data yet.")

            st.divider()

            trend1, trend2 = st.columns(2)
            with trend1:
                st.subheader("Daily mood intensity")
                if not mood_df.empty:
                    mood_daily = mood_df.groupby("Date", as_index=False)["Intensity"].mean().sort_values("Date")
                    st.line_chart(mood_daily.set_index("Date"))
                else:
                    st.info("No mood trend available.")

            with trend2:
                st.subheader("Daily sleep hours")
                if not sleep_df.empty:
                    sleep_chart_df = _prepare_sleep_dashboard_df(sleep_df)
                    accent = THEMES.get(st.session_state.theme, THEMES["Purple"])["primary"]
                    hours_fig = _sleep_hours_figure(sleep_chart_df, accent)
                    consistency_fig = _sleep_consistency_figure(sleep_chart_df)
                    heatmap_fig = _sleep_heatmap_figure(sleep_chart_df)
                    if hours_fig is not None:
                        st.plotly_chart(
                            hours_fig,
                            use_container_width=True,
                            key="analytics_sleep_hours_chart",
                        )
                    else:
                        fallback_hours = sleep_chart_df.groupby("Date", as_index=False)["Hours"].mean().sort_values("Date")
                        st.line_chart(fallback_hours.set_index("Date"))

                    if consistency_fig is not None:
                        st.plotly_chart(
                            consistency_fig,
                            use_container_width=True,
                            key="analytics_sleep_consistency_chart",
                        )

                    if heatmap_fig is not None:
                        st.plotly_chart(
                            heatmap_fig,
                            use_container_width=True,
                            key="analytics_sleep_heatmap_chart",
                        )
                else:
                    st.info("No sleep trend available.")

            st.divider()

            top1, top2 = st.columns(2)
            with top1:
                st.subheader("Top habits completed")
                if not habit_df.empty:
                    done_df = habit_df[habit_df["Completed"] == 1]
                    if not done_df.empty:
                        habit_counts = done_df["Habit"].value_counts().head(10).reset_index()
                        habit_counts.columns = ["Habit", "Completions"]
                        st.bar_chart(habit_counts.set_index("Habit"))
                    else:
                        st.info("No completed habits in selected window.")
                else:
                    st.info("No habit data yet.")

            with top2:
                st.subheader("Top mindfulness activities")
                if not activity_df.empty:
                    activity_counts = activity_df["Activity"].value_counts().head(10).reset_index()
                    activity_counts.columns = ["Activity", "Sessions"]
                    st.bar_chart(activity_counts.set_index("Activity"))
                else:
                    st.info("No activity data yet.")

            st.divider()
            st.subheader("Pattern detection")
            if snapshot["pattern_insights"]:
                for insight in snapshot["pattern_insights"]:
                    st.write(f"• {insight}")
            else:
                st.info("Not enough combined data for pattern detection yet.")

        with tab_export:
            st.subheader("Clinical-style report summary")
            st.caption("Export a concise summary with clear focus metrics for personal review or therapist discussions.")
            _render_report_header_card(st.session_state.user, report_days, scores, metrics)

            export_stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")

            summary_report = {
                "user": st.session_state.user,
                "generated_at": str(datetime.datetime.now()),
                "window_days": report_days,
                "scores": scores,
                "metrics": {
                    "mood_entries": len(history),
                    "mood_tracking_consistency": metrics["tracking_consistency"],
                    "avg_mood_intensity": scores["intensity_score"],
                    "avg_sleep_hours": round(metrics["avg_sleep"], 2),
                    "sleep_target_ratio": metrics["sleep_target_ratio"],
                    "low_mood_ratio": metrics["low_mood_ratio"],
                    "habit_completion_rate": metrics["habit_completion_rate"],
                    "habit_streak": metrics["habit_streak"],
                    "meditation_minutes": metrics["meditation_minutes"],
                    "coping_plan_ready": metrics["plan_ready"],
                },
                "focus_metrics": snapshot["focus_metrics"],
                "pattern_insights": snapshot["pattern_insights"],
                "recommendations": recommendations,
            }

            summary_text = (
                f"SereneMind Report\n"
                f"User: {st.session_state.user}\n"
                f"Generated: {datetime.datetime.now()}\n"
                f"Window: {report_days} days\n\n"
                f"Wellbeing Score: {scores['wellbeing_score']}/100\n"
                f"Mood tracking consistency: {metrics['tracking_consistency']}%\n"
                f"Low mood share: {metrics['low_mood_ratio']}%\n"
                f"Average sleep: {metrics['avg_sleep']:.1f}h\n"
                f"Sleep nights >= 7h: {metrics['sleep_target_ratio']}%\n"
                f"Habit completion rate: {metrics['habit_completion_rate']}%\n"
                f"Habit streak: {metrics['habit_streak']} days\n"
                f"Meditation minutes: {metrics['meditation_minutes']}\n"
                f"Coping Plan Ready: {'Yes' if metrics['plan_ready'] else 'No'}\n\n"
                f"Recommendations:\n- " + "\n- ".join(recommendations)
            )

            st.markdown("#### Clinical snapshot")
            snap1, snap2, snap3, snap4 = st.columns(4)
            with snap1:
                st.metric("Wellbeing", f"{scores['wellbeing_score']}/100", f"Window {report_days}d")
            with snap2:
                st.metric("Sleep target", f"{metrics['sleep_target_ratio']}%", ">= 7h nights")
            with snap3:
                st.metric("Habit adherence", f"{metrics['habit_completion_rate']}%", f"streak {metrics['habit_streak']}d")
            with snap4:
                st.metric("Low mood ratio", f"{metrics['low_mood_ratio']}%", "risk signal")

            st.markdown("#### Focus metrics")
            st.dataframe(pd.DataFrame(snapshot["focus_metrics"]), use_container_width=True, hide_index=True)

            st.markdown("#### Recommended actions")
            for idx, rec in enumerate(recommendations, start=1):
                st.markdown(
                        f"<div style='padding:12px 14px;border-radius:10px;margin:8px 0;background:linear-gradient(135deg,#fff9fb,#ffe4ec);border:1px solid rgba(244,114,182,0.16);color:#831843;box-shadow:0 1px 3px rgba(0,0,0,0.04);'><b style='color:#881337;'>Action {idx}.</b> {rec}</div>",
                    unsafe_allow_html=True,
                )

            ex1, ex2, ex3 = st.columns(3)
            with ex1:
                st.download_button(
                    "Download Summary (TXT)",
                    data=summary_text,
                    file_name=f"serenemind_summary_{export_stamp}.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
            with ex2:
                st.download_button(
                    "Download Summary (JSON)",
                    data=json.dumps(summary_report, indent=2, ensure_ascii=False),
                    file_name=f"serenemind_summary_{export_stamp}.json",
                    mime="application/json",
                    use_container_width=True,
                )
            with ex3:
                combined_frames = {
                    "mood": mood_df,
                    "sleep": sleep_df,
                    "meditation": meditation_df,
                    "habits": habit_df,
                    "activities": activity_df,
                }
                st.metric("Rows available", sum([len(df) for df in combined_frames.values()]))

            pdf_bytes = generate_pdf_report(summary_text)
            if pdf_bytes:
                st.download_button(
                    "Download Clinical PDF",
                    data=pdf_bytes,
                    file_name=f"serenemind_report_{export_stamp}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
            else:
                st.warning("PDF export requires fpdf2. Install dependencies to enable this option.")

            st.divider()
            st.markdown("#### Export Raw CSV Files")

            csv_col1, csv_col2, csv_col3, csv_col4, csv_col5 = st.columns(5)
            with csv_col1:
                st.download_button(
                    "Mood CSV",
                    data=mood_df.to_csv(index=False),
                    file_name=f"mindwell_mood_{export_stamp}.csv",
                    mime="text/csv",
                    use_container_width=True,
                    disabled=mood_df.empty,
                )
            with csv_col2:
                st.download_button(
                    "Sleep CSV",
                    data=sleep_df.to_csv(index=False),
                    file_name=f"mindwell_sleep_{export_stamp}.csv",
                    mime="text/csv",
                    use_container_width=True,
                    disabled=sleep_df.empty,
                )
            with csv_col3:
                st.download_button(
                    "Meditation CSV",
                    data=meditation_df.to_csv(index=False),
                    file_name=f"mindwell_meditation_{export_stamp}.csv",
                    mime="text/csv",
                    use_container_width=True,
                    disabled=meditation_df.empty,
                )
            with csv_col4:
                st.download_button(
                    "Habits CSV",
                    data=habit_df.to_csv(index=False),
                    file_name=f"mindwell_habits_{export_stamp}.csv",
                    mime="text/csv",
                    use_container_width=True,
                    disabled=habit_df.empty,
                )
            with csv_col5:
                st.download_button(
                    "Activities CSV",
                    data=activity_df.to_csv(index=False),
                    file_name=f"mindwell_activities_{export_stamp}.csv",
                    mime="text/csv",
                    use_container_width=True,
                    disabled=activity_df.empty,
                )

    # ===============================
    # SETTINGS
    # ===============================
    elif option == "Settings":
        st.title("⚙️ Settings")
        
        st.subheader("🎨 Theme Preferences")
        col1, col2 = st.columns(2)
        with col1:
            theme_names = list(THEMES.keys())
            current_index = theme_names.index(st.session_state.theme) if st.session_state.theme in theme_names else 0
            selected_theme = st.selectbox("Choose your theme:", theme_names, index=current_index)
            
            if selected_theme != st.session_state.theme:
                st.session_state.theme = selected_theme
                st.success(f"✅ Theme changed to {selected_theme}!")
                st.rerun()
        
        with col2:
            st.markdown("**Available Themes:**")
            for theme_name in theme_names:
                st.caption(f"🎨 {theme_name}")

        st.divider()
        st.subheader("📱 Contact Details")

        current_phone = get_user_phone(st.session_state.user)

        contact_phone = st.text_input("Phone number (E.164)", value=current_phone, placeholder="+40700111222")

        if st.button("Save Contact Details", use_container_width=True):
            phone_clean = normalize_phone(contact_phone)
            if phone_clean and not phone_clean.startswith("+"):
                st.error("Phone should use E.164 format (example: +40700111222)")
            else:
                try:
                    c.execute(
                        "UPDATE users SET phone=? WHERE username=?",
                        (phone_clean if phone_clean else None, st.session_state.user),
                    )
                    conn.commit()
                    st.success("Phone saved!")
                except Exception as error:
                    st.error(f"Error: {error}")

        st.divider()
        st.subheader("📬 Delivery Log")
        logs = get_notification_logs(st.session_state.user, 50)
        if logs:
            logs_df = pd.DataFrame(
                logs,
                columns=["ID", "Channel", "Recipient", "Subject", "Status", "Details", "CreatedAt"],
            )
            st.dataframe(logs_df[["CreatedAt", "Channel", "Recipient", "Status", "Details"]], use_container_width=True)
        else:
            st.info("No notifications sent yet.")

        st.divider()
        st.subheader("🔐 Data & Privacy")

        export_payload = export_all_user_data(st.session_state.user)
        st.download_button(
            "Export All My Data (JSON)",
            data=json.dumps(export_payload, indent=2, ensure_ascii=False),
            file_name=f"serenemind_full_export_{st.session_state.user}_{datetime.date.today()}.json",
            mime="application/json",
            use_container_width=True,
        )

        st.warning("Danger Zone: this action permanently deletes your account and all personal data.")
        confirm_delete_text = st.text_input("Type DELETE to confirm account deletion")
        if st.button("Delete Account and All Data", use_container_width=True):
            if confirm_delete_text == "DELETE":
                delete_user_account_and_data(st.session_state.user)
                st.session_state.user = None
                st.success("Your account and data were deleted.")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Type DELETE exactly to confirm.")
        
        st.divider()
        
        st.subheader("About SereneMind")
        st.markdown("""
        **SereneMind** is your personal mental health companion, designed to support your emotional wellness journey.
        
        Features:
        - 😊 Comprehensive mood tracking
        - 💤 Sleep monitoring
        - 🧘 Meditation & breathing exercises
        - 📝 Gratitude journaling
        - 🎯 Goal setting
        - 📊 Advanced analytics
        - ✨ Daily affirmations
        - 🎨 Customizable themes
        
        Remember: This app is not a replacement for professional mental health care.
        If you're struggling, please reach out to a mental health professional.
        """)
