import streamlit as st
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import bcrypt
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
from fpdf import FPDF

# Konfigurasi database
DB_CONFIG = {
    'host': 'https://risky-cnn.streamlit.app/',
    'user': 'u1362490_d4u5',
    'password': 'h9Di8%*1IPL2',
    'database': 'u1362490_sistem_presensi'
}

def get_db_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        st.error(f"Database connection error: {e}")
        return None

def validate_token(user_id, token_plain):
    conn = get_db_connection()
    if not conn:
        return False
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT token_hash, expired_at FROM user_tokens WHERE user_id=%s", (user_id,))
    tokens = cursor.fetchall()
    cursor.close()
    conn.close()
    now = datetime.now()
    for t in tokens:
        if t['expired_at'] is None or t['expired_at'] > now:
            token_hash = t['token_hash'].encode('utf-8')
            if bcrypt.checkpw(token_plain.encode('utf-8'), token_hash):
                return True
    return False

def check_login():
    if "user" not in st.session_state or "token" not in st.session_state:
        st.error("Silakan login terlebih dahulu.")
        st.stop()
    user = st.session_state['user']
    token = st.session_state['token']
    if not validate_token(user['id'], token):
        st.error("Sesi Anda tidak valid atau sudah kadaluarsa. Silakan login ulang.")
        logout()
        st.stop()
    if user['role'] != 'admin':
        st.error("Anda tidak memiliki akses ke halaman ini.")
        st.stop()

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


def fetch_attendance_per_day():
    conn = get_db_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.tanggal, COUNT(*) AS jumlah_hadir
        FROM presensi p
        GROUP BY p.tanggal
        ORDER BY p.tanggal
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def fetch_total_courses():
    conn = get_db_connection()
    if not conn:
        return 0
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) AS total FROM matakuliah")
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return data['total']

def fetch_total_classes():
    conn = get_db_connection()
    if not conn:
        return 0
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) AS total FROM kelas")
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return data['total']

def fetch_total_students():
    conn = get_db_connection()
    if not conn:
        return 0
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) AS total FROM mahasiswa")
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return data['total']
    

def fetch_total_lecturers():
    conn = get_db_connection()
    if not conn:
        return 0
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) AS total FROM users WHERE role='dosen'")
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return data['total']

def dashboard():
    
    st.title("Dashboard Analitik")

    # Fetch the data
    attendance_per_day = fetch_attendance_per_day()
    total_courses = fetch_total_courses()
    total_classes = fetch_total_classes()
    total_students = fetch_total_students()
    total_lecturers = fetch_total_lecturers()

    # Display total counts
    st.subheader("Total Statistik")
    cols = st.columns(4)
    cols[0].metric("Total Mata Kuliah", total_courses)
    cols[1].metric("Total Kelas", total_classes)
    cols[2].metric("Total Mahasiswa", total_students)
    cols[3].metric("Total Dosen", total_lecturers)

    # Display Attendance per Day as a Bar Chart
    st.subheader("Kehadiran Per Hari")

    if attendance_per_day:
        # Data for the Bar chart
        dates = [data['tanggal'] for data in attendance_per_day]
        hadir = [data['jumlah_hadir'] for data in attendance_per_day]

        # Create a bar chart
        plt.figure(figsize=(10, 6))
        plt.bar(dates, hadir, color='skyblue')
        plt.xlabel('Tanggal')
        plt.ylabel('Jumlah Kehadiran')
        plt.title('Jumlah Kehadiran Per Hari')
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Show the chart in Streamlit
        st.pyplot(plt)
    else:
        st.info("Tidak ada data kehadiran.")


def fetch_users():
    conn = get_db_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, username, role, nama_lengkap, email FROM users ORDER BY id")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users

def add_user(username, password, role, nama_lengkap, email):
    conn = get_db_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        cursor.execute(
            "INSERT INTO users (username, password, role, nama_lengkap, email) VALUES (%s, %s, %s, %s, %s)",
            (username, hashed_pw.decode(), role, nama_lengkap, email)
        )
        conn.commit()
        return True
    except mysql.connector.IntegrityError:
        st.error("Username sudah digunakan!")
        return False
    finally:
        cursor.close()
        conn.close()

