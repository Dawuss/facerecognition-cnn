import streamlit as st
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import numpy as np
from PIL import Image, ExifTags
import tensorflow as tf
import pandas as pd
import bcrypt
from streamlit_option_menu import option_menu

# Konfigurasi database
DB_CONFIG = {
    'host': 'risky-cnn.streamlit.app',
    'user': 'u1362490_d4u5',
    'password': 'h9Di8%*1IPL2',
    'database': 'u1362490_sistem_presensi'
}

def get_db_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        st.error(f"Error connecting to database: {e}")
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
    if user['role'] != 'mahasiswa':
        st.error("Anda tidak memiliki akses ke halaman ini.")
        st.stop()

@st.cache_resource
def load_model():
    return tf.keras.models.load_model("model2/face_classifier_model.h5")

def load_and_correct(img_file):
    img = Image.open(img_file)
    try:
        for tag in ExifTags.TAGS:
            if ExifTags.TAGS[tag] == "Orientation":
                orientation_tag = tag
                break
        exif = dict(img._getexif().items())
        ori = exif.get(orientation_tag)
        if ori == 3:
            img = img.rotate(180, expand=True)
        elif ori == 6:
            img = img.rotate(270, expand=True)
        elif ori == 8:
            img = img.rotate(90, expand=True)
    except:
        pass
    return img

def fetch_kelas():
    conn = get_db_connection()
    if not conn:
        return []
    cursor = conn.cursor()
    cursor.execute("SELECT id, nama_kelas, semester FROM kelas ORDER BY nama_kelas")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def fetch_mk():
    conn = get_db_connection()
    if not conn:
        return []
    cursor = conn.cursor()
    cursor.execute("SELECT id_mk, nama FROM matakuliah ORDER BY nama")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def fetch_mahasiswa_by_kelas(kelas_id):
    conn = get_db_connection()
    if not conn:
        return []
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nama_mahasiswa 
        FROM mahasiswa 
        WHERE kelas_id = %s 
        ORDER BY nama_mahasiswa
    """, (kelas_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [r[0] for r in rows]

def fetch_kelas_detail(kelas_id):
    conn = get_db_connection()
    if not conn:
        return None
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.nama AS matakuliah, d.nama_lengkap AS dosen, COUNT(ma.id_mahasiswa) AS jumlah_mahasiswa
        FROM matakuliah m
        JOIN users d ON m.dosen_id = d.id
        JOIN mahasiswa ma ON ma.kelas_id = %s
        WHERE ma.kelas_id = %s
        GROUP BY m.id_mk, d.id
    """, (kelas_id, kelas_id))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if not rows:
        return None
    matakuliah, dosen, jumlah_mahasiswa = rows[0]
    return (matakuliah, dosen, jumlah_mahasiswa)

