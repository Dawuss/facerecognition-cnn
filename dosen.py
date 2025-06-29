import streamlit as st
import mysql.connector
from mysql.connector import Error
from datetime import datetime
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


def fetch_daftar_kelas_by_dosen(dosen_id):
    """
    Mengambil semua entri daftar_kelas yang diampu dosen (berdasarkan m.dosen_id).
    Kita juga mengambil kelas_id agar nanti bisa memfilter presensi berdasarkan kelas + tanggal.
    """
    conn = get_db_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            dk.id AS daftar_id, 
            m.kode, 
            m.nama AS matakuliah, 
            dk.tanggal, 
            dk.kelas_id
        FROM daftar_kelas dk
        JOIN matakuliah m ON dk.matakuliah_id = m.id_mk
        WHERE m.dosen_id = %s
        ORDER BY dk.tanggal DESC
    """, (dosen_id,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result  # list of dicts: {daftar_id, kode, matakuliah, tanggal, kelas_id}

def fetch_presensi_by_kelas_tanggal(kelas_id, tanggal):
    """
    Mengambil semua data presensi untuk kombinasi kelas_id + tanggal tertentu.
    """
    conn = get_db_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT nama, tanggal, status, waktu_masuk
        FROM presensi
        WHERE kelas_id = %s AND tanggal = %s
        ORDER BY nama
    """, (kelas_id, tanggal))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result  # list of dicts: {nama, tanggal, status, waktu_masuk}

def main():
    st.title("👩‍🏫 Dashboard Dosen")

    # Cek apakah sudah login
    if "user" not in st.session_state:
        st.warning("Anda harus login terlebih dahulu.")
        return

    user = st.session_state['user']
    if user.get('role') != 'dosen':
        st.error("Anda tidak memiliki akses ke halaman ini.")
        return

    dosen_id = user['id']
    st.subheader(f"Nama Dosen: {user['nama_lengkap']}")
    
    # Ambil daftar kelas yang diampu
    daftar_kelas = fetch_daftar_kelas_by_dosen(dosen_id)
    if not daftar_kelas:
        st.info("Anda belum mengampu kelas apapun.")
        return

    # Buat opsi selectbox: “KODE – NamaMatakuliah (Tanggal)”
    # Simpan mapping ke tuple (kelas_id, tanggal)
    opsi_map = {}
    opsi_list = []
    for item in daftar_kelas:
        kode = item['kode']
        matkul = item['matakuliah']
        tgl = item['tanggal'].strftime("%Y-%m-%d")
        kelas_id = item['kelas_id']
        label = f"{kode} – {matkul} ({tgl})"
        opsi_list.append(label)
        opsi_map[label] = (kelas_id, tgl)

    pilihan = st.selectbox("Pilih Kelas dan Tanggal Presensi", options=opsi_list)

    if st.button("Lihat Presensi"):
        kelas_id, tanggal_terpilih = opsi_map[pilihan]
        presensi_list = fetch_presensi_by_kelas_tanggal(kelas_id, tanggal_terpilih)
        if presensi_list:
            st.subheader(f"Daftar Presensi: {pilihan}")
            for p in presensi_list:
                waktu = p.get('waktu_masuk', '')
                st.write(f"- {p['nama']}  (Status: {p['status']} at {waktu})")
        else:
            st.info("Belum ada data presensi untuk kelas dan tanggal tersebut.")
    
if __name__ == "__main__":
    main()