def update_user(user_id, username, role, nama_lengkap, email, password=None):
    conn = get_db_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    
    # Jika password diberikan, masukkan password baru
    if password:
        try:
            cursor.execute(
                "UPDATE users SET username=%s, role=%s, nama_lengkap=%s, email=%s, password=%s WHERE id=%s",
                (username, role, nama_lengkap, email, password, user_id)
            )
            conn.commit()
            return True
        except Exception as e:
            st.error(f"Gagal update user: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    else:
        # Jika password tidak diberikan, hanya update kolom lainnya
        try:
            cursor.execute(
                "UPDATE users SET username=%s, role=%s, nama_lengkap=%s, email=%s WHERE id=%s",
                (username, role, nama_lengkap, email, user_id)
            )
            conn.commit()
            return True
        except Exception as e:
            st.error(f"Gagal update user: {e}")
            return False
        finally:
            cursor.close()
            conn.close()


def delete_user(user_id):
    conn = get_db_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return True

def kelola_user():
    users = fetch_users()
    if not users:
        st.info("Belum ada user.")
        return

    if "show_add_form" not in st.session_state:
        st.session_state.show_add_form = False
    if "show_edit_form" not in st.session_state:
        st.session_state.show_edit_form = False
    if "edit_user_id" not in st.session_state:
        st.session_state.edit_user_id = None

    st.title("Daftar User")

    if not st.session_state.show_add_form:
        if st.button("➕ Tambah User"):
            st.session_state.show_add_form = True
            st.rerun()
        st.markdown("---")
     # Define the headers
        col0, col1, col2, col3, col4, col5 = st.columns([1, 3, 2, 3, 3, 1.5])

        # Set column headers
        col0.markdown("<h6 style='text-align: left;'>ID</h6>", unsafe_allow_html=True)
        col1.markdown("<h6 style='text-align: left;'>Username</h6>", unsafe_allow_html=True)
        col2.markdown("<h6 style='text-align: left;'>Role</h6>", unsafe_allow_html=True)
        col3.markdown("<h6 style='text-align: left;'>Nama</h6>", unsafe_allow_html=True)
        col4.markdown("<h6 style='text-align: left;'>Email</h6>", unsafe_allow_html=True)
        col5.markdown("<h6 style='text-align: left;'>Operasi</h6>", unsafe_allow_html=True)
    

    for user in users:
        cols = st.columns([1, 3, 2, 3, 3, 1.5])
        cols[0].write(user['id'])
        cols[1].write(user['username'])
        cols[2].write(user['role'].capitalize())
        cols[3].write(user['nama_lengkap'])
        cols[4].write(user['email'] if user['email'] else "-")

        with cols[5]:
            col_edit, col_del = st.columns(2)
            if col_edit.button("✏️", key=f"edit_{user['id']}"):
                st.session_state.show_edit_form = True
                st.session_state.edit_user_id = user['id']
                st.rerun()
            if col_del.button("🗑️", key=f"delete_{user['id']}"):
                if delete_user(user['id']):
                    st.success(f"User {user['username']} berhasil dihapus.")
                    st.rerun()
                else:
                    st.error("Gagal hapus user.")

    st.markdown("---")

    if st.session_state.show_add_form:
        st.subheader("Tambah User Baru")
        with st.form("form_tambah_user", clear_on_submit=True):
            username = st.text_input("Username", max_chars=50)
            password = st.text_input("Password", type="password")
            role = st.selectbox("Role", options=["mahasiswa", "dosen", "admin"])
            nama_lengkap = st.text_input("Nama Lengkap")
            email = st.text_input("Email (opsional)")
            submit = st.form_submit_button("Tambah User")
            cancel = st.form_submit_button("Batal")

            if submit:
                if not username or not password or not role or not nama_lengkap:
                    st.error("Username, password, role, dan nama lengkap wajib diisi.")
                else:
                    if add_user(username, password, role, nama_lengkap, email):
                        st.success(f"User {username} berhasil ditambahkan.")
                        st.session_state.show_add_form = False
                        st.rerun()
            if cancel:
                st.session_state.show_add_form = False
                st.rerun()

    if st.session_state.show_edit_form:
        user_id = st.session_state.edit_user_id
        user_edit = next((u for u in users if u['id'] == user_id), None)
        if user_edit:
            st.subheader(f"Edit User: {user_edit['username']}")
            with st.form("form_edit_user", clear_on_submit=False):
                username = st.text_input("Username", value=user_edit['username'], max_chars=50)
                role = st.selectbox("Role", options=["mahasiswa", "dosen", "admin"], index=["mahasiswa","dosen","admin"].index(user_edit['role']))
                nama_lengkap = st.text_input("Nama Lengkap", value=user_edit['nama_lengkap'])
                email = st.text_input("Email (opsional)", value=user_edit['email'] if user_edit['email'] else "")
                
                # Adding the password field for editing
                password = st.text_input("Password Baru (Kosongkan jika tidak ingin mengganti)", type="password")

                submit = st.form_submit_button("Update User")
                cancel = st.form_submit_button("Batal")

                if submit:
                    if not username or not role or not nama_lengkap:
                        st.error("Username, role, dan nama lengkap wajib diisi.")
                    else:
                        # Hash password if provided
                        if password:
                            hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                            update_data = (username, role, nama_lengkap, email, user_id, hashed_pw.decode())
                            update_query = "UPDATE users SET username=%s, role=%s, nama_lengkap=%s, email=%s, password=%s WHERE id=%s"
                        else:
                            update_data = (username, role, nama_lengkap, email, user_id)
                            update_query = "UPDATE users SET username=%s, role=%s, nama_lengkap=%s, email=%s WHERE id=%s"
                        
                        if update_user(user_id, username, role, nama_lengkap, email, password=hashed_pw if password else None):
                            st.success(f"User {username} berhasil diperbarui.")
                            st.session_state.show_edit_form = False
                            st.session_state.edit_user_id = None
                            st.rerun()
                if cancel:
                    st.session_state.show_edit_form = False
                    st.session_state.edit_user_id = None
                    st.rerun()

def fetch_dosen():
    conn = get_db_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nama_lengkap FROM users WHERE role = 'dosen' ORDER BY nama_lengkap")
    dosen_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return dosen_list

def fetch_mata_kuliah_with_dosen():
    conn = get_db_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT m.id_mk AS id, m.kode, m.nama, u.nama_lengkap AS nama_dosen
        FROM matakuliah m
        JOIN users u ON m.dosen_id = u.id
        ORDER BY m.id_mk
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def add_mata_kuliah(kode, nama, dosen_id):
    conn = get_db_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO matakuliah (kode, nama, dosen_id) VALUES (%s, %s, %s)",
            (kode, nama, dosen_id)
        )
        conn.commit()
        return True
    except mysql.connector.IntegrityError as e:
        st.error(f"Gagal menambahkan mata kuliah: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def update_mata_kuliah(mk_id, kode, nama, dosen_id):
    conn = get_db_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE matakuliah SET kode=%s, nama=%s, dosen_id=%s WHERE id_mk=%s",
            (kode, nama, dosen_id, mk_id)
        )
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Gagal update mata kuliah: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def delete_mata_kuliah(mk_id):
    conn = get_db_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM matakuliah WHERE id_mk=%s", (mk_id,))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Gagal hapus mata kuliah: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def fetch_daftar_kelas_by_date(tanggal):
    conn = get_db_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT dk.id AS daftar_kelas_id, 
               CONCAT(k.semester, ' ', k.nama_kelas) AS kode_kelas, 
               m.nama AS mata_kuliah
        FROM daftar_kelas dk
        JOIN matakuliah m ON dk.matakuliah_id = m.id_mk
        JOIN kelas k ON dk.kelas_id = k.id
        WHERE dk.tanggal = %s
        ORDER BY m.nama
    """, (tanggal,))
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return res


def kelola_mata_kuliah():
    mata_kuliah_list = fetch_mata_kuliah_with_dosen()
    dosen_list = fetch_dosen()
    dosen_dict = {d['nama_lengkap']: d['id'] for d in dosen_list}
    dosen_nama_list = list(dosen_dict.keys())

    if "show_add_form_mk" not in st.session_state:
        st.session_state.show_add_form_mk = False
    if "show_edit_form_mk" not in st.session_state:
        st.session_state.show_edit_form_mk = False
    if "edit_mk_id" not in st.session_state:
        st.session_state.edit_mk_id = None

    st.title("Kelola Mata Kuliah")

    if not st.session_state.show_add_form_mk:
        if st.button("➕ Tambah Mata Kuliah"):
            st.session_state.show_add_form_mk = True
            st.rerun()
    
        
        st.markdown("---")
     # Define the headers
        col0, col1, col2, col3, col4 = st.columns([1, 2, 3, 3, 1.5])

        # Set column headers
        col0.markdown("<h6 style='text-align: left;'>ID</h6>", unsafe_allow_html=True)
        col1.markdown("<h6 style='text-align: left;'>Kode</h6>", unsafe_allow_html=True)
        col2.markdown("<h6 style='text-align: left;'>Mata Kuliah</h6>", unsafe_allow_html=True)
        col3.markdown("<h6 style='text-align: left;'>Dosen</h6>", unsafe_allow_html=True)
        col4.markdown("<h6 style='text-align: left;'>Operasi</h6>", unsafe_allow_html=True)

    if mata_kuliah_list:
        for mk in mata_kuliah_list:
            cols = st.columns([1, 2, 3, 3, 1.5])
            cols[0].write(mk['id'])
            cols[1].write(mk['kode'])
            cols[2].write(mk['nama'])
            cols[3].write(mk['nama_dosen'])
            with cols[4]:
                col_edit, col_del = st.columns(2)
                if col_edit.button("✏️", key=f"edit_mk_{mk['id']}"):
                    st.session_state.show_edit_form_mk = True
                    st.session_state.edit_mk_id = mk['id']
                    st.rerun()
                if col_del.button("🗑️", key=f"delete_mk_{mk['id']}"):
                    if delete_mata_kuliah(mk['id']):
                        st.success(f"Mata kuliah {mk['nama']} berhasil dihapus.")
                        st.rerun()
                    else:
                        st.error("Gagal hapus mata kuliah.")
    else:
        st.info("Belum ada mata kuliah yang terdaftar.")

    st.markdown("---")

    if st.session_state.show_add_form_mk:
        st.subheader("Tambah Mata Kuliah Baru")
        with st.form("form_tambah_mk", clear_on_submit=True):
            kode = st.text_input("Kode Mata Kuliah", max_chars=20)
            nama = st.text_input("Nama Mata Kuliah", max_chars=100)
            dosen_nama = st.selectbox("Pilih Dosen", options=dosen_nama_list)
            submit = st.form_submit_button("Tambah Mata Kuliah")
            cancel = st.form_submit_button("Batal")

            if submit:
                if not kode or not nama or not dosen_nama:
                    st.error("Semua field wajib diisi.")
                else:
                    dosen_id = dosen_dict[dosen_nama]
                    if add_mata_kuliah(kode, nama, dosen_id):
                        st.success(f"Mata kuliah {nama} berhasil ditambahkan.")
                        st.session_state.show_add_form_mk = False
                        st.rerun()
            if cancel:
                st.session_state.show_add_form_mk = False
                st.rerun()

    if st.session_state.show_edit_form_mk:
        mk_id = st.session_state.edit_mk_id
        mk_edit = next((m for m in mata_kuliah_list if m['id'] == mk_id), None)
        if mk_edit:
            st.subheader(f"Edit Mata Kuliah: {mk_edit['nama']}")
            with st.form("form_edit_mk", clear_on_submit=False):
                kode = st.text_input("Kode Mata Kuliah", value=mk_edit['kode'], max_chars=20)
                nama = st.text_input("Nama Mata Kuliah", value=mk_edit['nama'], max_chars=100)
                dosen_nama_sel = mk_edit['nama_dosen']
                index_dosen = dosen_nama_list.index(dosen_nama_sel) if dosen_nama_sel in dosen_nama_list else 0
                dosen_nama = st.selectbox("Pilih Dosen", options=dosen_nama_list, index=index_dosen)
                submit = st.form_submit_button("Update Mata Kuliah")
                cancel = st.form_submit_button("Batal")

                if submit:
                    if not kode or not nama or not dosen_nama:
                        st.error("Semua field wajib diisi.")
                    else:
                        dosen_id = dosen_dict[dosen_nama]
                        if update_mata_kuliah(mk_id, kode, nama, dosen_id):
                            st.success(f"Mata kuliah {nama} berhasil diperbarui.")
                            st.session_state.show_edit_form_mk = False
                            st.session_state.edit_mk_id = None
                            st.rerun()
                if cancel:
                    st.session_state.show_edit_form_mk = False
                    st.session_state.edit_mk_id = None
                    st.rerun()

def fetch_kelas():
    conn = get_db_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM kelas ORDER BY id")
    kelas = cursor.fetchall()
    cursor.close()
    conn.close()
    return kelas

def add_kelas(nama_kelas, semester):
    conn = get_db_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO kelas (nama_kelas, semester) VALUES (%s, %s)",
            (nama_kelas, semester)
        )
        conn.commit()
        return True
    except mysql.connector.IntegrityError as e:
        st.error(f"Gagal menambah kelas: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def update_kelas(kelas_id, nama_kelas, semester):
    conn = get_db_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE kelas SET nama_kelas=%s, semester=%s WHERE id=%s",
            (nama_kelas, semester, kelas_id)
        )
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Gagal update kelas: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def delete_kelas(kelas_id):
    conn = get_db_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM kelas WHERE id=%s", (kelas_id,))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Gagal hapus kelas: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def kelola_kelas():
    st.title("Kelola Kelas")

    if "show_add_form_kelas" not in st.session_state:
        st.session_state.show_add_form_kelas = False
    if "show_edit_form_kelas" not in st.session_state:
        st.session_state.show_edit_form_kelas = False
    if "edit_kelas_id" not in st.session_state:
        st.session_state.edit_kelas_id = None

    kelas_list = fetch_kelas()

    if not st.session_state.show_add_form_kelas:
        if st.button("➕ Tambah Kelas"):
            st.session_state.show_add_form_kelas = True
            st.rerun()
        
        st.markdown("---")
     # Define the headers
        col0, col1, col2, col3 = st.columns([1, 3, 2, 1.5])

        # Set column headers
        col0.markdown("<h6 style='text-align: left;'>ID</h6>", unsafe_allow_html=True)
        col1.markdown("<h6 style='text-align: left;'>Kelas</h6>", unsafe_allow_html=True)
        col2.markdown("<h6 style='text-align: left;'>Semester</h6>", unsafe_allow_html=True)
        col3.markdown("<h6 style='text-align: left;'>Operasi</h6>", unsafe_allow_html=True)
    
    if kelas_list:
        for k in kelas_list:
            cols = st.columns([1, 3, 2, 1.5])
            cols[0].write(k['id'])
            cols[1].write(k['nama_kelas'])
            cols[2].write(k['semester'])
            with cols[3]:
                col_edit, col_del = st.columns(2)
                if col_edit.button("✏️", key=f"edit_kelas_{k['id']}"):
                    st.session_state.show_edit_form_kelas = True
                    st.session_state.edit_kelas_id = k['id']
                    st.rerun()
                if col_del.button("🗑️", key=f"delete_kelas_{k['id']}"):
                    if delete_kelas(k['id']):
                        st.success(f"Kelas {k['nama_kelas']} berhasil dihapus.")
                        st.rerun()
                    else:
                        st.error("Gagal hapus kelas.")

    st.markdown("---")
    # Add form
    if st.session_state.show_add_form_kelas:
        st.subheader("Tambah Kelas Baru")
        with st.form("form_tambah_kelas", clear_on_submit=True):
            nama_kelas = st.text_input("Nama Kelas")
            semester = st.number_input("Semester", min_value=1, step=1)
            submit = st.form_submit_button("Tambah Kelas")
            cancel = st.form_submit_button("Batal")

            if submit:
                if not nama_kelas or not semester:
                    st.error("Nama kelas dan semester wajib diisi.")
                else:
                    if add_kelas(nama_kelas, semester):
                        st.success(f"Kelas {nama_kelas} berhasil ditambahkan.")
                        st.session_state.show_add_form_kelas = False
                        st.rerun()
            if cancel:
                st.session_state.show_add_form_kelas = False
                st.rerun()

    # Edit form
    if st.session_state.show_edit_form_kelas:
        kelas_id = st.session_state.edit_kelas_id
        k_edit = next((k for k in kelas_list if k['id'] == kelas_id), None)
        if k_edit:
            st.subheader(f"Edit Kelas: {k_edit['nama_kelas']}")
            with st.form("form_edit_kelas", clear_on_submit=False):
                nama_kelas = st.text_input("Nama Kelas", value=k_edit['nama_kelas'])
                semester = st.number_input("Semester", min_value=1, value=k_edit['semester'], step=1)
                submit = st.form_submit_button("Update Kelas")
                cancel = st.form_submit_button("Batal")

                if submit:
                    if not nama_kelas or not semester:
                        st.error("Nama kelas dan semester wajib diisi.")
                    else:
                        if update_kelas(kelas_id, nama_kelas, semester):
                            st.success(f"Kelas {nama_kelas} berhasil diperbarui.")
                            st.session_state.show_edit_form_kelas = False
                            st.session_state.edit_kelas_id = None
                            st.rerun()
                if cancel:
                    st.session_state.show_edit_form_kelas = False
                    st.session_state.edit_kelas_id = None
                    st.rerun()


def fetch_mahasiswa():
    conn = get_db_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT m.*, k.nama_kelas
        FROM mahasiswa m
        JOIN kelas k ON m.kelas_id = k.id
        ORDER BY m.id_mahasiswa
    """)
    mahasiswa = cursor.fetchall()
    cursor.close()
    conn.close()
    return mahasiswa

