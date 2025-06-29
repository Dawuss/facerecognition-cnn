import streamlit as st
import mysql.connector
from mysql.connector import Error
import bcrypt
import secrets
from datetime import datetime, timedelta
import time


def apply_inline_styles():
    css = """
    body {
        background-color: #311B92;
    }
    .stButton>button {
        color: white;
        background-color: #007bff;
    }
    """
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    
# Konfigurasi database
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'sistem_presensi'
}


def get_db_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        st.error(f"Database connection error: {e}")
        return None

def verify_user_and_create_token(username, password, role):
    conn = get_db_connection()
    if not conn:
        return None, None
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s AND role=%s", (username, role))
    user = cursor.fetchone()
    if not user:
        cursor.close()
        conn.close()
        return None, None

    hashed_pw = user['password'].encode('utf-8')
    if not bcrypt.checkpw(password.encode('utf-8'), hashed_pw):
        cursor.close()
        conn.close()
        return None, None

    token = secrets.token_urlsafe(32)
    token_hash = bcrypt.hashpw(token.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    expired_at = datetime.now() + timedelta(days=1)

    cursor.execute(
        "INSERT INTO user_tokens (user_id, token_hash, expired_at) VALUES (%s, %s, %s)",
        (user['id'], token_hash, expired_at)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return user, token

def logout():
    if "user" in st.session_state and "token" in st.session_state:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            user_id = st.session_state['user']['id']
            token_plain = st.session_state['token']
            cursor.execute("SELECT id, token_hash FROM user_tokens WHERE user_id=%s", (user_id,))
            tokens = cursor.fetchall()
            for t in tokens:
                token_hash = t[1].encode('utf-8')
                if bcrypt.checkpw(token_plain.encode('utf-8'), token_hash):
                    cursor.execute("DELETE FROM user_tokens WHERE id=%s", (t[0],))
                    conn.commit()
                    break
            cursor.close()
            conn.close()

        del st.session_state['user']
        del st.session_state['token']
        if 'page' in st.session_state:
            del st.session_state['page']
        st.success("Logout berhasil.")
        st.rerun()

def main():
    apply_inline_styles()
    # Jika sudah login, langsung navigasi halaman sesuai role
    if "user" in st.session_state and "page" in st.session_state:
        role = st.session_state['page']
        
        st.sidebar.title(f"Selamat datang, {st.session_state['user']['nama_lengkap']}")

        # Import dan jalankan halaman sesuai role
        if role == "admin":
            import admin
            admin.main()
            return
        elif role == "dosen":
            import dosen
            dosen.main()
            return
        elif role == "mahasiswa":
            import app
            app.main()
            return

    # Belum login, tampilkan form login
    st.title("🔐 Login Sistem Presensi")

    role = st.selectbox("Login sebagai", ["admin", "dosen", "mahasiswa"], key="role_select")
    username = st.text_input("Username", key="username_input")
    password = st.text_input("Password", type="password", key="password_input")

    if st.button("Login", key="login_btn"):
        if not username or not password:
            st.error("Username dan password wajib diisi.")
            return
        
        with st.spinner("Memverifikasi login..."):
            time.sleep(2)  # Simulate loading process
            user, token = verify_user_and_create_token(username, password, role)
        
        if user:
            st.success(f"Selamat datang, {user['nama_lengkap']}!")
            st.session_state['user'] = user
            st.session_state['token'] = token
            st.session_state['page'] = role
            st.rerun()
        else:
            st.error("Login gagal. Periksa username, password, dan role Anda.")

if __name__ == "__main__":
    main()
