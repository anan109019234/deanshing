import sqlite3
import pandas as pd
import streamlit as st
import numpy as np
import joblib
import warnings
from feature import FeatureExtraction
from streamlit_option_menu import option_menu
import os

st.set_page_config(page_title="Deanshing", layout="wide")

warnings.filterwarnings('ignore')

gbc = joblib.load("rf_url.joblib")

DATABASE = 'url_history.db'

DEFAULT_URLS = [
    ("https://www.google.com", "aman"),
    ("http://yutup.hub", "phishing"),
    ("http://ignito.html/maps/traffic?setlang=en-us&FORM=WFWE01&ocid=msedgntp&pc=LCTS&cvid=8279fdcca74e42418910c450227d45b7&ei=10&cp=-6.23476%7E107.101593&lvl=11.0", "phishing"),
    ("https://www.kaggle.com/datasets/eswarchandt/phishing-website-detector", "aman"),
    ("https://deanshing.streamlit.app/", "aman"),
    ("https://www.cnbcindonesia.com/tech/20230202074601-37-410248/cara-cek-dan-melindungi-data-pribadi-bocor-di-internet", "aman"),
    ("http://rota.id/index.php/jishi", "phishing"),
    ("https://www.msn.com/en-us/feed?ocid=msedgntp&pc=LCTS&cvid=8279fdcca74e42418910c450227d45b7&ei=10", "aman"),
    ("https://www.netflix.com", "aman"),
    ("https://x.com/EmilyGiam/status/1815758243014103049", "aman"),
    ("https://www.stackoverflow.com", "aman"),
    ("https://opac.perpusnas.go.id/?__cf_chl_tk=9HHgSdqYQSecT070krrKlZKBtDTFVGnlJJpallGXc0k-1721964189-0.0.1.1-4180", "aman"),
    ("http://kuyhya.html", "phishing"),
    ("https://www.tribunnews.com/regional/2024/07/26/bekal-yang-disiapkan-kuasa-hukum-saka-tatal-untuk-sidang-pk-hari-ini-di-pn-cirebon", "aman"),
    ("http://linkdin.com", "phishing"),
    ("https://bansm.kemdikbud.go.id/akreditasi", "aman"),
    ("https://periksadata.com/simcardkominfo/", "aman"),
    ("http://netflux.app/YQSecT070k-0", "phishing"),
    ("https://pddikti.kemdikbud.go.id/", "aman"),
    ("https://www.kemdikbud.go.id/", "aman"),
    ("http://g1owchrt@rudan.php", "phishing"),
    ("https://www.perpusnas.go.id/", "aman"),
    ("https://www.dukcapil.online/", "aman"),
    ("http://pafikotamataram.org/", "phishing"),
    ("http://kerjasamagtk.id/app/img/sgacor/","phishing"),
    ("http://pmb.iaysningo.ac.id/gacor/","phishing"),
    ("http://pengaduan.poltekim.php/ver/slot777/","phishing"),
    ("https://machine-learning-for-fake-news-csjzpm4wwy5jqkjpvurpz2.streamlit.app/","aman"),
    ("https://www.tiktok.com/@darksistemwoii/video/7393238500994190598?_r=1&u_code=dbj0f55jdaic72&region=ID&mid=7393238507596352261&preview_pb=0&sharer_language=id","aman"),
]