def add_mahasiswa(id_mahasiswa, nama_mahasiswa, kelas_id, semester):
    conn = get_db_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO mahasiswa (id_mahasiswa, nama_mahasiswa, kelas_id, semester) VALUES (%s, %s, %s, %s)",
            (id_mahasiswa, nama_mahasiswa, kelas_id, semester)
        )
        conn.commit()
        return True
    except mysql.connector.IntegrityError as e:
        st.error(f"Gagal menambah mahasiswa: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def update_mahasiswa(id_mahasiswa, nama_mahasiswa, kelas_id, semester):
    conn = get_db_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE mahasiswa SET nama_mahasiswa=%s, kelas_id=%s, semester=%s WHERE id_mahasiswa=%s",
            (nama_mahasiswa, kelas_id, semester, id_mahasiswa)
        )
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Gagal update mahasiswa: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def delete_mahasiswa(id_mahasiswa):
    conn = get_db_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM mahasiswa WHERE id_mahasiswa=%s", (id_mahasiswa,))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Gagal hapus mahasiswa: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def kelola_mahasiswa():
    st.title("Kelola Mahasiswa")

    if "show_add_form_mhs" not in st.session_state:
        st.session_state.show_add_form_mhs = False
    if "show_edit_form_mhs" not in st.session_state:
        st.session_state.show_edit_form_mhs = False
    if "edit_mhs_id" not in st.session_state:
        st.session_state.edit_mhs_id = None

    mahasiswa_list = fetch_mahasiswa()
    kelas_list = fetch_kelas()
    kelas_options = {f"{k['nama_kelas']} (Semester {k['semester']})": k['id'] for k in kelas_list}
    
    if not st.session_state.show_add_form_mhs:
        if st.button("➕ Tambah Mahasiswa"):
            st.session_state.show_add_form_mhs = True
            st.rerun()

        st.markdown("---")
     # Define the headers
        col0, col1, col2, col3, col4 = st.columns([2, 4, 2, 2, 2])

        # Set column headers
        col0.markdown("<h6 style='text-align: left;'>NIM</h6>", unsafe_allow_html=True)
        col1.markdown("<h6 style='text-align: left;'>Nama</h6>", unsafe_allow_html=True)
        col2.markdown("<h6 style='text-align: left;'>Kelas</h6>", unsafe_allow_html=True)
        col3.markdown("<h6 style='text-align: left;'>Semester</h6>", unsafe_allow_html=True)
        col4.markdown("<h6 style='text-align: left;'>Operasi</h6>", unsafe_allow_html=True)
    
    if mahasiswa_list:
        for m in mahasiswa_list:
            cols = st.columns([2, 4, 2, 2, 2])
            cols[0].write(m['id_mahasiswa'])
            cols[1].write(m['nama_mahasiswa'])
            cols[2].write(m['nama_kelas'])
            cols[3].write(m['semester'])
            with cols[4]:
                col_edit, col_del = st.columns(2)
                if col_edit.button("✏️", key=f"edit_mhs_{m['id_mahasiswa']}"):
                    st.session_state.show_edit_form_mhs = True
                    st.session_state.edit_mhs_id = m['id_mahasiswa']
                    st.rerun()
                if col_del.button("🗑️", key=f"delete_mhs_{m['id_mahasiswa']}"):
                    if delete_mahasiswa(m['id_mahasiswa']):
                        st.success(f"Mahasiswa {m['nama_mahasiswa']} berhasil dihapus.")
                        st.rerun()
                    else:
                        st.error("Gagal hapus mahasiswa.")

    st.markdown("---")
    # Add form
    if st.session_state.show_add_form_mhs:
        st.subheader("Tambah Mahasiswa Baru")
        with st.form("form_tambah_mahasiswa", clear_on_submit=True):
            id_mahasiswa = st.text_input("NIM")
            nama_mahasiswa = st.text_input("Nama Mahasiswa")
            kelas_nama = st.selectbox("Kelas", list(kelas_options.keys()))
            semester = st.number_input("Semester", min_value=1, step=1)
            submit = st.form_submit_button("Tambah Mahasiswa")
            cancel = st.form_submit_button("Batal")

            if submit:
                if not id_mahasiswa or not nama_mahasiswa or not kelas_nama or not semester:
                    st.error("Semua field wajib diisi.")
                else:
                    kelas_id = kelas_options[kelas_nama]
                    if add_mahasiswa(id_mahasiswa, nama_mahasiswa, kelas_id, semester):
                        st.success(f"Mahasiswa {nama_mahasiswa} berhasil ditambahkan.")
                        st.session_state.show_add_form_mhs = False
                        st.rerun()
            if cancel:
                st.session_state.show_add_form_mhs = False
                st.rerun()

    # Edit form
    if st.session_state.show_edit_form_mhs:
        mhs_id = st.session_state.edit_mhs_id
        m_edit = next((m for m in mahasiswa_list if m['id_mahasiswa'] == mhs_id), None)
        if m_edit:
            st.subheader(f"Edit Mahasiswa: {m_edit['nama_mahasiswa']}")
            with st.form("form_edit_mahasiswa", clear_on_submit=False):
                nama_mahasiswa = st.text_input("Nama Mahasiswa", value=m_edit['nama_mahasiswa'])
                kelas_nama = st.selectbox("Kelas", list(kelas_options.keys()), index=list(kelas_options.values()).index(m_edit['kelas_id']))
                semester = st.number_input("Semester", min_value=1, value=m_edit['semester'], step=1)
                submit = st.form_submit_button("Update Mahasiswa")
                cancel = st.form_submit_button("Batal")

                if submit:
                    if not nama_mahasiswa or not kelas_nama or not semester:
                        st.error("Semua field wajib diisi.")
                    else:
                        kelas_id = kelas_options[kelas_nama]
                        if update_mahasiswa(mhs_id, nama_mahasiswa, kelas_id, semester):
                            st.success(f"Mahasiswa {nama_mahasiswa} berhasil diperbarui.")
                            st.session_state.show_edit_form_mhs = False
                            st.session_state.edit_mhs_id = None
                            st.rerun()
                if cancel:
                    st.session_state.show_edit_form_mhs = False
                    st.session_state.edit_mhs_id = None
                    st.rerun()