def fetch_daftar_kelas(selected_date):
    conn = get_db_connection()
    if not conn:
        return []
    cursor = conn.cursor()
    cursor.execute(""" 
        SELECT dk.id, m.nama, dk.tanggal, dk.kelas_id, dk.matakuliah_id 
        FROM daftar_kelas dk
        JOIN matakuliah m ON dk.matakuliah_id = m.id_mk
        JOIN kelas k ON dk.kelas_id = k.id
        WHERE dk.tanggal = %s
        ORDER BY m.nama
    """, (selected_date,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def simpan_presensi_nama(nama, tanggal, status="hadir", kelas_id=None, matakuliah_id=None):
    conn = get_db_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    waktu_masuk = datetime.now().time()
    try:
        cursor.execute(
            "INSERT INTO presensi (nama, tanggal, waktu_masuk, status, kelas_id, matakuliah_id) VALUES (%s, %s, %s, %s, %s, %s)",
            (nama, tanggal, waktu_masuk, status, kelas_id, matakuliah_id)
        )
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Gagal menyimpan presensi: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def main():
    check_login()
    st.markdown("<h1 style='text-align: center;'>📚 Sistem Presensi Mahasiswa</h1>", unsafe_allow_html=True)
    st.write("---")

    # Sidebar dengan option_menu
    with st.sidebar:
        selected = option_menu(
            "Menu",
            ["Daftar Kelas Baru", "Presensi Mahasiswa", "Logout"],
            icons=["file-earmark-plus", "clipboard-check", "box-arrow-left"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "5px"},
                "icon": {"font-size": "18px"},
                "nav-link": {
                    "font-size": "15px",
                    "text-align": "left",
                    "margin": "10px 0",
                    "--hover-color": "#399be1"
                },
                "nav-link-selected": {"background-color": "#FFFFFF", "color": "black"},
                "nav-link:hover": {"color": "black", "background-color": "#0d2a5b"}
            }
        )

    if selected == "Daftar Kelas Baru":
        st.subheader("1. Daftar Kelas Baru")
        st.write("Pilih tanggal, kelas, dan mata kuliah untuk mendaftarkan kelas presensi.")

        kelas_data = fetch_kelas()
        mk_data = fetch_mk()
        kelas_dict = {f"{nama} (Semester {semester})": id for (id, nama, semester) in kelas_data}
        mk_dict = {nama: id_mk for id_mk, nama in mk_data}

        selected_kelas = st.selectbox(
            "Pilih Kelas",
            options=[f"{nama} (Semester {semester})" for (id, nama, semester) in kelas_data],
            index=0 if kelas_data else None
        )
        selected_kelas_id = kelas_dict.get(selected_kelas, None)

        selected_mk = st.selectbox("Pilih Mata Kuliah", options=[nama for nama in mk_dict])
        selected_mk_id = mk_dict.get(selected_mk, None)

        selected_date = st.date_input("Pilih Tanggal Kelas", value=datetime.today())

        if st.button("Daftar Kelas"):
            if selected_kelas_id is None or selected_mk_id is None:
                st.error("Pilih Kelas dan Mata Kuliah terlebih dahulu.")
            else:
                conn = get_db_connection()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT * FROM daftar_kelas
                        WHERE matakuliah_id = %s AND tanggal = %s
                    """, (selected_mk_id, selected_date))
                    existing_class = cursor.fetchone()

                    if existing_class:
                        st.warning("Kelas ini sudah didaftarkan untuk tanggal tersebut.")
                    else:
                        try:
                            cursor.execute(
                                "INSERT INTO daftar_kelas (matakuliah_id, tanggal, kelas_id) VALUES (%s, %s, %s)",
                                (selected_mk_id, selected_date, selected_kelas_id)
                            )
                            conn.commit()
                            st.success(
                                f"Kelas '{selected_kelas}' dan Mata Kuliah '{selected_mk}' berhasil didaftarkan untuk tanggal {selected_date}."
                            )
                        except Exception as e:
                            st.error(f"Gagal daftar kelas: {e}")
                        finally:
                            cursor.close()
                            conn.close()

    elif selected == "Presensi Mahasiswa":
        st.subheader("2. Presensi Mahasiswa")
        st.write("Pilih tanggal dan kelas, kemudian lakukan presensi dengan mengunggah atau mengambil foto.")

        selected_date = st.date_input("Pilih Tanggal Kelas", value=datetime.today())

        daftar_kelas = fetch_daftar_kelas(selected_date)
        if not daftar_kelas:
            st.info(f"Tidak ada kelas yang terdaftar untuk tanggal {selected_date}. Silakan daftarkan kelas terlebih dahulu.")
            return

        kelas_data_all = fetch_kelas()
        map_kelasid_to_nama = {id: nama for (id, nama, semester) in kelas_data_all}
        map_kelasid_to_semester = {id: semester for (id, nama, semester) in kelas_data_all}

        kelas_ids_unik = sorted({row[3] for row in daftar_kelas})
        opsi_kelas = []
        opsi_label_to_id = {}
        for kid in kelas_ids_unik:
            nama_kelas = map_kelasid_to_nama.get(kid, f"(Kelas ID: {kid})")
            semester = map_kelasid_to_semester.get(kid, "")
            label = f"Semester {semester} – {nama_kelas}"
            opsi_kelas.append(label)
            opsi_label_to_id[label] = kid

        selected_label_kelas = st.selectbox("Pilih Kelas untuk Presensi", options=opsi_kelas)
        presensi_kelas_id = opsi_label_to_id[selected_label_kelas]

        # Perbaikan: Unpacking 5 kolom!
        filtered_daftar = [
            (daftar_id, nama_mk, tgl, kelas_id, matakuliah_id)
            for (daftar_id, nama_mk, tgl, kelas_id, matakuliah_id) in daftar_kelas
            if kelas_id == presensi_kelas_id
        ]

        opsi_matakuliah = [nama_mk for (daftar_id, nama_mk, tgl, kelas_id, matakuliah_id) in filtered_daftar]
        # Mapping nama mk ke tuple (daftar_id, matakuliah_id)
        map_matakuliah_to_ids = {
            nama_mk: (daftar_id, matakuliah_id)
            for (daftar_id, nama_mk, tgl, kelas_id, matakuliah_id) in filtered_daftar
        }

        if not opsi_matakuliah:
            st.warning("Tidak ada matakuliah untuk kelas ini pada tanggal terpilih.")
            return

        selected_mk_label = st.selectbox("Pilih Mata Kuliah", options=opsi_matakuliah)

        daftar_id, matakuliah_id = map_matakuliah_to_ids[selected_mk_label]

        kelas_detail = fetch_kelas_detail(presensi_kelas_id)
        if kelas_detail:
            matakuliah, dosen, jumlah_mahasiswa = kelas_detail
            st.markdown(f"""
                **Detail Kelas yang Dipilih**  
                • **Matakuliah**: {matakuliah}  
                • **Dosen**: {dosen}  
                • **Jumlah Mahasiswa**: {jumlah_mahasiswa}
            """)

        st.markdown("**Pilih Metode Presensi:**")
        col1, col2 = st.columns(2)

        if 'camera_started' not in st.session_state:
            st.session_state.camera_started = False

        if not st.session_state.camera_started:
            if col2.button("Start Camera"):
                st.session_state.camera_started = True
        else:
            if col2.button("Close Camera"):
                st.session_state.camera_started = False

        if st.session_state.camera_started:
            camera_file = col2.camera_input("📷 Ambil Foto Langsung")
        else:
            camera_file = None

        uploaded_files = col1.file_uploader(
            "Unggah Foto Wajah Mahasiswa (jpg/png)",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True
        )

        foto_list = []
        if uploaded_files:
            foto_list.extend(uploaded_files)
        if camera_file:
            foto_list.append(camera_file)

        st.markdown("### Input Manual (tanpa foto)")
        daftar_mahasiswa = fetch_mahasiswa_by_kelas(presensi_kelas_id)
        if daftar_mahasiswa:
            nama_manual = st.selectbox("Nama Mahasiswa (Manual)", options=daftar_mahasiswa)
        else:
            st.warning("Tidak ada mahasiswa di kelas ini.")
            nama_manual = None

        keterangan_manual = st.selectbox("Keterangan (Manual)", ["tanpa keterangan", "izin", "sakit"])

        if st.button("Submit Presensi (Manual)"):
            if not nama_manual:
                st.error("Tidak ada mahasiswa yang bisa dipilih.")
            else:
                simpan_presensi_nama(
                    nama_manual,
                    selected_date,
                    status=keterangan_manual,
                    kelas_id=presensi_kelas_id,
                    matakuliah_id=matakuliah_id  # <-- Tambahkan ini!
                )
                st.success(f"Presensi manual untuk **{nama_manual}** ({keterangan_manual}) berhasil disimpan.")

        if foto_list:
            model = load_model()
            IMG_SIZE = (150, 150)

            st.markdown("---")
            st.write("### Hasil Prediksi")

            for i in range(0, len(foto_list), 5):
                chunk = foto_list[i:i + 5]
                cols = st.columns(len(chunk))

                for idx, f in enumerate(chunk):
                    pil_img = load_and_correct(f)
                    arr = np.array(pil_img.resize(IMG_SIZE)) / 255.0
                    preds = model.predict(np.expand_dims(arr, 0))[0]
                    class_index = np.argmax(preds)
                    confidence = preds[class_index] * 100

                    class_names = [
                        'Aisyah Wulan Dari', 'Arya Thomas', 'Azzahra Karindiva', 'Dila Puspitasari',
                        'Dody Ardiansyah', 'Emilia Fransiska', 'Feni Mutia', 'Ferdinan Sastra Anggara',
                        'Ilham Saleh', 'Laras Anggi Wijayanti', 'M. Putra Pamungkas', 'Marsellina',
                        'Muhammad Kannu Santara', 'Muhammad Rafi Athallah', 'Rafika Ayu',
                        'Risky Firdaus', 'Sella', 'Serli Monica', 'Sina Widianti', 'Tona Lestari',
                        'Vikken Aghenta Pradana', 'Violin Annisa Ramadhani',
                        'Wulan Restu Utami', 'Zahrany Mega Lestari'
                    ]
                    nama_mahasiswa_pred = class_names[class_index]

                    col = cols[idx]
                    col.image(pil_img, use_container_width=True)
                    col.markdown(f"**{nama_mahasiswa_pred}**  \n{confidence:.2f}%")

            presensi_status = st.selectbox("Jika tidak hadir (Foto), pilih alasan:", ["hadir", "izin", "sakit", "alpha"])

            if st.button("Submit Presensi (Foto)"):
                for f in foto_list:
                    pil_img = load_and_correct(f)
                    arr = np.array(pil_img.resize(IMG_SIZE)) / 255.0
                    preds = model.predict(np.expand_dims(arr, 0))[0]
                    class_index = np.argmax(preds)
                    nama_mahasiswa_pred = class_names[class_index]

                    simpan_presensi_nama(
                        nama_mahasiswa_pred,
                        selected_date,
                        status=presensi_status,
                        kelas_id=presensi_kelas_id,
                        matakuliah_id=matakuliah_id     # <-- WAJIB TAMBAH INI!
                    )
                st.success("Semua hasil presensi (Foto) berhasil disimpan.")

    elif selected == "Logout":
        logout()

if __name__ == "__main__":
    main()