def create_table():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS url_history (
                url TEXT NOT NULL,
                result TEXT NOT NULL
            )
        ''')
        if conn.execute('SELECT COUNT(*) FROM url_history').fetchone()[0] == 0:
            conn.executemany('INSERT INTO url_history (url, result) VALUES (?, ?)', DEFAULT_URLS)
            conn.commit()

def save_url_history(url, result):
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('INSERT INTO url_history (url, result) VALUES (?, ?)', (url, result))
        conn.commit()

def load_url_history():
    with sqlite3.connect(DATABASE) as conn:
        df = pd.read_sql_query('SELECT * FROM url_history', conn)
    return df

def initialize_session_state():
    if 'url_history' not in st.session_state:
        st.session_state['url_history'] = load_url_history()
    else:
        st.session_state['url_history'] = load_url_history()

def welcome_page():
    st.title("Selamat Datang di Aplikasi Deteksi Phishing")
    st.markdown("""
        **Tentang Aplikasi**
        
        Aplikasi ini dirancang untuk membantu Anda mengidentifikasi apakah sebuah URL aman untuk dikunjungi atau berpotensi menjadi phishing. Phishing adalah teknik penipuan yang digunakan oleh pelaku kejahatan siber untuk mencuri informasi pribadi seperti kata sandi, informasi keuangan, dan data sensitif lainnya dengan menipu pengguna agar mengunjungi situs web palsu yang terlihat sah.
        Tujuan utama aplikasi ini adalah memberikan alat yang sederhana namun efektif untuk memeriksa keamanan URL secara real-time. Dengan menggunakan algoritma machine learning seperti Random Forest, aplikasi ini menganalisis berbagai fitur dari URL dan memberikan penilaian apakah URL tersebut berpotensi berbahaya atau tidak.
        
        Aplikasi ini dirancang untuk semua pengguna yang ingin melindungi diri mereka dari serangan phishing, termasuk individu yang menggunakan internet untuk aktivitas sehari-hari maupun profesional yang mengelola data sensitif.
        Landasan utama pembuatan aplikasi ini adalah untuk memberikan solusi praktis dan mudah diakses dalam melawan ancaman phishing yang semakin canggih. Dengan memanfaatkan teknologi machine learning dan analisis fitur URL, aplikasi ini bertujuan untuk meningkatkan kesadaran dan keamanan pengguna di dunia maya.
        
        Tujuan pembuatan aplikasi ini adalah untuk memberikan alat yang efisien dalam mendeteksi dan memitigasi risiko phishing, serta memberikan edukasi kepada pengguna tentang tanda-tanda phishing dan praktik terbaik untuk menjaga keamanan informasi pribadi mereka.
    """)
    st.title("Apa Itu Phishing?")
    col1, col2, col3 = st.columns([1, 3, 1])

    with col1:
        st.write("")

    with col2:
        st.image("assets/heker.gif", width=600)

    with col3:
        st.write("")

    st.markdown("""
        Teman-teman tau ga, phishing itu serangan cyber yang bahaya banget lohh, karena kalau kamu sampai terkena serangan ini, informasi-informasi sensitif seperti kata sandi kamu, informasi keuangan kamu, dan bahkan identitas kamu bisa digunakan oleh pihak yang tidak bertanggung jawab untuk melakukan sesuatu yang ilegal atas nama kamu, ya! sekali lagi ku katakan ATAS NAMA KAMU!!!. Jadi jangan dianggap sepele ya teman-teman.
    """)
    st.title("Awas hindari kaktus!!!")
    col1, col2, col3 = st.columns([1, 3, 1])

    with col1:
        st.write("")

    with col2:
        st.image("assets/dino.gif", width=600)

    with col3:
        st.write("")

    st.markdown("""
        Untuk menghindari URL phishing, ada beberapa langkah yang bisa teman-teman lakukan, yaitu:
        - Periksa URL dengan cermat sebelum mengklik atau memasukkan informasi sensitif.
        - Gunakan alamat URL langsung daripada mengklik tautan dari email atau pesan yang mencurigakan.
        - Pastikan situs web menggunakan protokol HTTPS dan memiliki sertifikat keamanan yang valid.
        - Waspadai tanda-tanda umum phishing seperti tekanan waktu, ancaman, atau penawaran yang terlalu bagus untuk menjadi kenyataan.
    """)
    st.title("Yuk kenalan sama Random Forest")
    col1, col2, col3 = st.columns([1, 3, 1])

    with col1:
        st.write("")

    with col2:
        st.image("assets/security.gif", width=600)

    with col3:
        st.write("")

    st.markdown("""
        [1] Pertama, coba bayangkan kamu memiliki sebuah alat untuk mengidentifikasi apakah sebuah URL aman atau berbahaya untuk dikunjungi. Nah, Random Forest adalah seperti tim ahli keamanan yang terdiri dari banyak orang dengan keahlian berbeda-beda dalam mengenali tanda-tanda URL phishing.

        [2] Nah, setiap "ahli keamanan" dalam tim ini (dalam kasus ini, setiap pohon di hutan Random Forest) memiliki cara unik untuk memeriksa URL. Mereka bisa memeriksa apakah domainnya mencurigakan, apakah menggunakan protokol HTTPS yang aman, atau apakah ada kata-kata atau pola tertentu dalam URL yang menunjukkan tanda phishing.

        [3] Sehingga, ketika kamu memasukkan sebuah URL ke dalam Random Forest, setiap pohon (ahli keamanan) akan memberikan pendapatnya sendiri berdasarkan fitur-fitur yang diperiksa. Misalnya, satu pohon mungkin melihat bahwa URL menggunakan domain yang tidak umum atau tidak lazim, sementara pohon lain mungkin mencatat bahwa URL tidak menggunakan protokol HTTPS.

        [4] Setelah itu, Random Forest pun kemudian mengumpulkan semua pendapat dari seluruh "ahli keamanan" dan menentukan mayoritasnya. Jika sebagian besar pohon mengatakan bahwa URL tersebut mencurigakan berdasarkan fitur-fitur yang diperiksa, maka Random Forest akan memutuskan bahwa URL tersebut kemungkinan besar berbahaya atau phishing.

        [5] Kelebihan dari Random Forest dalam konteks ini adalah kemampuannya untuk menangani berbagai jenis fitur dan pola dalam URL tanpa perlu penyetelan yang rumit secara manual. Ini membuatnya sangat efektif dalam memprediksi apakah sebuah URL aman atau berpotensi phishing, dengan memanfaatkan kekuatan kolektif dari banyak "ahli keamanan" yang bekerja bersama-sama.
    """)

def panduan_aplikasi_page():
    st.title("Panduan Aplikasi")
    st.markdown("""
        ### Tata Cara Penggunaan Aplikasi Deteksi Phishing

        1. Buka halaman "Periksa Disini".
        2. Masukkan URL yang ingin Anda periksa ke dalam kotak teks yang tersedia.
        3. Pastikan URL yang anda masukkan berisi protokol seperti HTTPS.
        4. Klik tombol "Periksa" untuk memulai proses analisis URL.
        5. Hasil analisis akan ditampilkan apakah URL tersebut aman atau berbahaya.
        6. Anda dapat melihat riwayat URL yang telah diperiksa di halaman "Daftar URL".

        ### Video Demo
    """)
    st.video("assets/kenalan.mp4")
    st.markdown("""
        #### Penjelasan Video:

        **Kategori Phishing**
        - Alamat URL "yutup.hub" mencoba menyerupai "YouTube" namun menggunakan ejaan yang tidak lazim dan domain ".hub", yang tidak umum untuk situs resmi seperti YouTube. Ini adalah teknik umum yang digunakan oleh situs phishing untuk menipu pengguna agar percaya bahwa mereka mengunjungi situs yang sah.
        - URL ini menggunakan protokol "http" bukan "https". Situs yang sah biasanya menggunakan "https" untuk memastikan keamanan data pengguna melalui enkripsi. Ketidakadaan HTTPS bisa menjadi tanda bahwa situs tersebut tidak aman dan mungkin berbahaya.
        - Domain ".hub" tidak umum digunakan oleh situs terpercaya. Situs phishing sering kali menggunakan domain yang tidak biasa atau baru untuk menghindari deteksi dan memberikan rasa urgensi atau keunikan palsu kepada pengguna.
        
        **Kategori Non-Phishing**
        - Domain "google.com" adalah domain resmi milik Google, salah satu perusahaan teknologi terbesar dan terpercaya di dunia. Ini adalah domain yang umum dan diakui secara global.
        - URL ini menggunakan protokol "https", yang menunjukkan bahwa situs ini memiliki sertifikat keamanan dan mengenkripsi data pengguna untuk melindungi informasi pribadi mereka.
        - Google telah lama dikenal sebagai penyedia layanan yang sah dengan banyak pengguna di seluruh dunia. Situs ini sering diverifikasi oleh berbagai otoritas dan memiliki reputasi yang sangat baik, sehingga kecil kemungkinan untuk menjadi situs phishing.
    """)

def extract_features(url):
    obj = FeatureExtraction(url)
    features = obj.getFeaturesList()
    return features

def detect_page():
    initialize_session_state()

    url = st.text_input("Masukkan link di bawah ini")
    
    if st.button("Periksa"):
        if url:
            features = extract_features(url)
            x = np.array(features).reshape(1, -1) 
            y_pred = gbc.predict(x)[0]
            
            result = "aman" if y_pred == 1 else "berbahaya"
            save_url_history(url, result)
            
            st.session_state['url_history'] = load_url_history()
            
            if y_pred == 1:
                st.success(f"Horaay link yang kamu masukkan aman untuk diakses.")
                st.image("assets/s.gif")
                st.warning("""Mengapa demikian? karena URL tersebut sudah menggunakan protokol "https" yang menunjukkan bahwa URL tersebut memiliki sertifikat keamanan dan mengenkripsi data untuk melindungi informasi pribadi kamu.""")
            else:
                st.error(f"Waspadaa!!! link yang kamu berikan kemungkinan berbahaya.")
                st.image("assets/e.gif")
                st.warning("""Mengapa demikian? karena URL tersebut menggunakan protokol "http" bukan "https". Situs yang sah biasanya menggunakan "https" untuk memastikan keamanan data pengguna melalui enkripsi. Ketidakadaan HTTPS bisa menjadi tanda bahwa situs tersebut tidak aman dan mungkin berbahaya, karena bisa saja ada penyusup yang bisa meretas dan mengambil data pribadi yang kamu kirimkan.""")
        else:
            st.warning("Uhm.. sepertinya kamu belum memasukkan URLnya kawan :)")
            st.image("assets/w.gif")

def about_page():
    st.image("assets/profil.jpg", use_column_width=True)

    st.markdown("""
        <div style="display: flex; flex-direction: row; justify-content: center;">
            <div style="text-align: center; margin-right: 80px;">
                <a href="https://github.com/anan109019234/deanshing.git">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Octicons-mark-github.svg/200px-Octicons-mark-github.svg.png" alt="GitHub" style="width:30px;height:30px;">
                </a>
                <p style="margin-top: 5px;">Direktori</p>
            </div>
            <div style="text-align: center; margin-left: 80px;">
                <a href="https://www.kaggle.com/eswarchandt/phishing-website-detector">
                    <img src="https://cdn4.iconfinder.com/data/icons/logos-and-brands/512/189_Kaggle_logo_logos-512.png" alt="Kaggle" style="width:30px;height:30px;">
                </a>
                <p style="margin-top: 5px;">Dataset</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

def url_list_page():
    initialize_session_state()

    st.markdown("### Daftar URL yang telah diperiksa:")

    df = st.session_state['url_history']
    if not df.empty:
        df.columns = ['URL', 'Status']
        df['Status'] = df['Status'].apply(lambda x: 'Aman' if x == 'aman' else 'Phishing')
        st.write(df)
    else:
        st.warning("Belum ada URL yang diperiksa.")

    st.download_button(
        label="Download CSV",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name='url_history.csv',
        mime='text/csv'
    )

def main():
    create_table()
    initialize_session_state()

    selected = option_menu(
        menu_title=None,
        options=["Selamat Datang", "Panduan Aplikasi", "Periksa Disini", "Daftar URL", "Tentang Saya"],
        icons=["house", "book", "search", "list", "envelope"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )

    if selected == "Selamat Datang":
        welcome_page()
    elif selected == "Panduan Aplikasi":
        panduan_aplikasi_page()
    elif selected == "Periksa Disini":
        detect_page()
    elif selected == "Daftar URL":
        url_list_page()
    elif selected == "Tentang Saya":
        about_page()

if __name__ == "__main__":
    main()