def fetch_presensi_summary(tanggal, daftar_kelas_id):
    conn = get_db_connection()
    if not conn:
        return {}
    cursor = conn.cursor(dictionary=True)
    # Ambil id kelas dan id matakuliah untuk daftar_kelas_id
    cursor.execute("SELECT kelas_id, matakuliah_id FROM daftar_kelas WHERE id=%s", (daftar_kelas_id,))
    kelas_row = cursor.fetchone()
    if not kelas_row:
        cursor.close()
        conn.close()
        return {}
    kelas_id = kelas_row['kelas_id']
    matakuliah_id = kelas_row['matakuliah_id']
    # Query presensi hanya untuk kelas_id, matakuliah_id, tanggal
    cursor.execute("""
        SELECT status, COUNT(*) as jumlah
        FROM presensi
        WHERE tanggal = %s AND kelas_id = %s AND matakuliah_id = %s
        GROUP BY status
    """, (tanggal, kelas_id, matakuliah_id))
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    summary = {'hadir': 0, 'izin': 0, 'sakit': 0, 'tanpa keterangan': 0}
    for row in data:
        stat = (row['status'] or 'tanpa keterangan').lower()
        if stat in summary:
            summary[stat] = row['jumlah']
        else:
            summary['tanpa keterangan'] += row['jumlah']
    return summary



