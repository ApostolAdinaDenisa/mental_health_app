import streamlit as st
import sqlite3
import datetime
import random

# ===============================
# CONFIG
# ===============================

st.set_page_config(
    page_title="Mental Health App",
    page_icon="💗",
    layout="centered"
)

# CSS Pink Theme
st.markdown("""
<style>
body {
    background-color: #ffe6f2;
}

.stButton > button {
    background-color: #ff69b4;
    color: white;
    border-radius: 10px;
}

h1, h2, h3 {
    color: #d63384;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# DATABASE
# ===============================

conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT PRIMARY KEY,
    password TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS moods(
    username TEXT,
    mood TEXT,
    date TEXT
)
""")

conn.commit()

# ===============================
# FUNCTIONS
# ===============================

def register(username, password):
    c.execute("INSERT INTO users VALUES (?,?)", (username, password))
    conn.commit()


def login(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username, password))
    return c.fetchone()


def save_mood(user, mood):
    date = str(datetime.date.today())
    c.execute("INSERT INTO moods VALUES (?,?,?)", (user, mood, date))
    conn.commit()


def get_history(user):
    c.execute("SELECT * FROM moods WHERE username=?", (user,))
    return c.fetchall()


# ===============================
# SESSION
# ===============================

if "user" not in st.session_state:
    st.session_state.user = None

# ===============================
# LOGIN / REGISTER
# ===============================

if st.session_state.user is None:

    st.title("💗 Mental Health App")

    menu = st.selectbox("Alege:", ["Login", "Register"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if menu == "Register":
        if st.button("Creează cont"):
            try:
                register(username, password)
                st.success("Cont creat! Acum te poți loga.")
            except:
                st.error("Username deja folosit!")

    if menu == "Login":
        if st.button("Login"):
            user = login(username, password)

            if user:
                st.session_state.user = username
                st.success("Bine ai venit!")
                st.experimental_rerun()
            else:
                st.error("Date greșite!")

# ===============================
# MAIN APP
# ===============================

else:

    st.sidebar.title(f"👤 {st.session_state.user}")

    option = st.sidebar.selectbox(
        "Meniu",
        ["Dashboard", "Stare", "Quiz", "Jocuri", "Rapoarte", "Logout"]
    )

    # ===============================
    # DASHBOARD
    # ===============================
    if option == "Dashboard":

        st.title("🌸 Dashboard")

        history = get_history(st.session_state.user)

        if len(history) == 0:
            st.info("Welcome! Completează prima ta stare 💗")
        else:
            st.success("Bine ai revenit!")
            st.write("Ultimele stări:")

            for h in history[-5:]:
                st.write(f"📅 {h[2]} → {h[1]}")

    # ===============================
    # MOOD
    # ===============================
    elif option == "Stare":

        st.title("📝 Cum te simți azi?")

        mood = st.selectbox(
            "Alege starea:",
            ["Fericit 😊", "Calm 😌", "Trist 😢", "Stresat 😰", "Obosit 😴"]
        )

        if st.button("Salvează"):
            save_mood(st.session_state.user, mood)
            st.success("Stare salvată!")

    # ===============================
    # QUIZ
    # ===============================
    elif option == "Quiz":

        st.title("📊 Mini Quiz")

        q1 = st.radio("Cum a fost ziua ta?", ["Bună", "Ok", "Grea"])
        q2 = st.radio("Ai dormit bine?", ["Da", "Nu"])
        q3 = st.radio("Nivel stres:", ["Mic", "Mediu", "Mare"])

        if st.button("Trimite"):
            st.success("Mulțumim pentru răspuns! 💗")

    # ===============================
    # GAMES
    # ===============================
    elif option == "Jocuri":

        st.title("🎮 Jocuri Relaxare")

        game = st.selectbox(
            "Alege joc:",
            ["Respirație", "Recunoștință", "Afirmații"]
        )

        # Breathing
        if game == "Respirație":

            st.write("Inspiră... 4 secunde")
            st.write("Ține... 4 secunde")
            st.write("Expiră... 6 secunde")

            st.button("Repetă")

        # Gratitude
        elif game == "Recunoștință":

            st.write("Scrie 3 lucruri pentru care ești recunoscător:")

            g1 = st.text_input("1")
            g2 = st.text_input("2")
            g3 = st.text_input("3")

            if st.button("Salvează"):
                st.success("Minunat! 💗")

        # Affirmations
        elif game == "Afirmații":

            affirmations = [
                "Ești suficient 💗",
                "Meriți fericire 🌸",
                "Ești puternic 💪",
                "Totul va fi bine ✨"
            ]

            if st.button("Primește mesaj"):
                st.success(random.choice(affirmations))

    # ===============================
    # REPORTS
    # ===============================
    elif option == "Rapoarte":

        st.title("📈 Rapoarte")

        history = get_history(st.session_state.user)

        if len(history) == 0:
            st.info("Nu există date încă.")
        else:
            st.write("Istoric complet:")

            for h in history:
                st.write(f"{h[2]} → {h[1]}")

            if st.button("Distribuie raport"):
                st.success("Raport generat! (simulat) 📤")

    # ===============================
    # LOGOUT
    # ===============================
    elif option == "Logout":

        st.session_state.user = None
        st.experimental_rerun()