def fetch_presensi_mahasiswa(tanggal, daftar_kelas_id, status):
    conn = get_db_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    # Dapatkan kelas_id dan matakuliah_id dari daftar_kelas_id
    cursor.execute("SELECT kelas_id, matakuliah_id FROM daftar_kelas WHERE id=%s", (daftar_kelas_id,))
    row = cursor.fetchone()
    if not row:
        cursor.close()
        conn.close()
        return []
    kelas_id = row['kelas_id']
    matakuliah_id = row['matakuliah_id']
    cursor.execute("""
        SELECT m.id_mahasiswa, m.nama_mahasiswa, p.waktu_masuk
        FROM presensi p
        JOIN mahasiswa m ON p.kelas_id = m.kelas_id AND p.nama = m.nama_mahasiswa
        WHERE p.tanggal = %s AND p.kelas_id = %s AND p.matakuliah_id = %s AND p.status = %s
    """, (tanggal, kelas_id, matakuliah_id, status))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

# Fungsi untuk menghasilkan laporan PDF dari tabel presensi
def generate_pdf_report(presensi_data, kelas_info, tanggal):
    pdf = FPDF()
    pdf.add_page()

    # Set font untuk judul
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Laporan Presensi Mata Kuliah", ln=True, align='C')

    # Set font untuk tabel
    pdf.set_font("Arial", '', 12)
    pdf.ln(10)

    # Tambahkan informasi mata kuliah dan kelas
    pdf.cell(200, 10, f"Mata Kuliah: {kelas_info['mata_kuliah']}", ln=True, align='L')
    pdf.cell(200, 10, f"Kelas: {kelas_info['kode_kelas']}", ln=True, align='L')
    pdf.cell(200, 10, f"Tanggal: {tanggal.strftime('%d %B %Y')}", ln=True, align='L')

    # Header tabel
    pdf.ln(10)
    pdf.cell(40, 10, "NIM", border=1, align='C')
    pdf.cell(60, 10, "Nama", border=1, align='C')
    pdf.cell(50, 10, "Keterangan", border=1, align='C')
    pdf.cell(40, 10, "Jam Masuk", border=1, align='C')
    pdf.ln()

    # Menambahkan data presensi
    for data in presensi_data:
        pdf.cell(40, 10, data['NIM'], border=1, align='C')
        pdf.cell(60, 10, data['Nama'], border=1, align='C')
        pdf.cell(50, 10, data['Keterangan'], border=1, align='C')
        pdf.cell(40, 10, data['Jam Masuk'], border=1, align='C')
        pdf.ln()

    # Simpan file PDF
    file_path = f"Presensi_{kelas_info['kode_kelas']}_{tanggal.strftime('%Y%m%d')}.pdf"
    pdf.output(file_path)

    return file_path

def kelola_presensi(tanggal):
    daftar_kelas = fetch_daftar_kelas_by_date(tanggal)
    if not daftar_kelas:
        st.info(f"Tidak ada kelas yang terdaftar pada tanggal {tanggal}.")
    else:
        st.subheader(f"Rekap Presensi Tanggal {tanggal}")

        # Define the headers
        col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 3, 2, 2, 2, 2, 2])

        # Set column headers
        col1.markdown("<h6 style='text-align: left;'>Kelas</h6>", unsafe_allow_html=True)
        col2.markdown("<h6 style='text-align: left;'>Mata Kuliah</h6>", unsafe_allow_html=True)
        col3.markdown("<h6 style='text-align: left;'>Hadir</h6>", unsafe_allow_html=True)
        col4.markdown("<h6 style='text-align: left;'>Izin</h6>", unsafe_allow_html=True)
        col5.markdown("<h6 style='text-align: left;'>Sakit</h6>", unsafe_allow_html=True)
        col6.markdown("<h6 style='text-align: left;'>Tanpa Keterangan</h6>", unsafe_allow_html=True)
        col7.markdown("<h6 style='text-align: left;'>Operasi</h6>", unsafe_allow_html=True)

        for i, kelas in enumerate(daftar_kelas):
            summary = fetch_presensi_summary(tanggal, kelas['daftar_kelas_id'])
            hadir = summary.get('hadir', 0)
            izin = summary.get('izin', 0)
            sakit = summary.get('sakit', 0)
            tanpa_keterangan = summary.get('alpha', 0)

            col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 3, 2, 2, 2, 2, 2])
            col1.write(kelas['kode_kelas'])
            col2.write(kelas['mata_kuliah'])
            col3.write(hadir)
            col4.write(izin)
            col5.write(sakit)
            col6.write(tanpa_keterangan)

            # Tombol Show untuk melihat presensi mahasiswa
            if col7.button("Show", key=f"show_{kelas['daftar_kelas_id']}"):
                # Fetch daftar mahasiswa berdasarkan status presensi
                status_types = ['hadir', 'izin', 'sakit', 'tanpa keterangan']
                presensi_data = []

                # Ambil data presensi berdasarkan status
                for status in status_types:
                    mahasiswa = fetch_presensi_mahasiswa(tanggal, kelas['daftar_kelas_id'], status)
                    for m in mahasiswa:
                        # Format the time
                        if isinstance(m['waktu_masuk'], timedelta):
                            total_seconds = m['waktu_masuk'].total_seconds()
                            hours = int(total_seconds // 3600)
                            minutes = int((total_seconds % 3600) // 60)
                            formatted_time = f"{hours:02}:{minutes:02} {'AM' if hours < 12 else 'PM'}"
                        else:
                            waktu_masuk = datetime.strptime(m['waktu_masuk'], '%H:%M:%S')
                            formatted_time = waktu_masuk.strftime('%I:%M %p')

                        presensi_data.append({
                            'NIM': m['id_mahasiswa'],
                            'Nama': m['nama_mahasiswa'],
                            'Keterangan': status.capitalize(),
                            'Jam Masuk': formatted_time
                        })

                if presensi_data:
                    # Display student details in a table format
                    df = pd.DataFrame(presensi_data, columns=['NIM', 'Nama', 'Keterangan', 'Jam Masuk'])
                    st.write(f"Data Presensi Mata Kuliah {kelas['mata_kuliah']} di Kelas {kelas['kode_kelas']}")  # Display the title for the table
                    st.table(df)

                     # Tombol untuk mencetak PDF dan mengunduhnya
                    if st.button("Print Laporan Presensi", key=f"print_{kelas['daftar_kelas_id']}"):
                        file_path = generate_pdf_report(presensi_data, kelas, tanggal)
                        st.success("Laporan Presensi berhasil dihasilkan.")
                        
                        # Tombol unduh PDF
                        with open(file_path, "rb") as file:
                            st.download_button(
                                label="Download PDF",
                                data=file,
                                file_name=f"Presensi_{kelas['kode_kelas']}_{tanggal.strftime('%Y%m%d')}.pdf",
                                mime="application/pdf"
                            )
                            
                    # Add button for "Close"
                    col_close = st.columns([1])
                    col_close[0].button("Tutup Tabel", key=f"close_{kelas['daftar_kelas_id']}")
                else:
                    st.write(f"Tidak ada data presensi untuk Kelas {kelas['nama']} pada tanggal {tanggal}.")


                

def main():
    check_login()  # Mengecek apakah user sudah login

    with st.sidebar:
        selected = option_menu(
            "Menu", 
            ["Dashboard", "Kelola User", "Kelola Mata Kuliah", "Kelola Kelas", "Kelola Mahasiswa", "Data Presensi", "Logout"], 
            icons=["house", "person", "book", "layers", "person-gear", "clipboard", "box-arrow-left"], 
            menu_icon="cast", 
            default_index=0,  # Set default menu item
            styles={
                "container": {"padding": "5px"},
                "icon": { "font-size": "18px"},
                "nav-link": {
                    "font-size": "15px", 
                    "text-align": "left", 
                    "margin": "5px", 
                    "--hover-color": "#399be1"
                },
                "nav-link-selected": {"background-color": "#FFFFFF", "color": "black"},
                "nav-link:hover": {"color": "black", "background-color": "#0d2a5b"}
            }
        )

    if selected == "Dashboard":
        dashboard()
    elif selected == "Kelola User":
        kelola_user()
    elif selected == "Kelola Mata Kuliah":
        kelola_mata_kuliah()
    elif selected == "Kelola Kelas":
        kelola_kelas()
    elif selected == "Kelola Mahasiswa":
        kelola_mahasiswa()
    elif selected == "Data Presensi":
        # Menampilkan halaman Data Presensi
        st.title("Data Presensi")
        
        # Memilih tanggal untuk melihat data presensi
        tanggal = st.date_input("Pilih Tanggal Presensi", value=None)

        if tanggal:
            kelola_presensi(tanggal)  # Memanggil fungsi kelola_presensi untuk menampilkan data
        else:
            st.info("Silakan pilih tanggal untuk menampilkan data presensi.")
    
    elif selected == "Logout":
        logout()

if __name__ == "__main__":
    main()
